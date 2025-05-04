from PyQt6.QtGui import QIcon
import os

def get_icon(name: str) -> QIcon:
    """
    İstediğin ikon adını vererek QIcon nesnesi döndürür.
    Örn: get_icon("chef.png")
    """
    path = os.path.join(os.path.dirname(__file__), f"{name}.png")
    if os.path.exists(path):
        return QIcon(path)
    return QIcon()  # Dosya yoksa boş ikon
