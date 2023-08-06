import datetime
import webbrowser
import os


def get_current_date():
    return datetime.date.today()


def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%p %H:%M:%S")


def convert_to_string(list_type):
    string = ""
    for i in list_type:
        string = string + i + " "
        
    return string.strip()


def open_url(url):
    webbrowser.open(url)


def clear_screen():
    os.system("clear")


def guide_to_exit():
    print("\033[0m[+] Press 'Enter' to exit\033[0m")
