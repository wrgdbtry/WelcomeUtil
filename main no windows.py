import os, webbrowser
import sys, random
from pathlib import Path
from tkinter import messagebox, ttk
from tkinter import *

try:
    import customtkinter as ctk
except:
    print("please do ""pip install customtkinter""", file=sys.stderr)
    while True:
        pass

try:
    import pyperclip
except:
    print("please do ""pip install pyperclip""", file=sys.stderr)
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

def fade_out():
    current_alpha = root.attributes("-alpha")
    if current_alpha > 0:
        new_alpha = max(current_alpha - 0.02, 0.0)
        root.attributes("-alpha", new_alpha)
        root.after(15, fade_out)
    else:
        root.destroy()

def passwdGenerator():
    letters = config["passwd"]["letters"]
    digits = config["passwd"]["digits"]
    symbols = config["passwd"]["symbols"]
    password = ""

    for i in range(0, random.randint(12, 24)):
        rand = random.randint(0, 2)
        if rand == 0:
            password += letters[random.randrange(len(letters))]
        if rand == 1:
            password += digits[random.randrange(len(digits))]
        if rand == 2:
            password += symbols[random.randrange(len(symbols))]

    pyperclip.copy(password)
    messagebox.showinfo(title="Пароль успешно сгенерирован!",
                        message=f"Ваш пароль: {password}, он скопирован в буфер обмена.")
    return password


def openShortcut1():
    if chkShortcut(1):
        webbrowser.open(config["shortcuts"][f'shortcut1'])


def openShortcut2():
    if chkShortcut(2):
        webbrowser.open(config["shortcuts"][f'shortcut2'])


def openShortcut3():
    if chkShortcut(3):
        webbrowser.open(config["shortcuts"][f'shortcut3'])


def chkShortcut(i):
    if config["shortcuts"][f'shortcut{i}'] is not None:
        return True
    else:
        return False


config = load_config()

script_directory = Path(__file__).parent


def configure_styles():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    style = ttk.Style()
    root.attributes("-alpha", 0.96)
    style.theme_use("clam")

    style.configure("TFrame", background="#2E2E2E")
    style.configure("TLabel", background="#2E2E2E", foreground="white", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 10), padding=6)
    style.map("TButton",
              background=[("active", "#4A4A4A"), ("pressed", "#6A6A6A")],
              foreground=[("active", "white")]
              )


def openZapretFix():
    messagebox.showerror(title="ФИКСИК НЕ РОБИТ", message="Ты на маке/линуксе, какие тебе батники?")


def openBrowser():
    selected_browser = webbrowser.get(config["paths"]["browser_reg_page"])
    try:
        selected_browser.open(config["paths"]["browser_main_page"])
    except:
       webbrowser.open(config["paths"]["browser_main_page"])

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

btn3 = ctk.CTkButton(
    master=button_frame,
    text="Запустить браузер",
    corner_radius=config["button_style"]["corner_radius"],
    command=openBrowser
)
btn3.pack(fill=X, pady=5)

btn4 = ctk.CTkButton(
    master=button_frame,
    text="Сгенерировать надежный пароль",
    corner_radius=config["button_style"]["corner_radius"],
    command=passwdGenerator
)
btn4.pack(fill=X, pady=5)

btn5 = ctk.CTkButton(
    master=button_frame,
    text=config["shortcuts"]["shortcut1_name"],
    corner_radius=config["button_style"]["corner_radius"],
    command=openShortcut1
)
if config["shortcuts"]["shortcut1"] != 0:
    btn5.pack(fill=X, pady=5)

btn6 = ctk.CTkButton(
    master=button_frame,
    text=config["shortcuts"]["shortcut3_name"],
    corner_radius=config["button_style"]["corner_radius"],
    command=openShortcut2
)
if config["shortcuts"]["shortcut2"] != 0:
    btn6.pack(fill=X, pady=5)

btn7 = ctk.CTkButton(
    master=button_frame,
    text=config["shortcuts"]["shortcut3_name"],
    corner_radius=config["button_style"]["corner_radius"],
    command=openShortcut3
)
if config["shortcuts"]["shortcut3"] != 0:
    btn7.pack(fill=X, pady=5)

btn_exit = ctk.CTkButton(
    master=button_frame,
    text="Выход",
    corner_radius=config["button_style"]["corner_radius"],
    command=fade_out
)
btn_exit.pack(fill=X, pady=5)

status_bar = ttk.Frame(root, height=20)
status_bar.pack(fill=X, side=BOTTOM)
ttk.Label(status_bar,
          text="Может работать криво",
          anchor=W,
          style="TLabel").pack(side=LEFT, padx=5)

try:
    root.iconbitmap(os.path.join(script_directory, "notepad.ico"))
except:
    pass

root.mainloop()
