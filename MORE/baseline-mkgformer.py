import os
import argparse
import logging
import sys
sys.path.append("..")

import torch
import numpy as np
import random
from torchvision import transforms
from torch.utils.data import DataLoader
from models.unimo_model import UnimoREModel
from models.modeling_clip import CLIPModel
from transformers.models.clip import CLIPProcessor

from transformers import BertConfig, CLIPConfig, BertModel
from processor.dataset import MMREProcessor, MMREDataset
from modules.train import BertTrainer


import warnings
warnings.filterwarnings("ignore", category=UserWarning)
# from tensorboardX import SummaryWriter