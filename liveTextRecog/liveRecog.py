from ultralytics import YOLO
import cv2

model = YOLO('yolov8_project/exp/weights/best.pt')
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, img = cap.read()
    if not ret:
        break

    results = model.predict(img)

    # Annotator 대신 OpenCV로 직접 박스 그리기[1][4]
    for r in results:
        for box in r.boxes:
            # 좌표 추출 및 정수 변환
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            # 박스 그리기
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # 라벨 추가
            label = f"{model.names[int(box.cls)]} {box.conf.item():.2f}"
            cv2.putText(img, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow('YOLOv8 Detection', img)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()
