import requests
import sys

# Cấu hình thông tin Proxy Render của bạn
PROXY_HOST = "render-proxy-ip-xxxx.onrender.com"  # Thay bằng URL Render thực tế của bạn
PROXY_PORT = 443  # Cổng HTTPS mặc định của Render
PROXY_USER = "ksmart"
PROXY_PASS = "RenderProxy2026!"

def test_proxy():
    # Render tự động cung cấp SSL qua port 443 (HTTPS)
    proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }

    print(f"📡 Đang kiểm tra kết nối qua Proxy: {PROXY_HOST}...")
    try:
        # Lấy IP gốc trước
        my_ip = requests.get("https://api.ipify.org?format=json", timeout=10).json()["ip"]
        print(f"🏠 IP gốc hiện tại của máy bạn: {my_ip}")

        # Lấy IP qua Proxy Render
        res = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=15)
        proxy_ip = res.json()["ip"]
        print(f"🚀 IP Mới qua Render Proxy: {proxy_ip}")

        # Tra cứu vị trí địa lý của IP Render
        geo = requests.get(f"https://ipapi.co/{proxy_ip}/json/", proxies=proxies, timeout=15).json()
        print(f"🌍 Vị trí IP: {geo.get('city')}, {geo.get('country_name')} ({geo.get('org')})")
        print("✅ Proxy hoạt động hoàn hảo 100%!")
    except Exception as e:
        print(f"❌ Lỗi kết nối proxy: {e}")

if __name__ == "__main__":
    test_proxy()
