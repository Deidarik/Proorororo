import random
import time
import tkinter as tk  # для графического окна
import matplotlib.pyplot as plt

words_per_minute_per_second = []


def calculateTypingSpeedPerSecond(startTime, endTime, typedText):
    elapsedTime = endTime - startTime
    minutes = elapsedTime / 60
    wordsTyped = len(typedText.split())
    wordsInMinute = wordsTyped / minutes
    return wordsInMinute

def plotTypingSpeed(startTime, endTime, typedText):
    global words_per_minute_per_second
    words_per_minute_per_second = []  # Очищаем список перед новым рассчетом
    for i in range(int(startTime), int(endTime) + 1):  # Изменяем границы range
        wordsInMinute = calculateTypingSpeedPerSecond(startTime, i, typedText)
        words_per_minute_per_second.append(wordsInMinute)
        print(f"Время: {i - startTime} секунды, Слов в минуту: {wordsInMinute}")

    time_range = range(0, int(endTime - startTime) + 2)  # Изменяем границы range (+2 вместо +1)

    plt.figure(figsize=(10, 5))
    plt.plot(time_range, words_per_minute_per_second, marker='o')
    plt.title('Скорость набора текста в минуту')
    plt.xlabel('Время (секунды)')
    plt.ylabel('Слов в минуту')
    plt.grid(True)
    plt.show()

# функция generateRandomText генерирует случайный текст из списка слов указанной длины
def generateRandomText(length, word_list):
    return ' '.join(random.choice(wordList) for _ in range(length))

# функция calculateTypingSpeed вычисляет скорость печати по набранному тексту
def calculateTypingSpeed(startTime, endTime, typedText):
    elapsedTime = endTime - startTime
    minutes = elapsedTime / 60
    wordsTyped = len(typedText.split())
    wordsInMinute = wordsTyped / minutes
    return wordsInMinute

# функция startTyping вызывается при нажатии клавиши ввода
def startTyping(event):
    global startTime
    startTime = time.time()

# функция endTyping вызывается при завершении ввода
def endTyping(event):
    global startTime, finishPressed
    if finishPressed:
        endTime = time.time()

        typedText = entry.get()
        typedWords = typedText.split()
        totalErrors = 0

        for index, word in enumerate(typedWords):
            actualWord = textToType.split()[index]
            errors1 = abs(len(word) - len(actualWord))
            errors2 = sum(a != b for a, b in zip(textToType.split()[index], word))
            totalErrors = totalErrors + errors1 + errors2

        wordsInMinute = calculateTypingSpeed(startTime, endTime, typedText)

        resultLabel.config(text=f"Вы набрали текст со скоростью {wordsInMinute:.0f} знак. в минуту\nОбщее количество ошибок: {totalErrors}")
        # Отображаем график скорости набора текста
    plotTypingSpeed(startTime, endTime, typedText)

# функция finishTyping вызывается при нажатии кнопки "Завершить"
def finishTyping():
    global finishPressed
    finishPressed = True
    entry.unbind("<KeyPress>")  # отключение обработчика события нажатия клавиши
    entry.unbind("<KeyRelease>")  # отключение обработчика события отпускания клавиши
    endTyping(None)  # вызов функции завершения ввода


# список слов для генерации случайного текста
wordList = ["кот", "собака", "дом", "солнце", "вода"]

# генерация случайного текста
textToType = generateRandomText(5, wordList)

# создание главного окна
root = tk.Tk()
root.config(bg="black")  # установка черного фона главного окна
root.title("Тренажер быстрой печати")
root.geometry("650x400")

# создание метки с инструкцией
instructionLabel = tk.Label(root, text="Наберите этот текст в белом окне как можно быстрее и без ошибок:", font=("Arial", 14))
instructionLabel.config(fg="white", bg="black")  # установка белого текста и черного фона для метки с инструкцией
instructionLabel.pack(side=tk.TOP, padx=20, pady=10)

# создание метки с текстом для набора
textLabel = tk.Label(root, text=textToType, font=("Arial", 18, "bold"))
textLabel.config(fg="white", bg="black")  # установка белого текста и черного фона для метки с текстом для набора
textLabel.pack(padx=20, pady=10)

# создание поля ввода
entry = tk.Entry(root, font=("Arial", 16))
entry.config(fg="black", bg="white", width=30)  # установка черного текста и белого фона для поля ввода
entry.pack(padx=20, pady=10)
entry.bind("<KeyPress>", startTyping)  # привязка события нажатия клавиши к функции startTyping
entry.bind("<KeyRelease>", endTyping)  # привязка события отпускания клавиши к функции endTyping

# создание кнопки "Завершить"
finishButton = tk.Button(root, text="Завершить", font=("Arial", 14), command=finishTyping)
finishButton.pack(side=tk.BOTTOM, padx=20, pady=10)

# создание метки для отображения результата
resultLabel = tk.Label(root, text="", font=("Arial", 14))
resultLabel.config(fg="white", bg="black")  # установка белого текста и черного фона для метки с результатом
resultLabel.pack(padx=20, pady=10)
finishPressed = False  # флаг, указывающий, была ли нажата кнопка "Завершить"

# запуск главного цикла обработки событий
root.mainloop()