from sklearn.decomposition import PCA
from skimage.feature import hog
import numpy as np
import cv2

def compare_images(image_path1, image_path2, resize_percentage):
    def process_image(image_path, resize_percentage):
        image = cv2.imread(image_path)
        height, width, channels = image.shape
        rect_width = int(width * resize_percentage)
        rect_height = int(height * resize_percentage)
        start_x = (width - rect_width) // 2
        start_y = (height - rect_height) // 2
        mask = np.zeros(image.shape[:2], np.uint8)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        rect = (start_x, start_y, rect_width, rect_height)
        cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        image = image * mask2[:, :, np.newaxis]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized_image = cv2.resize(image, (128, 128))
        hog_features = hog(resized_image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1))
        pca = PCA(n_components=10)
        pca_result = pca.fit_transform(resized_image)
        combined_features = np.concatenate((hog_features, pca_result.flatten()))
        return hash(tuple(combined_features))

    hash1 = process_image(image_path1, resize_percentage)
    hash2 = process_image(image_path2, resize_percentage)
    distance = np.linalg.norm(np.array(hash1) - np.array(hash2))
    return distance


import csv


csv_file_path = "distances.csv"
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["resize_percentage", "distance"])

# Define image paths
image_path1 = r"C:\Users\edens\Downloads\PXL_20231002_035549068.jpg"
image_path2 = r"C:\Users\edens\Downloads\PXL_20231002_145546283.jpg"

# Define a series of percentages
percentages = [0.5, 0.6, 0.7, 0.8]

# Loop through each percentage and calculate distance
for percentage in percentages:
    distance = compare_images(image_path1, image_path2, percentage)
    print(f"Calculated distance for {percentage * 100}%: {distance}")

    # Save to CSV
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([percentage, distance])

print(f"Distances saved to {csv_file_path}")

