from ultralytics import YOLO
import numpy as np
import cv2
from show_result import plot_bboxes
from return_string import print_plate
from pre_process import pre_processing

detect_model = YOLO("D:/TIPA/License/Read_License_YOLOv8/models/Detect.pt")
ORC_model = YOLO("D:/TIPA/License/Read_License_YOLOv8/models/OCR.pt")

image_name = "TEST BIEN SO/no_support/IPSS2.7_s7aw.cn_2017-10-24.12-14-05.jpg"
image = cv2.imread(f"D:/TIPA/License/Read_License_YOLOv8/test/test_img/{image_name}")
image_arr = np.asarray(image)

license_results = detect_model.predict(image_arr)

boxes = license_results[0].boxes.xyxy.to('cpu').numpy().astype(int)
confidences = license_results[0].boxes.conf.to('cpu').numpy().astype(float)
labels = license_results[0].boxes.cls.to('cpu').numpy().astype(int) 

if len(boxes) == 0:
    print("""-------------------------------\nCan't detect any license plate\n-------------------------------""")
else:
    for box, conf, label in zip(boxes, confidences, labels):
        x_min, y_min, x_max, y_max = box
        image_crop = image[y_min:y_max, x_min:x_max]

    license_img = pre_processing(image_crop)
    results = ORC_model.predict(license_img)

    if len(results[0].boxes.boxes) == 0:
        print("""--------------------------------------\nCan't read any character from the plate\n--------------------------------------""")
    else:
        plot_bboxes(license_img, results[0].boxes.boxes, score=True, conf=0)
        print_plate(license_img, results[0].boxes.boxes)