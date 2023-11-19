import torch
import torch.nn as nn
from model.mlp import MLP
from data.dataset import load_data


def train_model(model, train_loader, test_loader, criterion, optimizer, num_epochs=10):
    model.train()
    for epoch in range(num_epochs):
        model.train()
        for i, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.cuda(), labels.cuda()

            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

        model.eval()
        with torch.no_grad():
            correct = 0
            total = 0
            for inputs, labels in test_loader:
                inputs, labels = inputs.cuda(), labels.cuda()
                outputs = model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            accuracy = 100 * correct / total

            print(f'Accuracy of the model on the test set: {accuracy}%')

            if accuracy > 85:
                break


def main():
    if torch.cuda.is_available():
        print("CUDA is available, trying to use it.")
        device = torch.device("cuda")
    else:
        print("CUDA is not available.")
        device = torch.device("cpu")

    hidden_size = 64
    num_epochs = 30
    batch_size = 16
    learning_rate = 0.01

    train_loader, test_loader, input_size, num_classes = load_data('./data/input/train-ds.csv', './data/input/test-ds.csv', batch_size)

    print(f'Input size (X1, ..., Xn): {input_size}, Number of classes (Language): {num_classes}')

    model = MLP(input_size, hidden_size, num_classes).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    train_model(model, train_loader, test_loader, criterion, optimizer, num_epochs)

    # Save the trained model
    model_weights = model.state_dict();
    torch.save(model_weights, './output/mlp_model.ckpt')

if __name__ == '__main__':
    main()
