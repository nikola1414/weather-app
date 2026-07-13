import sys
import requests
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                              QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

load_dotenv()

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_btn = QPushButton("Enter",self)
        self.temp_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.desc_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
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

        self.get_weather_btn.clicked.connect(self.get_weather)

    def get_weather(self):
        API_KEY = os.environ.get("WEATHER_API_KEY")
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data["cod"] == 200:
                self.display_weather(data)
                    
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nCheck your input")
                case 401:
                    self.display_error("Unauthorized:\nAPI key is invalid")
                case 403:
                    self.display_error("Forbidden:\nAccess denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nTry again later")
                case 502:
                    self.display_error("Bad Gateway:\nBad server response")
                case 503:
                    self.display_error("Service Unavailable:\nThe server is down")
                case 504:
                    self.display_error("Gateway timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
        self.temp_label.setStyleSheet("font-size: 30px")
        self.temp_label.setText(message)
        self.emoji_label.clear()
        self.desc_label.clear()

    def display_weather(self, data):
        self.temp_label.setStyleSheet("font-size: 75px")
        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15
        w_desc = data["weather"][0]["description"]
        w_id = data["weather"][0]["id"] 

        self.temp_label.setText(f"{temp_c:.1f}°C")
        self.emoji_label.setText(self.get_weather_emoji(w_id))
        self.desc_label.setText(w_desc.capitalize());

    @staticmethod
    def get_weather_emoji(w_id):
        if 200 <= w_id <=232:
            return "⛈️"
        elif 300 <= w_id <=321:
            return "🌥️"
        elif 500 <= w_id <=531:
            return "🌧️"
        elif 600 <= w_id <= 622:
            return "❄️"
        elif 701 <= w_id <= 741:
            return "🌫️"
        elif w_id == 762:
            return "🌋"
        elif w_id == 771:
            return "💨"
        elif w_id == 761:
            return "🌪️"
        elif w_id == 800:
            return "☀️"
        elif 801 <= w_id <=804:
            return "☁️"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
