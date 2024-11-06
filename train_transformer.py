from transformer_maskgit import CTViT, MaskGit, MaskGITTransformer
from transformer_maskgit.videotextdataset import VideoTextDataset
from transformer_maskgit.train_transformer import TransformerTrainer
from torch.utils.data import Dataset, DataLoader, random_split
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
import torch.multiprocessing as mp
import os

def cycle(dl):
    while True:
        for data in dl:
            yield data
            
def train():
    # set up distributed training

    ctvit = CTViT(
        dim = 64,
        codebook_size = 1024,
        image_size = 64,
        patch_size = 16,
        temporal_patch_size = 2,
        spatial_depth = 4,
        temporal_depth = 4,
        dim_head = 8,
        heads = 4
    )


    # Load the pre-trained weights

    pretrained_ctvit_path = 'pretrained_models/ctvit_pretrained.pt'
    ctvit.load(pretrained_ctvit_path)

    maskgit = MaskGit(
        num_tokens=1024,
        max_seq_len=10000,
        dim=64,
        dim_context=768,
        depth=2,
    )
   
    transformer_model = MaskGITTransformer(
        ctvit=ctvit,
        maskgit=maskgit
    )
    batch_size=1
    #transformer_model.load('pretrained_models/transformer_pretrained.pt')

    # initialize DDP
    trainer = TransformerTrainer(
        transformer_model,
        # num_train_steps=100000000,
        num_train_steps=100,
        batch_size=1,
        pretrained_ctvit_path='pretrained_models/ctvit_pretrained.pt',
        results_folder="transformer_train"
    )


    trainer.train()

if __name__ == '__main__':
    # set up multiprocessing
    train()
