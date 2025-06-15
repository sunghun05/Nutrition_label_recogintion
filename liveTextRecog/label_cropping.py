from ultralytics import YOLO
import cv2
import os


def cropping(source_img, classes_to_detect, save_dir='cropped'):

    model = YOLO('yolov8_project/exp/weights/best.pt')
    model.classes = classes_to_detect
    results = model.predict(source_img, conf=0.5)

    os.makedirs(save_dir, exist_ok=True)

    img = cv2.imread(source_img)

    for i, box in enumerate(results[0].boxes.xyxy):
        x1, y1, x2, y2 = map(int, box[:4])

        crop = img[y1:y2, x1:x2]

        cv2.imwrite(f'{save_dir}/{os.path.basename(source_img)}_crop_{i}.jpg', crop)
        print(i)

def process_folder(image_folder):
    for file in os.listdir(image_folder):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            full_path = os.path.join(image_folder, file)
            cropping(source_img=full_path,
             classes_to_detect=[0])


if __name__ == "__main__":
    folder_path = './images'
    process_folder(folder_path)

