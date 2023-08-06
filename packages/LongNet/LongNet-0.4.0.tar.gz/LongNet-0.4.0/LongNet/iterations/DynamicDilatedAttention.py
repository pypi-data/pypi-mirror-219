import torch 
import torch.nn as nn
import torch.nn.functional as F

from LongNet.utils import XPOS, RelativePositionBias
from LongNet.attend import FlashAttention

# Replace this with your correct GPU device
device = "cuda:0"
dtype=torch.float16




class DynamicDilatedAttention(nn.Module):
    def __init__(self, d_model, num_heads, num_rates, dropout=0.0, casual=False, use_xpos=False, use_rel_pos_bias=False):
        super(DynamicDilatedAttention, self).__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.casual = casual  # Define this before FlashAttention

        # Generate geometric sequences for dilation rates and segment sizes
        self.dilation_rates = torch.logspace(start=0, end=num_rates-1, steps=num_rates, base=2, dtype=torch.int, device=device)
        self.segment_sizes = torch.logspace(start=0, end=num_rates-1, steps=num_rates, base=2, dtype=torch.int, device=device)

        self.attention = [FlashAttention(causal=self.casual, dropout=dropout).to(device) for _ in range(num_rates)] # Corrected here]
        self.dropout = nn.Dropout(dropout)

        self.use_xpos = use_xpos
        self.use_rel_pos_bias = use_rel_pos_bias

        if use_xpos:
            self.xpos = XPOS(head_dim=d_model//num_heads)
        if use_rel_pos_bias:
            self.relative_bias = RelativePositionBias(num_buckets=32, max_distance=128, n_heads=num_heads)

        self.softmax = nn.Softmax(dim=-1)

    def get_mask(self, i, j):
        return torch.ones((i, j), device=device, dtype=torch.bool).triu(j - i + 2)

    def forward(self, x):
        batch_size, seq_len, _ = x.shape

        if self.use_xpos:
            x = self.xpos(x)

        # Initialize tensor to store outputs
        outputs = torch.zeros((batch_size, seq_len, self.d_model), device=device, dtype=dtype)

        # Initialize tensor to store softmax denominators
        softmax_denominators = torch.zeros((batch_size, seq_len, self.num_heads), device=device, dtype=dtype)

        for head_idx, attention in enumerate(self.attention):
            dilation_rate = self.dilation_rates[head_idx]
            segment_size = self.segment_sizes[head_idx]

            for offset in range(dilation_rate):
                x_ = x[:, offset::dilation_rate, :]  # Apply offset for each head
                x_ = x_.contiguous().view(batch_size, -1, segment_size, self.d_model)

                attn_output, attn_weights, *_ = attention(x_, x_, x_)  # Collect all additional return values into a list
                
                if self.use_rel_pos_bias:
                    attn_output += self.relative_bias(batch_size, attn_output.size(1), attn_output.size(1))

                if self.casual:
                    mask = self.get_mask(attn_output.size(1), attn_output.size(1))
                    attn_output = attn_output.masked_fill(mask, float('-inf'))

                attn_output = self.dropout(attn_output)

                # Add output to the corresponding positions in the outputs tensor
                outputs[:, offset::dilation_rate, :] += attn_output.contiguous().view(batch_size, -1, self.d_model)
                
                # Add softmax denominators to the corresponding positions in the softmax_denominators tensor
                softmax_denominators[:, offset::dilation_rate, :] += attn_weights.sum(dim=-1)

        # Calculate the weights for the different dilated attentions
        weights = self.softmax(softmax_denominators)

        # Apply the weights to the outputs
        outputs_weighted = weights * outputs

        return outputs_weighted


