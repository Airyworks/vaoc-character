from __future__ import print_function
from PIL import Image
import random
import torch
import numpy
import torchvision.utils as vutils
from torch.autograd import Variable
import torchvision.transforms
import hashlib
import math
import sys
import models


model_path = sys.argv[1]
netG = models._netG_1(2, 100, 3, 64, 1) # ngpu, nz, nc, ngf, n_extra_layers
netG.load_state_dict(torch.load(model_path, map_location=lambda storage, loc: storage))
print(netG)

sqrt2pi = 2.5066282746310002 # sqrt(pi * 2)


def convert_img(img_tensor, nrow):
    img_tensor = img_tensor.cpu()
    grid = vutils.make_grid(img_tensor, nrow=nrow, padding=2)
    ndarr = grid.mul(0.5).add(0.5).mul(255).byte().transpose(0, 2).transpose(0, 1).numpy()
    im = Image.fromarray(ndarr)
    return im


def get_pic(hash_str:str):
    l_seed, r_seed = hash_str[:32], hash_str[32:]
    l_generator, r_generator = hashlib.sha256(), hashlib.sha256()
    for i in range(19):
        l_generator.update(l_seed.encode('utf-8'))
        r_generator.update(r_seed.encode('utf-8'))
        l_seed += l_generator.hexdigest()
        r_seed += r_generator.hexdigest()
    def makearr(seed):
        seed_arr = map(lambda x: seed[x:x + 6], range(100))
        return map(lambda x: int(x, 16) / int('ffffff', 16), seed_arr)
    def normal(l, r):
        proto = zip(l, r)
        flow_1 = lambda x: math.sqrt(-2 * math.log(x))
        flow_2 = lambda x: math.cos(2 * math.pi * x)
        norm = map(lambda x, y: flow_1(x) * flow_2(y), proto)
        return norm
    normalize = normal(makearr(l_seed), makearr(r_seed))
    norm_tensor = torch.from_numpy(numpy.fromiter(normalize, dtype=numpy.float))
    return norm_tensor


def predict(input_tensor):
    z2 = torch.FloatTensor(1, 100, 1, 1).normal_(0, 1)
    zd = (z2 - input_tensor) / 15
    pre = torch.FloatTensor(16, 100, 1, 1)
    for i in range(16):
        pre[i] = input_tensor + i * zd
    pre = Variable(pre)
    res = netG(pre)
    return convert_img(res.data, 16), res.data






a = get_pic('db675a1e3c04cf53e7916a9c919e2f3ecb22165c20f2b87763137decaa11ccd1')
print(a)



