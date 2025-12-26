import sys
import os

# Добавляем родительскую директорию в sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Updated Python path:")
for p in sys.path:
    print(p)

try:
    import app
    print("\nSuccessfully imported app")
    print(f"app location: {app.__file__}")
except ImportError as e:
    print(f"\nImportError: {e}")

try:
    from app import main
    print("\nSuccessfully imported main from app")
    print(f"main location: {main.__file__}")
except ImportError as e:
    print(f"\nImportError when importing main: {e}")