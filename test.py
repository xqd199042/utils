import torch
import numpy as np
from torch.autograd import Variable


if __name__ == '__main__':
    # np_data = np.arange(6).reshape((2,3))
    # torch_data = torch.from_numpy(np_data)
    # print(np_data)
    # print(torch_data)
    # print(torch_data.numpy())

    # data = np.array([-1, -2, 1, 2])
    # tensor = torch.FloatTensor(data)
    # print(data)
    # print(tensor)

    tensor = torch.FloatTensor([[1, 2], [3, 4]])
    variable = Variable(tensor, requires_grad=True)
    t_out = torch.mean(tensor*tensor)
    v_out = torch.mean(variable*variable)
    print(t_out)
    print(v_out)
    v_out.backward()
    print(variable.grad)


