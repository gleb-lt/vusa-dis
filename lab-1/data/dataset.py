import torch
from torch.utils.data import TensorDataset, DataLoader

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

import pandas as pd


def prepare_data(data_path, input_data_csv, train_data_csv, test_data_csv, test_size_override, random_state_override):
    data = pd.read_csv(f"{data_path}/{input_data_csv}")
    data_shuffled = data.sample(frac=1).reset_index(drop=True)

    train_data, test_data = train_test_split(data_shuffled, test_size=test_size_override, random_state=random_state_override)

    train_data_path = f"{data_path}/{train_data_csv}"
    test_data_path = f"{data_path}/{test_data_csv}"

    train_data.to_csv(train_data_path, index=False)
    test_data.to_csv(test_data_path, index=False)


def load_data(train_data_path, test_data_path, batch_size):
    df_train = pd.read_csv(train_data_path)
    df_test = pd.read_csv(test_data_path)

    # Užkoduojam kalbų kodus į skaičius (duomenų rinkinys apmokymui)
    label_encoder = LabelEncoder()
    df_train['language'] = label_encoder.fit_transform(df_train['language'])
    X_train = df_train.drop('language', axis=1).values
    y_train = df_train['language'].values

    # Nustatom duomenų rinkinio dydį ir klasės skaičių
    input_size = X_train.shape[1]
    num_classes = len(label_encoder.classes_)

    # Užkoduojam kalbų kodus į skaičius (testavimo duomenų rinkinys)
    df_test['language'] = label_encoder.fit_transform(df_test['language'])
    X_test = df_test.drop('language', axis=1).values
    y_test = df_test['language'].values

    # Normalizuojami mokymo ir testavimo duomenų rinkiniai
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.long)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.long)

    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader, input_size, num_classes
