import os

def change_label_ids(label_dir, old_id, new_id):
    for split in ['train', 'valid', 'test']:
        path = os.path.join(label_dir, split, 'labels')
        for file in os.listdir(path):
            with open(os.path.join(path, file), 'r') as f:
                lines = f.readlines()
            new_lines = []
            for line in lines:
                parts = line.strip().split()
                parts[0] = str(new_id)
                new_lines.append(' '.join(parts) + '\n')
            with open(os.path.join(path, file), 'w') as f:
                f.writelines(new_lines)
    print("✅ Updated all label IDs for dataset:", label_dir)

change_label_ids('data2', 0, 1)
