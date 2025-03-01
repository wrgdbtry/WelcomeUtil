import os
import winreg
import subprocess
import sys
import yaml
from pathlib import Path
from tkinter import messagebox
import customtkinter as ctk
from tkinter import ttk


# Загрузка конфигурации
def load_config():
    config_path = Path(__file__).parent / "config.yaml"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка загрузки конфига: {e}")
        sys.exit(1)


config = load_config()
script_directory = Path(__file__).parent

# Инициализация приложения
root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# Функции приложения
def openZapretFix():
    bat_path = script_directory / config["paths"]["bat_script"]
    try:
        subprocess.Popen(str(bat_path), shell=True)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить файл:\n{e}")


def find_exe_in_registry(app_name):
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"
        )
        subkey = winreg.OpenKey(key, f"{app_name}.exe")
        path, _ = winreg.QueryValueEx(subkey, "")
        winreg.CloseKey(subkey)
        return path
    except Exception as e:
        print(f"Ошибка: {e}")
        return None


def openBrowser():
    browser_name = config["paths"]["browser_reg_name"]
    if browser_path := find_exe_in_registry(browser_name):
        subprocess.Popen(browser_path)
    else:
        messagebox.showerror("Ошибка", "Браузер не найден в системе!")


# Конфигурация окна
root.title(config["app"]["title"])
root.geometry(f"{config['app']['geometry'][0]}x{config['app']['geometry'][1]}")
root.resizable(config["app"]["resizable"], config["app"]["resizable"])
root.attributes("-alpha", config["app"]["opacity"])
root.configure(fg_color=config["app"]["background"])

try:
    root.iconbitmap(str(script_directory / config["app"]["icon"]))
except Exception as e:
    print(f"Ошибка загрузки иконки: {e}")

# GUI элементы
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Заголовок
header = ctk.CTkLabel(
    main_frame,
    text=f"Добро пожаловать, {os.getlogin()}!",
    font=("Helvetica", 14, "bold")
)
header.pack(pady=10)

# Кнопки
button_frame = ctk.CTkFrame(main_frame)
button_frame.pack(pady=10, fill="x")

command_mapping = {
    "openZapretFix": openZapretFix,
    "root.destroy": root.destroy
}

for btn_cfg in config["buttons"]:
    btn = ctk.CTkButton(
        master=button_frame,
        text=btn_cfg["text"],
        command=command_mapping[btn_cfg["command"]],
        corner_radius=btn_cfg["corner_radius"],
        fg_color=btn_cfg["fg_color"],
        hover_color=btn_cfg.get("hover_color", None)
    )
    btn.pack(fill="x", pady=5)

# Статус бар
status_bar = ctk.CTkFrame(root, height=20)
status_bar.pack(fill="x", side="bottom")
status_label = ctk.CTkLabel(status_bar, text="Готово к работе", anchor="w")
status_label.pack(side="left", padx=5)

# Запуск
root.mainloop()
