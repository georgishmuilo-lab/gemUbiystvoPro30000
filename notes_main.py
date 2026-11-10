from PyQt5.QtWidgets import (QInputDialog, QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QListWidget)
import json

notes = {}

app = QApplication([])
main_win = QWidget()

TEXT = QTextEdit()
text = QLineEdit()
text.setPlaceholderText('Введите тег...')
text1 = QLabel('Список заметок')
text2 = QLabel('Список тегов')

list_notes = QListWidget()
list_tags = QListWidget()

btn_save = QPushButton('Сохранить заметку')
btn_add = QPushButton('Добавить заметку')
btn_delete = QPushButton('Удалить заметку')
btn_pin = QPushButton("Закрепить тег")
btn_unpin = QPushButton("Открепить тег")
btn_search = QPushButton("Найти тег")

line1 = QHBoxLayout()
line2 = QHBoxLayout()
col = QVBoxLayout()
main = QHBoxLayout()

line1.addWidget(btn_add)
line1.addWidget(btn_delete)

line2.addWidget(btn_pin)
line2.addWidget(btn_unpin)

col.addWidget(text1)
col.addWidget(list_notes)
col.addLayout(line1)
col.addWidget(btn_save)
col.addWidget(text2)
col.addWidget(list_tags)
col.addWidget(text)
col.addLayout(line2)
col.addWidget(btn_search)

main.addWidget(TEXT, 3)
main.addLayout(col, 2)
main_win.setLayout(main)

def show_note():
    name = list_notes.selectedItems()[0].text()
    TEXT.clear()
    TEXT.setText(notes[name]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[name]["теги"])

def add_note():
    note_name, ok = QInputDialog.getText(list_notes, 'Добавь заметку', 'Имя заметки')
    if ok and note_name != '':
        notes[note_name] = {'текст':'', 'теги':[]}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])

def del_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        del notes[name]
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w', encoding = 'utf-8') as file:
            json.dump(notes, file, ensure_ascii = False, indent = 2)
    else:
        pass

def save_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        notes[name]['текст'] = TEXT.toPlainText()
        with open('notes_data.json', 'w', encoding = 'utf-8') as file:
            json.dump(notes, file, ensure_ascii = False, indent = 2)
    else:
        pass

def add_tag():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        tag = text.text()
        if not tag in notes[name]['теги'] and tag != '':
            notes[name]['теги'].append(tag)
            text.clear()
            with open("notes_data.json", "w", encoding='utf-8') as file:
                json.dump(notes, file, ensure_ascii=False, indent=2)

def del_tag():
    if list_tags.selectedItems():
        name = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[name]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[name]['теги'])
        with open("notes_data.json", "w", encoding='utf-8') as file:
            json.dump(notes, file, ensure_ascii=False, indent=2)

def search_tag():
    tag = text.text()
    if btn_search.text() == "Найти тег" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        btn_search.setText("Сбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif btn_search.text() == "Сбросить поиск":
        text.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        btn_search.setText("Найти тег")

list_notes.itemClicked.connect(show_note)
btn_add.clicked.connect(add_note)
btn_delete.clicked.connect(del_note)
btn_save.clicked.connect(save_note)
btn_pin.clicked.connect(add_tag)
btn_unpin.clicked.connect(del_tag)
btn_search.clicked.connect(search_tag)

with open('notes_data.json', 'r', encoding = 'utf-8') as file:
    notes = json.load(file)


list_notes.addItems(notes)
main_win.show()
app.exec_()