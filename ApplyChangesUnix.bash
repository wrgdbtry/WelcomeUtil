python3 -m pip install pyinstaller

python3 -m PyInstaller --onefile --noconsole  --add-data "config.yaml:." --add-data "notepad.ico:." "main no windows.py"
