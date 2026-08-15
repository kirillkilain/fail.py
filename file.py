import streamlit as st
from datetime import datetime, date
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
ANN_FILE = os.path.join(BASE_DIR, "announcement.txt")

if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        f.write("Система|Добро пожаловать в игру-мессенджер! Крутите казик или ждите званий от kain! 🎰|🤖\n")

# ОБЩАЯ ПАМЯТЬ СЕРВЕРА
@st.cache_resource
class SharedChat:
    def __init__(self):
        self.fake_user = ""
        self.online_users = {}
        self.user_statuses = {}
        
        # Списки выданных прав и ограничений
        self.moderators = []  # Кто может мутить (Ранг: Модератор)
        self.admins = []      # Кто может банить (Ранг: Админ)
        self.muted_users = [] # Кто сейчас в муте
        
        # История прокруток казино (имя: объект date последнего кручения)
        self.casino_history = {}
        
        # 🔑 ТАБЛИЦА ТОКЕНОВ И ИМЕН
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

# Функция для определения текущего звания
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
    
    # Режим маскировки для пранков
    if real_user == "kain" and chat_storage.fake_user != "":
        current_user = chat_storage.fake_user
    else:
        current_user = real_user
        
    st.sidebar.success(f"Вы вошли как: {current_user} 😎")
    
    # ОБНОВЛЯЕМ СТАТУС ОНЛАЙН
    now_local = datetime.now(LOCAL_TZ)
    chat_storage.online_users[real_user] = now_local

    # --- ⚙️ ПРОФИЛЬ И СТАТУС ---
    st.sidebar.markdown("### ⚙️ Твой профиль")
    st.sidebar.write(f"🎖️ Звание: **{get_rank(current_user)}**")
    if current_user in chat_storage.muted_users:
        st.sidebar.error("🔇 ВНИМАНИЕ: Ты в муте!")
    
    current_status = chat_storage.user_statuses.get(current_user, "")
    new_status = st.sidebar.text_input("Изменить свой статус:", value=current_status, max_chars=30)
    if new_status != current_status:
        chat_storage.user_statuses[current_user] = new_status
        st.rerun()

    # --- 🎰 КАЗИК С ОГРАНИЧЕНИЕМ РАЗ В ДЕНЬ ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎰 Казик на Админки")
    
    today_date = datetime.now(LOCAL_TZ).date()
    last_spin_date = chat_storage.casino_history.get(current_user, None)
    
    # Проверяем, крутил ли юзер сегодня (для kain всегда доступно)
    if last_spin_date == today_date and current_user != "kain":
        st.sidebar.warning("⏳ Вы уже крутили казик сегодня! Возвращайтесь завтра.")
    else:
        if st.sidebar.button("🎰 Крутить слоты!"):
            # Записываем дату прокрутки
            chat_storage.casino_history[current_user] = today_date
            
            slots = ["🍒", "🍋", "💎", "7️⃣", "🍉"]
            res1 = random.choice(slots)
            res2 = random.choice(slots)
            res3 = random.choice(slots)
            
            st.sidebar.subheader(f"🎰 [ {res1} | {res2} | {res3} ]")
            
            if res1 == res2 == res3:
                st.balloons()
                if res1 == "7️⃣":
                    st.sidebar.success("🏆 ДЖЕКПОТ! Ты выиграл силу АДМИНА!")
                    if current_user not in chat_storage.admins:
                        chat_storage.admins.append(current_user)
                    with open(CHAT_FILE, "a", encoding="utf-8") as f:
                        f.write(f"Система|🎉 {current_user} ВЫБИЛ 777 И ПОЛУЧИЛ СИЛУ АДМИНА В КАЗИНО! 🎉|🤖\n")
                    st.rerun()
                elif res1 == "🍋":
                    st.sidebar.success("⚡ ДЖЕКПОТ! Ты стал Модератором!")
                    if current_user not in chat_storage.moderators:
                        chat_storage.moderators.append(current_user)
                    with open(CHAT_FILE, "a", encoding="utf-8") as f:
                        f.write(f"Система|⚡ {current_user} ВЫБИЛ ЛИМОНЫ И СТАЛ МОДЕРАТОРОМ В КАЗИНО! ⚡|🤖\n")
                    st.rerun()
                else:
                    st.sidebar.success("🎉 Обычный джекпот! Просто повезло.")
            else:
                st.sidebar.error("😢 Мимо! Следующая попытка завтра.")

    # --- 🔨 ПАНЕЛЬ УПРАВЛЕНИЯ ДЛЯ ДРУГИХ АДМИНОВ / МОДЕРОВ ---
    is_moderator = current_user in chat_storage.moderators
    is_admin = current_user in chat_storage.admins
    active_names = [n for n in chat_storage.tokens_db.values() if n != "kain"]
    
    if is_moderator or is_admin:
        st.sidebar.markdown("---")
        st.sidebar.subheader("🛠️ Выигранные Права")
        
        if is_moderator:
            mute_target = st.sidebar.selectbox("Кого замутить/размутить (Модератор):", [""] + active_names, key="mod_m")
            if mute_target:
                if st.sidebar.button("🔇 Мут", key="mod_m_btn"):
                    if mute_target not in chat_storage.muted_users:
                        chat_storage.muted_users.append(mute_target)
                        st.rerun()
                        
        if is_admin:
            ban_target = st.sidebar.selectbox("Кого забанить (Админ):", [""] + active_names, key="adm_b")
            if ban_target and st.sidebar.button("🔨 Забанить", key="adm_b_btn"):
                if ban_target != "kain":
                    token_to_del = [k for k, v in chat_storage.tokens_db.items() if v == ban_target]
                    if token_to_del:
                        del chat_storage.tokens_db[token_to_del[0]]
                        st.rerun()

    # --- 👑 ЭКСКЛЮЗИВНЫЙ ПУЛЬТ УПРАВЛЕНИЯ РАНГАМИ ТОЛЬКО ДЛЯ НАСТОЯЩЕГО KAIN ---
    if real_user == "kain":
        st.sidebar.markdown("---")
        st.sidebar.subheader("👑 ГЛАВНЫЙ ПУЛЬТ СОЗДАТЕЛЯ")
        
        # 👑 Фича ручной выдачи и отбора рангов
        st.sidebar.markdown("**⭐ Выдача и отбор званий:**")
        target_user = st.sidebar.selectbox("Выберите ученика:", [""] + active_names)
        new_rank = st.sidebar.selectbox("Назначить ранг:", ["Обычный Чебурек", "Модератор (Мут)", "Временный Админ (Бан)"])
        
        if target_user and st.sidebar.button("⭐ Применить ранг"):
            # Сначала чистим старые временные права
            if target_user in chat_storage.moderators: chat_storage.moderators.remove(target_user)
            if target_user in chat_storage.admins: chat_storage.admins.remove(target_user)
            
            # Выдаем новые
            if new_rank == "Модератор (Мут)":
                chat_storage.moderators.append(target_user)
            elif new_rank == "Временный Админ (Бан)":
                chat_storage.admins.append(target_user)
                
            st.sidebar.success(f"Успешно изменен ранг {target_user} на {new_rank}!")
            st.rerun()
            
        st.sidebar.markdown("---")
        
        # Режим маскировки
        target_prank = st.sidebar.selectbox("Маскировка под:", active_names)
        if st.sidebar.button("🕵️‍♂️ Включить маскировку"):
            chat_storage.fake_user = target_prank
            st.rerun()
        if st.sidebar.button("❌ Сбросить маскировку"):
            chat_storage.fake_user = ""
            st.rerun()
            
        # Управление вечным объявлением
        new_announcement = st.sidebar.text_input("Создать вечное объявление:")
        if st.sidebar.button("📢 Опубликовать"):
            with open(ANN_FILE, "w", encoding="utf-8") as f: f.write(new_announcement)
            st.rerun()
            
        # Полная очистка
        if st.sidebar.button("🧹 СБРОСИТЬ ВСЕХ И ЧАТ"):
            chat_storage.moderators = []
            chat_storage.admins = []
            chat_storage.muted_users = []
            chat_storage.casino_history = {}
            with open(CHAT_FILE, "w", encoding="utf-8") as f:
                f.write("Система|Чат и все ранги полностью сброшены Создателем kain! 🧼|🤖\n")
            st.rerun()

    # --- 🟢 БЛОК ОНЛАЙНА ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("👥 Кто в сети:")
    for token_key, username in chat_storage.tokens_db.items():
        status_text = chat_storage.user_statuses.get(username, "")
        status_display = f" | *«{status_text}»*" if status_text else ""
        
        if username in chat_storage.online_users:
            last_seen = chat_storage.online_users[username]
            seconds_passed = (datetime.now(LOCAL_TZ) - last_seen).total_seconds()
            if seconds_passed < 10:
                st.sidebar.write(f"🟢 **{username}** ({get_rank(username)}){status_display}")
            else:
                st.sidebar.write(f"⚪ *{username}* (был недавно) ({get_rank(username)})")
        else:
            st.sidebar.write(f"⚪ *{username}* (оффлайн) ({get_rank(username)})")

    # --- 🔄 АВТО-ОБНОВЛЕНИЕ ЧАТА ---
    @st.fragment(run_every="3s")
    def show_chat():
        if os.path.exists(ANN_FILE):
            with open(ANN_FILE, "r", encoding="utf-8") as f: saved_ann = f.read().strip()
