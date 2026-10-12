import tkinter as tk

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("شطرنج تفاعلي - Tkinter")
        
        # إعدادات حجم الرقعة والألوان
        self.size = 8
        self.square_size = 70
        self.light_color = "#f0d9b5"
        self.dark_color = "#b58863"
        self.selected_color = "#7b9c5e"
        
        self.selected_square = None
        
        # توزيع قطع الشطرنج المبدئي (رموز يونيكود)
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
        
        # إنشاء مصفوفة لتخزين الأزرار (المربعات)
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.create_board()

    def create_board(self):
        """إنشاء رقعة الشطرنج وتوزيع الأزرار"""
        for row in range(self.size):
            for col in range(self.size):
                # تحديد لون المربع بالتبادل
                bg_color = self.light_color if (row + col) % 2 == 0 else self.dark_color
                
                # إنشاء مربع كـ Button وتعيين الخط والحجم
                btn = tk.Button(
                    self.root, 
                    text=self.board_state[row][col], 
                    font=("Segoe UI Historic", 26), 
                    bg=bg_color, 
                    activebackground=bg_color,
                    command=lambda r=row, c=col: self.on_square_click(r, c)
                )
                # وضع المربع في المكان الصحيح داخل الشبكة
                btn.grid(row=row, column=col, width=4, height=1)
                self.buttons[row][col] = btn

    def on_square_click(self, row, col):
        """إدارة عملية الضغط وتحريك القطع"""
        # الضغطة الأولى: اختيار قطعة لتحريكها
        if self.selected_square is None:
            if self.board_state[row][col] != '':
                self.selected_square = (row, col)
                self.buttons[row][col].config(bg=self.selected_color) # تلوين المربع المختار بالأخضر
        
        # الضغطة الثانية: نقل القطعة إلى المكان الجديد
        else:
            prev_row, prev_col = self.selected_square
            
            # إذا ضغط اللاعب على نفس المربع مجدداً، يتم إلغاء التحديد
            if (prev_row, prev_col) == (row, col):
                self.reset_square_color(prev_row, prev_col)
                self.selected_square = None
                return
            
            # نقل رمز القطعة في المصفوفة البرمجية
            piece = self.board_state[prev_row][prev_col]
            self.board_state[row][col] = piece
            self.board_state[prev_row][prev_col] = ''
            
            # تحديث النص (المرئي) على الأزرار
            self.buttons[row][col].config(text=piece)
            self.buttons[prev_row][prev_col].config(text='')
            
            # إعادة لون المربع القديم لطبيعته وإعادة تعيين الاختيار
            self.reset_square_color(prev_row, prev_col)
            self.selected_square = None

    def reset_square_color(self, row, col):
        """إعادة المربع إلى لونه الأصلي (بني أو بيج)"""
        original_color = self.light_color if (row + col) % 2 == 0 else self.dark_color
        self.buttons[row][col].config(bg=original_color)

# تشغيل اللعبة
if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()
