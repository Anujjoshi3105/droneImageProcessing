import cv2
import numpy as np
from imutils import paths
import argparse
import os
import datetime

MATCH_DISTANCE_THRESHOLD = 0.6

def load_dataset(input_path):
    try:
        image_paths = sorted(list(paths.list_images(input_path)))
        images = [cv2.resize(cv2.imread(image_path), (0, 0), fx=0.5, fy=0.5) for image_path in image_paths]
        return images
    except Exception as e:
        print(f"Error loading images: {e}")
        return []

def stitch_images(image1, image2, feature_detector=cv2.ORB_create(), matcher=cv2.BFMatcher_create(cv2.NORM_HAMMING)):
    keypoints1, descriptors1 = feature_detector.detectAndCompute(image1, None)
    keypoints2, descriptors2 = feature_detector.detectAndCompute(image2, None)
    matches = matcher.knnMatch(descriptors1, descriptors2, k=2)

    good = [m for m, n in matches if m.distance < MATCH_DISTANCE_THRESHOLD * n.distance]

    MIN_MATCH_COUNT = 0
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        return wrap_images(image2, image1, M)
    else:
        print("Error: Insufficient matches")
        return None

def wrap_images(image1, image2, H):
    rows1, cols1 = image1.shape[:2]
    rows2, cols2 = image2.shape[:2]
    H_translation = np.array([[1, 0, cols1], [0, 1, rows1], [0, 0, 1]])
    output_img = cv2.warpPerspective(image2, H_translation.dot(H), (cols1 + cols2, rows1 + rows2))
    output_img[:rows1, :cols1] = image1
    return output_img

def main():
    parser = argparse.ArgumentParser(description='Image stitching script')
    parser.add_argument('input_path', help='Path to the input images')
    args = parser.parse_args()

    images = load_dataset(args.input_path)

    temp_image = None
    for idx, image in enumerate(images):
        temp_image = stitch_images(temp_image, image) if temp_image else image

    if temp_image is not None:
        cv2.imshow("output", temp_image)
        output_filename = f"output_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        cv2.imwrite(output_filename, temp_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()