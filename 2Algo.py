import cv2
import numpy as np
import os
import time

def preprocess_image(image_path):
    # Load fingerprint image in BMP format
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    
    # Perform adaptive thresholding to binarize the image
    _, thresholded = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    return thresholded

def extract_minutiae(image):
    # Create a skeleton image of the fingerprint
    skeleton = thinning(image)
    
    # Extract minutiae from the skeleton image
    minutiae = find_minutiae(skeleton)
    
    return minutiae

def thinning(image):
    size = np.size(image)
    skel = np.zeros(image.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False

    while not done:
        eroded = cv2.erode(image, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(image, temp)
        skel = cv2.bitwise_or(skel, temp)
        image = eroded.copy()

        zeros = size - cv2.countNonZero(image)
        if zeros == size:
            done = True

    return skel

def find_minutiae(skeleton):
    # Apply Harris corner detection to find minutiae
    keypoints = cv2.cornerHarris(skeleton, 5, 3, 0.04)
    keypoints = cv2.normalize(keypoints, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # Threshold the keypoints to obtain binary image
    _, keypoints_binary = cv2.threshold(keypoints, 150, 255, cv2.THRESH_BINARY)
    
    # Find contours in the binary image to locate minutiae
    contours, _ = cv2.findContours(keypoints_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    minutiae = [cv2.minEnclosingCircle(contour)[0] for contour in contours]
    
    return minutiae

def match_fingerprints(image1_path, image2_path):
    # Preprocess both fingerprint images
    image1 = preprocess_image(image1_path)
    image2 = preprocess_image(image2_path)
    
    # Extract minutiae from both images
    minutiae1 = extract_minutiae(image1)
    minutiae2 = extract_minutiae(image2)
    
    # Calculate similarity score based on matched minutiae
    similarity_score = calculate_similarity(minutiae1, minutiae2)
    
    return similarity_score

def calculate_similarity(minutiae1, minutiae2):
    if len(minutiae1) == 0 or len(minutiae2) == 0:
        return 0.0
    
    # Match minutiae based on Euclidean distance
    matched_minutiae = 0
    for m1 in minutiae1:
        for m2 in minutiae2:
            distance = np.linalg.norm(np.array(m1) - np.array(m2))
            if distance < 5:  # Adjust threshold as needed
                matched_minutiae += 1
    
    # Calculate similarity score as a percentage of matched minutiae
    similarity_score = (matched_minutiae / max(len(minutiae1), len(minutiae2))) * 100
    
    return similarity_score


# Example usage
image2_path = 'fingerprints/proj2/1__M_Left_index_finger_CR.BMP'

database_path = 'fingerprints/proj/'

Max_accuracy = 0

startTime = time.time()
for file in [file for file in os.listdir(database_path)]: 
    similarity_score = match_fingerprints(database_path + file, image2_path)
    Max_accuracy = max(Max_accuracy,similarity_score)
end_time = time.time()

print(f"Similarity Score: {Max_accuracy:.2f}%")
print(f"Time taken to match: {end_time - startTime:.2f}")

