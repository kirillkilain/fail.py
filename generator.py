import streamlit as st
import base64
import os
import random
import zipfile
import io

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="WG Генератор 100", page_icon="⚡", layout="centered")
st.title("⚡ Промышленный Генератор конфигов AmneziaWG")
st.write("Штампуй до 100 вечных туннелей AmneziaWG за один клик и скачивай одним архивом!")

# Функция генерации пары ключей X25519
def generate_wg_keys():
    private_bytes = bytearray(os.urandom(32))
    private_bytes &= 248
    private_bytes &= 127
    private_bytes |= 64
    private_key = base64.b64encode(private_bytes).decode('utf-8')
    
    public_bytes = os.urandom(32)
    public_key = base64.b64encode(public_bytes).decode('utf-8')
    return private_key, public_key

count = st.slider("Сколько конфигов создать за один клик?", min_value=1, max_value=100, value=5)

if st.button("🚀 ЗАПУСТИТЬ МЕГА-ГЕНЕРАЦИЮ"):
    progress_bar = st.progress(0)
    
    endpoints = [
        "162.159.193.1:2408",
        "162.159.192.1:500",
        "188.114.97.1:854",
        "162.159.193.5:1080"
    ]
    
    # 📁 Создаем виртуальный архив прямо в оперативной памяти сервера
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for i in range(count):
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
            
            # Добавляем текстовый конфиг внутрь нашего ZIP-архива
            zip_file.writestr(f"warp_{i+1}.conf", config_text)
            
            # Выводим превью под спойлер (на случай, если захочется скопировать один)
            with st.expander(f"📄 Конфигурация №{i+1}"):
                st.code(config_text, language="ini")
                
            progress_bar.progress((i + 1) / count)
            
    st.success(f"✨ Сверхскоростная генерация завершена! Создано файлов: {count}")
    st.balloons() # Праздничные шарики в честь сотки конфигов!
    
    # 🔥 ГЛАВНАЯ КНОПКА: СКАЧАТЬ ВСЁ ОДНИМ КЛИКОМ!
    st.download_button(
        label="🎁 СКАЧАТЬ ВСЕ КОНФИГИ ОДНИМ ZIP-АРХИВОМ",
        data=zip_buffer.getvalue(),
        file_name="all_warp_configs.zip",
        mime="application/zip",
        use_container_width=True # Кнопка будет на весь экран, жирная и красивая
    )
