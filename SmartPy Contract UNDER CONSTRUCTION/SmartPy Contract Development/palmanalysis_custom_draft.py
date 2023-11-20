from sklearn.decomposition import PCA
from skimage.feature import hog
import cv2
import numpy as np
import matplotlib.pyplot as plt
#5.4010313545241e+18 same hand different photo
#6.176472226998971e+18 comparing different hand
#7.005114015405684e+18 comparing different hand cropped
#5.4010313545241e+18 same hand different photo and cropped
#6.904699387965578e+17 same hand different photo, different lighting, different location and cropped


# Load and preprocess the image
image = cv2.imread(r"C:\Users\edens\Downloads\PXL_20231002_035542024.jpg")

#get the shape of the image
height, width, channels = image.shape

# Define the dimensions of the rectangle (width and height)
# Increase these values for a larger rectangle
rect_width = int(width * 0.9)  # 90% of image width
rect_height = int(height * 0.9)  # 90% of image height


# Calculate the starting x and y coordinates for the rectangle
start_x = (width - rect_width) // 2
start_y = (height - rect_height) // 2

mask = np.zeros(image.shape[:2], np.uint8)
#
bgd_model = np.zeros((1, 65), np.float64)
fgd_model = np.zeros((1, 65), np.float64)
#
rect = (start_x, start_y, rect_width, rect_height)  # (start_x, start_y, width, height)
cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
#
image = image * mask2[:, :, np.newaxis]

#save the image
cv2.imwrite(r"C:\Users\edens\Downloads\cropped.jpg", image)
# Convert to grayscale
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
resized_image = cv2.resize(image, (128, 128))


# Compute HOG features
hog_features = hog(resized_image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1))

# Perform PCA
pca = PCA(n_components=10)
pca_result = pca.fit_transform(resized_image)

# Combine HOG and PCA features
combined_features = np.concatenate((hog_features, pca_result.flatten()))

# Hash the combined features (using SHA-256 or your chosen algorithm)
hash1 = hash(tuple(combined_features))


# Load and preprocess the image
image = cv2.imread(r"C:\Users\edens\Downloads\PXL_20231002_035542024.jpg")

#get the shape of the image
height, width, channels = image.shape


# Calculate the starting x and y coordinates for the rectangle
start_x = (width - rect_width) // 2
start_y = (height - rect_height) // 2

mask = np.zeros(image.shape[:2], np.uint8)
#
bgd_model = np.zeros((1, 65), np.float64)
fgd_model = np.zeros((1, 65), np.float64)
#
rect = (start_x, start_y, rect_width, rect_height)  # (start_x, start_y, width, height)
cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
#
image = image * mask2[:, :, np.newaxis]


#show the image
cv2.imshow("Image", image)

# Convert to grayscale
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

resized_image = cv2.resize(image, (128, 128))

# Compute HOG features
hog_features = hog(resized_image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1))

# Perform PCA
pca = PCA(n_components=10)
pca_result = pca.fit_transform(resized_image)

# Combine HOG and PCA features
combined_features = np.concatenate((hog_features, pca_result.flatten()))

# Hash the combined features (using SHA-256 or your chosen algorithm)
hash2 = hash(tuple(combined_features))

# Compare the hashes using euclidean distance
distance = np.linalg.norm(hash1 - hash2)

print(distance)

# Store the hash on the blockchain
