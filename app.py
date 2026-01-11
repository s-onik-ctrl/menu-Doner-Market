import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO

# --- 1. НАСТРОЙКИ (ЗАМЕНИТЕ ССЫЛКУ НИЖЕ) ---
# Ссылка должна быть с доступом "Все, у кого есть ссылка - Читатель"
SHEET_URL = "https://docs.google.com/spreadsheets/d/18_UvUWeE3YyaTGGWuh-7jpvhksocqaOHWGWHxVTPCOM/edit?usp=sharing"

# --- 2. ФУНКЦИЯ ЗАГРУЗКИ ДАННЫХ ---
def load_data(url):
    try:
        # Преобразование ссылки для прямого скачивания CSV
        csv_url = url.replace('/edit?usp=sharing', '/export?format=csv').replace('/edit#gid=', '/export?format=csv&gid=')
        data = pd.read_csv(csv_url)
        # Очистка данных от пустых строк
        data = data.dropna(subset=['Название'])
        return data
    except Exception as e:
        st.error(f"Ошибка подключения к таблице: {e}")
        return None

# --- 3. КОНФИГУРАЦИЯ СТРАНИЦЫ ---
st.set_page_config(page_title="Digital Menu", layout="wide", initial_sidebar_state="collapsed")

# Кастомный CSS для красоты
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1 { color: #2c3e50; text-align: center; font-family: 'Helvetica'; }
    h2 { color: #e67e22; border-bottom: 2px solid #e67e22; padding-bottom: 5px; margin-top: 40px; }
    .dish-card { background: white; padding: 20px; border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ОСНОВНОЙ ИНТЕРФЕЙС ---
st.title("🍴 Добро пожаловать в наше Кафе")
st.markdown("<p style='text-align: center;'>Свежие продукты и авторские рецепты каждый день</p>", unsafe_allow_html=True)

# Загрузка данных
df = load_data(SHEET_URL)

if df is not None:
    # --- БОКОВАЯ ПАНЕЛЬ С QR ---
    with st.sidebar:
        st.header("📱 Для гостей")
        menu_url = st.text_input("URL этого сайта (после деплоя):", "https://my-menu.streamlit.app")
        if st.button("Создать QR-код"):
            qr = qrcode.make(menu_url)
            buf = BytesIO()
            qr.save(buf)
            st.image(buf.getvalue(), caption="Сканируйте для входа в меню")
        
        st.divider()
        st.info(f"Чтобы изменить меню, отредактируйте свою [Google Таблицу]({SHEET_URL})")

    # --- ВЫВОД МЕНЮ ПО КАТЕГОРИЯМ ---
    categories = df['Категория'].unique()

    for cat in categories:
        st.header(f"📂 {cat}")
        category_items = df[df['Категория'] == cat]
        
        for idx, row in category_items.iterrows():
            with st.container():
                # Создаем колонки: Фото | Описание | Цена
                col1, col2, col3 = st.columns([1.5, 3, 1])
                
                with col1:
                    if pd.notna(row['Фото']) and str(row['Фото']).startswith('http'):
                        st.image(row['Фото'], use_container_width=True)
                    else:
                        st.write("🖼️ *Нет фото*")
                
                with col2:
                    # Формируем название с бейджами (Острое/Новинка)
                    icons = ""
                    if row.get('Новинка') == 1: icons += " ✨"
                    if row.get('Острое') == 1: icons += " 🔥"
                    
                    st.subheader(f"{row['Название']}{icons}")
                    st.write(f"*{row['Описание']}*")
                    
                    if row.get('Новинка') == 1:
                        st.caption("✨ Рекомендуем попробовать!")
                
                with col3:
                    st.write("##") # Отступ
                    st.metric(label="Цена", value=f"{int(row['Цена'])} ₽")
                
                st.divider()
else:
    st.warning("Ожидание подключения к базе данных...")

# --- 5. ФУТЕР ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>📍 Ул. Примерная, 10 | 🕒 09:00 - 22:00</p>", unsafe_allow_html=True)  

# Right-click code on any website to run it here
# Or, write your own Python code below
# Click 💾 to save your code as a clip Welcome to Python Playground! 🐍
# 
# This is a browser extension that lets you write and run 
# Python code directly in your browser.
#
# Get started by writing some Python code below and 
# clicking the "Run" button. You can also create new files
# using the (+) button or upload files using the upload 
# icon (↑) in the sidebar. To use external libraries, import 
# them directly. Install additional PyPI packages using 
# the "Manage Packages" button.
#
# Try this example:

print("Hello, Python Playground!")

# Happy coding!
