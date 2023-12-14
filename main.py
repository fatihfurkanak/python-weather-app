# Importing required libraries
from tkinter import *  # Tkinter library for GUI components
from tkinter import messagebox  # Tkinter messagebox module for alert messages
import requests  # Requests library for HTTP requests
from PIL import ImageTk, Image  # PIL for image processing and compatibility with Tkinter
from urllib.request import urlopen  # urllib for downloading data from URLs
import ssl  # SSL for working with SSL certificates

# Defining global variables
icon_image = None  # To store the weather icon image
icon_label = None  # To store the label widget for the weather icon
info_label = None  # To store the label widget for weather information

# Function to fetch and display weather information
def getWeather():
    global icon_image, icon_label, info_label  # Access to global variables
    api_key = "bd5e378503939ddaee76f12ad7a97608"  # API key
    # URL formatted to fetch weather info based on the city name entered by the user
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_entry.get()}&appid={api_key}"
    response = requests.get(url)  # Sending HTTP GET request to fetch data from the API

    # Processing the HTTP response
    if response.status_code == 200:  # Success response (200 OK)

        # Clear previous weather labels if they exist
        if icon_label and info_label:
            icon_label.destroy()
            info_label.destroy()

        # Parsing the data from the API response
        data = response.json()
        temperature = data['main']['temp']  # Temperature information
        # Formatting the temperature to Celsius
        formatted_temp = f"{(int(temperature)-272.15):.0f} °C"
        description = data['weather'][0]['description'].capitalize()  # Weather description

        # Fetching and loading the weather icon
        weather_icon = data['weather'][0]['icon']
        weather_icon_url = f"https://openweathermap.org/img/wn/{weather_icon}@2x.png"
        icon_data = urlopen(weather_icon_url)
        icon_image = ImageTk.PhotoImage(data=icon_data.read())
        # Adding the weather icon to the GUI
        icon_label = Label(window, image=icon_image)
        icon_label.pack()

        # Adding the weather information to the GUI
        info_label = Label(text=f"{description} \n {formatted_temp} \n {city_entry.get()}")
        info_label.pack()

        # Clearing the city entry field and focusing on it
        city_entry.delete(0,END)
        city_entry.focus()

    else:  # If the response is not successful (e.g., 404 Not Found)
        # Showing a warning message for incorrect city name
        messagebox.showwarning("Warning","Please type correct city name!")
        city_entry.delete(0,END)

# Creating a Tkinter window
window = Tk()
window.title("Weather App")  # Setting the window title
window.geometry("400x600")  # Setting the window size

# Creating and adding a label for the logo
image = Image.open("logo.png").resize((150,65))
logo = ImageTk.PhotoImage(image)
logo_label = Label(image=logo)
logo_label.config(pady=250)
logo_label.pack()

# Creating and adding a label widget for city name entry
city_label = Label(text="Enter City Name")
city_label.pack()

# Creating and adding an entry widget for city name
city_entry = Entry()
city_entry.focus()
city_entry.pack()

# Disabling SSL certificate verification (Can carry security risks)
ssl._create_default_https_context = ssl._create_unverified_context

# Creating and adding a search button
search_button = Button(text="Search", command=getWeather)
search_button.pack()

# Starting the GUI and maintaining the event loop
window.mainloop()