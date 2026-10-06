import subprocess
import time
import urllib.request
import json
import re

gost_exe = r"D:\Test_script\render_proxy_service\bin\gost.exe"
cmd = [gost_exe, "-L", ":10808", "-F", "wss://ksmart:98427189427194817294817294817294@render-proxy-ip.onrender.com:443"]

print("[1] Dang khoi dong cau noi qua Render Singapore Proxy...")
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
time.sleep(3)

try:
    proxy_handler = urllib.request.ProxyHandler({"http": "http://127.0.0.1:10808", "https": "http://127.0.0.1:10808"})
    opener = urllib.request.build_opener(proxy_handler)
    
    # 1. Kiem tra IP qua proxy
    req_ip = urllib.request.Request("https://api.ipify.org?format=json", headers={"User-Agent": "Mozilla/5.0"})
    with opener.open(req_ip, timeout=10) as resp:
        ip = json.loads(resp.read().decode()).get("ip")
        print(f"[2] IP xac thuc qua Proxy: {ip} (Singapore Datacenter)")

    # 2. Truy cap truc tiep bai bao GenK qua IP Singapore
    target_link = "https://genk.vn/tin-tac-trung-quoc-gia-mao-nhan-vien-anthropic-de-danh-cap-bi-mat-tri-tue-nhan-tao-165261006115104685.chn"
    print(f"[3] Dang gui HTTP Request qua IP Singapore den: {target_link}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(target_link, headers=headers)
    with opener.open(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")

    title_m = re.search(r'<title>(.*?)</title>', html)
    title = title_m.group(1).split('|')[0].strip() if title_m else "N/A"

    meta_sapo = re.search(r'<meta property="og:description" content="([^"]+)"', html)
    if not meta_sapo:
        meta_sapo = re.search(r'<meta name="description" content="([^"]+)"', html)
    sapo = meta_sapo.group(1) if meta_sapo else "N/A"

    print("\n" + "="*70)
    print("🎯 DỮ LIỆU BÀI VIẾT LẤY THÀNH CÔNG TỪ GENK.VN QUA IP RENDER SINGAPORE:")
    print("="*70)
    print(f"📰 TIÊU ĐỀ : {title}")
    print(f"🔗 NGUỒN   : {target_link}")
    print(f"📝 TÓM TẮT : {sapo}")
    print("="*70)

except Exception as e:
    print("[LOI]:", e)
finally:
    proc.terminate()
