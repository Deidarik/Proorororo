import sys
import os
import random
import time
import codecs
import math
import numpy as np
import pynput
from pynput.keyboard import Key, Listener
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtGui import QAction, QIcon,QKeySequence,QPixmap
from enum import Enum
from PyQt6.QtWidgets import (
    QApplication,
    QMessageBox,
    QMainWindow,
    QToolBar,
    QFileDialog,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit
)
import playsound
from threading import Thread
from mutagen.mp3 import MP3
import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
matplotlib.use("QtAgg")
#для типов открытых файлов
FILE_FILTERS = [
    "Portable Network Graphics files (*.png)",
    "Text files (*.txt)",
    "Comma Separated Values (*.csv)",
    "All files (*)",
    "Music (*.mp3)"
]

file_contents=""#строка, куда считывается текст
real_filename="er.png"
basedir = os.path.dirname(__file__) #механизм, по которому открытие файлов
percentage=[0.0,0.0,0.0]
Text_variants=Enum('Lesson',['First','Second','Third','No','Unique'])
state=Text_variants.No
#типо курсы, индекс массива+1=соответсвующий урок
course=np.array([ 
    ["аооа ааоо аааооо аоаоаоа влвлв лвлв ывы лдлд ывлд ывлддлвы"],
    ["фыва олдж фыва олдж фждылво фывждлоа фыжд ждфы пруфыыыыыыы"],
    ["чувак, ты так хорош, что я в твою честь назову страну, ей-богу"]
],
dtype=(np.unicode_, 16),order='C')
mistakes=0
def playy(real_filename,f):
    playsound.playsound(real_filename)
    while(f>0):
        time.sleep(1)
        f-=1

class AnotherWindow1(QWidget):
      global percentage
      def __init__(self):
        super().__init__()
        self.setWindowTitle("Another Window1")  # <2>
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.setMaximumWidth(1000)
        self.setMaximumHeight(1000)
        pagelayout=QVBoxLayout()
        btn=QPushButton("Lesson_first "+str(percentage[0])+" %")
        btn.pressed.connect(self.activate_lesson_first)
        pagelayout.addWidget(btn)
        btn2=QPushButton("Lesson_first "+str(percentage[1])+" %")
        btn2.pressed.connect(self.activate_lesson_second)
        pagelayout.addWidget(btn2)
        btn3=QPushButton("Lesson_third "+str(percentage[2])+" %")
        btn3.pressed.connect(self.activate_lesson_third)
        pagelayout.addWidget(btn3)
        self.setLayout(pagelayout)

      def activate_lesson_first(self):
        global course
        global percentage
        global file_contents
        global Text_variants
        global state
        state=Text_variants.First
        self.w = AnotherWindow2()
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()

      def activate_lesson_second(self):
        global course
        global percentage
        global file_contents
        global Text_variants
        global state
        state=Text_variants.Second
        self.w = AnotherWindow2()
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()
      def activate_lesson_third(self):
        global course
        global percentage
        global file_contents
        self.w = AnotherWindow2()
        global Text_variants
        global state
        state=Text_variants.Third
        self.w.setInputMethodHints
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()
keys = []
  
def on_press(key):
    keys.append(key)
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
                     
    print('{0} released'.format(key))
    if key == Key.esc:
        # Stop listener
        return False
