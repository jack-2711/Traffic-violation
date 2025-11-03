import os, shutil

# Paths to your two datasets
DATASETS = ['data1', 'data2']
OUT = 'combined'  # output folder

splits = ['train', 'valid', 'test']

for split in splits:
    for subfolder in ['images', 'labels']:
        os.makedirs(os.path.join(OUT, split, subfolder), exist_ok=True)

    for dataset in DATASETS:
        img_src = os.path.join(dataset, split, 'images')
        lbl_src = os.path.join(dataset, split, 'labels')
        img_dst = os.path.join(OUT, split, 'images')
        lbl_dst = os.path.join(OUT, split, 'labels')

        for f in os.listdir(img_src):
            shutil.copy(os.path.join(img_src, f), os.path.join(img_dst, f))
        for f in os.listdir(lbl_src):
            shutil.copy(os.path.join(lbl_src, f), os.path.join(lbl_dst, f))

print("✅ All datasets merged successfully into 'combined/' folder!")
