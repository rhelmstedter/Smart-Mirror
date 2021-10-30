#! python3

from tkinter import *
import feedparser
import json
import locale
import os
import requests
import threading
import time
import traceback
from PIL import Image, ImageTk
from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()

ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 12 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
news_country_code = 'us'

API_KEY = os.getenv('WEATHER_API')
CITY = 'Ventura'
STATE = 'CA'
weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"

xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

icon_lookup = {
    '01d': "assets/Sun.png",  # clear sky day
    '01n': "assets/Moon.png",  # clear sky night
    '02d': "assets/PartlySunny.png",  # partly cloudy day
    '02n': "assets/PartlyMoon.png",  # partly cloudy night
    '03d': "assets/PartlySunny.png",  # cloudy day
    '03n': "assets/PartlyMoon.png",  # cloudy night
    '04d': "assets/Cloud.png",  # cloudy day
    '04n': "assets/Cloud.png",  # cloudy night
    '09d': "assets/Rain.png",  # rain day
    '09d': "assets/Rain.png",  # rain day
    '10n': "assets/Rain.png",  # rain night
    '10n': "assets/Rain.png",  # rain night
    '13d': "assets/Snow.png",  # snow day
    '13n': "assets/Snow.png",  # snow night
    '50d': "assets/Haze.png",  # fog day
    '50n': "assets/Haze.png",  # fog night
    '11d': "assets/Storm.png",  # thunderstorm day
    '11n': "assets/Storm.png",  # thunderstorm night
    'windy': "assets/Wind.png",   #windy
}

class Clock(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)


class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.min_temp = ''
        self.location = ''
        self.max_temp = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.max_tempLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.max_tempLbl.pack(side=TOP, anchor=W)
        self.min_tempLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.min_tempLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)
        self.get_weather()


    def get_weather(self):
        try:
            def convert_kelvin_to_fahrenheit(kelvin_temp):
                f_temp = 1.8 * (kelvin_temp - 273) + 32
                return f"{f_temp:.1f}"

            r = requests.get(weather_url)
            weather_obj = json.loads(r.text)
            degree_sign= u'\N{DEGREE SIGN}'
            location = f"{CITY}, {STATE}"
            temperature = convert_kelvin_to_fahrenheit(weather_obj['main']['temp'])
            max_temp = convert_kelvin_to_fahrenheit(weather_obj["main"]["temp_max"])
            min_temp = convert_kelvin_to_fahrenheit(weather_obj['main']['temp_min'])
            wind = weather_obj["wind"]["speed"]
            weather_icon = weather_obj['weather'][0]['icon']

            icon = None
            if wind >= 8:
                icon = icon_lookup["windy"]
            elif weather_icon in icon_lookup:
                icon = icon_lookup[weather_icon]

            if icon is not None:
                if self.icon != icon:
                    self.icon = icon
                    image = Image.open(icon)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)
                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo

            if self.max_temp != max_temp:
                self.max_temp = max_temp
                self.max_tempLbl.config(text=f"High: {max_temp}{degree_sign}")
            if self.min_temp != min_temp:
                self.min_temp = min_temp
                self.min_tempLbl.config(text=f"Low: {min_temp}{degree_sign}")
            if self.temperature != temperature:
                self.temperature = temperature
                self.temperatureLbl.config(text=f"{temperature}{degree_sign}F")
            if self.location != location:
                self.location = location
                self.locationLbl.config(text=location)
        except Exception as e:
            traceback.print_exc()
            print(f"Error: {e}. Cannot get weather.")

        self.after(600000, self.get_weather)


class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'News' # 'News' is more internationally generic
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = Frame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()

    def get_headlines(self):
        try:
            # remove all children
            for widget in self.headlinesContainer.winfo_children():
                widget.destroy()
            if news_country_code == None:
                headlines_url = "https://news.google.com/news?ned=us&output=rss"
            else:
                headlines_url = "https://news.google.com/news?ned=%s&output=rss" % news_country_code

            feed = feedparser.parse(headlines_url)

            for post in feed.entries[0:5]:
                headline = NewsHeadline(self.headlinesContainer, post.title)
                headline.pack(side=TOP, anchor=W)
        except Exception as e:
            traceback.print_exc()
            print(f"Error: {e}. Cannot get news.")

        self.after(600000, self.get_headlines)


class NewsHeadline(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=N)


class Calendar(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.title = 'Calendar Events'
        self.calendarLbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.calendarLbl.pack(side=TOP, anchor=E)
        self.calendarEventContainer = Frame(self, bg='black')
        self.calendarEventContainer.pack(side=TOP, anchor=E)
        self.get_events()

    def get_events(self):
        #TODO: implement this method
        # reference https://developers.google.com/google-apps/calendar/quickstart/python

        # remove all children
        for widget in self.calendarEventContainer.winfo_children():
            widget.destroy()

        calendar_event = CalendarEvent(self.calendarEventContainer)
        calendar_event.pack(side=TOP, anchor=E)
        pass


class CalendarEvent(Frame):
    def __init__(self, parent, event_name="Event 1"):
        Frame.__init__(self, parent, bg='black')
        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=TOP, anchor=E)


class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)
        # news
        self.news = News(self.bottomFrame)
        self.news.pack(side=LEFT, anchor=S, padx=100, pady=60)
        # calender - removing for now
        # self.calender = Calendar(self.bottomFrame)
        # self.calender.pack(side = RIGHT, anchor=S, padx=100, pady=60)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
