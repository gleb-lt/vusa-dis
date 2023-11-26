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

import timm
from torchvision.transforms.functional import normalize, resize

import matplotlib.pyplot as plt
import json
import utils

# Užkrauname test_images_map.json failą, kuris susieja paveiksliukų pavadinimus su jų klasėmis (vazos)
with open('test_images_map.json') as labels_file:
    images_meta_map = json.load(labels_file)

# Užkrauname ImageNet klasifikatoriaus žodyną
with open('imagenet_class_index.json') as labels_file:
    labels_map = json.load(labels_file)

# Užkrauname Vision Transformer modelį, kuris buvo apmokytas ImageNet duomenimis
model = timm.create_model('vit_base_patch16_224', pretrained=True).eval()

# Sukuriame rezultatų skaitliuką
results_counter = Counter({'Success': 0, 'Failure': 0})

# Sukuriame masyvą, kuriame saugosime paveiksliukų atpažinimo rezultatus kiekvienam paveiksliukui
results = []

# Praeiname per visus paveiksliukus ir patikriname, ar modelis teisingai nustato paveiksliuko klasę
for image_meta in images_meta_map:
    filename = f"./data/input/{images_meta_map[image_meta][0]}"

    image = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = torch.from_numpy(image)
    img = img.permute(2,0,1)

    img = resize(img, (224, 224))

    plt.figure()
    plt.imshow(image)
    input_tensor = normalize(img / 255., [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    out = model(input_tensor.unsqueeze(0))
    out = out.detach().cpu().numpy()
    idx = np.argmax(out, axis=1)
    str_idx = str(idx[0])
    plt.close()

    if labels_map[str_idx][1] == images_meta_map[image_meta][1]:
        results_counter['Success'] += 1
        results.append('Success')
    else:
        print("-"*3)
        print("Klaidingas modelio spėjimas: ", labels_map[str_idx][1])
        print("Failo pavadinimas: ", images_meta_map[image_meta][0])
        results_counter['Failure'] += 1
        results.append('Failure')

utils.add_column_to_csv('test_images.csv', results, 'ViT(timm)')

print("*"*50)
print("ViT(timm) modelio rezultatai:")
print("Teisingai nustatytos klasės: ", results_counter['Success'])
print("Neteisingai nustatytos klasės: ", results_counter['Failure'])

print("Tikslumas: ", (results_counter['Success'] / (results_counter['Success'] + results_counter['Failure']))*100, "%")
