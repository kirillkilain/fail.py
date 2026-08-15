import streamlit as st
from datetime import datetime
import pytz
import os
import random

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="Чат 6 'Б'", page_icon="💬", layout="wide")
st.title("🔥 Чат Ферамир")

# Твой часовой пояс (Пермский край)
LOCAL_TZ = pytz.timezone("Asia/Yekaterinburg")

# Пути к файлам в облаке
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_FILE = os.path.join(BASE_DIR, "chat_history.txt")
TEACHER_CHAT_FILE = os.path.join(BASE_DIR, "teacher_chat_history.txt")

# ОБЩАЯ СВЕРХБЫСТРАЯ ПАМЯТЬ СЕРВЕРА
@st.cache_resource
class SharedChat:
    def __init__(self):
        self.fake_user = ""
        self.online_users = {}
        self.user_statuses = {}
        self.moderators = []  
        self.admins = []      
        self.muted_users = [] 
        self.casino_history = {}
        self.private_messages = {}
        
        # 🔑 ТВОЯ ТАБЛИЦА ТОКЕНОВ ДЛЯ ВСЕГО КЛАССА
        self.tokens_db = {
            "boss_kain_777": "kain",
            "artem_key_31": "Артем 1",
            "zera_pass_99": "Зарина",
            "art_token_55": "Артем 2",
            "6354_secret_12": "Эмилия",
            "lenaid_83463": "Лена",
            "markovka6583": "Марк"
        }
        
        # 1. Загружаем чат БЕЗ учителя
        self.messages = []
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if "|" in line:
                        msg_name, msg_text, msg_avatar = line.strip().split("|", 2)
                        self.messages.append({"name": msg_name, "text": msg_text, "avatar": msg_avatar})
        else:
            self.messages.append({"name": "Система", "text": "Добро пожаловать в Чат БЕЗ Учителя! Свобода! 🎰", "avatar": "🤖"})

        # 2. Загружаем чат С учителем
        self.teacher_messages = []
        if os.path.exists(TEACHER_CHAT_FILE):
            with open(TEACHER_CHAT_FILE, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if "|" in line:
                        msg_name, msg_text, msg_avatar = line.strip().split("|", 2)
                        self.teacher_messages.append({"name": msg_name, "text": msg_text, "avatar": msg_avatar})
        else:
            self.teacher_messages.append({"name": "Система", "text": "Добро пожаловать в официальный Чат с Учителем. Ведите себя прилично! 🏫", "avatar": "🤖"})

chat_storage = SharedChat()

def get_rank(username):
    if username == "kain": return "👑 Создатель"
    if username not in chat_storage.tokens_db.values(): return "🔨 ЗАБАНЕН"
    if username in chat_storage.admins: return "🏆 Временный Админ"
    if username in chat_storage.moderators: return "⚡ Модератор (Мут)"
    return "🎒 Обычный Человек"

def load_private_chat(u1, u2):
    pair = tuple(sorted([u1, u2]))
    if pair in chat_storage.private_messages: return chat_storage.private_messages[pair]
    chat_storage.private_messages[pair] = []
    filename = os.path.join(BASE_DIR, f"private_{pair}_{pair}.txt")
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if "|" in line:
                    m_name, m_text, m_avatar = line.strip().split("|", 2)
                    chat_storage.private_messages[pair].append({"name": m_name, "text": m_text, "avatar": m_avatar})
    return chat_storage.private_messages[pair]

# 🔄 МАГИЯ АВТО-АВТОРИЗАЦИИ (Ищем токен в ссылке или в памяти приложения)
query_params = st.query_params
url_token = query_params.get("token", None)

if url_token:
    st.session_state["user_token"] = url_token

# Если токена нет ни в ссылке, ни в памяти — показываем форму авторизации
if "user_token" not in st.session_state:
    st.subheader("🔒 Авторизация в системе Ферамир")
    input_token = st.text_input("Введите ваш персональный секретный токен для входа:", type="password")
    if st.button("🚀 Войти в мессенджер"):
        if input_token in chat_storage.tokens_db:
            st.session_state["user_token"] = input_token
            st.success("Успешный вход! Загрузка чата...")
            st.rerun()
        else:
            st.error("Неверный токен! Доступ заблокирован.")
    st.info("ℹ️ Если у вас нет токена, обратитесь к Создателю чата (kain).")
    st.stop()

# Дальнейший код выполняется, только если авторизация успешна
user_token = st.session_state["user_token"]

if user_token in chat_storage.tokens_db:
    real_user = chat_storage.tokens_db[user_token]
    current_user = chat_storage.fake_user if (real_user == "kain" and chat_storage.fake_user) else real_user
        
    st.sidebar.success(f"Вы вошли как: {current_user} 😎")
    chat_storage.online_users[real_user] = datetime.now(LOCAL_TZ)

    # --- 🔀 ВЫБОР КОМНАТЫ ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("📂 Выбор комнаты")
    chat_mode = st.sidebar.radio("Куда зайти:", ["🏫 Чат с Учителем", "🤫 Чат БЕЗ Учителя", "🔒 Личные сообщения (ЛС)"])
    
    active_names = [n for n in chat_storage.tokens_db.values() if n != "kain"]
    all_names_for_dm = list(chat_storage.tokens_db.values())

    if chat_mode == "🔒 Личные сообщения (ЛС)":
        available_friends = [n for n in all_names_for_dm if n != current_user]
        dm_target = st.sidebar.selectbox("С кем шепчемся:", available_friends)
    else:
        dm_target = None

    # --- ПРОФИЛЬ И СТАТУС ---
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"🎖️ Звание: **{get_rank(current_user)}**")
    if current_user in chat_storage.muted_users: st.sidebar.error("🔇 Ты в муте!")
    
    current_status = chat_storage.user_statuses.get(current_user, "")
    new_status = st.sidebar.text_input("Твой статус:", value=current_status, max_chars=30)
    if new_status != current_status:
        chat_storage.user_statuses[current_user] = new_status
        st.rerun()

    # --- КАЗИК РАЗ В ДЕНЬ (Только в чате БЕЗ учителя) ---
    if chat_mode == "🤫 Чат БЕЗ Учителя":
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🎰 Казик на Админки")
        today_date = datetime.now(LOCAL_TZ).date()
        last_spin_date = chat_storage.casino_history.get(current_user, None)
        
        if last_spin_date == today_date and current_user != "kain":
            st.sidebar.warning("⏳ Слот заблокирован до завтра!")
        else:
            if st.sidebar.button("🎰 Крутить слоты!"):
                chat_storage.casino_history[current_user] = today_date
                slots = ["🍒", "🍋", "💎", "7️⃣", "🍉"]
                res1, res2, res3 = random.choice(slots), random.choice(slots), random.choice(slots)
                st.sidebar.subheader(f"🎰 [ {res1} | {res2} | {res3} ]")
                
                if res1 == res2 == res3:
                    st.balloons()
                    if res1 == "7️⃣":
                        chat_storage.admins.append(current_user)
                        chat_storage.messages.append({"name": "Система", "text": f"🎉 {current_user} выиграл АДМИНКУ! 🎉", "avatar": "🤖"})
                    elif res1 == "🍋":
                        chat_storage.moderators.append(current_user)
                        chat_storage.messages.append({"name": "Система", "text": f"⚡ {current_user} стал МОДЕРАТОРОМ! ⚡", "avatar": "🤖"})
                    st.rerun()
                else: st.sidebar.error("😢 Мимо!")

    # --- ПУЛЬТ СОЗДАТЕЛЯ ---
    if real_user == "kain":
        st.sidebar.markdown("---")
        st.sidebar.subheader("👑 ПУЛЬТ СОЗДАТЕЛЯ")
        target_user = st.sidebar.selectbox("Ученик:", [""] + active_names)
        new_rank = st.sidebar.selectbox("Ранг:", ["Обычный Человек", "Модератор (Мут)", "Временный Админ (Бан)"])
        if target_user and st.sidebar.button("⭐ Применить ранг"):
            if target_user in chat_storage.moderators: chat_storage.moderators.remove(target_user)
            if target_user in chat_storage.admins: chat_storage.admins.remove(target_user)
            if new_rank == "Модератор (Мут)": chat_storage.moderators.append(target_user)
            elif new_rank == "Временный Админ (Бан)": chat_storage.admins.append(target_user)
            st.rerun()
            
        if st.sidebar.button("🧹 СБРОСИТЬ ВСЕ ЧАТЫ"):
            chat_storage.moderators, chat_storage.admins, chat_storage.muted_users, chat_storage.casino_history = [], [], [], {}
            chat_storage.messages = [{"name": "Система", "text": "Чат сброшен Создателем kain! 🧼", "avatar": "🤖"}]
            chat_storage.teacher_messages = [{"name": "Система", "text": "Чат с учителем сброшен! 🏫", "avatar": "🤖"}]
            if os.path.exists(CHAT_FILE): os.remove(CHAT_FILE)
            if os.path.exists(TEACHER_CHAT_FILE): os.remove(TEACHER_CHAT_FILE)
            st.rerun()

    # --- ОНЛАЙН СТАТУСЫ ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("👥 В сети:")
    for token_key, username in chat_storage.tokens_db.items():
        if username in chat_storage.online_users:
            sec = (datetime.now(LOCAL_TZ) - chat_storage.online_users[username]).total_seconds()
            st.sidebar.write(f"{'🟢' if sec < 10 else '⚪'} **{username}** ({get_rank(username)})")
        else: st.sidebar.write(f"⚪ *{username}* (оффлайн) ({get_rank(username)})")

    # --- 🔄 АВТО-ОБНОВЛЕНИЕ ОТОБРАЖЕНИЯ КОМНАТ ---
    @st.fragment(run_every="4s")
    def show_chat_history(mode, target):
        if mode == "🏫 Чат с Учителем":
            st.subheader("🏫 Официальный chat 6 'Б' (С Учителем)")
            for msg in chat_storage.teacher_messages:
                with st.chat_message(msg["name"], avatar=msg["avatar"]):
                    st.write(f"**{msg['name']}**" if msg["name"] == "Система" else f"**{msg['name']}** ({get_rank(msg['name'])})")
                    st.write(msg["text"])
        elif mode == "🤫 Чат БЕЗ Учителя":
            st.subheader("🤫 Секретный чат (БЕЗ Учителя)")
            for msg in chat_storage.messages:
