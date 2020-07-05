import sys
from win10toast import ToastNotifier
from datetime import datetime
from PyQt5.QtCore import QEvent, Qt, QTimer, QRegExp
from PyQt5.QtGui import QIcon, QFont, QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QLabel, QLineEdit, QGridLayout, QPushButton

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.icon = QIcon('C:\\Users\\ostyn\\PycharmProjects\\BirthdayReminder\\Images\\cake.png')
        self.title = 'Birthday Reminder'
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.background_color = 'background-color: #EFF0F1'
        self.grid = QGridLayout(self)
        self.init_ui()

# Minimizes to Tray
    def event(self, event):
        if event.type() == QEvent.WindowStateChange and self.isMinimized():
            self.setWindowFlags(self.windowFlags() & ~Qt.Tool)
            self.tray_icon.show()
            return True
        else:
            return super(Window, self).event(event)

# Opens window from Tray
    def restore_window(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.tray_icon.hide()
            self.showNormal()

# Checks if there is a birthday today
    def check_birthday(self):
        with open('birthday_info.txt', 'r') as dataFile:
            for line in dataFile:
                currentLine = line.rstrip()
                (data_first, data_last, data_month, data_day, data_year) = currentLine.split(',')

                if int(data_month) == datetime.now().month and int(data_day) == datetime.now().day:
                    age = datetime.now().year - int(data_year)
                    title = 'Happy Birthday!'
                    message = 'Today is ' + data_first + ' ' + data_last + "'s " + str(age) + ' Birthday!'
                    path = 'C:\\Users\\ostyn\\PycharmProjects\\BirthdayReminder\\Images\\cake.ico'
                    self.toaster.show_toast(title, message, threaded=True, icon_path=path, duration=8)

# Adds birthday to data
    def add_info(self, first, last, month, day, year):
        error_message = QLabel(self)
        error_message.setText('')
        error_message.setStyleSheet('color: red')
        error_message.setFont(QFont('Montserrat', 10, QFont.Bold))
        self.grid.addWidget(error_message, 4, 3)

        if first or last or month or day or year == '':
            error_message.setText('Missing Field')
            return

        conv_month = int(month)
        conv_day = int(day)
        conv_year = int(year)

# Checks if data is valid
        if conv_month not in range(1, 13):
            error_message.setText('Month not in range')
        elif conv_day not in range(1, 33):
            error_message.setText('Day not in range')
        elif conv_year not in range(datetime.now().year - 120, datetime.now().year):
            error_message.setText('Year not in range')
        else:
            # Checks if person already exists in data
            with open('birthday_info.txt', 'r') as dataFile:
                for line in dataFile:
                    currentLine = line.rstrip()
                    (data_first, data_last, data_month, data_day, data_year) = currentLine.split(',')
                    if first == data_first and last == data_last:
                        print('Person already exists in database')

            with open('birthday_info.txt', 'a') as dataFile:
                dataFile.write(first + ',' + last + ',' + month + ',' + day + ',' + year + '\n')
                error_message.setStyleSheet('color: blue')
                error_message.setText('Person Added!')

                # Reset Qlineedits after adding person
                self.get_first_name.setText('')
                self.get_last_name.setText('')
                self.get_month.setText('')
                self.get_day.setText('')
                self.get_year.setText('')

    def init_ui(self):
        self.toaster = ToastNotifier()
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setStyleSheet(self.background_color)

        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(QIcon(self.icon))
        self.setWindowIcon(QIcon(self.icon))

        # Restore the window when the tray icon is double clicked.
        self.tray_icon.activated.connect(self.restore_window)

        first_name = QLabel(self)
        first_name.setText('First Name: ')
        first_name.setFont(QFont('Montserrat', 10, QFont.Bold))

        self.get_first_name = QLineEdit(self)
        self.get_first_name.setStyleSheet('background-color: white')
        self.get_first_name.setValidator(QRegExpValidator(QRegExp("[a-z-A-Z_]+")))
        self.get_first_name.setMaxLength(15)
        self.get_first_name.setText('')

        last_name = QLabel(self)
        last_name.setText('Last Name: ')
        last_name.setFont(QFont('Montserrat', 10, QFont.Bold))

        self.get_last_name = QLineEdit(self)
        self.get_last_name.setStyleSheet('background-color: white')
        self.get_last_name.setValidator(QRegExpValidator(QRegExp("[a-z-A-Z_]+")))
        self.get_last_name.setMaxLength(15)
        self.get_last_name.setText('')

        birth_date = QLabel(self)
        birth_date.setText('Birth Date: \n(MM/DD/YYYY)')
        birth_date.setFont(QFont('Montserrat', 10, QFont.Bold))

        self.get_month = QLineEdit(self)
        self.get_month.setStyleSheet('background-color: white')
        self.get_month.setValidator(QIntValidator(1, 12))
        self.get_month.setText('')
        # get_month.setFixedWidth(60)

        self.get_day = QLineEdit(self)
        self.get_day.setStyleSheet('background-color: white')
        self.get_day.setValidator(QIntValidator(1, 32))
        self.get_day.setText('')

        self.get_year = QLineEdit(self)
        self.get_year.setStyleSheet('background-color: white')
        self.get_year.setValidator(QIntValidator(1900, 3000))
        self.get_year.setText('')

        slash_label1 = QLabel(self)
        slash_label1.setText('/')
        slash_label1.setFont(QFont('Montserrat', 10, QFont.Bold))

        slash_label2 = QLabel(self)
        slash_label2.setText('/')
        slash_label2.setFont(QFont('Montserrat', 10, QFont.Bold))

        add_button = QPushButton(self)
        add_button.setText('Add')
        add_button.setStyleSheet('background-color: #ECFEFF')
        add_button.clicked.connect(lambda: self.add_info(self.get_first_name.text().capitalize(),
                                                         self.get_last_name.text().capitalize(), self.get_month.text(),
                                                         self.get_day.text(), self.get_year.text()))

        show_button = QPushButton(self)
        show_button.setText('Data')
        show_button.setStyleSheet('background-color: #CEE9C8')
        show_button.clicked.connect(lambda: self.show_data())


        # Timer
        check_timer = QTimer(self)
        check_timer.timeout.connect(self.check_birthday)
        check_timer.start(18000000)
        self.check_birthday()

        # grid
        self.grid.addWidget(first_name, 0, 0)
        self.grid.addWidget(self.get_first_name, 0, 1)
        self.grid.addWidget(last_name, 1, 0)
        self.grid.addWidget(self.get_last_name, 1, 1)
        self.grid.addWidget(birth_date, 3, 0)
        self.grid.addWidget(self.get_month, 3, 1)
        self.grid.addWidget(slash_label1, 3, 2)
        self.grid.addWidget(self.get_day, 3, 3)
        self.grid.addWidget(slash_label2, 3, 4)
        self.grid.addWidget(self.get_year, 3, 5)
        self.grid.addWidget(add_button, 4, 1)
        self.grid.addWidget(show_button, 4, 0)
        self.setLayout(self.grid)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    program = Window()
    program.showMinimized()
    sys.exit(App.exec_())
