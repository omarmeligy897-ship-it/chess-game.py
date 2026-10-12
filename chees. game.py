import streamlit as st
import chess  # مكتبة إدارة قوانين الشطرنج الذكية

st.set_page_config(page_title="لعبة شطرنج القوانين - Streamlit", layout="centered")

st.markdown("<h2 style='text-align: center;'>لوحة شطرنج ذكية خاضعة للقوانين</h2>", unsafe_allow_html=True)

# ⚠️ علامتك المائية الثابتة
watermark_text = "PY/OMAR MELIGY"

# قاموس لترجمة رموز مكتبة chess إلى قطع يونيكود مرئية
PIECE_SYMBOLS = {
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙', # القطع البيضاء
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟'  # القطع السوداء
}

# إعداد اللعبة والذاكرة عند أول تشغيل
if 'board' not in st.session_state:
    st.session_state.board = chess.Board() # إنشاء رقعة شطرنج ذكية حقيقية
if 'selected_square' not in st.session_state:
    st.session_state.selected_square = None

# دالة التحكم بالضغط والنقلات القانونية
def handle_click(clicked_square):
    selected = st.session_state.selected_square
    board = st.session_state.board
    
    # الضغطة الأولى: اختيار قطعة
    if selected is None:
        if board.piece_at(clicked_square):
            st.session_state.selected_square = clicked_square
    # الضغطة الثانية: محاولة النقل
    else:
        # إنشاء حركية من المربع القديم إلى الجديد
        move = chess.Move(selected, clicked_square)
        
        # التعامل مع ترقية البيدق تلقائياً لوزير إذا وصل لنهاية الرقعة
        if board.piece_at(selected) and board.piece_at(selected).piece_type == chess.PAWN:
            if chess.square_rank(clicked_square) in:
                move.promotion = chess.QUEEN
        
        # 🛡️ التحقق الصارم: إذا كانت الحركة قانونية يتم تنفيذها، وإذا كانت عشوائية يتم تجاهلها
        if move in board.legal_moves:
            board.push(move)
        else:
            st.warning("⚠️ نقلة غير قانونية وفقاً لقوانين الشطرنج!")
            
        st.session_state.selected_square = None

# بناء الرقعة 8×8 (تنبيه: مكتبة chess تبدأ الحساب برمجياً من الأسفل للأعلى)
board_container = st.container()

with board_container:
    for row in range(8):
        cols = st.columns(8)
        for col in range(8):
            # تحويل إحداثيات العرض إلى مربعات نظام مكتبة chess
            square = chess.square(col, 7 - row)
            
            # تحديد لون المربع الافتراضي
            is_light = (row + col) % 2 == 0
            bg_color = "#f0d9b5" if is_light else "#b58863"
            
            # تلوين المربع بالأخضر إذا تم تحديده
            if st.session_state.selected_square == square:
                bg_color = "#7b9c5e"
            
            # جلب القطعة الحالية من المحرك الذكي
            piece = st.session_state.board.piece_at(square)
            button_text = PIECE_SYMBOLS[piece.symbol()] if piece else " "
            
            with cols[col]:
                st.button(
                    button_text, 
                    key=f"sq_{square}", 
                    on_click=handle_click, 
                    args=(square,),
                    use_container_width=True
                )

# زر لإعادة بدء اللعبة من جديد وتصفير اللوحة
if st.button("🔄 إعادة بدء اللعبة"):
    st.session_state.board = chess.Board()
    st.session_state.selected_square = None
    st.rerun()

# حقن كود الـ CSS لتلوين المربعات بدقة وإظهار علامتك المائية في الخلفية
st.markdown(f"""
    <style>
        div[data-testid="stButton"] button {{
            font-size: 32px !important;
            height: 65px !important;
            width: 100% !important;
            border: 1px solid rgba(0,0,0,0.1) !important;
            border-radius: 0px !important;
            color: #000000 !important;
        }}
        
        /* تلوين المربعات بالتبادل وإلغاء ألوان Streamlit الداكنة */
        div[data-testid="stHorizontalBlock"] > div:nth-child(even) button {{
            background-color: #f0d9b5 !important;
        }}
        div[data-testid="stHorizontalBlock"] > div:nth-child(odd) button {{
            background-color: #b58863 !important;
        }}
        
        /* علامة مائية مائلة واحترافية بالخلفية */
        .stMainBlockContainer::before {{
            content: "{watermark_text}";
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-30deg);
            font-size: 70px;
            font-weight: bold;
            font-family: Arial, sans-serif;
            color: rgba(255, 255, 255, 0.04);
            z-index: -1;
            pointer-events: none;
            white-space: nowrap;
        }}
    </style>
""", unsafe_allow_html=True)
