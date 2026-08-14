import streamlit as st

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="Чат 6 'Б'", page_icon="💬", layout="wide")
st.title("💬 Мессенджер 6 класса")

# Используем общую память сервера, чтобы сообщения перелетали между всеми вкладками!
if "global_chat" not in st.session_state:
    st.session_state.global_chat = [
        {"name": "Система", "text": "Добро пожаловать в общий чат 6 класса! 🎉", "avatar": "🤖"}
    ]

# Список разрешенных пользователей
class_list = ["kain", "Артем", "Маша", "Данил", "София", "china"]

# ПАНЕЛЬ ВХОДА СЛЕВА
st.sidebar.header("🔑 Вход в систему")
name = st.sidebar.text_input("Введите ваше имя:")

if name in class_list:
    st.sidebar.success(f"Вы вошли как: {name} 😎")
    
    st.subheader("📋 История сообщений")
    
    # Кнопка для ручного обновления, если сидишь с разных вкладок
    if st.button("🔄 Обновить чат"):
        st.rerun()

    # ВЫВОД СООБЩЕНИЙ В СТИЛЕ ТЕЛЕГРАМА 
    for msg in st.session_state.global_chat:
        # st.chat_message сам рисует красивые облачка сообщений!
        with st.chat_message(msg["name"], avatar=msg["avatar"]):
            st.write(f"**{msg['name']}**")
            st.write(msg["text"])

    st.markdown("---")

    # ОТПРАВКА СООБЩЕНИЯ (Красивая ТГ-строка внизу)
    if message := st.chat_input("Напишите сообщение..."):
        # Выбираем аватарку в зависимости от того, кто пишет
        user_avatar = "👑" if name == "kain" else "🎒"
        
        # Добавляем сообщение в общую память сервера
        st.session_state.global_chat.append({
            "name": name,
            "text": message,
            "avatar": user_avatar
        })
        # Сразу обновляем экран, чтобы текст мгновенно появился
        st.rerun()

else:
    if name:
        st.sidebar.error("❌ Ошибка! Тебя нет в списке класса.")
    else:
        st.info("👋 Введи свое имя на панели слева, чтобы войти в мессенджер.")
