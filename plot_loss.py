import numpy as np
import json
import matplotlib.pyplot as plt

#with open('/tmp/logw.txt', encoding='utf-8') as f:
#    lines = f.readlines()

with open('/Users/cschaefe/workspace/WaveRNNGerman2/checkpoints/cutted_raw.wavernn/log.txt', encoding='utf-8') as f:
    lines = f.readlines()


def get_loss(line):
    line_split = line.split('|')
    loss = line_split[2].replace('Loss:', '').replace(' ', '')
    loss = float(loss)
    return loss


losses = [get_loss(l) for l in lines]

plt.plot(range(len(losses)), losses, color='red', alpha=1, label='de')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()