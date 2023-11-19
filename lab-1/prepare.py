from data.dataset import prepare_data


def main():
    print("Preparing data...")
    data_path = './data/input'
    input_data_csv = 'mfcc-lang-dataset.csv'
    train_data_csv = 'train-ds.csv'
    test_data_csv = 'test-ds.csv'
    prepare_data(data_path, input_data_csv, train_data_csv, test_data_csv, 0.2, 42)
    print("Data prepared!")


if __name__ == '__main__':
    main()
