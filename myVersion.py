import sys
import os
import time
import codecs
import math
import numpy as np
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon,QKeySequence
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
    QTextEdit
)
import playsound
from threading import Thread
from mutagen.mp3 import MP3
import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import (
  NavigationToolbar2QT as NavigationToolbar,
)
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
course_percentage=[0.0,0.0,0.0]
custom_percentage=[]
Text_variants=Enum('Lesson',['First','Second','Third','No','Unique'])
state=Text_variants.No
#типо курсы, индекс массива+1=соответсвующий урок
course=np.array([ 
    ["аооа ааоо аааооо аоаоаоа влвлв лвлв ывы лдлд ывлд ывлддлвы"],
    ["фыва олдж фыва олдж фждылво фывждлоа фыжд ждфы пруфыыыыыыы"],
    ["чувак, ты так хорош, что я в твою честь назову страну, ей-богу"]
],
dtype=(np.unicode_, 58),order='C') #здесь число - количество символов юникода, что показаны будут
mistakes=0 #переменная для подсчета неправильно введенных символов
index=0 #индекс для массива символов неизменяемой строки
jndex=-1 #индекс для массива символов изменяемой строки
size=0 #переменная, дубликат для размера изменяемой строки. Если ошибся,стер, то стирание не засчитывается
symb_per_min=[] #массив для символов в мин
words_per_min=[] #массив для слов в мин
initial_time=0 #для начального времени
n_words=0 #количество слов
n_symb=0 #количество символов
elapsed_timer_per_iter=0 #время за итерацию
keys = [] #массив нажатых символов
tim=0.0 #общее время, нужно для оси абсцисс
def playy(real_filename,f): #функция для потока, который отрубается после проигрывания почти всего трека
    playsound.playsound(real_filename)
    while(f>0):
        time.sleep(1)
        f-=1

