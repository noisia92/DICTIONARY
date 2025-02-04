import speech_recognition as sr

from gtts import gTTS

import os

import time

import playsound

import sys
from PyQt5.QtWidgets import *

import requests
from bs4 import BeautifulSoup





from PyQt5 import uic

form_class = uic.loadUiType("./quiz.ui")[0]

class MyWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.word_list = []
        self.num = 0
        f = open("C:/LOGS/word.txt", 'rb')
        words = f.readlines()
        f.close()

        for x in words:
            self.word_list.append(x.strip().decode('utf-8'))
        # self.speak_again()
        self.pushButton_2.clicked.connect(self.speak_next)
        self.pushButton_3.clicked.connect(self.speak_again)
        self.pushButton.clicked.connect(self.speak_before)

    def speak_next(self):
        try:
            self.num = self.num + 1
            self.lcdNumber.display(self.num)
            self.label.setText(self.word_list[self.num].split('@')[0])
            self.label_2.setText('')
            word = self.word_list[self.num].split('@')[0]
            tts = gTTS(text=word, lang='en')

            filename = word+'.mp3'

            if os.path.exists(filename):
                playsound.playsound(filename,block=False)
                self.search_daum_dic(word)
                #self.label_2.setText(self.word_list[self.num].split('@')[1])
            else :
                tts.save(filename)

                if os.path.exists(filename):
                    playsound.playsound(filename, block=False)
                #self.label_2.setText(self.word_list[self.num].split('@')[1])
        except Exception as e:
            print(e)
            print('ERROR')
        self.label_2.setText(self.word_list[self.num].split('@')[1])

    def speak_again(self):
        try:

            self.lcdNumber.display(self.num)
            self.label.setText(self.word_list[self.num].split('@')[0])
            tts = gTTS(text=self.word_list[self.num].split('@')[0], lang='en')
            filename = self.word_list[self.num].split('@')[0]+'.mp3'

            if os.path.exists(filename):
                playsound.playsound(filename,block=False)
            else :
                tts.save(filename)
                playsound.playsound(filename,block=False)
        except Exception as e:
            print(e)
        self.label_2.setText(self.word_list[self.num].split('@')[1])


    def speak_before(self):
        try:
            self.num = self.num - 1
            self.lcdNumber.display(self.num)
            self.label.setText(self.word_list[self.num ].split('@')[0])

            tts = gTTS(text=self.word_list[self.num].split('@')[0], lang='en')
            filename = self.word_list[self.num].split('@')[0]+'.mp3'

            if os.path.exists(filename):
                playsound.playsound(filename,block=False)
            else :
                tts.save(filename)
                playsound.playsound(filename,block=False)
        except Exception as e:
            print(e)
        self.label_2.setText(self.word_list[self.num].split('@')[1])

    def search_daum_dic(self,query_keyword):
        dic_url = """http://dic.daum.net/search.do?q={0}"""
        r = requests.get(dic_url.format(query_keyword))
        soup = BeautifulSoup(r.text, "html.parser")
        result_means = soup.find_all(attrs={'class':'list_search'})
        self.print_result("daum", result_means)

    def print_result(self, site, result_means):
        print("*" * 25)
        print("*** %s dic ***" % site)
        print("*" * 25)
        for elem in result_means:
            text = elem.get_text().strip()
            if text:
                print(text.replace('\n', ', '))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
