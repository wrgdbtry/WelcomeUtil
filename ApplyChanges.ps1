# Проверка прав администратора
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$($PSScriptRoot)\$($MyInvocation.MyCommand.Name)`"" -Verb RunAs
    exit
}

# Установка текущей директории
Set-Location -Path $PSScriptRoot

# Функция проверки PyInstaller
function Check-PyInstaller {
    $venv_path = ".venv"
    
    # Если есть виртуальное окружение
    if (Test-Path $venv_path) {
        Write-Host "Обнаружено виртуальное окружение (.venv)" -ForegroundColor Cyan
        
        # Активация .venv
        try {
            & .\.venv\Scripts\Activate.ps1
            Write-Host "Виртуальное окружение активировано" -ForegroundColor Green
            
            # Проверка PyInstaller в .venv
            $has_pyinstaller = python -m pip list | Select-String "pyinstaller"
            
            if (-not $has_pyinstaller) {
                Write-Host "Установка PyInstaller в виртуальное окружение..." -ForegroundColor Yellow
                python -m pip install pyinstaller
            }
        }
        catch {
            Write-Host "Ошибка активации .venv: $_" -ForegroundColor Red
            exit 1
        }
    }
    else {
        # Проверка глобального PyInstaller
        $has_pyinstaller = python -m pip list | Select-String "pyinstaller"
        
        if (-not $has_pyinstaller) {
            Write-Host "Установка PyInstaller глобально..." -ForegroundColor Yellow
            python -m pip install pyinstaller
        }
    }
}

# Выполняем проверки
Check-PyInstaller

# Сборка проекта
Write-Host "Запуск сборки..." -ForegroundColor Cyan
python -m PyInstaller `
  --onefile `
  --noconsole `
  --icon "notepad.ico" `
  --add-data "config.yaml;." `
  --add-data "settings.py;." `
  --add-data "notepad.ico;." `
  "main no windows.py"

# Пауза для просмотра результатов
pause