class AnotherWindow1(QWidget): #класс-окно выбор курса
      global course_percentagepercentage
      def __init__(self):
        super().__init__()
        self.setWindowTitle("Another Window1")
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.setMaximumWidth(1000)
        self.setMaximumHeight(1000)
        pagelayout=QVBoxLayout() #добавляем верт. раскладку
        btn=QPushButton("Lesson_first "+str(course_percentage[0])+" %")#тут бы процентики обновлялись чтоб-todo
        btn.pressed.connect(self.activate_lesson_first) #соединяем нажатие кнопки с функцией
        pagelayout.addWidget(btn) #добавляем виджет в раскладку
        btn2=QPushButton("Lesson_second "+str(course_percentage[1])+" %")
        btn2.pressed.connect(self.activate_lesson_second)
        pagelayout.addWidget(btn2)
        btn3=QPushButton("Lesson_third "+str(course_percentage[2])+" %")
        btn3.pressed.connect(self.activate_lesson_third)
        pagelayout.addWidget(btn3)
        btn4=QPushButton("end")
        btn4.pressed.connect(self.to_exit)
        pagelayout.addWidget(btn4)
        self.setLayout(pagelayout)
      def to_exit(self): #функция для закрытия окна
         self.deleteLater()

      def activate_lesson_first(self):
        global course
        global percentage
        global file_contents
        global Text_variants
        global state
        state=Text_variants.First
        self.w = AnotherWindow2()
        if self.w.isVisible(): #проверка и динамическое открытие/закрытие окна.
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
        global Text_variants
        global state
        state=Text_variants.Third
        self.w = AnotherWindow2()
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()
class AnotherWindow2(QWidget): #окно для ввода текста. 
      def __init__(self):
        super().__init__()
        global state
        global file_contents
        global course
        global mistakes
        global keys
        global initial_time
        self.setWindowTitle("Tempts")
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.setMaximumWidth(1000)
        self.setMaximumHeight(1000)
        pagelayout=QVBoxLayout()
        if(state.value==4): #если состояние=значению нет,те юзер не загрузил текст/зашел с окно уроков
            mes=QMessageBox.information( #то вылезет оповещение, за которым закроется спустя время окно
            self,
            "Warning",
            "GET U'R FILE via ctrl+p",
            buttons=QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.Yes
            )
            self.deleteLater() #hz
        elif(state.value!=5): #если не unique-для своего текста и не базовое, то подгружаем уроки
            file_contents=course[state.value-1][0]
        if(state.value!=4): #хз, почему, но при втором выборе загрузки своего текста окно быстро не удаляется->костыль
         self.input_for_prepared=QTextEdit(file_contents) #здесь надо сделать выделение текущего символа
         pagelayout.addWidget(self.input_for_prepared)
         self.input_for_unprepared=QTextEdit()
         pagelayout.addWidget(self.input_for_unprepared)
         btn=QPushButton("To end suffer")
         btn.pressed.connect(self.activate_math) #закрывающая кнопка и подсчитывающая статистику
         pagelayout.addWidget(btn)
         self.setLayout(pagelayout)
         self.input_for_unprepared.textChanged.connect(self.key_logger) #если изменяется текст, то фун. считает символ
         initial_time=time.time() #ставим изначальное время работы

      def key_logger(self): #логика работы:пока все символы не будет введены правильно
          global mistakes #если больше, то ошибка
          global keys     #если меньше, то когда как
          global index    #добавить бы подсчет верных слов+подчеркивание символа
          global jndex    #если встречен неправильный символ, то он заносится в keys
          global size     #а его время суммируется к последнему правильному символу-если это не особый случай с 1м неверным символом
          global elapsed_timer_per_iter
          global symb_per_min
          global initial_time
          flag=False
          fin_str=self.input_for_prepared.toPlainText() #извлекаем строку типа QString
          tmp_str=self.input_for_unprepared.toPlainText()
          elapsed_timer_per_iter=time.time()-initial_time-elapsed_timer_per_iter #время на символ
          elapsed_timer_per_iter/=10 #получаем секунды
          bound=len(tmp_str) #для кого нужен size из начала
          if(bound!=0): #при удалении первого неверного символа bound=0
           keys.append(tmp_str[bound-1]) #добавляем символ и индекс для его извлечения
           jndex+=1                     #из keys
           if bound==1:size=1  #костыль на случай удаления первого символа
           if(bound>=size): #добавили новый символ
              if(keys[jndex]!=fin_str[index]):
                  mistakes+=1
                  if(len(symb_per_min)==0): #для случая с первым неправильны символом
                       if(keys[jndex]!=' '):
                        symb_per_min.append(elapsed_timer_per_iter)
                        flag=True
                  else:
                      symb_per_min[len(symb_per_min)-1]+=elapsed_timer_per_iter
              else:
                  if(not(flag)):
                     if(keys[jndex]!=' '):
                        symb_per_min.append(elapsed_timer_per_iter)
                  else:
                     symb_per_min[len(symb_per_min)-1]+=elapsed_timer_per_iter
                     flag=False
                  index+=1
          elif(size!=0): #добавляем пробелы, что уберет split
            keys.append(' ')
            jndex+=1   
          size=bound
      def activate_math(self): #логика работы схожа с zip(), но если встречено ошибочное слово, то 
          global mistakes      #мы его не учитываем
          global keys          #если из-за ошибочных слов список введенных слов больше
          global words_per_min #то исходя из количества ошибок досматриваем последние n(кол-во ошибок) слова
          global course_percentage #далее узнаем список длины слов в исходной строке
          global custom_percentage #и находим приблизительное времена на эти слова
          global state             #эти времена сохраняем, формируем список слов в мин
          global Text_variants     #также формируем список символов в мин
          global symb_per_min      #в зависимости от урока сохраняем процент
          global n_words           #обнуляем все данные для прохождения след урока и удаляем окно
          global n_symb
          global tim
          global file_contents
          global index
          global jndex
          global initial_time
          global size
          global elapsed_timer_per_iter
          tmp_str=self.input_for_prepared.toPlainText().split()
          tmp_words=""
          n_word=0
          tmp_words=tmp_words.join(keys).split()
          for i in range(0,len( tmp_str)):
              for j in range(0,len(tmp_str)):
                  if(tmp_words[i]==tmp_str[j]):
                     n_word+=1
                     break
          w_border=0
          if(len(tmp_words)>len(tmp_str)):
              w_border=len(tmp_words)-len(tmp_str)
              for i in range(len( tmp_str),len(tmp_words)):
                 for j in range(len(tmp_str)-w_border,len(tmp_str)):
                   if(tmp_words[i]==tmp_str[j]):
                     n_word+=1
                     break
          len_list=[len(s) for s in tmp_str]
          j_index=0
          for k in len_list:
              fef=0
              for f in range(j_index,j_index+k):
                  fef+=symb_per_min[f]
              words_per_min.append(60/fef)
              j_index=k
          if(state==Text_variants.Unique):
              custom_percentage.append((n_word/len(tmp_words)*100))
          else:
              course_percentage[state.value-1]=(n_word/len(tmp_words)*100)
          for i in range(0,len(symb_per_min)):
             tim+=symb_per_min[i]
             symb_per_min[i]=60/symb_per_min[i]
          n_words=len(words_per_min)
          n_symb=len(symb_per_min)
          state=Text_variants.No
          keys=[]
          file_contents=[]
          mistakes=0
          jndex=-1
          index=0
          size=0
          initial_time=0
          elapsed_timer_per_iter=0
          self.deleteLater()
          
            
