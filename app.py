import streamlit as st
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="Админ-панель Меню Кафе", layout="wide")

# Инициализация "базы данных" в сессии (чтобы данные не пропадали при обновлении страницы)
if 'menu' not in st.session_state:
    st.session_state.menu = [
        {"Категория": "Завтраки", "Название": "Омлет", "Описание": "Классический из 3 яиц", "Цена": 250, "Фото": None},
        {"Категория": "Напитки", "Название": "Капучино", "Описание": "200 мл, арабика", "Цена": 180, "Фото": None}
    ]

st.title("🍴 Управление Онлайн-Меню")

# --- БОКОВАЯ ПАНЕЛЬ (Добавление блюда) ---
st.sidebar.header("Добавить новое блюдо")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_cat = st.selectbox("Категория", ["Завтраки", "Супы", "Горячее", "Десерты", "Напитки"])
    new_name = st.text_input("Название блюда")
    new_desc = st.text_area("Описание")
    new_price = st.number_input("Цена", min_value=0)
    new_photo = st.file_uploader("Загрузить фото", type=["jpg", "jpeg", "png"])
    
    submit = st.form_submit_button("Добавить в меню")
    
    if submit and new_name:
        st.session_state.menu.append({
            "Категория": new_cat,
            "Название": new_name,
            "Описание": new_desc,
            "Цена": new_price,
            "Фото": new_photo
        })
        st.success(f"Блюдо '{new_name}' добавлено!")

# --- ОСНОВНАЯ ЧАСТЬ (Отображение и удаление) ---
categories = list(set([item["Категория"] for item in st.session_state.menu]))

for cat in categories:
    st.header(f"--- {cat} ---")
    
    # Фильтруем блюда по категории
    items_to_show = [i for i in st.session_state.menu if i["Категория"] == cat]
    
    for idx, item in enumerate(st.session_state.menu):
        if item["Категория"] == cat:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if item["Фото"]:
                    st.image(item["Фото"], width=150)
                else:
                    st.gray()
                    st.write("Нет фото")
            
            with col2:
                st.subheader(item["Название"])
                st.write(item["Описание"])
                st.write(f"**Цена: {item['Цена']} руб.**")
            
            with col3:
                # Кнопка удаления
                if st.button(f"Удалить {item['Название']}", key=f"del_{item['Название']}_{idx}"):
                    st.session_state.menu.remove(item)
                    st.rerun()
            st.divider()
