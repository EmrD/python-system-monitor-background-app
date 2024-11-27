from pystray import Icon, MenuItem, Menu  # type:ignore
from PIL import Image, ImageDraw
import threading
import psutil  # type:ignore
from win10toast import ToastNotifier  # type:ignore
import time

islemci_kullanim = "0"
ram_kullanim = "0"
toast = ToastNotifier()
lock = threading.Lock() 

def control_system():
    global islemci_kullanim, ram_kullanim
    while True:
        with lock: 
            islemci = float(islemci_kullanim)
            ram = float(ram_kullanim)
        if islemci > 75 or ram > 80:
            toast.show_toast(
                "Sisteminiz Zorlanıyor Gibi Görünüyor",
                f"İşlemci Kullanımı: {islemci_kullanim}%\nRAM Kullanımı: {ram_kullanim}%\nKullanmadığınız uygulamaları kapatın.",
                duration=5,
            )
        time.sleep(5)

def background_task(icon):
    global islemci_kullanim, ram_kullanim
    while True:
        with lock:
            islemci_kullanim = str(psutil.cpu_percent(interval=1))
            ram_kullanim = str(psutil.virtual_memory().percent)

        icon.menu = Menu(
            MenuItem(f"İşlemci Kullanımı: {islemci_kullanim}%", lambda: None, enabled=False),
            MenuItem(f"RAM Kullanımı: {ram_kullanim}%", lambda: None, enabled=False),
            MenuItem("Uygulamayı Kapat", lambda: quit_app(icon))
        )
        icon.update_menu()

def create_image(width, height, color1, color2):
    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill=color2)
    return image

def quit_app(icon):
    icon.stop()

def setup_tray_icon():
    icon = Icon("System Monitor", create_image(64, 64, "blue", "white"), menu=None)

    task_thread = threading.Thread(target=background_task, args=(icon,), daemon=True)
    control_thread = threading.Thread(target=control_system, daemon=True)
    task_thread.start()
    control_thread.start()

    icon.run()

setup_tray_icon()