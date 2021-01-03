# Author : Ankesh Kumar
# Date :-
# Version 1.0 - 10 May 2020
# Version 1.1 - 25 September 2020
# Version 1.2 - 5 November 2020

import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import webbrowser
import os
import smtplib
from os import system
import requests
import json
import pyautogui
import datetime
import wikipedia
from functools import lru_cache
import speedtest


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def Getdatetime():
    return datetime.datetime.now()


def speak(audio):  # Function that uses system's audio and speaks
    engine.say(audio)
    engine.runAndWait()


def wishMe(name):  # Function to wish user
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morining!")
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        print("Good Afternoon!")
        speak("Good Afternoon!")

    else:
        print("Good Evening!")
        speak("Good Evening!")
    print(f"I am Amplex {name}. Please tell me how may I help you")
    speak(f"I am Amplex {name}. Please tell me how may I help you")


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            speak("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
    except:
        print("Please Ensure that your microphone is inserted properly")
        speak("Please Ensure that your microphone is inserted properly")

    try:
        print("Recognizing...")
        speak("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except:
        print("Say that again please...")
        speak("Say that again please...")
        return "None"
    return query


def sendEmail(to, content, email_sen, re_email, password):  # Function to send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_sen, password)
    server.sendmail(re_email, to, content)
    server.close()


@lru_cache(maxsize=50)
def news_reader():
    """
    This function calls news API and retrieves latest news
    """
    url = ('http://newsapi.org/v2/top-headlines?'
           'country=us&'
           'apiKey=49490b8a2fed496ebfc5a63a7ca3a96f')  # Url of the API
    response = requests.get(url)
    parsed_json = json.loads(response.text)
    for i in range(1, 11):
        speak(f"News number {i}")
        speak(parsed_json['articles'][i]['title'])
        speak(parsed_json['articles'][i]['description'])

def internet_speed():
    """
    This function calculates the Download and upload internet speed
    """
    try:
        print("Calculating the internet speed.....")
        speak("Calculating the internet speed")
        s = speedtest.Speedtest()
        down_speed = str(s.download())  # Initializing download speed
        up_speed = str(s.upload())  # Initializing upload speed
        print(f"Download speed is {down_speed[0:2]}Mbps")
        print(f"Upload speed is {up_speed[0:2]}Mbps")
        speak(f"Sir your Download speed is {down_speed[0:2]}Mbps and your Upload speed is {up_speed[0:2]}Mbps")

    except:
        """
        If any internet issue will be there the exception will be executed
        """
        print("Error: Connection timed out try again")
        speak("Error: Connection timed out try again")

def main():
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'hello' in query.lower():
            speak("Hello Sir how may I help you")

        elif 'wikipedia' in query.lower():
            """
            It will give the wikipedia of 'query'
            """
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'time' in query.lower():  # If user asks for time it will speak the time
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'whatsapp' in query.lower():  # Opens Whatsapp web
            speak("Opening Whatsapp web")
            print("Opening Whatsapp web")
            webbrowser.open("https://web.whatsapp.com/")



        elif 'email' in query.lower():  # Sends email

            with open("u_email.txt", "a+") as f_e:
                with open("u_password.txt", "a+") as f_p:
                    f_e.seek(0)
                    first_char = f_e.read(1)
                    if not first_char:
                        print("Please Login ones to send emails: ")
                        speak("Please Login ones to send emails: ")
                        print("Enter your email address: ")
                        speak("Enter your email address: ")
                        email_sen = input()
                        f_e.write(email_sen)
                        print("Enter your password: ")
                        speak("Enter your password: ")
                        password = input()
                        f_p.write(password)
                    else:
                        email_sen = f_e.read()
                        password = f_p.read()

            print("Enter the email of reciever: ")
            speak("Enter the email of reciever: ")
            email = input()
            if '@' not in email:
                print("Please enter a valid email address")
                speak("Please enter a valid email address")
                print("Do you want to retry(y/n): ")
                speak("Do you want to retry(y/n): ")
                retry = input()
                if retry == 'Y' or retry == 'y':
                    while '@' not in email:
                        print("Enter the email of reciever: ")
                        speak("Enter the email of reciever: ")
                        email = input()
                        # sendEmail(to, content, email_sen, email, password)
            try:
                speak("What should I send?")
                content = takeCommand()
                to = email
                with open("u_email.txt", "r") as f_e:
                    with open("u_password.txt", "r") as f_p:
                        sendEmail(to, content, f_e.read(), email, f_p.read())
                speak("Email has been sent successfully!")
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to send this email")

        elif 'speed' in query.lower():
            internet_speed()

        elif 'news' in query.lower():
            news_reader()

        elif 'logout' in query.lower() or 'log out' in query.lower():
            with open("u_email.txt", "w") as f_e:
                with open("u_password.txt", "w") as f_p:
                    with open("name.txt","w") as f_n:
                        f_e.write("")
                        f_p.write("")
                        f_n.write("")

        elif 'full screen' in query.lower():
            pyautogui.press("F11")

        elif 'shutdown' in query.lower():
            speak("shutting down Sir")
            system("shutdown /s /t 1")

        elif 'search on google' in query.lower():
            speak("What should I search?")
            print("What should I search?")
            query = takeCommand().lower()
            webbrowser.open(f"{query}.com")

        elif 'open google' in query.lower():
            speak("Opening Google")
            webbrowser.open("google.com")

        elif 'open youtube' in query.lower():
            speak("Opening Youtube")
            webbrowser.open("youtube.com")

        elif 'exit' in query.lower():
            print("Ok quitting sir thanks for your time")
            speak("Ok quitting sir thanks for your time")
            exit()
        # system('cls')


if __name__ == "__main__":

    with open("name.txt","a+") as n:
        n.seek(0)
        if not n.read(1):
            print("Please enter your name:")
            speak("Please enter your name")
            name = input()
            n.write(" "+name)
        else:
            name = n.read()

    wishMe(name)
    # # main function starts
    main()
