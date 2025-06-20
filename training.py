import os
import numpy as np ,shutil,random,re
from PIL import Image 
# ----------- Dataset Split -----------

data_path = 'dataset/'

# print("Looking in folder:", data_path)
# print("Files in folder:", os.listdir(data_path))

train_folder = os.path.join("train_validation/train")
validation_folder = os.path.join("train_validation/validation")

split_ratio = 0.7  # 70% train and 30% val

# Clean old folders
for d in [train_folder, validation_folder]:
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)

# Loop over each class folder
for class_name in os.listdir(data_path):
    class_path = os.path.join(data_path, class_name)
    if not os.path.isdir(class_path):
        continue

    images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(images)

    split_index = int(len(images) * split_ratio)
    train_images = images[:split_index]
    val_images = images[split_index:]

    # Create class folders in train and val
    os.makedirs(os.path.join(train_folder, class_name), exist_ok=True)
    os.makedirs(os.path.join(validation_folder, class_name), exist_ok=True)

    # Copy train images
    for img in train_images:
        shutil.copy(os.path.join(class_path, img), os.path.join(train_folder, class_name, img))

    # Copy val images
    for img in val_images:
        shutil.copy(os.path.join(class_path, img), os.path.join(validation_folder, class_name, img))

print("✅ Dataset split complete. All  classes are present in both train and val.")

# ----------- Split Data Organize -----------
def organize_images(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            cleaned = re.sub(r'\s*\([^)]*\)', '', filename)
            class_name = os.path.splitext(cleaned)[0]
            

            class_folder = os.path.join(folder_path, class_name)
            os.makedirs(class_folder, exist_ok=True)

            src_path = os.path.join(folder_path, filename)
            dst_path = os.path.join(class_folder, filename)
            shutil.move(src_path, dst_path)
            print(f"Moved {filename} → {class_name}/")

# ----------- IntelDataset Class -----------
class IntelDataset:
    def __init__(self, data_path):
        self.data_path = data_path
        self.image_files = []
        self.labels = []

        self.class_names = sorted(os.listdir(data_path))  
        self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.class_names)}
        print("Interldatset..")
        for cls in self.class_names:
            cls_folder = os.path.join(data_path, cls)
            for filename in os.listdir(cls_folder):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    self.image_files.append(os.path.join(cls_folder, filename))
                    self.labels.append(self.class_to_idx[cls])

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = self.image_files[idx]
        label = self.labels[idx]

        image = Image.open(img_path).convert("RGB")
        image = image.resize((224, 224))  # Resize all images to 224x224
        image = np.array(image) / 255.0   # Normalize to [0,1]
        return image, label

# ----------- Custom Dataloader -----------
class Dataloader:
    def __init__(self, dataset1, dataset2, batch_size, shuffle=False):
        print("dataloader ...")
        self.dataset1 = dataset1
        self.dataset2 = dataset2
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __len__(self):
        return min(len(self.dataset1), len(self.dataset2)) // self.batch_size

    def __iter__(self):
        data_len = self.__len__() * self.batch_size

        if self.shuffle:
            indices = np.random.permutation(data_len)
        else:
            indices = np.arange(data_len)

        for i in range(self.__len__()):
            batch_indices = indices[i * self.batch_size: (i + 1) * self.batch_size]

            batch1 = [self.dataset1[idx] for idx in batch_indices]
            images1, targets1 = zip(*batch1)
            images1 = np.stack(images1, axis=0)
            targets1 = np.stack(targets1, axis=0)

            batch2 = [self.dataset2[idx] for idx in batch_indices]
            images2, targets2 = zip(*batch2)
            images2 = np.stack(images2, axis=0)
            targets2 = np.stack(targets2, axis=0)

            yield images1, targets1, images2, targets2

organize_images(train_folder)
organize_images(validation_folder)

# ----------- Initialize Datasets & Dataloader -----------
dataset1 = IntelDataset(data_path="train_validation/train")
dataset2 = IntelDataset(data_path="train_validation/validation")

dataloader = Dataloader(dataset1, dataset2, batch_size=32, shuffle=False)

# ----------- Iterate Through Batches -----------
for i, (images1, targets1, images2, targets2) in enumerate(dataloader):
    print(f"Batch {i+1}")
    print("Train batch - images:", images1.shape, "labels:", targets1)
    print("validation batch  - images:", images2.shape, "labels:", targets2)
    
    if i == 2:  # Only show first 3 batches
        break
