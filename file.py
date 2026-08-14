import streamlit as st

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="Чат 6 'Б'", page_icon="💬", layout="wide")
st.title("💬 Мессенджер 6 класса")

# ОБЩАЯ ПАМЯТЬ СЕРВЕРА
@st.cache_resource
class SharedChat:
    def __init__(self):
        self.messages = [
            {"name": "Система", "text": "Добро пожаловать в супер-защищенный чат! 🔐", "avatar": "🤖"}
        ]
        self.announcement = ""
        # 🎭 Переменная для пранка (изначально пустая)
        self.fake_user = ""
        
        # 🔑 ТАБЛИЦА СЕКРЕТНЫХ КЛЮЧЕЙ (Токенов) И ИМЁН
        self.tokens_db = {
            "boss_kain_777": "kain",    # Твой секретный ключ админа
            "artem_key_31": "Артем",
            "zera_pass_99": "Зарина",
            "art_token_55": "Артём",
            "6354_secret_12": "Эмилия",
            "lenaid_83463": "Лена",
            "markovka6583": "Марк"
        }

chat_storage = SharedChat()

# ЧИТАЕМ СЕКРЕТНЫЙ КЛЮЧ ИЗ ССЫЛКИ
query_params = st.query_params
user_token = query_params.get("token", None)

if user_token in chat_storage.tokens_db:
    real_user = chat_storage.tokens_db[user_token]
    
    # 🎭 ЛОГИКА МАСКИРОВКИ: Если админ включил пранк, подменяем его имя
    if real_user == "kain" and chat_storage.fake_user != "":
        current_user = chat_storage.fake_user
    else:
        current_user = real_user
        
    st.sidebar.success(f"Вход выполнен! Вы вошли как: {current_user} 😎")
    if real_user == "kain" and chat_storage.fake_user != "":
        st.sidebar.warning(f"⚠️ Включен режим маскировки под: {chat_storage.fake_user}")
    
    if chat_storage.announcement:
        st.warning(f"📢 **ВАЖНОЕ ОБЪЯВЛЕНИЕ ОТ АДМИНА:** {chat_storage.announcement}")
    
    # 👑 СЕКРЕТНОЕ МЕНЮ АДМИНА ДЛЯ KAIN (Доступно только по твоему НАСТОЯЩЕМУ токену)
    if real_user == "kain":
        st.sidebar.markdown("---")
        st.sidebar.subheader("👑 МЕНЮ СОЗДАТЕЛЯ (ПРОКАЧАННОЕ)")
        
        # 🎭 ФИЧА ПРАНКА: Выбор жертвы для маскировки
        st.sidebar.markdown("### 🎭 Режим маскировки")
        # Получаем список всех имен в чате, кроме самого kain
        all_users = [name for name in chat_storage.tokens_db.values() if name != "kain"]
        target_prank = st.sidebar.selectbox("Выберите кого разыграть:", all_users)
        
        if st.sidebar.button("🕵️‍♂️ Включить маскировку"):
            chat_storage.fake_user = target_prank
            st.rerun()
            
        if st.sidebar.button("❌ Сбросить маскировку (Стать kain)"):
            chat_storage.fake_user = ""
            st.rerun()
            
        st.sidebar.markdown("---")
        
        # Управление объявлением
        new_announcement = st.sidebar.text_input("Создать объявление для всех:")
        if st.sidebar.button("📢 Опубликовать объявление"):
            chat_storage.announcement = new_announcement
            st.rerun()
        if st.sidebar.button("🚫 Удалить объявление"):
            chat_storage.announcement = ""
            st.rerun()
            
        st.sidebar.markdown("---")
        
        # Очистка чата
        if st.sidebar.button("🧹 ОЧИСТИТЬ ВЕСЬ ЧАТ"):
            chat_storage.messages = [
                {"name": "Система", "text": "Чат был полностью очищен администратором kain! 🧼", "avatar": "🤖"}
            ]
            st.sidebar.success("История сообщений стерта!")
            st.rerun()
            
        st.sidebar.markdown("---")
        
        # Шпионский список токенов
        with st.sidebar.expander("👁️ Посмотреть список ключей"):
            st.write("Слева ключ, справа имя:")
            st.json(chat_storage.tokens_db)
        
        # Функция бана
        ban_token = st.sidebar.text_input("Введите КЛЮЧ (токен) для бана:")
        if st.sidebar.button("🔨 Забанить пользователя"):
            if ban_token in chat_storage.tokens_db and ban_token != "boss_kain_777":
                deleted_user = chat_storage.tokens_db[ban_token]
                del chat_storage.tokens_db[ban_token]
                st.sidebar.warning(f"Пользователь {deleted_user} успешно забанен!")
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

    # ОТПРАВКА СООБЩЕНИЯ
    if message := st.chat_input("Напишите сообщение..."):
        # Если маскировка включена, аватарка будет как у обычного игрока
        user_avatar = "👑" if current_user == "kain" else "🎒"
        chat_storage.messages.append({
            "name": current_user,
            "text": message,
            "avatar": user_avatar
        })
        st.rerun()

else:
    st.error("<code>❌ Доступ заблокирован! Неверный или отсутствующий ключ авторизации.</code>", icon="🔒")
    st.info("ℹ️ Для входа в мессенджер используйте только свою персональную ссылку, выданную kain.")
