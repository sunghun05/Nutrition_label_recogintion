from tkinter import *
from PIL import Image, ImageTk

def show_image(index):
    image_label.config(image=images[index])
    image_label.image = images[index]  # 참조 유지
    message_label.config(text=f"지금 선택한 그림은 {names[index]}입니다.")  # 텍스트 업데이트

root = Tk()
root.title("가위 바위 보")

# 이미지 열기
img_scissors = Image.open("scissors.png").resize((150, 150))
img_rock = Image.open("rock.png").resize((150, 150))
img_paper = Image.open("paper.png").resize((150, 150))

# PIL 이미지를 Tkinter용 이미지로 변환
tk_img_scissors = ImageTk.PhotoImage(img_scissors)
tk_img_rock = ImageTk.PhotoImage(img_rock)
tk_img_paper = ImageTk.PhotoImage(img_paper)

images = [tk_img_scissors, tk_img_rock, tk_img_paper]
names = ["가위", "바위", "보"]

# 이미지 표시용 라벨
image_label = Label(root, image=images[0])
image_label.pack(pady=10)

# 문구 표시용 라벨
message_label = Label(root, text="선택한 그림이 여기에 표시됩니다.", font=("Arial", 12))
message_label.pack(pady=5)

# 버튼 3개
Button(root, text="가위", command=lambda: show_image(0)).pack(pady=5)
Button(root, text="바위", command=lambda: show_image(1)).pack(pady=5)
Button(root, text="보", command=lambda: show_image(2)).pack(pady=5)

root.mainloop()