class MplCanvas(FigureCanvasQTAgg):
  def __init__(self, parent=None, width=5, height=5, dpi=100):
   fig = Figure(figsize=(width, height), dpi=dpi)
   self.axes = fig.add_subplot(111)
   super().__init__(fig)

class AnotherWindow3(QWidget):
   def __init__(self):
        super().__init__()
        global words_per_min
        global symb_per_min
        global n_words
        global n_symb
        global tim
        sc = MplCanvas(self, width= 5, height=5, dpi=100)
        sc.axes.plot(np.linspace(0,tim,n_words), words_per_min)
        sc.axes.set_xlabel("Time in sec",loc='left',va="baseline") #va может по-разному работать на устройствах
        sc.axes.set_ylabel("Words per minute")                     #мне он надпись поднимает до оси абсцисс
        sc2 = MplCanvas(self, width=5, height=5, dpi=100)
        sc2.axes.plot(np.linspace(0,tim,n_symb), symb_per_min)
        sc2.axes.set_xlabel("Time in sec",loc='left',va="baseline")
        sc2.axes.set_ylabel("Symbols per minute")
        layout = QVBoxLayout() # Create toolbar, passing canvas as first parameter, parent(self, the MainWindow) as second.
        layout.addWidget(sc)
        layout.addWidget(sc2)
        self.setLayout(layout) # Create a placeholder widget to hold our toolbar and canvas.
        tim=0.0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ket-Trenazhyor")
        self.setMinimumWidth(400)    #мин и макс длину и высоту задаем
        self.setMinimumHeight(400)
        self.setMaximumWidth(1000)
        self.setMaximumHeight(1000)
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar) #создаем навигационную панель                                          поместите иконку в директорию с проггой!
        button_action = QAction(QIcon(os.path.join(basedir, "disk-share.png")),"To get your file",self) #создаем кнопку, подхватили иконку
        button_action.setStatusTip("To get your file") #создали подсказку
        button_action.triggered.connect(self.onMyToolBarButton1Click)  #законнектили на воздействия кнопку
        button_action.setShortcut(QKeySequence("Ctrl+p")) #задали шорткат и сделали подсказку по нему
        button_action.setCheckable(False)
        toolbar.addAction(button_action)  #добавили воздействие на кнопку через нав.панель
        button_action2 = QAction(QIcon(os.path.join(basedir, "disk.png")),"To save your file",self,)
        button_action2.setStatusTip("To save your file")
        button_action2.triggered.connect(self.onMyToolBarButton2Click)
        button_action2.setShortcut(QKeySequence("Ctrl+l"))
        button_action2.setCheckable(False) #добавляем кнопке сигнал, нажата ли
        toolbar.addAction(button_action2)
        toolbar.addSeparator() #добавили линию |
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
        menu = self.menuBar() #сделали меню - далее добавили два компонента
        file_menu = menu.addMenu("File") 
        file_menu2 = menu.addMenu("Folder")
        file_submenu = file_menu.addMenu("Get file") #сделали подменю
        file_submenu.addAction(button_action) #связали к подменю кнопку
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
        stats_layout=QHBoxLayout()
        sbtn=QPushButton("1lesson stats")
        sbtn.pressed.connect(self.activate_stat)
        stats_layout.addWidget(sbtn)
        sbtn2=QPushButton("2 stats")
        sbtn2.pressed.connect(self.activate_stat2)
        stats_layout.addWidget(sbtn2)
        sbtn3=QPushButton("3lesson stats")
        sbtn3.pressed.connect(self.activate_stat3)
        stats_layout.addWidget(sbtn3)
        sbtnu=QPushButton("unique lesson stats")
        sbtnu.pressed.connect(self.activate_statu)
        stats_layout.addWidget(sbtnu)
        pagelayout.addLayout(stats_layout)
        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
    def onMyToolBarButton1Click(self):    #функция, подгружающая файлы
        global file_contents
        global state
        caption = ""  # Empty uses default caption.
        initial_dir = ""  # Empty uses current folder.
        initial_filter = FILE_FILTERS[3]  # Select one from the list.
        filters = ";;".join(FILE_FILTERS)
        print("Filters are:", filters)
        print("Initial filter:", initial_filter)
        #встроенный диалог для подгрузки файлов
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
            with codecs.open(filename, "rb","utf-8") as f:  #кодек нужен для расшифровки символа в нужной кодировке
                file_contents = f.read()                    #у меня это utf-8
                state=Text_variants.Unique                  #подгрузили .txt, урок свой готов->обновили статус
                print(file_contents)
        if(selected_filter==FILE_FILTERS[4]):  #для mp3
           if filename:
             filename2=filename.split('/')     #из найденного пути mp3 выделяем лишь его имя
             real_filename=filename2[len(filename2)-1] #тк работает, если трек в директории с программой
             f = MP3(real_filename)  #это чтобы узнать длину трека в сек, реализация через mutagen
             f=f.info.length         #немного сокращаем длительность трека во избежание казусов
             f-=1
             f=math.floor(f)
             P = Thread(name="playsound",target=playy,args=(real_filename,f)).start() #запускаем поток
    def onMyToolBarButton2Click(self):   #бутафорская функция по сохранению в файл
        global file_contents             #оставил, вдруг пригодится
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
        if filename:
            if os.path.exists(filename):
                write_confirmed = QMessageBox.question(
                    self,
                    "Overwrite file?",
                    f"The file {filename} exists. Are you sure you want to overwrite it?",
                )
            else:
                write_confirmed = True
            if write_confirmed:
                with codecs.open(filename, "w","utf-8") as f:
                    f.write(file_contents)
    def onMyToolBarButton3Click(self):        #бутафорская функция по определению выбранного пути, вдруг пригодится
        caption = ""  # Empty uses default caption.
        initial_dir = ""  # Empty uses current folder.
        folder_path = QFileDialog.getExistingDirectory(
            self,
            caption=caption,
            directory=initial_dir,
        )
        print("Result:", folder_path)
    def activate_tab_1(self): #если ему нужны уроки
        self.w = AnotherWindow1() #подгружаем страничку с уроками
        if self.w.isVisible():
            self.w.hide()

        else:
            self.w.show()
    def activate_tab_2(self): #если он хочет свое загрузить, подгружаем окно с полями текста, см.выше класс AnotherWindow2
        self.w = AnotherWindow2()
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()

    def activate_stat(self):          #логика работы последних четырех функций:
       global course_percentage       #если не найдены данные о прохождении урока 1/2/3/своего
       if(course_percentage[0]==0.0): #то вылезает окно,оповещающее об этом, иначе подгружаем класс AnotherWindow3
         mes=QMessageBox.critical(    #этот класс уже работает с графиками
            self, 
            "Stats not found",
            "Go&study 1st lesson",
            buttons=QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.Yes
            )
       else:
          self.g = AnotherWindow3()
          if self.g.isVisible():
             self.g.hide()
          else:
             self.g.show()
    def activate_stat2(self):
       global course_percentage
       if(course_percentage[1]==0.0):
         mes=QMessageBox.critical(
            self,
            "Stats not found",
            "Go&study 2nd lesson",
            buttons=QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.Yes
            )
       else:
          self.g = AnotherWindow3()
          if self.g.isVisible():
             self.g.hide()
          else:
             self.g.show()
    def activate_stat3(self):
       global course_percentage
       if(course_percentage[2]==0.0):
         mes=QMessageBox.critical(
            self,
            "Stats not found",
            "Go&study 3rd lesson",
            buttons=QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.Yes
            )
       else:
          self.g = AnotherWindow3()
          if self.g.isVisible():
             self.g.hide()
          else:
             self.g.show()
    def activate_statu(self):
       global custom_percentage
       if(len(custom_percentage)==0):
          mes=QMessageBox.critical(
            self,
            "Stats not found",
            "Go&study unique lesson",
            buttons=QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.Yes
            )
       else:
          self.g = AnotherWindow3()
          if self.g.isVisible():
             self.g.hide()
          else:
             self.g.show()
app = QApplication(sys.argv) #для приема аргументов с устройств ввода-вывода
app.setStyle('Fusion')  #стиль для всех компонент готовый
window = MainWindow()   #создание главного окна
window.show()           #показываем главное окно

app.exec()              #запускаем программу


