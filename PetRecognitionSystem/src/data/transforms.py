from torchvision import transforms

def get_train_transforms(image_size):
    """
    Data Augmentation pipeline for training.
    Includes random cropping, flipping, and color jitter to prevent overfitting.
    """
    return transforms.Compose([
        transforms.Resize((int(image_size * 1.2), int(image_size * 1.2))),
        transforms.RandomCrop((image_size, image_size)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2), # Robustness to lighting
        transforms.RandomRotation(10), # Robustness to orientation
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

def get_val_transforms(image_size):
    """
    Transforms for validation/inference.
    Only resizing and normalization.
    """
    return transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
