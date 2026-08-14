import streamlit as st
import time

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
        self.fake_user = ""
        
        # 🔑 ТАБЛИЦА СЕКРЕТНЫХ КЛЮЧЕЙ И ИМЁН
        # ⚠️ Не забудь переписать сюда свои настоящие 7 имён и ключей, которые ты настроил!
        self.tokens_db = {
            "boss_kain_777": "kain",
            "artem_key_31": "Артем 1",     # Твой токен №2
            "zera_pass_99": "Зарина",      # Твой токен №3
            "art_token_55": "Артем 2",     # Твой токен №4 (Второй Артем!)
            "6354_secret_12": "Эмилия",    # Твой токен №5
            "lenaid_83463": "Лена",        # Твой токен №6
            "markovka6583": "Марк"         # Твой токен №7
        }

chat_storage = SharedChat()

# ЧИТАЕМ СЕКРЕТНЫЙ КЛЮЧ ИЗ ССЫЛКИ
query_params = st.query_params
user_token = query_params.get("token", None)

if user_token in chat_storage.tokens_db:
    real_user = chat_storage.tokens_db[user_token]
    
    # Режим маскировки
    if real_user == "kain" and chat_storage.fake_user != "":
        current_user = chat_storage.fake_user
    else:
        current_user = real_user
        
    st.sidebar.success(f"Вход выполнен! Вы вошли как: {current_user} 😎")
    
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

    # 🔄 МАГИЯ АВТО-ОБНОВЛЕНИЯ (Блок st.fragment обновляется сам по таймеру)
    @st.fragment(run_every="3s")
    def show_chat():
        if chat_storage.announcement:
            st.warning(f"📢 **ВАЖНОЕ ОБЪЯВЛЕНИЕ:** {chat_storage.announcement}")
            
        st.subheader("📋 История сообщений")
        
        # Вывод сообщений из памяти сервера
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
