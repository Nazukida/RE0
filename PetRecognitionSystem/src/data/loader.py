import os
from torch.utils.data import Dataset, DataLoader
from PIL import Image, UnidentifiedImageError
from .transforms import get_train_transforms, get_val_transforms
from glob import glob
import logging

logger = logging.getLogger("PetRecSystem")

class PetDataset(Dataset):
    def __init__(self, root_dir, mode='train', transform=None):
        """
        Custom Dataset for Pet Images with Robust Error Handling.
        Args:
            root_dir (str): Path to dataset folder (e.g., .../PetImages).
            mode (str): 'train' or 'val'.
            transform (callable, optional): Transform to be applied on a sample.
        """
        self.root_dir = root_dir
        self.mode = mode
        self.transform = transform
        self.image_paths = []
        self.labels = [] # 0: Cat, 1: Dog
        
        # Handle folder mapping (some datasets use 'val', some 'test')
        target_dir = os.path.join(root_dir, mode)
        if not os.path.exists(target_dir):
            if mode == 'val' and os.path.exists(os.path.join(root_dir, 'test')):
                target_dir = os.path.join(root_dir, 'test')
                print(f"Mapping 'val' mode to 'test' folder at {target_dir}")
            elif mode == 'train' and not os.path.exists(os.path.join(root_dir, 'train')):
                # Maybe user just provided root?
                 if os.path.exists(os.path.join(root_dir, 'Cat')):
                     target_dir = root_dir # Use root as train dir if no train folder
            else:
                 print(f"Directory {target_dir} not found. Dataset might be empty.")

        self.target_dir = target_dir
        self.classes = ['Cat', 'Dog'] 
        
        # Determine actual class names (case-insensitive)
        if os.path.exists(target_dir):
            subdirs = [d for d in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, d))]
            found_classes = []
            for cls_name in ['Cat', 'Dog', 'cat', 'dog']:
                if cls_name in subdirs and cls_name not in found_classes:
                     found_classes.append(cls_name)
            
            # Use found classes if valid
            if len(found_classes) >= 2:
                self.classes = sorted(found_classes)[:2] # Take first two if more
            elif len(subdirs) >= 2:
                self.classes = sorted(subdirs)[:2] # Fallback to any 2 folders

        print(f"Loading {mode} dataset from {target_dir} with classes: {self.classes}")

        for label_idx, class_name in enumerate(self.classes):
            class_dir = os.path.join(target_dir, class_name)
            if os.path.exists(class_dir):
                # Recursively find images
                files = []
                for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.JPG']:
                    files.extend(glob(os.path.join(class_dir, ext)))
                
                # Basic validation: Filter out empty files
                valid_files = [f for f in files if os.path.getsize(f) > 0]
                
                self.image_paths.extend(valid_files)
                self.labels.extend([label_idx] * len(valid_files))

        if len(self.image_paths) == 0:
            print(f"WARNING: No images found in {target_dir}. Please check your dataset path.")

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        if idx >= len(self.image_paths):
            idx = 0 
            
        img_path = self.image_paths[idx]
        label = self.labels[idx]

        try:
            with Image.open(img_path) as img:
                image = img.convert('RGB')
                
            if self.transform:
                image = self.transform(image)
                
            return image, label
            
        except (UnidentifiedImageError, OSError, Exception) as e:
            # Handle corrupted images (common in PetImages dataset)
            # print(f"Skipping corrupt image: {img_path}")
            # Try next image (simple retry logic)
            new_idx = (idx + 1) % len(self.image_paths)
            return self.__getitem__(new_idx)


def get_loaders(config):
    train_transform = get_train_transforms(config['image_size'])
    val_transform = get_val_transforms(config['image_size'])
    
    train_dataset = PetDataset(config['dataset_path'], mode='train', transform=train_transform)
    val_dataset = PetDataset(config['dataset_path'], mode='val', transform=val_transform)
    
    train_loader = DataLoader(
        train_dataset, 
        batch_size=config['batch_size'], 
        shuffle=True, 
        num_workers=4, 
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset, 
        batch_size=config['batch_size'], 
        shuffle=False, 
        num_workers=4,
        pin_memory=True
    )
    
    return train_loader, val_loader
