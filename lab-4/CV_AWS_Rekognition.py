#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import boto3
from collections import Counter

import json
import utils

# Užkrauname test_images_map.json failą, kuris susieja paveiksliukų pavadinimus su jų klasėmis (vazos)
with open('test_images_map.json') as labels_file:
    images_meta_map = json.load(labels_file)

# Užkrauname ImageNet klasifikatoriaus žodyną
with open('imagenet_class_index.json') as labels_file:
    labels_map = json.load(labels_file)

# AWS Rekognition klientas
rekognition_client = boto3.client(
    'rekognition',
    aws_access_key_id='****',
    aws_secret_access_key='****',
    region_name='us-east-1'
)

# Sukuriame rezultatų skaitliuką
results_counter = Counter({'success': 0, 'failure': 0})

# Sukuriame masyvą, kuriame saugosime paveiksliukų atpažinimo rezultatus kiekvienam paveiksliukui
results = []

# Sukuriame masyvą, kuriame saugosime paveiksliukų atpažinimo metu nustatytus raktažodžius kiekvienam paveiksliukui
keywords = []

# Praeiname per visus paveiksliukus ir patikriname, ar modelis teisingai nustato paveiksliuko klasę
for image_meta in images_meta_map:
    filename = f"./data/input/{images_meta_map[image_meta][0]}"

    expected_label = images_meta_map[image_meta][1].lower()

    image  = cv2.imread(filename)
    _, encoded_image = cv2.imencode('.jpg', image)

    rekognition_response = rekognition_client.detect_labels(
        Image={'Bytes': encoded_image.tobytes()},
        MaxLabels=20
    )

    detected_labels = [(label['Name'].lower(), label['Confidence']) for label in rekognition_response['Labels']]

    print("detected_labels= ", detected_labels)
    print("expected_label]= ", expected_label)

    detected_label = next(((label, confidence) for label, confidence in detected_labels if label == expected_label), None)
    if detected_label:
        keywords.append(detected_label)
    else:
        keywords.append("N/A")

    is_success = any(images_meta_map[image_meta][1] in label for label, _ in detected_labels)

    if is_success:
        results_counter['success'] += 1
        results.append('Success')
    else:
        print("-"*3)
        print("Klaidingas modelio spėjimas: ", detected_labels)
        print("Failo pavadinimas: ", images_meta_map[image_meta][0])
        results_counter['failure'] += 1
        results.append('Failure')

utils.add_column_to_csv('test_images.csv', results, 'aws-rekognition result')
utils.add_column_to_csv('test_images.csv', keywords, 'aws-rekognition keywords')

print("*"*50)
print("AWS Rekognition rezultatai:")
print("Teisingai nustatytos klasės: ", results_counter['success'])
print("Neteisingai nustatytos klasės: ", results_counter['failure'])

print("Tikslumas: ", (results_counter['success'] / (results_counter['success'] + results_counter['failure']))*100, "%")
