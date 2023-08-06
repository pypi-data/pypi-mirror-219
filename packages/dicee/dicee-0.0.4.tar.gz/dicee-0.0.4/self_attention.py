# Notes and codes from A.Karpahty Let's build GPT
import torch

torch.manual_seed(1)
# T denotes a sequence of tokens
# Each token should only interact with previous tokens, e.g.
# T[3] should only be aware of  T[0], T[1], T[2]

B, T, C = 4, 8, 2  # batch time channels

x = torch.randn(B, T, C)

# Interactions by means of averaged representation
xbow = torch.zeros((B, T, C))
for b in range(B):
    for t in range(T):
        xbow[b, t] = torch.mean(x[b, :t + 1], 0)
# (1) At each batch, the first token does not have any previous tokens.So it must be equal to itself
assert torch.allclose(x[:, 0], xbow[:, 0])
# (2) The second token in the first should be average of previous tokens.
assert torch.allclose(xbow[0, 1], torch.mean(x[0, :2], 0))

# =>>> REPLACING THE NESTED FOR LOOP
wei = torch.tril((torch.ones(T, T)))
wei = wei / wei.sum(1, keepdim=True)
xbow2 = wei @ x
assert torch.allclose(xbow, xbow2)

# =>>> USING SOFTMAX
tril = torch.tril(torch.ones(T, T))
wei = torch.zeros((T, T))
wei = wei.masked_fill(tril == 0, float('-inf'))
wei = torch.nn.functional.softmax(wei, dim=-1)
xbow3 = wei @ x
assert torch.allclose(xbow, xbow3)

# Single head perform self-attention
head_size = 16
key = torch.nn.Linear(C, head_size, bias=False)
query = torch.nn.Linear(C, head_size, bias=False)
value = torch.nn.Linear(C, head_size, bias=False)

wei = query(x) @ key(x).transpose(-2,-1)

wei.masked_fill(torch.tril(torch.ones(T, T)) == 0, float('-inf'))
out = torch.nn.functional.softmax(wei, dim=-1) @ value(x)

# Why do we normalize weights before softmax
k = torch.randn(B, T, head_size)
q = torch.randn(B, T, head_size)
wei = q @ k.transpose(-2, -1)
# if you have unit gaussian input (k,q)
# The variance of wei will be the order of head size ~ 16.
print(wei.var())
print((wei * (head_size ** -0.5)).var())
