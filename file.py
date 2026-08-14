import streamlit as st
from datetime import datetime
import pytz
import os

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="Чат 6 'Б'", page_icon="💬", layout="wide")
st.title("💬 Мессенджер 6 класса")

# Твой часовой пояс (Пермский край)
LOCAL_TZ = pytz.timezone("Asia/Yekaterinburg")

# Определяем надежное место для хранения файла в облаке
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_FILE = os.path.join(BASE_DIR, "chat_history.txt")

# Если файла с историей еще нет на сервере, создаем его
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        f.write("Система|Добро пожаловать в вечный чат 6 класса! 🔐|🤖\n")

# ОБЩАЯ ПАМЯТЬ СЕРВЕРА (Для онлайна и пранков)
@st.cache_resource
class SharedChat:
    def __init__(self):
        self.announcement = ""
        self.fake_user = ""
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
    
    # ОБНОВЛЯЕМ СТАТУС ОНЛАЙН
    now_local = datetime.now(LOCAL_TZ)
    chat_storage.online_users[real_user] = now_local

    # БЛОК ОТОБРАЖЕНИЯ ОНЛАЙНА
    st.sidebar.markdown("---")
    st.sidebar.subheader("👥 Кто в сети:")
    for token_key, username in chat_storage.tokens_db.items():
        if username in chat_storage.online_users:
            last_seen = chat_storage.online_users[username]
            seconds_passed = (datetime.now(LOCAL_TZ) - last_seen).total_seconds()
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
        
        # Жесткая очистка файла чата
        if st.sidebar.button("🧹 ОЧИСТИТЬ ВЕСЬ ЧАТ"):
            with open(CHAT_FILE, "w", encoding="utf-8") as f:
                f.write("Система|Чат был полностью очищен администратором kain! 🧼|🤖\n")
            st.rerun()
            
        with st.sidebar.expander("👁️ Список ключей"):
            st.json(chat_storage.tokens_db)

    # 🔄 МАГИЯ ВЕЧНОГО АВТО-ОБНОВЛЕНИЯ ЧАТА ИЗ ФАЙЛА
    @st.fragment(run_every="3s")
    def show_chat():
        if chat_storage.announcement:
            st.warning(f"📢 **ВАЖНОЕ ОБЪЯВЛЕНИЕ:** {chat_storage.announcement}")
            
        st.subheader("📋 История сообщений")
        
        # Читаем сообщения прямо из вечного текстового файла
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            for line in lines:
                if "|" in line:
                    msg_name, msg_text, msg_avatar = line.strip().split("|", 2)
                    with st.chat_message(msg_name, avatar=msg_avatar):
                        st.write(f"**{msg_name}**")
                        st.write(msg_text)

    show_chat()
    st.markdown("---")

    # ОТПРАВКА СООБЩЕНИЯ (С записью в файл)
    if message := st.chat_input("Напишите сообщение..."):
        user_avatar = "👑" if current_user == "kain" else "🎒"
        
        # Записываем строчку в файл на сервере через разделитель "|"
        with open(CHAT_FILE, "a", encoding="utf-8") as f:
            f.write(f"{current_user}|{message}|{user_avatar}\n")
        st.rerun()

else:
    st.error("<code>❌ Доступ заблокирован!</code>", icon="🔒")
