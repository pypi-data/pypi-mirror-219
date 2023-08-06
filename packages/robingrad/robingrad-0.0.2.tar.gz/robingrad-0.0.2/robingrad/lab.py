import numpy as np 
from tensor import Tensor
from graph import draw_dot
import torch


# class Linear:
#     def __init__(self, in_features: int, out_features: int, bias: bool = True):
#         self.weight = Tensor.normal(0, 1, (out_features, in_features))
#         self.bias = Tensor.normal(0, 1, (out_features,)) if bias else None
    
#     def __call__(self, x: Tensor) -> Tensor:
#         out = x @ self.weight.T  # Matrix multiplication
#         if self.bias is not None:
#             out += self.bias
#         return out


# a = Tensor.ones((2,3), requires_grad=True)
# b = Tensor.full((3,2), 3., requires_grad=True)
# c = a @ b
# loss = c.sum()
# loss.backward()
# print(a.grad)
# print(b.grad)

# draw_dot(loss, filename="img/graph_inspect", inspect=True)

# a = torch.ones((2,3), requires_grad=True)
# b = torch.full((3,2), 3., requires_grad=True)
# c = a @ b
# loss = c.sum()
# loss.backward()
# print(a.grad)
# print(b.grad)


# a = Tensor.ones((3,2), requires_grad=True)
# aa = a.reshape((2,3))
# b = Tensor.full((3,2), 3., requires_grad=True)
# c = aa @ b
# loss = c.sum()
# loss.backward()
# print(a.grad)
# print(b.grad)
# print(aa.grad)
# draw_dot(loss, filename="img/graph_inspect", inspect=True)

# a = torch.ones((3,2), requires_grad=True)
# aa = a.view((2,3))
# b = torch.full((3,2), 3., requires_grad=True)
# c = aa @ b
# loss = c.sum()
# loss.backward()
# print(a.grad)
# print(b.grad)

# a = Tensor.ones((3,3), requires_grad=True)
# aa = a[0:2]
# b = Tensor.full((3,2), 3., requires_grad=True)
# c = aa @ b
# loss = c.sum()
# loss.backward()
# draw_dot(loss, filename="img/graph_inspect", inspect=True)
# print(a.grad)
# print(b.grad)

# a = torch.ones((3,3), requires_grad=True)
# aa = a[0:2]
# b = torch.full((3,2), 3., requires_grad=True)
# c = aa @ b
# loss = c.sum()
# loss.backward()
# print(a.grad)
# print(b.grad)


a = Tensor.ones((3,2), requires_grad=True)
b = a.T
c = Tensor.full((3,2), 3., requires_grad=True)
d = b @ c
loss = d.sum()
loss.backward()
draw_dot(loss, filename="img/graph_inspect", inspect=True)
print(a.grad)
print(c.grad)

a = torch.ones((3,2), requires_grad=True)
b = torch.transpose(a,1,0)
c = torch.full((3,2), 3., requires_grad=True)
d = b @ c
loss = d.sum()
loss.backward()
print(a.grad)
print(c.grad)

