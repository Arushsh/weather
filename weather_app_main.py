from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import requests
import datetime
from kivy.uix.image import Image

# Loading Screen
class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

         # Add a GIF to the layout
        self.gif = Image(
            source="Lightning.gif",  # Replace with the path to your GIF file
            anim_delay=0.05,       # Adjust the speed of the GIF (default is fine for most)
            size_hint=(1, 1.2),
            size=(1200, 1000),  # Width and height in pixels
            allow_stretch=True,  # Allow the image to be stretched to fit the widget size           
        )
        self.layout.add_widget(self.gif)

        footer = Label(
            text="Made by Arush & Team",
            font_size=24,
            color=(1, 1, 1, 1),
            size_hint=(1, 1.1),
            halign="center",
            valign="bottom",
        )
        footer.bind(size=footer.setter("text_size"))
        self.layout.add_widget(footer)

        self.label = Label(text="Loading... 0%", font_size=24,valign="bottom", halign="auto")
        self.progress_bar = ProgressBar(max=100, value=0)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.progress_bar)
        self.add_widget(self.layout)

        self.progress = 0

    def on_enter(self):
        Clock.schedule_interval(self.update_progress, 0.03)

    def update_progress(self, dt):
        self.progress += 1
        self.progress_bar.value = self.progress
        self.label.text = f"Loading... {self.progress}%"

        if self.progress >= 100:
            Clock.unschedule(self.update_progress)
            self.manager.current = "main"


# Main Weather Application Screen
class WeatherAppScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.add_widget(self.layout)

        # Header Section
        header_layout = BoxLayout(size_hint=(1, 0.2), orientation="vertical", spacing=10)
        self.title_label = Label(
            text="Weather App",
            font_size=36,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.6),
            halign="center",
        )
        header_layout.add_widget(self.title_label)

        self.clock_label = Label(
            text="00:00:00",
            font_size=24,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.4),
            halign="center",
        )
        header_layout.add_widget(self.clock_label)
        self.layout.add_widget(header_layout)

        # City Selection and Check Button
        city_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.city_spinner = Spinner(
            text="Select a City",
            values=[
                "Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai", "Hyderabad",
                "Ahmedabad", "Pune", "Jaipur", "Surat", "Varanasi", "Lucknow", "Nagpur",
            ],
            font_size=18,
            size_hint=(0.7, 1),
        )
        city_layout.add_widget(self.city_spinner)

        self.check_button = Button(
            text="Check Weather",
            font_size=18,
            size_hint=(0.3, 1),
            background_color=(0, 0.6, 0.8, 1),
            bold=True,
            on_press=self.get_weather,
        )
        city_layout.add_widget(self.check_button)
        self.layout.add_widget(city_layout)

        # Weather Information Section
        info_layout = ScrollView(size_hint=(1, 0.6))
        weather_grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        weather_grid.bind(minimum_height=weather_grid.setter("height"))

        self.labels = {}
        fields = [
            "Climate", "Description", "Temperature (°C)", "Pressure",
            "Latitude", "Longitude", "Humidity", "Sunrise Time", "Sunset Time",
        ]
        for field in fields:
            label = Label(
                text=f"{field}: ",
                font_size=16,
                halign="right",
                valign="middle",
                size_hint_y=None,
                height=40,
            )
            label.bind(size=label.setter("text_size"))
            weather_grid.add_widget(label)

            value_label = Label(
                text="--",
                font_size=16,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=40,
            )
            value_label.bind(size=value_label.setter("text_size"))
            weather_grid.add_widget(value_label)
            self.labels[field] = value_label

        info_layout.add_widget(weather_grid)
        self.layout.add_widget(info_layout)

        # Footer Section
        footer = Label(
            text="Created by Arush & Team",
            font_size=14,
            color=(0.5, 0.5, 0.5, 1),
            size_hint=(1, 0.1),
            halign="center",
            valign="middle",
        )
        footer.bind(size=footer.setter("text_size"))
        self.layout.add_widget(footer)

        # Schedule the clock update every second
        Clock.schedule_interval(self.update_clock, 1)

    def update_clock(self, dt):
        now = datetime.datetime.now()
        formatted_time = now.strftime("%H:%M:%S")
        self.clock_label.text = formatted_time

    def get_weather(self, instance):
        city = self.city_spinner.text
        if city == "Select a City":
            self.labels["Climate"].text = "Please select a city."
            return

        try:
            api_key = "4d82c5d0f454c9d692300be0d568c45f"
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            response = requests.get(url)
            data = response.json()

            if data["cod"] != 200:
                self.labels["Climate"].text = f"Error: {data['message']}"
                return

            self.labels["Climate"].text = f"{data['weather'][0]['main']}"
            self.labels["Description"].text = f"{data['weather'][0]['description']}"
            self.labels["Temperature (°C)"].text = f"{round(data['main']['temp'] - 273.15, 2)}°C"
            self.labels["Pressure"].text = f"{data['main']['pressure']} hPa"
            self.labels["Latitude"].text = f"{data['coord']['lat']}"
            self.labels["Longitude"].text = f"{data['coord']['lon']}"
            self.labels["Humidity"].text = f"{data['main']['humidity']}%"

            sunrise_timestamp = data["sys"]["sunrise"]
            sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp)
            self.labels["Sunrise Time"].text = sunrise_time.strftime("%H:%M")

            sunset_timestamp = data["sys"]["sunset"]
            sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp)
            self.labels["Sunset Time"].text = sunset_time.strftime("%H:%M")

        except Exception as e:
            self.labels["Climate"].text = f"Error: {str(e)}"


class WeatherAppByArushTeam(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoadingScreen(name="loading"))
        sm.add_widget(WeatherAppScreen(name="main"))
        return sm


if __name__ == "__main__":
    WeatherAppByArushTeam().run()
