# -*- coding: utf-8 -*-
import datetime  # Date
import json  # JSON things
import os  # Collect data from os
import sys  # For some sys vars
import random  # Randomizer
import re  # For deleting HTML tags when logging

from nltk.tokenize import TweetTokenizer  # Lang tools
from difflib import SequenceMatcher  # Calculate diff btw words


def resource_path(relative_path):
    # This needs for PyInstaller
    # Link: https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


''' SET VARS '''
message = ""
prefix = "<font color='green'>AskBOT:</font><br>"
# Set tokenizer
wtokenizer = TweetTokenizer()


def fileCheck():
    # checks files, if not exists create from local
    if not os.path.exists("Settings.json"):
        open("Settings.json", "w").write(open(resource_path("Settings.json"), "r").read())
    if not os.path.exists("Brain.json"):
        open("Brain.json", "w").write(open(resource_path("Brain.json"), "r").read())


fileCheck()

with open("Brain.json", encoding="utf-8") as brain:
    data = json.load(brain)

with open("Settings.json", "r", encoding="utf-8") as settingfile:
    settings = json.load(settingfile)

admin = []
lined_status = []


def logger(entry):
    if os.path.exists("log") is True:
        with open("log", "a", encoding="utf-8") as log:
            cleaner = re.compile('<.*?>')
            log.write(re.sub(cleaner, '', entry) + "\n")
            log.close()
    elif os.path.exists("log") is False:
        x = open("log", "w", encoding="utf-8")
        x.write("'CREATED'\n\n")
        x.close()
        logger(entry)


def lined():
    if 1 in lined_status:
        return True
    else:
        return False


def linedchange(d):
    lined_status.clear()
    lined_status.append(d)


class Settings:
    def setSetting(setting, val):
        settings[setting] = val
        with open("Settings.json", "w", encoding="utf-8") as settfile:
            json.dump(settings, settfile, sort_keys=True)
            settfile.close()

    def getSetting(setting):
        return settings[setting]


def fullScreen():
    if Settings.getSetting("Fullscreen") == "Yes":
        Settings.setSetting("Fullscreen", "No")
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        Settings.setSetting("Fullscreen", "Yes")
        os.execl(sys.executable, sys.executable, *sys.argv)


def similarity(a, b):
    '''
    CALCULATE BTW 2 WORDS
    MODULE: difflib
    '''
    return SequenceMatcher(None, a, b).ratio()


