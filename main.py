import os
import winreg
import subprocess
import sys
from pathlib import Path
from tkinter import messagebox, ttk
import customtkinter as ctk
from tkinter import *

try:
    import customtkinter as ctk
except:
    print("please do ""pip install customtkinter""", file=sys.stderr)
    while True:
        pass

try:
    import yaml
except:
    print("please do ""pip install pyyaml""", file=sys.stderr)
    while True:
        pass

script_directory = os.path.dirname(os.path.abspath(__file__))


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


def configure_styles():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    style = ttk.Style()
    root.attributes("-alpha", 0.96)
    style.theme_use("clam")

    # Настройка цветов
    style.configure("TFrame", background="#2E2E2E")
    style.configure("TLabel", background="#2E2E2E", foreground="white", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 10), padding=6)
    style.map("TButton",
              background=[("active", "#4A4A4A"), ("pressed", "#6A6A6A")],
              foreground=[("active", "white")]
              )


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

        global browser
        try:
            browser = find_exe_in_registry(config["paths"]["browser_reg_name"])
            subprocess.Popen(browser)
        except:
            messagebox.showerror("Ошибка", f"Не удалось найти браузер!\n")


root = Tk()
root.title(config["app"]["title"])
root.geometry(f"{config['app']['geometry'][0]}x{config['app']['geometry'][1]}")
root.resizable(config["app"]["resizable"], config["app"]["resizable"])
root.attributes("-alpha", config["app"]["opacity"])
root.configure(bg=config["app"]["background"])

configure_styles()

main_frame = ttk.Frame(root)
main_frame.pack(fill=BOTH, expand=False, padx=20, pady=20)

header_frame = ttk.Frame(main_frame)
header_frame.pack(fill=X, pady=10)

label1 = ttk.Label(header_frame,
                   text=f"Добро пожаловать, {os.getlogin()}!",
                   font=("Helvetica", 14, "bold"),
                   anchor="center")
label1.pack(fill=X)

button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10, fill=X)

btn_style = ttk.Style()

btn_style.configure("Custom.TButton",
                    font=config["button_style"]["font"],
                    padding=config["button_style"]["padding"],
                    background=config["button_style"]["background"],
                    foreground=config["button_style"]["foreground"])

btn2 = ctk.CTkButton(
    master=button_frame,
    text="Запустить запретфикс",
    corner_radius=config["button_style"]["corner_radius"],
    command=openZapretFix
)
btn2.pack(fill=X, pady=5)

btn3 = ctk.CTkButton(
    master=button_frame,
    text="Запустить браузер",
    corner_radius=config["button_style"]["corner_radius"],
    command=openBrowser
)
btn3.pack(fill=X, pady=5)

btn_exit = ctk.CTkButton(
    master=button_frame,
    text="Выход",
    corner_radius=config["button_style"]["corner_radius"],
    command=root.destroy
)
btn_exit.pack(fill=X, pady=5)

status_bar = ttk.Frame(root, height=20)
status_bar.pack(fill=X, side=BOTTOM)
ttk.Label(status_bar,
          text="",
          anchor=W,
          style="TLabel").pack(side=LEFT, padx=5)

try:
    root.iconbitmap(os.path.join(script_directory, "notepad.ico"))
except:
    pass

root.mainloop()
