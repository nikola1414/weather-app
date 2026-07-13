import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                              QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Unesi ime grada: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_btn = QPushButton("Enter",self)
        self.temp_label = QLabel("29°C",self)
        self.emoji_label = QLabel("☀️",self)
        self.desc_label = QLabel("Suncano",self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Vremenska Prognoza")
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_btn)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.desc_label)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_btn.setObjectName("get_weather_btn")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.desc_label.setObjectName("desc_label")

        self.setStyleSheet("""
            QLabel,QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;     
                font-style: italic;          
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_btn{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temp_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;               
            }
            QLabel#desc_label{
                font-size: 50px;               
            }
        """)




if __name__ == "__main__":
    app = QApplication(sys.argv) 
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
