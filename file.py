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

# Пути к вечным файлам в облаке
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_FILE = os.path.join(BASE_DIR, "chat_history.txt")

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
        
        # 🔑 ТВОЯ ТАБЛИЦА ТОКЕНОВ
        self.tokens_db = {
            "boss_kain_777": "kain",
            "artem_key_31": "Артем 1",
            "zera_pass_99": "Зарина",
            "art_token_55": "Артем 2",
            "6354_secret_12": "Эмилия",
            "lenaid_83463": "Лена",
            "markovka6583": "Марк"
        }
        
        # Загружаем сообщения из файла ОДИН РАЗ при старте
        self.messages = []
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines:
                if "|" in line:
                    msg_name, msg_text, msg_avatar = line.strip().split("|", 2)
                    self.messages.append({"name": msg_name, "text": msg_text, "avatar": msg_avatar})
        else:
            self.messages.append({"name": "Система", "text": "Добро пожаловать в скоростной Чат Ферамир! 🎰", "avatar": "🤖"})

chat_storage = SharedChat()

def get_rank(username):
    if username == "kain": return "👑 Создатель"
    if username not in chat_storage.tokens_db.values(): return "🔨 ЗАБАНЕН"
    if username in chat_storage.admins: return "🏆 Временный Админ"
    if username in chat_storage.moderators: return "⚡ Модератор (Мут)"
    return "🎒 Обычный Чебурек"

# ЧИТАЕМ СЕКРЕТНЫЙ КЛЮЧ ИЗ ССЫЛКИ
query_params = st.query_params
user_token = query_params.get("token", None)

if user_token in chat_storage.tokens_db:
    real_user = chat_storage.tokens_db[user_token]
    if real_user == "kain" and chat_storage.fake_user:
        current_user = chat_storage.fake_user
    else:
        current_user = real_user
        
    st.sidebar.success(f"Вы вошли как: {current_user} 😎")
    
    # ОБНОВЛЯЕМ СТАТУС ОНЛАЙН
    chat_storage.online_users[real_user] = datetime.now(LOCAL_TZ)

    # --- ПРОФИЛЬ И СТАТУС ---
    st.sidebar.markdown(f"🎖️ Звание: **{get_rank(current_user)}**")
    if current_user in chat_storage.muted_users:
        st.sidebar.error("🔇 Ты в муте!")
    
    current_status = chat_storage.user_statuses.get(current_user, "")
    new_status = st.sidebar.text_input("Твой status:", value=current_status, max_chars=30)
    if new_status != current_status:
        chat_storage.user_statuses[current_user] = new_status
        st.rerun()

    # --- КАЗИК РАЗ В ДЕНЬ ---
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
            else:
                st.sidebar.error("😢 Мимо! Попытка использована.")

    # --- ПАНЕЛЬ МОДЕРАТОРА / АДМИНА ---
    is_moderator = current_user in chat_storage.moderators
    is_admin = current_user in chat_storage.admins
    active_names = [n for n in chat_storage.tokens_db.values() if n != "kain"]
    
    if is_moderator or is_admin:
        st.sidebar.markdown("---")
        if is_moderator:
            mute_target = st.sidebar.selectbox("Мут (Модератор):", [""] + active_names, key="mod_m")
            if mute_target and st.sidebar.button("🔇 Мут", key="mod_m_btn"):
                if mute_target not in chat_storage.muted_users:
                    chat_storage.muted_users.append(mute_target)
                    st.rerun()
        if is_admin:
            ban_target = st.sidebar.selectbox("Бан (Админ):", [""] + active_names, key="adm_b")
            if ban_target and st.sidebar.button("🔨 Бан", key="adm_b_btn"):
                if ban_target != "kain":
                    tok = [k for k, v in chat_storage.tokens_db.items() if v == ban_target]
                    if tok:
                        del chat_storage.tokens_db[tok[0]]
                        st.rerun()

    # --- ГЛАВНЫЙ ПУЛЬТ СОЗДАТЕЛЯ (Только для реального kain) ---
    if real_user == "kain":
        st.sidebar.markdown("---")
        st.sidebar.subheader("👑 ПУЛЬТ СОЗДАТЕЛЯ")
        
        target_user = st.sidebar.selectbox("Ученик:", [""] + active_names)
        new_rank = st.sidebar.selectbox("Ранг:", ["Обычный Чебурек", "Модератор (Мут)", "Временный Админ (Бан)"])
        if target_user and st.sidebar.button("⭐ Применить ранг"):
            if target_user in chat_storage.moderators: chat_storage.moderators.remove(target_user)
            if target_user in chat_storage.admins: chat_storage.admins.remove(target_user)
            if new_rank == "Модератор (Мут)": chat_storage.moderators.append(target_user)
            elif new_rank == "Временный Админ (Бан)": chat_storage.admins.append(target_user)
            st.rerun()
            
        target_prank = st.sidebar.selectbox("Маскировка под:", active_names)
        if st.sidebar.button("🕵️‍♂️ Маскировка"): chat_storage.fake_user = target_prank; st.rerun()
        if st.sidebar.button("❌ Сброс"): chat_storage.fake_user = ""; st.rerun()
            
        if st.sidebar.button("🧹 СБРОСИТЬ ВСЁ"):
            chat_storage.moderators, chat_storage.admins, chat_storage.muted_users, chat_storage.casino_history = [], [], [], {}
            chat_storage.messages = [{"name": "Система", "text": "Чат сброшен Создателем kain! 🧼", "avatar": "🤖"}]
            if os.path.exists(CHAT_FILE): os.remove(CHAT_FILE)
            st.rerun()

    # --- ОНЛАЙН СТАТУСЫ ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("👥 В сети:")
    for token_key, username in chat_storage.tokens_db.items():
        if username in chat_storage.online_users:
            sec = (datetime.now(LOCAL_TZ) - chat_storage.online_users[username]).total_seconds()
            st.sidebar.write(f"{'🟢' if sec < 10 else '⚪'} **{username}** ({get_rank(username)})")
        else:
            st.sidebar.write(f"⚪ *{username}* (оффлайн) ({get_rank(username)})")

    # --- СВЕРХБЫСТРЫЙ ВЫВОД ЧАТА (Из памяти сервера) ---
    st.subheader("📋 История сообщений")
    
    if st.button("🔄 Проверить новые сообщения"):
        st.rerun()
        
    for msg in chat_storage.messages:
        with st.chat_message(msg["name"], avatar=msg["avatar"]):
            st.write(f"**{msg['name']}** ({get_rank(msg['name'])})" if msg["name"] != "Система" else f"**{msg['name']}**")
            st.write(msg["text"])

    st.markdown("---")

    # --- ОТПРАВКА СООБЩЕНИЯ ---
    if current_user in chat_storage.muted_users:
        st.error("🔇 Ты замучен администрацией!")
    else:
        if message := st.chat_input("Напишите сообщение..."):
            user_avatar = "👑" if current_user == "kain" else "🎒"
            chat_storage.messages.append({"name": current_user, "text": message, "avatar": user_avatar})
            with open(CHAT_FILE, "a", encoding="utf-8") as f:
                f.write(f"{current_user}|{message}|{user_avatar}\n")
            st.rerun()

else:
    st.error("<code>❌ Доступ заблокирован! Зайдите по секретной ссылке.</code>", icon="🔒")
