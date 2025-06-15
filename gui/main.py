import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class FridgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("냉장고 식품 관리 및 레시피 추천 시스템")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.food_list = []

        self.setup_ui()

    def setup_ui(self):
        # 좌측 패널
        self.left_frame = ctk.CTkFrame(self, width=200)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.image_label = ctk.CTkLabel(self.left_frame, text="업로드된 이미지", width=180, height=180, fg_color="gray90")
        self.image_label.pack(pady=10)

        self.food_name_entry = ctk.CTkEntry(self.left_frame, placeholder_text="재고 이름")
        self.food_name_entry.pack(pady=5)

        self.upload_button = ctk.CTkButton(self.left_frame, text="이미지 업로드", command=self.upload_image)
        self.upload_button.pack(pady=5)

        self.register_button = ctk.CTkButton(self.left_frame, text="재고 등록", command=self.register_food)
        self.register_button.pack(pady=5)

        # 중앙 패널 - 재고 목록
        self.center_frame = ctk.CTkFrame(self)
        self.center_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.food_list_label = ctk.CTkLabel(self.center_frame, text="현재 재고", font=("Arial", 14))
        self.food_list_label.pack(anchor="nw", pady=5)

        self.food_list_frame = ctk.CTkScrollableFrame(self.center_frame, height=450)
        self.food_list_frame.pack(fill="both", expand=True, padx=10)

        # 우측 패널 - 추천 레시피
        self.right_frame = ctk.CTkFrame(self, width=300)
        self.right_frame.pack(side="right", fill="both", padx=10, pady=10)

        self.recipe_label = ctk.CTkLabel(self.right_frame, text="추천 레시피", font=("Arial", 14))
        self.recipe_label.pack(anchor="nw", pady=5)

        self.recipe_listbox = ctk.CTkTextbox(self.right_frame, height=500)
        self.recipe_listbox.pack(fill="both", padx=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((180, 180))
            self.photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=self.photo, text="")

    def register_food(self):
        food_name = self.food_name_entry.get()
        if food_name:
            item_frame = ctk.CTkFrame(self.food_list_frame)
            item_frame.pack(fill="x", pady=2, padx=5)

            food_label = ctk.CTkLabel(item_frame, text=f"• {food_name}  (영양정보 표시)", anchor="w")
            food_label.pack(side="left", fill="x", expand=True)

            delete_btn = ctk.CTkButton(item_frame, text="재고 삭제", width=80, command=lambda: item_frame.destroy())
            delete_btn.pack(side="right")

            self.food_list.append(food_name)
            self.update_recipe_list()

    def update_recipe_list(self):
        self.recipe_listbox.delete("0.0", "end")
        if not self.food_list:
            self.recipe_listbox.insert("end", "현재 재고가 없습니다.\n")
        else:
            self.recipe_listbox.insert("end", "재고를 바탕으로 추천된 메뉴:\n\n")
            for food in self.food_list:
                self.recipe_listbox.insert("end", f"• {food} 활용 요리\n  - (영양정보)\n  - 필요한 재료 예시\n\n")

if __name__ == "__main__":
    app = FridgeApp()
    app.mainloop()
