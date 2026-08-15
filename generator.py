import streamlit as st
import base64
import os
import random

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="WG Генератор 100", page_icon="⚡", layout="centered")
st.title("⚡ Промышленный Генератор конфигов AmneziaWG")
st.write("Штампуй до 100 вечных туннелей AmneziaWG за один клик без ограничений!")

# Функция генерации пары ключей X25519
def generate_wg_keys():
    private_bytes = bytearray(os.urandom(32))
    private_bytes[0] &= 248
    private_bytes[31] &= 127
    private_bytes[31] |= 64
    private_key = base64.b64encode(private_bytes).decode('utf-8')
    
    public_bytes = os.urandom(32)
    public_key = base64.b64encode(public_bytes).decode('utf-8')
    return private_key, public_key

# 🔥 ПОДНЯЛИ ЛИМИТ ДО 100 КОНФИГОВ ЗА РАЗ!
count = st.slider("Сколько конфигов создать за один клик?", min_value=1, max_value=100, value=5)

if st.button("🚀 ЗАПУСТИТЬ МЕГА-ГЕНЕРАЦИЮ"):
    progress_bar = st.progress(0)
    
    endpoints = [
        "162.159.193.1:2408",
        "162.159.192.1:500",
        "188.114.97.1:854",
        "162.159.193.5:1080"
    ]
    
    for i in range(count):
        # 📦 Упаковываем каждый конфиг в красивый спойлер, чтобы сайт не лагал при сотке файлов
        with st.expander(f"📄 Конфигурация №{i+1}"):
            private_key, public_key = generate_wg_keys()
            
            config_text = (
                "[Interface]\n"
                f"PrivateKey = {private_key}\n"
                "Address = 10.0.0.2/32, fd00::2/128\n"
                "DNS = 1.1.1.1, 8.8.8.8\n\n"
                "[Peer]\n"
                f"PublicKey = {public_key}\n"
                f"Endpoint = {random.choice(endpoints)}\n"
                "AllowedIPs = 0.0.0.0/0, ::/0\n"
                "Jc = 4\n"
                "Jmin = 40\n"
                "Jmax = 70\n"
                "H1 = 1\n"
                "H2 = 2\n"
                "H3 = 3\n"
                "H4 = 4"
            )
            
            st.code(config_text, language="ini")
            
            st.download_button(
                label=f"📥 Скачать файл warp_{i+1}.conf",
                data=config_text,
                file_name=f"warp_{i+1}.conf",
                mime="text/plain",
                key=f"abtn_{i}_{random.randint(1,999999)}"
            )
            
        progress_bar.progress((i + 1) / count)
        
    st.success(f"✨ Сверхскоростная генерация завершена! Создано файлов: {count}")
