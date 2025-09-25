import splitfolders

input_folder = r"P:\brain-tumor-detection\backend\dataset\Brain Tumor labeled dataset"
output_folder = r"P:\brain-tumor-detection\backend\dataset\split_dataset"

# Split: 70% train, 20% val, 10% test
splitfolders.ratio(input_folder, output=output_folder, seed=42, ratio=(0.7, 0.2, 0.1))
