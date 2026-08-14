import streamlit as st
from datetime import datetime
import pytz

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="Чат 6 'Б'", page_icon="💬", layout="wide")
st.title("💬 Мессенджер 6 класса")

# Твой часовой пояс (Пермский край)
LOCAL_TZ = pytz.timezone("Asia/Yekaterinburg")

# ОБЩАЯ ПАМЯТЬ СЕРВЕРА
@st.cache_resource
class SharedChat:
    def __init__(self):
        self.messages = [
            {"name": "Система", "text": "Добро пожаловать в мессенджер с индикатором онлайна! 🔐", "avatar": "🤖"}
        ]
        self.announcement = ""
        self.fake_user = ""
        
        # Общая база онлайна (имя: время последнего действия)
        self.online_users = {}
        
        # 🔑 ТАБЛИЦА СЕКРЕТНЫХ КЛЮЧЕЙ И ИМЁН
        self.tokens_db = {
            "boss_kain_777": "kain",
            "artem_key_31": "Артем 1",
            "zera_pass_99": "Зарина",
            "art_token_55": "Артем 2",
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
    
    # Режим маскировки для пранков
    if real_user == "kain" and chat_storage.fake_user != "":
        current_user = chat_storage.fake_user
    else:
        current_user = real_user
        
    st.sidebar.success(f"Вход выполнен! Вы вошли как: {current_user} 😎")
    
    # 🕒 ОБНОВЛЯЕМ СТАТУС ОНЛАЙН (Записываем текущее время в базу сервера)
    now_local = datetime.now(LOCAL_TZ)
    chat_storage.online_users[real_user] = now_local

    # 🟢 БЛОК ОТОБРАЖЕНИЯ ОНЛАЙНА НА БОКОВОЙ ПАНЕЛИ
    st.sidebar.markdown("---")
    st.sidebar.subheader("👥 Кто в сети:")
    
    for token_key, username in chat_storage.tokens_db.items():
        # Считаем, сколько секунд назад юзер подавал знак жизни
        if username in chat_storage.online_users:
            last_seen = chat_storage.online_users[username]
            seconds_passed = (datetime.now(LOCAL_TZ) - last_seen).total_seconds()
            
            # Если прошло меньше 10 секунд — он онлайн!
            if seconds_passed < 10:
                st.sidebar.write(f"🟢 **{username}** (в сети)")
            else:
                st.sidebar.write(f"⚪ *{username}* (был недавно)")
        else:
            st.sidebar.write(f"⚪ *{username}* (не в сети)")

    # 👑 СЕКРЕТНОЕ МЕНЮ АДМИНА ДЛЯ KAIN
    if real_user == "kain":
        st.sidebar.markdown("---")
        st.sidebar.subheader("👑 МЕНЮ СОЗДАТЕЛЯ")
        
        # Режим маскировки
        st.sidebar.markdown("### 🎭 Режим маскировки")
        all_users = [name for name in chat_storage.tokens_db.values() if name != "kain"]
        target_prank = st.sidebar.selectbox("Выберите кого разыграть:", all_users)
        
        if st.sidebar.button("🕵️‍♂️ Включить маскировку"):
            chat_storage.fake_user = target_prank
            st.rerun()
        if st.sidebar.button("❌ Сбросить маскировку"):
            chat_storage.fake_user = ""
            st.rerun()
            
        st.sidebar.markdown("---")
        
        # Управление объявлением
        new_announcement = st.sidebar.text_input("Создать объявление:")
        if st.sidebar.button("📢 Опубликовать"):
            chat_storage.announcement = new_announcement
            st.rerun()
        
        # Очистка чата
        if st.sidebar.button("🧹 ОЧИСТИТЬ ВЕСЬ ЧАТ"):
            chat_storage.messages = [{"name": "Система", "text": "Чат очищен админом kain! 🧼", "avatar": "🤖"}]
            st.rerun()
            
        # Список ключей
        with st.sidebar.expander("👁️ Список ключей"):
            st.json(chat_storage.tokens_db)

    # 🔄 МАГИЯ АВТО-ОБНОВЛЕНИЯ ЧАТА И ОНЛАЙНА
    @st.fragment(run_every="3s")
    def show_chat():
        if chat_storage.announcement:
            st.warning(f"📢 **ВАЖНОЕ ОБЪЯВЛЕНИЕ:** {chat_storage.announcement}")
            
        st.subheader("📋 История сообщений")
        
        for msg in chat_storage.messages:
            with st.chat_message(msg["name"], avatar=msg["avatar"]):
                st.write(f"**{msg['name']}**")
                st.write(msg["text"])

    # Запускаем наш обновляемый блок чата
    show_chat()

    st.markdown("---")

    # ОТПРАВКА СООБЩЕНИЯ
    if message := st.chat_input("Напишите сообщение..."):
        user_avatar = "👑" if current_user == "kain" else "🎒"
        chat_storage.messages.append({
            "name": current_user,
            "text": message,
            "avatar": user_avatar
        })
        st.rerun()

else:
    st.error("<code>❌ Доступ заблокирован!</code>", icon="🔒")