class AnotherWindow2(QWidget):
      def __init__(self):
        super().__init__()
        global state
        global file_contents
        global course
        global mistakes
        global keys
        self.setWindowTitle("Tempts")  # <2>
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.setMaximumWidth(1000)
        self.setMaximumHeight(1000)
        pagelayout=QVBoxLayout()
        if(state.value==5):
            mes=QMessageBox.information(
            self,
            "Warning",
            "GET U'R FILE via ctrl+p",
            buttons=QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.Yes
            )
        else:
            file_contents=course[state.value-1][0]
        input_for_prepared=QLineEdit(file_contents)
        pagelayout.addWidget(input_for_prepared)
        input_for_unprepared=QLineEdit()
        pagelayout.addWidget(input_for_unprepared)
        self.setLayout(pagelayout)
        index=0
        bound=len(input_for_prepared.text())
        while(len(input_for_unprepared.text())!=bound):
            #with Listener(on_press = on_press,
             # on_release = on_release) as listener:
                  #   listener.join()
            tmp_str=input_for_prepared.text()
            str_preparation="\033[0;37;40m{tmp_str[0:index]}"
            str_preparation+="\033[1;33;40m {tmp_str[index]}"
            str_preparation+="\033[0;37;40m{tmp_str[index:bound]}"
            input_for_prepared.setText(str_preparation)

            if(keys[index]!=tmp_str[index] and keys[index]!='a'):
                mistakes+=1
            

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ket-Trenazhyor")
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.setMaximumWidth(1000)
        self.setMaximumHeight(1000)
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        button_action = QAction(QIcon(os.path.join(basedir, "disk-share.png")),"To get your file",self)
        button_action.setStatusTip("To get your file")
        button_action.triggered.connect(self.onMyToolBarButton1Click)
        button_action.setShortcut(QKeySequence("Ctrl+p"))
        button_action.setCheckable(False)
        toolbar.addAction(button_action)
        button_action2 = QAction(QIcon(os.path.join(basedir, "disk.png")),"To save your file",self,)
        button_action2.setStatusTip("To save your file")
        button_action2.triggered.connect(self.onMyToolBarButton2Click)
        button_action2.setShortcut(QKeySequence("Ctrl+l"))
        button_action2.setCheckable(False)
        toolbar.addAction(button_action2)
        toolbar.addSeparator()
        button_action3 = QAction(QIcon(os.path.join(basedir, "folder.png")),"To choose your dir",self,)
        button_action3.setStatusTip("To choose your dir")
        button_action3.triggered.connect(self.onMyToolBarButton3Click)
        button_action3.setShortcut(QKeySequence("Ctrl+m"))
        button_action3.setCheckable(False)
        toolbar.addAction(button_action3)
        toolbar.addSeparator()
        button_action4 = QAction(QIcon(os.path.join(basedir, "bug.png")),"extraordinary",self,)
        button_action4.setStatusTip("extraordinary")
        button_action4.triggered.connect(self.onMyToolBarButton1Click)
        button_action4.setShortcut(QKeySequence("Ctrl+a"))
        button_action4.setCheckable(False)
        toolbar.addAction(button_action4)
        toolbar.addSeparator()
        button_action5 = QAction(QIcon(os.path.join(basedir, "music.png")),"extraordinary",self,)
        button_action5.setStatusTip("kaiff")
        button_action5.triggered.connect(self.onMyToolBarButton1Click)
        button_action5.setShortcut(QKeySequence("Ctrl+w"))
        button_action5.setCheckable(False)
        toolbar.addAction(button_action5)
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu2 = menu.addMenu("Folder")
        file_submenu = file_menu.addMenu("Get file")
        #file_menu.setStyleSheet("font-size: 10px; width: 120px; padding: 0px; text-align: start;")
        file_submenu.addAction(button_action)
        file_submenu2= file_menu.addMenu("Save file")
        file_submenu2.addAction(button_action2)
        file_submenu3=file_menu2.addMenu("Choose repos")
        file_submenu3.addAction(button_action3)
        pagelayout=QVBoxLayout()
        layout = QHBoxLayout()
        btn=QPushButton("Course")
        btn.pressed.connect(self.activate_tab_1)
        layout.addWidget(btn)
        btn2=QPushButton("Your own")
        btn2.pressed.connect(self.activate_tab_2)
        layout.addWidget(btn2)
        pagelayout.addLayout(layout)
        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)



    def onMyToolBarButton1Click(self):
        global file_contents
        caption = ""  # Empty uses default caption.
        initial_dir = ""  # Empty uses current folder.
        initial_filter = FILE_FILTERS[3]  # Select one from the list.
        filters = ";;".join(FILE_FILTERS)
        print("Filters are:", filters)
        print("Initial filter:", initial_filter)

        filename, selected_filter = QFileDialog.getOpenFileName(
            self,
            caption=caption,
            directory=initial_dir,
            filter=filters,
            initialFilter=initial_filter,
        )
        print("Result:", filename, selected_filter)
        # tag::get_filename[]
        if(selected_filter!=FILE_FILTERS[0] and selected_filter!=FILE_FILTERS[4]):
         if filename:
            with codecs.open(filename, "rb","utf-8") as f:
                file_contents = f.read()
                print(file_contents)
        if(selected_filter==FILE_FILTERS[4]):
           if filename:
             filename2=filename.split('/')
             real_filename=filename2[len(filename2)-1]
             f = MP3(real_filename)
             f=f.info.length
             f-=1
             f=math.floor(f)
             P = Thread(name="playsound",target=playy,args=(real_filename,f)).start()  
        #if(selected_filter==FILE_FILTERS[0]):
           # if filename:
           #  filename=filename.split('/')
            # real_filename=filename[len(filename)-1]
            # self.label.setPixmap(QPixmap(os.path.join(basedir,real_filename)))
          #   self.label.setScaledContents(True)


    def onMyToolBarButton2Click(self):
        global file_contents
        caption = ""  # Empty uses default caption.
        initial_dir = ""  # Empty uses current folder.
        initial_filter = FILE_FILTERS[2]  # Select one from the list.
        filters = ";;".join(FILE_FILTERS)
        print("Filters are:", filters)
        print("Initial filter:", initial_filter)

        filename, selected_filter = QFileDialog.getSaveFileName(
            self,
            caption=caption,
            directory=initial_dir,
            filter=filters,
            initialFilter=initial_filter,
        )
        print("Result:", filename, selected_filter)
        # tag::get_save_filename[]
        if filename:
            if os.path.exists(filename):
                # Existing file, ask the user for confirmation.
                write_confirmed = QMessageBox.question(
                    self,
                    "Overwrite file?",
                    f"The file {filename} exists. Are you sure you want to overwrite it?",
                )
            else:
                # File does not exist, always-confirmed.
                write_confirmed = True

            if write_confirmed:
                with codecs.open(filename, "w","utf-8") as f:
                    f.write(file_contents)
        # end::get_save_filename[]
    def onMyToolBarButton3Click(self):
        caption = ""  # Empty uses default caption.
        initial_dir = ""  # Empty uses current folder.
        folder_path = QFileDialog.getExistingDirectory(
            self,
            caption=caption,
            directory=initial_dir,
        )
        print("Result:", folder_path)

        
    def activate_tab_1(self): #если ему нужны уроки
        self.w = AnotherWindow1()
        if self.w.isVisible():
            self.w.hide()

        else:
            self.w.show()
    def activate_tab_2(self): #если он хочет свое загрузить
        global Text_variants
        global state
        state=Text_variants.Unique
        self.w = AnotherWindow2()
        if self.w.isVisible():
            self.w.hide()

        else:
            self.w.show()
app = QApplication(sys.argv)
app.setStyle('Fusion')
window = MainWindow()
window.show()

app.exec()


