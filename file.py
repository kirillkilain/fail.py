import streamlit as st
from streamlit_cookies_controller import CookieController

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="Чат 6 'Б'", page_icon="💬", layout="wide")
st.title("💬 Мессенджер 6 класса")

# Инициализируем контроллер куки (память браузера)
cookies = CookieController()

# ОБЩАЯ ПАМЯТЬ СЕРВЕРА
@st.cache_resource
class SharedChat:
    def __init__(self):
        self.messages = [
            {"name": "Система", "text": "Добро пожаловать в защищенный чат 6 класса! 🎉", "avatar": "🤖"}
        ]
        self.users_db = {
            "kain": "boss6b"
        }

chat_storage = SharedChat()

# ПРОВЕРЯЕМ: Помнит ли браузер этого пользователя?
saved_user = cookies.get("saved_user_6b")

login_success = False
current_user = ""

# Если браузер помнит имя, сразу пускаем в чат без пароля!
if saved_user and saved_user in chat_storage.users_db:
    login_success = True
    current_user = saved_user

# Если браузер никого не помнит — показываем форму входа/регистрации
if not login_success:
    st.sidebar.header("🚪 Личный кабинет")
    menu_mode = st.sidebar.radio("Выберите действие:", ["Войти", "Регистрация"])

    if menu_mode == "Регистрация":
        st.sidebar.subheader("📝 Создать новый аккаунт")
        reg_name = st.sidebar.text_input("Придумайте ник (имя):", key="reg_n")
        reg_pass = st.sidebar.text_input("Придумайте пароль:", type="password", key="reg_p")
        
        if st.sidebar.button("Зарегистрироваться"):
            if not reg_name.strip() or not reg_pass.strip():
                st.sidebar.error("❌ Имя и пароль не могут быть пустыми!")
            elif reg_name in chat_storage.users_db:
                st.sidebar.error("❌ Этот ник уже занят!")
            elif len(chat_storage.users_db) >= 8:
                st.sidebar.error("❌ В чате уже максимум участников (8 человек)!")
            else:
                chat_storage.users_db[reg_name] = reg_pass
                st.sidebar.success("🎉 Зарегистрировано! Теперь переключитесь на 'Войти'.")

    else:
        st.sidebar.subheader("🔑 Вход в систему")
        login_name = st.sidebar.text_input("Введите имя:", key="log_n")
        login_pass = st.sidebar.text_input("Введите пароль:", type="password", key="log_p")
        
        if st.sidebar.button("Войти"):
            if login_name in chat_storage.users_db and chat_storage.users_db[login_name] == login_pass:
                # 📜 ВАЖНЫЙ ШАГ: Прячем имя в память браузера на долгое время
                cookies.set("saved_user_6b", login_name)
                st.rerun()
            else:
                st.sidebar.error("❌ Неверное имя или пароль!")

# --- ГЛАВНЫЙ ЭКРАН (ОТКРЫВАЕТСЯ ДЛЯ ТЕХ, КТО МИШУРАНУЛ ВХОД ИЛИ КОГО ПОМНЯТ) ---
if login_success:
    st.sidebar.success(f"Вы вошли как: {current_user} 😎")
    
    # Кнопка «Выйти», чтобы сбросить авто-вход
    if st.sidebar.button("🚪 Выйти из аккаунта"):
        cookies.remove("saved_user_6b")
        st.rerun()
    
    # 👑 СЕКРЕТНАЯ АДМИНКА ДЛЯ KAIN
    if current_user == "kain":
        st.sidebar.markdown("---")
        st.sidebar.subheader("👑 Меню создателя")
        st.sidebar.write("Участники в базе:", list(chat_storage.users_db.keys()))
        
        ban_name = st.sidebar.text_input("Кого вычеркнуть (забанить)?")
        if st.sidebar.button("🔨 Забанить"):
            if ban_name in chat_storage.users_db and ban_name != "kain":
                del chat_storage.users_db[ban_name]
                st.sidebar.warning(f"Пользователь {ban_name} удален!")
                st.rerun()

    # ОТОБРАЖЕНИЕ ЧАТА
    st.subheader("📋 История сообщений")
    
    if st.button("🔄 Обновить чат"):
        st.rerun()

    for msg in chat_storage.messages:
        with st.chat_message(msg["name"], avatar=msg["avatar"]):
            st.write(f"**{msg['name']}**")
            st.write(msg["text"])

    st.markdown("---")

    if message := st.chat_input("Напишите сообщение..."):
        user_avatar = "👑" if current_user == "kain" else "🎒"
        chat_storage.messages.append({
            "name": current_user,
            "text": message,
            "avatar": user_avatar
        })
        st.rerun()

else:
    if 'menu_mode' in locals() and menu_mode == "Войти":
        st.info("👋 Введите свои данные слева, чтобы войти в мессенджер.")
