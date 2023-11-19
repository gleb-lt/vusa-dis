# Dirbtinio Intelekto Sistemos - Pirmas labaratorinis darbas

## Užduotis

Pasirinkus duomenų rinkinį,  sukurti neuroninį tinklą duomenų klasifikavimui ir jį apmokyti.

## Darbo eiga
1) Darbą atlikite su duomenų rinkiniu, kuris niurodyta asmenine žinute.
2) Sukurkite daugiasluoksnio perceptrono (MLP) tipo neuroninį tinklą klasifikavimo užduočiai atlikti.
3) Paruoškite duomenis mokymui (suskirstykite į mokymo ir testavimo dalis, juos normalizuokite).
4) Pasirinkite hiperparametrus: mokymosi greitį, vienu žingsniu paduodamo duomenų paketo dydį.
5) Paruoškite mokymo kodą.
6) Atlikite neuroninio tinklo mokymą.
7) Patikrinkite neuroninio tinklo veikimą su testiniais duomenimis, taikydami klasifikavimo metrikas.
8) Išsaugokite apmokyto tinklo svorius.

## Duomenys

CSV bylos naudojamos NT mokymui ir testavimui randasi ./data/input aplankale. Duomenų šaltinis: https://archive.ics.uci.edu/dataset/518/speaker+accent+recognition.

Už duomenų paruošimą atsakingas ./data/prepare.py failas. 

Duomenų rinkinys buvo padalinamas į dvi dalis: mokymo ir testavimo. Mokymo duomenų rinkinys sudarytas iš 80% visų duomenų, o testavimo - iš 20%. 
Eksperimentuojant, bandžiau padininti mokymo duomenų rinkinį, tačiau tai tik pablogindavo rezultatus - nesu tikras kodėl, gal dėl pačių duomenų kokybės.

## Neuroninio tinklo struktūra

Neuroninio tinklo struktūra aprašyta ./model/mlp.py. Empiriniu budu pasirinkau 3 sluoksnių tinklą su 2 paslėptais sluoksniais. 
Vidinis sluoksnio dydis 64, trečio - 64/3. visos reikšmės parinktos bandant skirtingas konfigūracijas. Aktivavimo funkcija - ReLU.

## Mokymas

Kadangi duomenų rinkinys yra labai mažas, po kiekvieno epochos skaičiuojamas tikslumas. Po kelių bandymų pasirinkau, kad mokymas būtų baigiamas, kai tikslumas yra didesnis nei 0.85. 
Jiegu mokymas nebuvo stabdomas, labai dažnai įvykdavo permokymas.

Mokymo kodas aprašytas ./train.py. Mokymo metu buvo naudojama 30 epochų. Gali būti ir daugiau, nes mokymas stabdomas, kai tikslumas yra didesnis nei 0.85.
Mokymo greitis - 0.01 (geriausias rezultatas buvo pasiektas su šiuo greičiu).
Duomenų paketo dydis (batch size) - 16.

## Rezultatai

Apmokytas neuroninis tinklas išsaugotas į ./output/ failą.
Pasiektas tiklsumas (accuracy) ~86.36%. 
