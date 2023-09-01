import tkinter as tk
import webbrowser
import requests
import threading
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime

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
    global website_previous_text, is_monitoring

    if is_monitoring:
        website_content = check_website(website_url.get())

        if website_content:
            soup = BeautifulSoup(website_content, 'html.parser')
            website_text = soup.get_text()
            website_hash = generate_hash(website_text)

            if website_hash != website_previous_text:
                play_notification_sound()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                notification_message = f"საიტის კონტენტი შეიცვალა {timestamp}."
                show_notification(notification_message)
                website_previous_text = website_hash

        root.after(check_interval, check_website_content)

# Function to play notification sound
def play_notification_sound():
    print("საიტზე არის ცვლილება!")

# Function to open the website in the browser
def open_website():
    webbrowser.open(website_url.get())

# Function to show the notification window
def show_notification(message):
    notification_window = tk.Toplevel(root)
    notification_window.title("საიტზე მოხვდა ცვლილება")
    notification_window.geometry("400x150")
    notification_window.resizable(False, False)
    tk.Label(notification_window, text=message).pack(pady=10)
    tk.Button(notification_window, text="დახურვა", command=notification_window.destroy).pack(pady=5)

# Function to toggle monitoring status
def toggle_monitoring():
    global is_monitoring

    if is_monitoring:
        is_monitoring = False
        monitoring_button.config(text="მონიტორინგის დაწყება", bg="#4CAF50")
        live_status_label.config(text="მონიტორინგის დაპაუზება", fg="red")
    else:
        is_monitoring = True
        monitoring_button.config(text="მონიტორინგის დაპაუზება", bg="#F44336")
        live_status_label.config(text="მიმდინარეობს საიტის მონიტორინგი", fg="#4CAF50")
        threading.Thread(target=check_website_content).start()

# GUI setup
root = tk.Tk()
root.title("პროგრამა დაწერილია by@Matik")
root.geometry("500x500")

# Variables for website URL and previous text hash
website_url = tk.StringVar()
website_previous_text = ""
is_monitoring = False

# Create GUI elements
tk.Label(root, text="საიტის მისამართი (http://yoursite.com/):", font=("Arial", 12)).place(relx=0.5, y=50, anchor=tk.CENTER)
tk.Entry(root, textvariable=website_url, width=40, font=("Arial", 12)).place(relx=0.5, y=100, anchor=tk.CENTER)

tk.Button(root, text="ვებსაიტის გახსნა", command=open_website, width=25, font=("Arial", 12)).place(relx=0.5, y=150, anchor=tk.CENTER)

monitoring_button = tk.Button(root, text="მონიტორინგის დაწყება", command=toggle_monitoring, width=25, bg="#4CAF50", font=("Arial", 12))
monitoring_button.place(relx=0.5, y=200, anchor=tk.CENTER)

live_status_label = tk.Label(root, text="მონიტორინგის დაპაუზება", fg="red", font=("Arial", 12))
live_status_label.place(relx=0.5, y=250, anchor=tk.CENTER)

check_interval = 5000  # Interval in milliseconds (5 seconds)

root.mainloop()
