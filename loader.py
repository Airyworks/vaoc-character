from __future__ import print_function
from PIL import Image
import random
import torch
import torchvision.utils as vutils
from torch.autograd import Variable
import torchvision.transforms
import hashlib
import sys
import models


# model_path = sys.argv[1]
# netG = models._netG_1(2, 100, 3, 64, 1) # ngpu, nz, nc, ngf, n_extra_layers
# netG.load_state_dict(torch.load(model_path, map_location=lambda storage, loc: storage))
# print(netG)

sqrt2pi = 2.5066282746310002 # sqrt(pi * 2)

def get_pic(hash_str:str):
    seed = hash_str
    hash_generator = hashlib.sha256()
    for i in range(9):
        hash_generator.update(seed.encode('utf-8'))
        seed += hash_generator.hexdigest()
    template = torch.FloatTensor(1, 100, 1, 1)
    for i in range(100):
        template[:, i, :, :] = int(seed[i:i + 6], 16)

    template = (template  - (int('ffffff', 16) / 2)) / int('ffffff', 16) * 2
    template = torch.exp(-(template.pow(2) / 2)) / sqrt2pi
    return template


a = get_pic('db675a1e3c04cf53e7916a9c919e2f3ecb22165c20f2b87763137decaa11ccd1')
print(a)



