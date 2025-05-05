def get_theme(name: str) -> str:
    if name == "dark":
        return """
        QWidget {
            background-color: #2e2e2e;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }

        QLabel {
            font-size: 15px;
        }

        QLineEdit, QTextEdit {
            background-color: #3c3c3c;
            border: 1px solid #555;
            border-radius: 6px;
            padding: 8px;
        }

        QGroupBox {
            background-color: #3c3c3c;
            border: 1px solid #666;
            border-radius: 8px;
            padding: 10px;
            margin-top: 10px;
        }

        QGroupBox:title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }

        QRadioButton {
            font-size: 15px;
        }

        QPushButton {
            background-color: #444;
            color: white;
            border-radius: 6px;
            padding: 10px;
            font-size: 15px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #666;
        }

        QScrollArea {
            border: none;
        }
        """
    elif name == "light":
        return """
        QWidget {
            background-color: #f4f4f4;
            color: #222222;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }

        QLabel {
            font-size: 15px;
        }

        QLineEdit, QTextEdit {
            background-color: #ffffff;
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 8px;
        }

        QGroupBox {
            background-color: #ffffff;
            border: 1px solid #aaa;
            border-radius: 8px;
            padding: 10px;
            margin-top: 10px;
        }

        QGroupBox:title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }

        QRadioButton {
            font-size: 15px;
        }

        QPushButton {
            background-color: #1976d2;
            color: white;
            border-radius: 6px;
            padding: 10px;
            font-size: 15px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #1259a4;
        }

        QScrollArea {
            border: none;
        }
        """
    return ""
