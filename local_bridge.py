import os
import sys
import time
import subprocess
import urllib.request
import json
import winreg
import atexit

UPSTREAM_HOST = "render-proxy-ip.onrender.com"
UPSTREAM_PORT = 443
UPSTREAM_USER = "ksmart"
UPSTREAM_PASS = "98427189427194817294817294817294"
LOCAL_PORT = 10808

BIN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
GOST_EXE = os.path.join(BIN_DIR, "gost.exe")

gost_proc = None

def set_windows_proxy(enable: bool):
    """Bật hoặc tắt Proxy trên hệ thống Windows."""
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) as key:
            if enable:
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, f"127.0.0.1:{LOCAL_PORT}")
                try:
                    import ctypes
                    ctypes.windll.Wininet.InternetSetOptionW(0, 39, 0, 0)
                    ctypes.windll.Wininet.InternetSetOptionW(0, 37, 0, 0)
                except:
                    pass
                print(f"[OK] Da BAT Proxy he thong Windows: 127.0.0.1:{LOCAL_PORT}")
            else:
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
                try:
                    import ctypes
                    ctypes.windll.Wininet.InternetSetOptionW(0, 39, 0, 0)
                    ctypes.windll.Wininet.InternetSetOptionW(0, 37, 0, 0)
                except:
                    pass
                print("[OK] Da TAT Proxy he thong Windows (Da khoi phuc ve mang goc)")
    except Exception as e:
        print(f"[LOI] Khong the thay doi Registry Windows: {e}")

def kill_existing_gost():
    try:
        subprocess.run(["taskkill", "/F", "/IM", "gost.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

def check_ip():
    """Kiem tra IP va vi tri hien tai."""
    print("------------------------------------------------------------")
    print(">> Dang kiem tra IP...")
    try:
        req = urllib.request.Request("https://api.ipify.org?format=json", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            ip = data.get("ip")
            print(f"[*] IP HIEN TAI : {ip}")
            try:
                geo_req = urllib.request.Request(f"http://ip-api.com/json/{ip}", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(geo_req, timeout=10) as geo_res:
                    geo = json.loads(geo_res.read().decode())
                    print(f"[*] VI TRI     : {geo.get('city')}, {geo.get('country')} (ISP: {geo.get('isp')})")
            except:
                pass
    except Exception as e:
        print(f"[!] Chua lay duoc IP: {e}")
    print("------------------------------------------------------------")

def cleanup():
    set_windows_proxy(False)
    kill_existing_gost()

atexit.register(cleanup)

def start_proxy():
    global gost_proc
    if not os.path.exists(GOST_EXE):
        print(f"[LOI] Khong tim thay {GOST_EXE}!")
        return

    kill_existing_gost()

    upstream_url = f"wss://{UPSTREAM_USER}:{UPSTREAM_PASS}@{UPSTREAM_HOST}:{UPSTREAM_PORT}"
    cmd = [
        GOST_EXE,
        "-L", f":{LOCAL_PORT}",
        "-F", upstream_url
    ]

    print("[*] Dang ket noi toi Render Proxy qua WebSocket TLS (Singapore)...")
    gost_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    time.sleep(2)
    set_windows_proxy(True)
    time.sleep(1)
    check_ip()

    print("\n============================================================")
    print(">> [DANG HOAT DONG] TOAN BO MAY TINH DA DOI SANG IP SINGAPORE!")
    print(">> Trinh duyet (Chrome, Edge, Coc Coc) va moi ung dung deu di qua IP nay.")
    print(">> Nhap Ctrl+C tren cua so nay de TAT va ve lai mang goc.")
    print("============================================================")

    try:
        while True:
            time.sleep(1)
            if gost_proc.poll() is not None:
                print("\n[!] Tien trinh Gost bi ngat.")
                break
    except KeyboardInterrupt:
        print("\n[*] Dang tat cau noi...")
    finally:
        cleanup()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "off":
        cleanup()
        check_ip()
    elif len(sys.argv) > 1 and sys.argv[1] == "check":
        check_ip()
    else:
        start_proxy()
