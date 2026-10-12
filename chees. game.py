import tkinter as tk

class ChessGameWithWatermark:
    def __init__(self, root):
        self.root = root
        self.root.title("شطرنج مع علامة مائية - Tkinter")
        
        self.size = 8
        self.light_color = "#f0d9b5"
        self.dark_color = "#b58863"
        self.selected_color = "#7b9c5e"
        
        # ⚠️ اكتب اسمك أو توقيعك هنا ليظهر كعلامة مائية خلف المربعات
        self.watermark_text = "PY/OMAR MELIGY" 
        
        self.selected_square = None
        
        # توزيع قطع الشطرنج المبدئي
        self.board_state = [
            ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
            ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
            ['',   '',   '',   '',   '',   '',   '',   ''],
            ['',   '',   '',   '',   '',   '',   '',   ''],
            ['',   '',   '',   '',   '',   '',   '',   ''],
            ['',   '',   '',   '',   '',   '',   '',   ''],
            ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
            ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
        ]
        
        # إعداد حاوية رئيسية تسمح بوضع طبقات (مربعات فوق العلامة المائية)
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(padx=20, pady=20)
        
        # 1. إضافة نص العلامة المائية في الخلفية تماماً
        self.watermark_label = tk.Label(
            self.main_container, 
            text=self.watermark_text, 
            font=("Arial", 36, "bold italic"), 
            fg="#d0b493",  # لون باهت وقريب من لون اللوحة ليظهر كعلامة مائية خفية
            alpha=0.3
        )
        # وضع العلامة المائية في منتصف الشاشة تماماً خلف اللوحة
        self.watermark_label.place(relx=0.5, rely=0.5, anchor="center")

        # 2. بناء الرقعة فوق الخلفية
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.create_board()

    def create_board(self):
        for row in range(self.size):
            for col in range(self.size):
                bg_color = self.light_color if (row + col) % 2 == 0 else self.dark_color
                
                # جعل الأزرار شبه شفافة أو بدون حواف سميكة لكي تندمج مع الخلفية
                btn = tk.Button(
                    self.main_container, 
                    text=self.board_state[row][col], 
                    font=("Segoe UI Historic", 26), 
                    bg=bg_color, 
                    activebackground=bg_color,
                    bd=0, # إلغاء الحواف لجعل الرقعة متناسقة
                    command=lambda r=row, c=col: self.on_square_click(r, c)
                )
                btn.grid(row=row, column=col, width=4, height=1)
                self.buttons[row][col] = btn

    def on_square_click(self, row, col):
        if self.selected_square is None:
            if self.board_state[row][col] != '':
                self.selected_square = (row, col)
                self.buttons[row][col].config(bg=self.selected_color)
        else:
            prev_row, prev_col = self.selected_square
            if (prev_row, prev_col) == (row, col):
                self.reset_square_color(prev_row, prev_col)
                self.selected_square = None
                return
            
            piece = self.board_state[prev_row][prev_col]
            self.board_state[row][col] = piece
            self.board_state[prev_row][prev_col] = ''
            
            self.buttons[row][col].config(text=piece)
            self.buttons[prev_row][prev_col].config(text='')
            
            self.reset_square_color(prev_row, prev_col)
            self.selected_square = None

    def reset_square_color(self, row, col):
        original_color = self.light_color if (row + col) % 2 == 0 else self.dark_color
        self.buttons[row][col].config(bg=original_color)

if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGameWithWatermark(root)
    root.mainloop()
