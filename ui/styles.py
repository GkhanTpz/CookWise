def get_theme(name: str) -> str:
    if name == "dark":
        return """
        QWidget {
            background-color: #2e2e2e;
            color: #f0f0f0;
            font-family: 'Arial', sans-serif;
            font-size: 14px;
        }

        QLabel, QLineEdit, QPushButton, QRadioButton, QGroupBox {
            font-size: 16px;
        }

        QLineEdit, QGroupBox {
            background-color: #3c3c3c;
            border: 1px solid #555;
            border-radius: 8px;
            padding: 10px;
            color: #f0f0f0;
        }

        QPushButton {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            font-weight: bold;
            padding: 15px;
        }

        QPushButton:hover {
            background-color: #45a049;
        }

        QRadioButton {
            padding: 5px;
            font-size: 16px;
        }

        QLabel {
            font-weight: bold;
            color: #e0e0e0;
        }
        """
    elif name == "light":
        return """
        QWidget {
            background-color: #f9f9f9;
            color: #333333;
            font-family: 'Arial', sans-serif;
            font-size: 14px;
        }

        QLabel, QLineEdit, QPushButton, QRadioButton, QGroupBox {
            font-size: 16px;
        }

        QLineEdit, QGroupBox {
            background-color: #ffffff;
            border: 1px solid #aaa;
            border-radius: 8px;
            padding: 10px;
            color: #333333;
        }

        QPushButton {
            background-color: #2196F3;
            color: white;
            border-radius: 10px;
            font-weight: bold;
            padding: 15px;
        }

        QPushButton:hover {
            background-color: #1976D2;
        }

        QRadioButton {
            padding: 5px;
            font-size: 16px;
        }

        QLabel {
            font-weight: bold;
            color: #333333;
        }
        """
    return ""
