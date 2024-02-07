import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.optim as optim
from torchvision.models import resnet50


def define_model(num_classes, train_path, test_path, learning_rate=0.001, num_epochs=10, batch_size=32):
    """
    Defines and trains a ResNet-50 model for binary classification.

    Args:
        num_classes (int): Number of output classes (usually 2 for binary classification).
        train_path (str): Path to the training dataset.
        test_path (str): Path to the testing dataset.
        learning_rate (float, optional): Learning rate for the optimizer. Default is 0.001.
        num_epochs (int, optional): Number of training epochs. Default is 10.
        batch_size (int, optional): Batch size for training. Default is 32.

    Returns:
        Trained model.
    """
    # Check if CUDA (GPU) is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Define data transformations
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Load training and validation datasets
    train_dataset = torchvision.datasets.ImageFolder(root=train_path, transform=transform)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # Load testing dataset
    test_dataset = torchvision.datasets.ImageFolder(root=test_path, transform=transform)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    # Initialize ResNet-50
    model = resnet50(pretrained=True)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, num_classes)  # Adjust for desired output classes

    # Move model to GPU if available
    model.to(device)

    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Training loop
    for epoch in range(num_epochs):
        model.train()
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

    # Validation
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f"Accuracy on testing dataset: {accuracy:.2f}%")

    return model
