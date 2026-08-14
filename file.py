import streamlit as st

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="Чат 6 'Б'", page_icon="💬", layout="wide")
st.title("💬 Мессенджер 6 класса")

# МАГИЯ ОБЩЕЙ ПАМЯТИ ДЛЯ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ В ИНТЕРНЕТЕ
@st.cache_resource
class SharedChat:
    def __init__(self):
        # Этот список сообщений будет ОДИН на весь интернет для всех вкладок
        self.messages = [
            {"name": "Система", "text": "Добро пожаловать в общий чат 6 класса! 🎉", "avatar": "🤖"}
        ]
        # Общий список класса
        self.class_list = ["kain", "Артем", "Маша", "Данил", "София", "china"]

# Подключаемся к общему хранилищу
chat_storage = SharedChat()

# ПАНЕЛЬ ВХОДА СЛЕВА
st.sidebar.header("🔑 Вход в систему")
name = st.sidebar.text_input("Введите ваше имя:")

if name in chat_storage.class_list:
    st.sidebar.success(f"Вы вошли как: {name} 😎")
    
    st.subheader("📋 История сообщений")
    
    # Кнопка для ручного обновления чата
    if st.button("🔄 Обновить чат"):
        st.rerun()

    # ВЫВОД СООБЩЕНИЙ С СЕРВЕРА
    for msg in chat_storage.messages:
        with st.chat_message(msg["name"], avatar=msg["avatar"]):
            st.write(f"**{msg['name']}**")
            st.write(msg["text"])

    st.markdown("---")

    # 👑 СЕКРЕТНАЯ АДМИНКА ДЛЯ KAIN
    if name == "kain":
        st.sidebar.markdown("---")
        st.sidebar.subheader("👑 Меню создателя")
        
        # Функция бана
        ban_name = st.sidebar.text_input("Кого вычеркнуть?")
        if st.sidebar.button("🔨 Забанить"):
            if ban_name in chat_storage.class_list:
                chat_storage.class_list.remove(ban_name)
                st.sidebar.warning(f"{ban_name} удален!")
                st.rerun()
                
        # Функция разбана
        unban_name = st.sidebar.text_input("Кого вернуть?")
        if st.sidebar.button("✅ Разбанить"):
            if unban_name not in chat_storage.class_list and unban_name.strip() != "":
                chat_storage.class_list.append(unban_name)
                st.sidebar.success(f"{unban_name} вернулся!")
                st.rerun()

    # ОТПРАВКА СООБЩЕНИЯ
    if message := st.chat_input("Напишите сообщение..."):
        user_avatar = "👑" if name == "kain" else "🎒"
        
        # Записываем в ОБЩУЮ память сервера
        chat_storage.messages.append({
            "name": name,
            "text": message,
            "avatar": user_avatar
        })
        st.rerun()

else:
    if name:
        st.sidebar.error("❌ Ошибка! Тебя нет в списке класса.")
    else:
        st.info("👋 Введи свое имя на панели слева, чтобы войти в мессенджер.")
