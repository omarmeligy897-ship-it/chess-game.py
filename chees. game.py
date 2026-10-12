import streamlit as st

# إعداد الصفحة وتغيير عنوان التبويب
st.set_page_config(page_title="لعبة شطرنج - Streamlit", layout="centered")

st.markdown("<h2 style='text-align: center;'>لوحة شطرنج تفاعلية مع علامة مائية</h2>", unsafe_allow_html=True)

# ⚠️ اكتب اسمك أو توقيعك هنا ليظهر كعلامة مائية خلف اللوحة
watermark_text = "PY/OMAR MELIGY"

# إعداد مصفوفة قطع الشطرنج في ذاكرة التخزين المؤقت لـ Streamlit
if 'board_state' not in st.session_state:
    st.session_state.board_state = [
        ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
        ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
        ['',   '',   '',   '',   '',   '',   '',   ''],
        ['',   '',   '',   '',   '',   '',   '',   ''],
        ['',   '',   '',   '',   '',   '',   '',   ''],
        ['',   '',   '',   '',   '',   '',   '',   ''],
        ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
        ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
    ]
if 'selected_square' not in st.session_state:
    st.session_state.selected_square = None

# دالة التحكم بالنقلات والضغط على الأزرار
def handle_click(row, col):
    selected = st.session_state.selected_square
    
    # الضغطة الأولى: تحديد قطعة
    if selected is None:
        if st.session_state.board_state[row][col] != '':
            st.session_state.selected_square = (row, col)
    # الضغطة الثانية: نقل القطعة للمربع الجديد
    else:
        prev_row, prev_col = selected
        if (prev_row, prev_col) != (row, col):
            piece = st.session_state.board_state[prev_row][prev_col]
            st.session_state.board_state[row][col] = piece
            st.session_state.board_state[prev_row][prev_col] = ''
        
        st.session_state.selected_square = None

# بناء رقعة الشطرنج على المتصفح
board_container = st.container()

with board_container:
    for row in range(8):
        cols = st.columns(8)
        for col in range(8):
            is_light = (row + col) % 2 == 0
            
            # تحديد لون المربع (بيج أو بني) وتغييره للأخضر عند التحديد
            if st.session_state.selected_square == (row, col):
                bg_color = "#7b9c5e"
            else:
                bg_color = "#f0d9b5" if is_light else "#b58863"
                
            piece = st.session_state.board_state[row][col]
            button_text = piece if piece != '' else " "
            
            # عرض الأزرار وربطها بالتنسيق والعمليات
            with cols[col]:
                st.button(
                    button_text, 
                    key=f"sq_{row}_{col}", 
                    on_click=handle_click, 
                    args=(row, col),
                    use_container_width=True
                )

# حقن كود CSS لتنسيق المربعات وعرض العلامة المائية خلف اللعبة
# حقن كود CSS المطور لتلوين مربعات اللوحة وإظهار العلامة المائية بشكل صحيح
st.markdown(f"""
    <style>
        /* تنسيق أزرار مربعات الشطرنج وإجبار الألوان على الظهور بالتبادل */
        div[data-testid="stButton"] button {{
            font-size: 32px !important;
            height: 65px !important;
            width: 100% !important;
            border: 1px solid rgba(0,0,0,0.1) !important;
            border-radius: 0px !important;
            color: #000000 !important;
            transition: background-color 0.2s;
        }}

        /* تلوين المربعات البيضاء (الزوجية) */
        div[data-testid="stHorizontalBlock"] > div:nth-child(even) button {{
            background-color: #f0d9b5 !important;
        }}
        
        /* تلوين المربعات البنية (الفردية) */
        div[data-testid="stHorizontalBlock"] > div:nth-child(odd) button {{
            background-color: #b58863 !important;
        }}

        /* تأثير العلامة المائية المائلة في خلفية الموقع */
        .stMainBlockContainer::before {{
            content: "{watermark_text}";
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-30deg);
            font-size: 70px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color: rgba(255, 255, 255, 0.04); /* لون خفيف جداً متوافق مع المظهر المظلم */
            z-index: -1;
            pointer-events: none;
            white-space: nowrap;
        }}
    </style>
""", unsafe_allow_html=True)

  
