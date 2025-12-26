import subprocess
import sys
import os

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} installed successfully")
        # После установки добавляем путь к site-packages в sys.path
        site_packages = os.path.join(os.path.dirname(sys.executable), 'lib', 'site-packages')
        if site_packages not in sys.path:
            sys.path.insert(0, site_packages)
        globals()[package] = __import__(package)

# Проверяем и устанавливаем необходимые пакеты
required_packages = ['fastapi', 'uvicorn', 'pyyaml', 'minio', 'chromadb', 'pymupdf']

for package in required_packages:
    install_and_import(package)
    print(f"✓ {package} is available")

print("\nAll required packages are available!")