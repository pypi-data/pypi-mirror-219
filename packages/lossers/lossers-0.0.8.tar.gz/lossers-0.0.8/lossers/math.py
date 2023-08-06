from torch.nn import functional as F_

def smooth_l1_loss(input, target, **kwargs):
    return F_.smooth_l1_loss(input, target, **kwargs)

def l1_loss(input, target, **kwargs):
    return F_.l1_loss(input, target, **kwargs)

def huber_loss(input, target, **kwargs):
    return F_.huber_loss(input, target, **kwargs)

def mse_loss(input, target, **kwargs):
    return F_.mse_loss(input, target, **kwargs)

def l2_loss(input, target, **kwargs):
    return F_.mse_loss(input, target, **kwargs)
