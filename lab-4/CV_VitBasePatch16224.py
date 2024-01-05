#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import torch
from collections import Counter
from transformers import ViTImageProcessor, ViTForImageClassification

import json
import utils

# Užkrauname test_images_map.json failą, kuris susieja paveiksliukų pavadinimus su jų klasėmis (vazos)
with open('test_images_map.json') as labels_file:
    images_meta_map = json.load(labels_file)

# Užkrauname ImageNet klasifikatoriaus žodyną
with open('imagenet_class_index.json') as labels_file:
    labels_map = json.load(labels_file)

# Užkrauname Vision Transformer (ViT)  modelį, kuris buvo apmokytas ImageNet duomenimis
model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

# Sukuriame rezultatų skaitliuką
results_counter = Counter({'success': 0, 'failure': 0})

# Sukuriame masyvą, kuriame saugosime paveiksliukų atpažinimo rezultatus kiekvienam paveiksliukui
results = []

# Sukuriame masyvą, kuriame saugosime paveiksliukų atpažinimo metu nustatytus raktažodžius kiekvienam paveiksliukui
keywords = []

# Praeiname per visus paveiksliukus ir patikriname, ar modelis teisingai nustato paveiksliuko klasę
for image_meta in images_meta_map:
    filename = f"./data/input/{images_meta_map[image_meta][0]}"

    image  = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = torch.from_numpy(image)
    img = img.permute(2,0,1)

    processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')

    inputs = processor(images=img, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits

    predicted_class_idx = logits.argmax(-1).item()

    keywords.append(model.config.id2label[predicted_class_idx])

    predicted_class = model.config.id2label[predicted_class_idx]

    if predicted_class == images_meta_map[image_meta][1]:
        results_counter['success'] += 1
        results.append('Success')
    else:
        print("-"*3)
        print("Klaidingas modelio spėjimas: ", predicted_class)
        print("Failo pavadinimas: ", images_meta_map[image_meta][0])
        results_counter['failure'] += 1
        results.append('Failure')

utils.add_column_to_csv('test_images.csv', results, 'google/vit-base-patch16-224 result')
utils.add_column_to_csv('test_images.csv', keywords, 'google/vit-base-patch16-224 keywords')

print("*"*50)
print("google/vit-base-patch16-224 modelio rezultatai:")
print("Teisingai nustatytos klasės: ", results_counter['success'])
print("Neteisingai nustatytos klasės: ", results_counter['failure'])

print("Tikslumas: ", (results_counter['success'] / (results_counter['success'] + results_counter['failure']))*100, "%")
