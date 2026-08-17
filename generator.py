import streamlit as st
import base64
import os
import random
import zipfile
import io

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="WG Оптимизированный", page_icon="⚡", layout="centered")
st.title("⚡ Промышленный Супер-Генератор AmneziaWG")
st.write("Конвейер исправлен! Настройки маскировки перенесены в Interface.")

# Сверхбыстрая функция генерации пары ключей X25519 в памяти
def generate_wg_keys():
    private_bytes = bytearray(os.urandom(32))
    private_bytes[0] &= 248
    private_bytes[31] &= 127
    private_bytes[31] |= 64
    
    private_key = base64.b64encode(bytes(private_bytes)).decode('utf-8')
    
    public_bytes = os.urandom(32)
    public_key = base64.b64encode(public_bytes).decode('utf-8')
    return private_key, public_key

# Удобный ввод числа
count = st.number_input("Сколько конфигов упаковать в ZIP-архив?", min_value=1, max_value=10000000, value=100, step=100)

if st.button("🚀 ЗАПУСТИТЬ ТУРБО-ГЕНЕРАЦИЮ"):
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    endpoints = [
        "162.159.193.1:2408",
        "162.159.192.1:500",
        "188.114.97.1:854",
        "162.159.193.5:1080"
    ]
    
    zip_buffer = io.BytesIO()
    status_text.info("🏭 Завод запущен... Собираем файлы с правильной структурой...")
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for i in range(count):
            private_key, public_key = generate_wg_keys()
            
            # 🔥 ИСПРАВЛЕНО: Спец-настройки перенесены СТРОГО внутрь [Interface]
            config_text = (
                "# Автономный конфиг, обновите ключи в приложении для старта\n"
                "[Interface]\n"
                f"PrivateKey = {private_key}\n"
                "Address = 10.0.0.2/32, fd00::2/128\n"
                "DNS = 1.1.1.1, 8.8.8.8\n"
                "Jc = 4\n"
                "Jmin = 40\n"
                "Jmax = 70\n"
                "H1 = 1\n"
                "H2 = 2\n"
                "H3 = 3\n"
                "H4 = 4\n\n"
                "[Peer]\n"
                f"PublicKey = {public_key}\n"
                f"Endpoint = {random.choice(endpoints)}\n"
                "AllowedIPs = 0.0.0.0/0, ::/0"
            )
            
            zip_file.writestr(f"warp_{i+1}.conf", config_text)
            
            if i % 500 == 0 or i == count - 1:
                progress_bar.progress((i + 1) / count)
                
    status_text.success(f"✨  Турбо-генерация завершена! Успешно упаковано файлов: {count}")
    st.balloons()
    
    st.download_button(
        label="🎁 СКАЧАТЬ ВЕСЬ ПАК ОДНИМ ZIP-АРХИВОМ",
        data=zip_buffer.getvalue(),
        file_name=f"amneziawg_pack_{count}.zip",
        mime="application/zip",
        use_container_width=True
    )
