import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import csv
import os
import tkinter as tk
from tkinter import ttk

def start_scraping():
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    link_to_scrape = link_entry.get()

    # Initialize the Selenium webdriver
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.maximize_window()

    driver.get("https://twitter.com/i/flow/login?lang=en")

    time.sleep(5)
    signin = driver.find_element(By.XPATH, value="//input[@name='text'][@autocomplete='username']").send_keys(email)
    pyautogui.press("enter")
    time.sleep(3) 
    try:
        username_input = driver.find_element(By.XPATH, value="//input[@autocapitalize='none' and @autocomplete='on' and @autocorrect='off' and @inputmode='text' and @name='text' and @spellcheck='false' and @type='text']")
        username_input.send_keys(username)
        pyautogui.press("enter")
    except NoSuchElementException:
        pass

    time.sleep(3)
    password = driver.find_element(By.XPATH, value="//input[@type='password']").send_keys(password)
    pyautogui.press("enter")

    time.sleep(3)
    driver.get(link_to_scrape)
    time.sleep(3)

    def scroll_to_bottom():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    scroll_to_bottom()

    csv_file = 'tweetie.csv'
    csv_header = ['Tweet', 'Retweet', 'Like', 'Comment', 'Time']

    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(csv_header)

    while True:
        tweets = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        for tweet in tweets:
            try:
                tweetcontent = tweet.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                tweetComments = tweet.find_element(By.XPATH, ".//div[@data-testid='reply']").text
                tweet_Retweet = tweet.find_element(By.XPATH, ".//div[@data-testid='retweet']").text
                tweet_Like = tweet.find_element(By.XPATH, ".//div[@data-testid='like']").text
                tweet_time_tag = tweet.find_element(By.XPATH, ".//time[@datetime]")
                tweet_time = tweet_time_tag.get_attribute('datetime')

                print(f'Tweet: {tweetcontent}')
                print(f'Retweet: {tweet_Retweet}')
                print(f'Like: {tweet_Like}')
                print(f'Comment: {tweetComments}')
                print(f'Time: {tweet_time}')
                print('---------------------------------------------------------')

                with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([tweetcontent, tweet_Retweet, tweet_Like, tweetComments, tweet_time])

            except StaleElementReferenceException:
                tweets = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
                continue
            except NoSuchElementException as e:
                pass

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

def exit_application():
    app.quit()

app = tk.Tk()
app.title("Twitter Scraper")

# Set the Tkinter GUI window size to 720 x 312
app.geometry("320x200")  # Adjust the height to accommodate the new username label and input

empty_label = ttk.Label(app, text="")
empty_label.grid(column=0, row=0, padx=10, pady=5)

frame = ttk.Frame(app, padding=10)
frame.grid(column=1, row=1, sticky=(tk.W, tk.N, tk.E, tk.S))

# Create labels, entries, and buttons
username_label = ttk.Label(frame, text="Username:")  # Add username label
username_entry = ttk.Entry(frame)
email_label = ttk.Label(frame, text="Email:")
password_label = ttk.Label(frame, text="Password:")
link_label = ttk.Label(frame, text="Link to scrape:")
email_entry = ttk.Entry(frame)
password_entry = ttk.Entry(frame, show="*")
link_entry = ttk.Entry(frame)
start_button = ttk.Button(frame, text="Start Scraping", command=start_scraping)
exit_button = ttk.Button(frame, text="Exit", command=exit_application)

# Configure grid layout for labels, entries, and buttons
username_label.grid(column=0, row=0, sticky=tk.E, padx=10, pady=5)
username_entry.grid(column=1, row=0, padx=10, pady=5, columnspan=2)
email_label.grid(column=0, row=1, sticky=tk.E, padx=10, pady=5)
email_entry.grid(column=1, row=1, padx=10, pady=5, columnspan=2)
password_label.grid(column=0, row=2, sticky=tk.E, padx=10, pady=5)
password_entry.grid(column=1, row=2, padx=10, pady=5, columnspan=2)
link_label.grid(column=0, row=3, sticky=tk.E, padx=10, pady=5)
link_entry.grid(column=1, row=3, padx=10, pady=5, columnspan=2)
start_button.grid(column=1, row=4, padx=10, pady=5, columnspan=2)
exit_button.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

# Center the frame in the window
frame.grid(column=0, row=0, sticky=(tk.W, tk.N, tk.E, tk.S))
frame.columnconfigure(0, weight=1)
frame.columnconfigure(3, weight=1)
frame.rowconfigure(0, weight=1)
frame.rowconfigure(6, weight=1)

app.mainloop()