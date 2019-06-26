from text_detection_and_recognition.text_recognition import start_ocr_job
from FraudBillBoardsDetectionApp.constants import application_constants
import cv2
import string
import os


def accuracy_with_single_alphabets_per_image(img_name, labbeled_data_file_name):
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

    all_text_detected = ''
    expected_all_text = ''

    for text in text_detected:
        formatted_text = ''
        for i in range(len(text)):
            ch_ascii = ord(text[i])
            if (ch_ascii >= ord('a') and ch_ascii <= ord('z')) or (ch_ascii >= ord('A') and ch_ascii <= ord('Z')):
                formatted_text = formatted_text + text[i]

        all_text_detected = all_text_detected + formatted_text

    all_text_detected = all_text_detected.lower()
    count_of_each_alphabet = dict()
    expected_count_of_each_alphabet = dict()

    for ch in string.ascii_lowercase:
        count_of_each_alphabet[ch] = 0
        expected_count_of_each_alphabet[ch] = 0

    for i in range(len(all_text_detected)):
        count_of_each_alphabet[all_text_detected[i]] = count_of_each_alphabet[all_text_detected[i]] + 1

    with open(labbeled_data_file_name) as file:
        for line in file:
            l = line.split(',')
            text = l[len(l) - 1]
            if text != '###':
                expected_all_text = expected_all_text + text

    for i in range(len(expected_all_text)):
        expected_count_of_each_alphabet[expected_all_text[i]] = expected_count_of_each_alphabet[expected_all_text[i]] + 1

    accuracy = 0.0

    for ch in string.ascii_lowercase:
        if expected_count_of_each_alphabet[ch] != 0:
            if count_of_each_alphabet[ch] <= expected_count_of_each_alphabet[ch]:
                accuracy = accuracy + (count_of_each_alphabet[ch] / expected_count_of_each_alphabet[ch]) * 100.0
            else:
                accuracy = accuracy + 100.0

    return accuracy / 26.0


def accuracy_for_multiple_images():
    accuracy = 0.0
    images = 0
    for file in os.listdir(application_constants['test_images_location']):
        accuracy = accuracy + accuracy_with_single_alphabets_per_image(
            application_constants['test_images_location'] + file,
            application_constants['test_images_location'] + 'gt_' + file)
        images = images + 1

    return accuracy / images


if __name__ == '__main__':
    # print(accuracy_for_multiple_images())
    filename = 'img_1'
    print(accuracy_with_single_alphabets_per_image(application_constants['test_images_location'] + filename,
                                                   application_constants['test_images_location'] + 'gt_' + filename))


