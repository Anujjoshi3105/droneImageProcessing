import cv2
import os
import sys

def compare_folders(folder1, folder2):
    files_folder1 = set(os.listdir(folder1))
    files_folder2 = set(os.listdir(folder2))

    files_only_in_folder1 = files_folder1 - files_folder2
    return files_only_in_folder1

def convert_to_gray(input_img, output_img):
    img = cv2.imread(input_img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_img, gray)

def rgb_to_gray(folder1, folder2):
    while True:
        files_to_convert = compare_folders(folder1, folder2)

        for img_file in files_to_convert:
            input_path = os.path.join(folder1, img_file)
            output_path = os.path.join(folder2, img_file)
            convert_to_gray(input_path, output_path)
        sleep(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("file not given !")
        sys.exit(1)

    rgb_to_gray(sys.argv[1], sys.argv[2])