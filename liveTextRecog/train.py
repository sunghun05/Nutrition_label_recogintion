from ultralytics import YOLO
import multiprocessing

def main():
    # 사전학습된 모델 불러오기 (yolov8n.pt, yolov8s.pt 등 선택 가능)
    model = YOLO('yolov8n.pt')

    # 학습 실행
    results = model.train(
        data='dataset/data.yaml',   # data.yaml 파일 경로
        epochs=100,                 # 학습 epoch 수
        imgsz=640,                  # 입력 이미지 크기
        batch=32,                   # 배치 사이즈
        workers=4,                  # 데이터 로더 워커 수
        project='yolov8_project',   # 결과 저장 폴더
        name='exp',                 # 실험명
        device=0,                   # GPU 번호 (여러개면 [0,1] 등)
        verbose=True,               # 로그 출력
        exist_ok=True,              # 기존 폴더 덮어쓰기 허용
        augment=True                # 데이터 증강 사용
    )
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()

