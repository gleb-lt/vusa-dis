#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 08:09:21 2023

@author: gintautas
"""
import numpy as np
import cv2
import torch
from collections import Counter
import utils
from torchvision.models import resnet152

from torchvision.transforms.functional import normalize

import matplotlib.pyplot as plt
import json

# Užkrauname test_images_map.json failą, kuris susieja paveiksliukų pavadinimus su jų klasėmis (vazos)
with open('test_images_map.json') as labels_file:
    images_meta_map = json.load(labels_file)

# Užkrauname ImageNet klasifikatoriaus žodyną
with open('imagenet_class_index.json') as labels_file:
    labels_map = json.load(labels_file)

# Užkrauname ResNet18 modelį, kuris buvo apmokytas ImageNet duomenimis
model = resnet152(pretrained=True).eval()

# Sukuriame rezultatų skaitliuką
results_counter = Counter({'success': 0, 'failure': 0})

# Write to CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    for filename in filenames:
        writer.writerow(
            [filename, f"![Thumbnail of {filename}](./data/input/thumbs/ILSVRC2012_val_00000895_n04522168.jpg)"])

# Praeiname per visus paveiksliukus ir patikriname, ar modelis teisingai nustato paveiksliuko klasę
for image_meta in images_meta_map:
    filename = f"./data/input/{images_meta_map[image_meta][0]}"

    image  = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = torch.from_numpy(image)
    img = img.permute(2,0,1)

    plt.figure()
    plt.imshow(image)
    input_tensor = normalize(img / 255., [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    out = model(input_tensor.unsqueeze(0))
    out = out.detach().cpu().numpy()
    idx = np.argmax(out, axis=1)
    str_idx = str(idx[0])
    plt.close()

    if labels_map[str_idx][1] == images_meta_map[image_meta][1]:
        results_counter['success'] += 1
    else:
        print("-"*3)
        print("Klaidingas modelio spėjimas: ", labels_map[str_idx][1])
        print("Failo pavadinimas: ", images_meta_map[image_meta][0])
        results_counter['failure'] += 1


print("*"*50)
print("Rezultatai:")
print("Teisingai nustatytos klasės: ", results_counter['success'])
print("Neteisingai nustatytos klasės: ", results_counter['failure'])

print("Tikslumas: ", (results_counter['success'] / (results_counter['success'] + results_counter['failure']))*100, "%")
