import tkinter as tk
import webbrowser
import requests
import threading
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime
import time
import winsound  # Import the 'winsound' module

# Function to check if the content of the website has changed
def check_website(website_url):
    try:
        response = requests.get(website_url)
        return response.text
    except requests.exceptions.RequestException:
        return None

# Function to generate a hash for website content
def generate_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

# Function to check the website text content
def check_website_content():
    global website_previous_text

    website_content = check_website(website_url.get())

    if website_content:
        soup = BeautifulSoup(website_content, 'html.parser')
        website_text = soup.get_text()
        website_hash = generate_hash(website_text)

        if website_hash != website_previous_text:
            play_notification_sound()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            notification_message = f"Text content was changed on the website at {timestamp}."
            show_notification(notification_message)
            website_previous_text = website_hash

    root.after(check_interval, check_website_content)

# Function to play notification sound
def play_notification_sound():
    winsound.PlaySound("notification.wav", winsound.SND_FILENAME)

# Function to open the website in the browser
def open_website():
    webbrowser.open(website_url.get())

# Function to show the notification window
def show_notification(message):
    notification_window = tk.Toplevel(root)
    notification_window.title("Notification")
    notification_window.geometry("300x100")
    notification_window.resizable(False, False)
    tk.Label(notification_window, text=message).pack(pady=10)
    tk.Button(notification_window, text="Close", command=notification_window.destroy).pack(pady=5)

# Function to toggle monitoring status
def toggle_monitoring():
    global is_monitoring

    if is_monitoring:
        is_monitoring = False
        monitoring_button.config(text="Start Monitoring", bg="#4CAF50")
        live_status_label.config(text="Monitoring Paused", fg="red")
    else:
        is_monitoring = True
        monitoring_button.config(text="Pause Monitoring", bg="#F44336")
        live_status_label.config(text="Monitoring Live", fg="#4CAF50")
        check_website_content()  # Call the function immediately to start monitoring
        threading.Thread(target=continuous_check_website_content).start()

def continuous_check_website_content():
    while is_monitoring:
        check_website_content()
        time.sleep(check_interval / 1000)

# GUI setup
root = tk.Tk()
root.title("Website Content Checker")
root.geometry("500x500")

# Variables for website URL and previous text hash
website_url = tk.StringVar()
website_previous_text = ""
is_monitoring = False

# Create GUI elements
tk.Label(root, text="Website URL:", font=("Arial", 12)).place(relx=0.5, y=50, anchor=tk.CENTER)
tk.Entry(root, textvariable=website_url, width=40, font=("Arial", 12)).place(relx=0.5, y=100, anchor=tk.CENTER)

tk.Button(root, text="Open Website", command=open_website, width=15, font=("Arial", 12)).place(relx=0.5, y=150, anchor=tk.CENTER)

monitoring_button = tk.Button(root, text="Start Monitoring", command=toggle_monitoring, width=15, bg="#4CAF50", font=("Arial", 12))
monitoring_button.place(relx=0.5, y=200, anchor=tk.CENTER)

live_status_label = tk.Label(root, text="Monitoring Paused", fg="red", font=("Arial", 12))
live_status_label.place(relx=0.5, y=250, anchor=tk.CENTER)

check_interval = 5000  # Interval in milliseconds (5 seconds)

root.mainloop()
