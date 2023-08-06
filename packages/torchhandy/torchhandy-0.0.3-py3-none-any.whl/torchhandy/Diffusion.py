import torch
import torch.nn as nn
import numpy as np

class Diffusion(object):
    def __init__(self, config):
        self.steps = config.steps
        self.begin_beta = config.begin_beta
        self.end_beta = config.end_beta
        
        try:
            self.betas = np.load(config.beta_path)
            assert(len(self.betas) == self.steps)
            assert(self.betas[0] == self.begin_beta)
            assert(self.betas[-1] == self.end_beta)
        except Exception as e:
            self.betas = np.linspace(self.end_beta, self.begin_beta, num = self.steps)
            np.save(self.betas, config.beta_path)
        
        self.betas = torch.tensor(self.betas)
        self.alphas = 1 - self.betas
        self.alpha_mul = torch.cumprod(self.alphas, dim = 0)
        
    def add_noise(self, x):
        bsz = x.shape[0]
        tim = torch.randint(0, self.steps, (bsz, ))
        alpha_muls = torch.gather(self.alpha_mul, dim = 0, index = tim)
        noise = torch.randn_like(x)
        noised_x = torch.sqrt(alpha_muls) * x + torch.sqrt(1 - alpha_muls) * noise
        return noised_x, noise, tim

    def denoise(self, x, tim, model, device):
        step = tim[0].item()
        pred_noise = model(x, tim, device)
        x_now = (x - self.beta[step] * pred_noise / (torch.sqrt(1 - self.alpha_mul[step]))) * torch.sqrt(1 / self.alpha[step]) 
        if step > 0:
            z = torch.randn_like(x)
            x_now += torch.sqrt((1 - self.alpha_mul[step - 1]) / (1 - self.alpha_mul[step]) * self.beta[step]) * z
        return pred_noise, x_now
        