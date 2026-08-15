import streamlit as st
import json
import urllib.request
import random

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="WARP Генератор 6 'Б'", page_icon="⚡", layout="centered")
st.title("⚡ Генератор вечных конфигов AmneziaWG")
st.write("Создавай неограниченное количество рабочих туннелей Cloudflare WARP для обхода блокировок в один клик!")

# База фальшивых браузеров для обхода защиты Cloudflare
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
]

# Ползунок выбора количества файлов за раз
count = st.slider("Сколько конфигов сгенерировать за раз?", min_value=1, max_value=5, value=1)

if st.button("🚀 ЗАПУСТИТЬ ГЕНЕРАЦИЮ"):
    progress_bar = st.progress(0)
    
    for i in range(count):
        st.markdown(f"### 📄 Конфигурация №{i+1}")
        
        st_data = {"key": "", "install_id": "", "fcm_token": ""}
        url = "https://cloudflareclient.com"
        
        try:
            req = urllib.request.Request(url, data=json.dumps(st_data).encode())
            req.add_header("Content-Type", "application/json; charset=utf-8")
            req.add_header("User-Agent", random.choice(USER_AGENTS))
            
            res = json.loads(urllib.request.urlopen(req).read().decode())
            private_key = res['config']['interface']['private_key']
            public_key = res['config']['peers']['public_key']
            
            # Собираем правильный текст файла с защитой от блокировок провайдеров
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
            
            # Выводим красивое текстовое окно с кодом
            st.code(config_text, language="ini")
            
            # Кнопка для моментального скачивания файла прямо на ПК/Телефон!
            st.download_button(
                label=f"📥 Скачать файл warp_{i+1}.conf",
                data=config_text,
                file_name=f"warp_{i+1}.conf",
                mime="text/plain",
                key=f"btn_{i}_{random.randint(1,9999)}"
            )
            
        except Exception as e:
            st.error(f"Не удалось достучаться до Cloudflare: {e}")
            
        progress_bar.progress((i + 1) / count)
        
    st.success("✨ Все конфигурации успешно созданы!")