def AskBot(isitfirst, message):
    if isitfirst:
        ''' Opening Message '''
        return "" + prefix + "Hello, I am AskBOT!<br>How can i help you?<br>"
    else:
        if message == "":
            ''' Empty input message '''
            return prefix + "Can you please write something?"
        else:
            while True:
                message = message.lower()
                message_elements = []
                message_elements.extend(wtokenizer.tokenize(message))
                if message.startswith("$") and message.endswith("$") and not (message == "$" or message == "$$"):
                    ''' Admin Commands '''
                    command = message[1:-1]
                    if "A" in admin:
                        if command == "exit":
                            sys.exit()
                        elif command == "restart":
                            os.execl(sys.executable, sys.executable, *sys.argv)
                        elif command == "fullscreen":
                            fullScreen()
                        elif command == "leave":
                            admin.remove("A")
                        else:
                            return "'" + command + "' is not a valid command."
                    else:
                        if command == "pass123":
                            admin.append("A")
                            return "Authorized. Do not forget to type $leave$ when you're done."
                        else:
                            return "Error!"
                else:
                    if "A" in admin:
                        admin.remove("A")
                    ''' Lined Messaging '''
                    for lineddata in data["Lined"]:
                        change = random.choice(lineddata["answer"])
                        change2 = random.choice(lineddata["answer2"])
                        changer = ""
                        changer2 = ""
                        if "empty" in lineddata["code"]:
                            changer = change
                            changer2 = change2
                        elif lineddata["code"] == "first":
                            changer = change.format(message_elements[0].lower().capitalize())
                            changer2 = change2.format(message_elements[0].lower().capitalize())
                        elif lineddata["code"] == "last":
                            changer = change.format(message_elements[-1].lower().capitalize())
                            changer2 = change2.format(message_elements[-1].lower().capitalize())
                        elif lineddata["code"] == "weather":
                            changer = change
                            changer2 = change2
                        elif lineddata["code"] == "announcements":
                            msg = ""
                            for dataaa in data["Announcements"]:
                                msg = dataaa + "<br>" + msg
                            changer = change.format(msg)
                            changer2 = change2.format(msg)
                        elif lineddata["code"] == "date":
                            changer = change.format(datetime.datetime.now().strftime("%d/%m/%y, %H:%M (%w. day)"))
                            changer2 = change.format(datetime.datetime.now().strftime("%d/%m/%y, %H:%M (%w. day)"))
                        elif lineddata["code"] == "program":
                            changer = change
                            for dataaa in data["Class-Programs"]:
                                if message in dataaa["Class"].lower() and lined():
                                    return prefix + change2.format(dataaa["Program"])
                                elif similarity(message, dataaa["Class"].lower()) >= 0.7 and lined():
                                    return prefix + change2.format(dataaa["Program"])
                        elif lineddata["code"] == "teachers":
                            changer = change
                            for dataaa in data["Teachers"]:
                                if message in dataaa["Name"].lower() and lined():
                                    return prefix + change2.format(
                                        "NAME: " + dataaa["Name"] + "<br>LESSON: " + dataaa["Lesson"] + "<br>SINCE: " +
                                        dataaa["Since"])
                                elif similarity(message, dataaa["Name"].lower()) >= 0.7 and lined():
                                    return prefix + change2.format(
                                        "NAME: " + dataaa["Name"] + "<br>LESSON: " + dataaa["Lesson"] + "<br>SINCE: " +
                                        dataaa["Since"])
                        elif lineddata["code"] == "exams":
                            changer = change
                            for dataaa in data["Exam-Dates"]:
                                if message == "all" and lined():
                                    m = []
                                    for i in range(0, len(data["Exam-Dates"])):
                                        m.append("<br>LESSON: " + data["Exam-Dates"][i]["Lesson"] + "<br>DATE: " +
                                                 data["Sinav-Tarihleri"][i]["Date"] + "<br>")
                                    return prefix + change2.format("".join(repr(e) for e in m))
                                if similarity(message, "all") >= 0.7 and lined():
                                    m = []
                                    for i in range(0, len(data["Exam-Dates"])):
                                        m.append("<br>LESSON: " + data["Exam-Dates"][i]["Lesson"] + "<br>DATE: " +
                                                 data["Exam-Dates"][i]["Date"] + "<br>")
                                    return prefix + change2.format("".join(repr(e) for e in m))
                                if message in dataaa["Lesson"].lower() and lined():
                                    return prefix + change2.format(dataaa["Date"])
                                elif similarity(message, dataaa["Lesson"].lower()) >= 0.7 and lined():
                                    return prefix + change2.format(dataaa["Date"])
                        for element in message_elements:
                            if message in lineddata["key"] and similarity(message, lineddata["key"]) >= 0.7:
                                linedchange(1)
                                return prefix + changer
                            elif element in lineddata["key"] and similarity(element, lineddata["key"]) >= 0.7:
                                linedchange(1)
                                return prefix + changer
                            elif message in lineddata["key2"] and lined() and similarity(message, lineddata[
                                "key2"]) >= 0.7:
                                linedchange(0)
                                return prefix + changer2
                            elif element in lineddata["key2"] and lined() and similarity(element, lineddata[
                                "key2"]) >= 0.7:
                                linedchange(0)
                                return prefix + changer2
                            else:
                                for key in lineddata["key"]:
                                    if similarity(element, key) >= 0.67:
                                        linedchange(1)
                                        return prefix + changer
                                    elif similarity(message, key) >= 0.67:
                                        linedchange(1)
                                        return prefix + changer
                                for key2 in lineddata["key2"]:
                                    if similarity(element, key2) >= 0.67 and lined():
                                        linedchange(0)
                                        return prefix + changer2
                                    elif similarity(message, key2) >= 0.67 and lined():
                                        linedchange(0)
                                        return prefix + changer2
                    else:
                        linedchange(0)
                        ''' ASK-ANSWER CHAT '''
                        for mindata in data["Chat"]:
                            for element in message_elements:
                                if message in mindata["key"] and similarity(message, mindata["key"]) >= 0.7:
                                    return prefix + random.choice(mindata["answer"])
                                elif element in mindata["key"] and similarity(element, mindata["key"]) >= 0.7:
                                    return prefix + random.choice(mindata["answer"])
                                else:
                                    for key in mindata["key"]:
                                        if similarity(message, key) >= 0.67:
                                            return prefix + random.choice(mindata["answer"])
                                        elif similarity(element, key) >= 0.67:
                                            return prefix + random.choice(mindata["answer"])
                        else:
                            return prefix + random.choice(data["NoAnswer"])
                        # Only returns error message
                        # If cant find word in a key, checks other keys too
