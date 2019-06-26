from FraudBillBoardsDetectionApp import string_matching_kmp
from text_detection_and_recognition.text_recognition import start_ocr_job
from FraudBillBoardsDetectionApp.constants import application_constants
import cv2
import os


def accuracy_with_single_alphabets_per_image(img_name, labeled_data_file_name):
    args_for_ocr_job = dict()
    args_for_ocr_job["image"] = application_constants['text_data_location'] + img_name
    image = cv2.imread(args_for_ocr_job["image"])
    (origH, origW) = image.shape[:2]
    origH = (origH // 32) * 32
    origW = (origW // 32) * 32

    print(origW, origH)
    args_for_ocr_job["east"] = application_constants['east_text_detector_location']
    args_for_ocr_job["min_confidence"] = 0.3
    args_for_ocr_job["height"] = origH
    args_for_ocr_job["width"] = origW
    args_for_ocr_job["padding"] = 0.04

    text_detected = start_ocr_job(args_for_ocr_job)

    accuracy = 0.0
    expected_all_text = ''
    matched_patterns = 0
    expected_patterns = 0

    with open(labeled_data_file_name) as file:
        for line in file:
            l = line.split(',')
            text = l[len(l) - 1]
            if text != '###':
                expected_all_text = expected_all_text + text
                expected_patterns = expected_patterns + 1

    for text in text_detected:
        formatted_text = ''
        for i in range(len(text)):
            ch_ascii = ord(text[i])
            if (ch_ascii >= ord('a') and ch_ascii <= ord('z')) or (ch_ascii >= ord('A') and ch_ascii <= ord('Z')):
                formatted_text = formatted_text + text[i]

        match = string_matching_kmp.KMPSearch(formatted_text.lower(), expected_all_text.lower())
        if match is True:
            matched_patterns = matched_patterns + 1

    accuracy = matched_patterns / expected_patterns
    return accuracy


def accuracy_for_multiple_images():
    accuracy = 0.0
    images = 0
    for file in os.listdir(application_constants['test_images_location']):
        accuracy = accuracy + accuracy_with_single_alphabets_per_image(application_constants['test_images_location'] + file,
                                                                       application_constants['test_images_location'] + 'gt_' + file)
        images = images + 1

    return accuracy / images


if __name__ == '__main__':
    #print(accuracy_for_multiple_images())
    filename = 'img_1'
    print(accuracy_with_single_alphabets_per_image(application_constants['test_images_location'] + filename,
                                                   application_constants['test_images_location'] + 'gt_' + filename))


