import streamlit as st
from datetime import datetime
import pytz
import os
import random
import json
import urllib.request

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="Чат 6 'Б'", page_icon="💬", layout="wide")
st.title("🔥 Чат Ферамир")

# Твой часовой пояс (Пермский край)
LOCAL_TZ = pytz.timezone("Asia/Yekaterinburg")

# Пути к файлам в облаке
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_FILE = os.path.join(BASE_DIR, "chat_history.txt")
TEACHER_CHAT_FILE = os.path.join(BASE_DIR, "teacher_chat_history.txt")

# База фальшивых браузеров для обхода блокировок Cloudflare
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]

# СВЕРХНАДЕЖНАЯ ФУНКЦИЯ ГЕНЕРАЦИИ (Вынесена отдельно от интерфейса)
def generate_warp_config():
    st_data = {"key": "", "install_id": "", "fcm_token": ""}
    url = "https://cloudflareclient.com"
    try:
        req = urllib.request.Request(url, data=json.dumps(st_data).encode())
        req.add_header("Content-Type", "application/json; charset=utf-8")
        req.add_header("User-Agent", random.choice(USER_AGENTS))
        
        res = json.loads(urllib.request.urlopen(req).read().decode())
        private_key = res['config']['interface']['private_key']
        public_key = res['config']['peers']['public_key']
        
        config_text = (
            "[Interface]\n"
            f"PrivateKey = {private_key}\n"
            "Address = 172.16.0.2/32, 2606:4700:110:8101::2/128\n"
            "DNS = 1.1.1.1, 1.0.0.1\n\n"
            "[Peer]\n"
            f"PublicKey = {public_key}\n"
            "Endpoint = 162.159.193.1:2408\n"
            "AllowedIPs = 0.0.0.0/0, ::/0\n"
            "Jc = 4\n"
            "Jmin = 40\n"
            "Jmax = 70\n"
            "H1 = 1\n"
            "H2 = 2\n"
            "H3 = 3\n"
            "H4 = 4"
        )
        return config_text
    except Exception as e:
        return f"error: {e}"

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
        
        # 🔑 ТВОЯ ТАБЛИЦА ТОКЕНОВ
        self.tokens_db = {
            "boss_kain_777": "kain",
            "artem_key_31": "Артем 1",
            "zera_pass_99": "Зарина",
            "art_token_55": "Артем 2",
            "6354_secret_12": "Эмилия",
            "lenaid_83463": "Лена",
            "markovka6583": "Марк",
            "secret_teacher_6b": "Мария Ивановна"
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

# 🔄 УМНЫЙ ПОИСК ТОКЕНА В АДРЕСНОЙ СТРОКЕ
if "user_token" not in st.session_state:
    query_params = st.query_params
    url_token = query_params.get("token", None)
    if url_token:
        st.session_state["user_token"] = url_token

# Если токена нет вообще — показываем окно ввода
if "user_token" not in st.session_state:
    st.subheader("🔒 Авторизация в системе Ферамир")
    input_token = st.text_input("Введите ваш персональный секретный токен для входа:", type="password")
    if st.button("🚀 Войти в мессенджер"):
        if input_token in chat_storage.tokens_db:
            st.session_state["user_token"] = input_token
            st.query_params["token"] = input_token
            st.success("Успешный вход! Загрузка чата...")
            st.rerun()
        else:
            st.error("Неверный токен! Доступ заблокирован.")
    st.info("ℹ️ Если у вас нет токена, обратитесь к Создателю чата (kain).")
    st.stop()

# Читаем проверенный токен
user_token = st.session_state["user_token"]

if user_token in chat_storage.tokens_db:
    real_user = chat_storage.tokens_db[user_token]
    current_user = chat_storage.fake_user if (real_user == "kain" and chat_storage.fake_user) else real_user
        
    st.sidebar.success(f"Вы вошли как: {current_user} 😎")
    chat_storage.online_users[real_user] = datetime.now(LOCAL_TZ)

    # Удобная кнопка выхода
    if st.sidebar.button("🚪 Выйти из аккаунта"):
        if "user_token" in st.session_state:
            del st.session_state["user_token"]
        st.query_params.clear()
        st.rerun()

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

    # --- КАЗИК РАЗ В ДЕНЬ ---
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

    # --- 👑 ПУЛЬТ СОЗДАТЕЛЯ (Только для реального kain) ---
    if real_user == "kain":
        st.sidebar.markdown("---")
        st.sidebar.subheader("👑 ПУЛЬТ СОЗДАТЕЛЯ")
        
        target_user = st.sidebar.selectbox("Ученик:", [""] + active_names)
        new_rank = st.sidebar.selectbox("Ранг:", ["Обычный Человек", "Модератор (Мут)", "Временный Админ (Бан)"])
        if target_user and st.sidebar.button("⭐ Применить ранг"):
