from collections import namedtuple
import torch
QuantizedTensor = namedtuple('QuantizedTensor', ['tensor', 'scale', 'zero_point'])


def quantize_tensor(x, cuda = True, num_bits=8):
    assert torch.is_tensor(x)
    qmin = 0.
    qmax = 2.**num_bits - 1.
    min_val, max_val = x.min(), x.max()

    scale = (max_val.item() - min_val.item()) / (qmax - qmin)
    initial_zero_point = qmin - min_val / scale

    zero_point = 0
    if initial_zero_point < qmin:
        zero_point = qmin
    elif initial_zero_point > qmax:
        zero_point = qmax
    else:
        zero_point = initial_zero_point.item()


    # zero_point = int(zero_point)
    zero_point_tensor = torch.full(x.shape,zero_point, dtype=x.dtype)
    scale_tensor = torch.full(x.shape,scale, dtype=x.dtype)
    if cuda:
        # x = x.cuda()
        zero_point_tensor = zero_point_tensor.cuda()
        scale_tensor = scale_tensor.cuda()
    q_x = x.div(scale_tensor).add(zero_point_tensor)
    q_x.clamp_(qmin, qmax).round_()

    q_x = q_x.to(x.dtype)
    scale = torch.tensor(scale, dtype=x.dtype)
    zero_point = torch.tensor(zero_point, dtype=x.dtype)

    return (q_x, scale, zero_point)

def dequantize_tensor(qt, cuda:bool = True):
    quantized_tensor, scale, zero_point = qt[0].cuda(), qt[1].cuda(), qt[2].cuda()
    zero_point_tensor = torch.full(quantized_tensor.shape, zero_point.item(), dtype=quantized_tensor.dtype)
    scale_tensor = torch.full(quantized_tensor.shape, scale.item(), dtype=quantized_tensor.dtype)
    if cuda:
        zero_point_tensor = zero_point_tensor.cuda()
        scale_tensor = scale_tensor.cuda()
    return quantized_tensor.sub(zero_point_tensor).mul(scale_tensor)


# Referred to https://github.com/eladhoffer/utils.pytorch/blob/master/quantize.py
#  and http://openaccess.thecvf.com/content_cvpr_2018/papers/Jacob_Quantization_and_Training_CVPR_2018_paper.pdf
def bk_quantize_tensor(x, num_bits=8):
    qmin = 0.0
    qmax = 2.0 ** num_bits - 1.0
    min_val, max_val = x.min(), x.max()
    scale = (max_val - min_val) / (qmax - qmin)
    initial_zero_point = qmin - min_val / scale
    zero_point = qmin if initial_zero_point < qmin else qmax if initial_zero_point > qmax else initial_zero_point
    zero_point = int(zero_point)
    qx = zero_point + x / scale
    qx = qx.clamp(qmin, qmax).round().byte()
    return QuantizedTensor(tensor=qx, scale=scale, zero_point=zero_point)


def bk_dequantize_tensor(q_x):
    return q_x.scale * (q_x.tensor.float() - q_x.zero_point)
