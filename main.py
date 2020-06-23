import sys
import time
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QStyle, QSystemTrayIcon, QDesktopWidget, QVBoxLayout, QLabel, \
    QInputDialog, QLineEdit, QHBoxLayout, QGridLayout, QPushButton


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.icon = QIcon('C:\\Users\\ostyn\\PycharmProjects\\BirthdayReminder\\Images\\cake.png')
        self.title = 'Birthday Reminder'
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.x = 23
        self.y = 20
        self.width = 20
        self.height = 20
        self.background_color = 'background-color: #EFF0F1'
        self.init_ui()


    def init_ui(self):

        def add_info(first, last, month, day, year):
            file = open('birthday_info.txt', 'a+')
            file.write(first + ', ' + last + ', ' + month + ', ' + day + ', ' + year)
            file.close()

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
        get_first_name = QLineEdit(self)
        get_first_name.setStyleSheet('background-color: white')
        name = get_first_name.text()

        last_name = QLabel(self)
        last_name.setText('Last Name: ')
        last_name.setFont(QFont('Montserrat', 10, QFont.Bold))
        get_last_name = QLineEdit(self)
        get_last_name.setStyleSheet('background-color: white')

        birth_date = QLabel(self)
        birth_date.setText('Birth Date: \n(MM/DD/YYYY)')
        birth_date.setFont(QFont('Montserrat', 10, QFont.Bold))
        get_month = QLineEdit(self)
        get_month.setStyleSheet('background-color: white')
        get_day = QLineEdit(self)
        get_day.setStyleSheet('background-color: white')
        get_year = QLineEdit(self)
        get_year.setStyleSheet('background-color: white')

        slash_label1 = QLabel(self)
        slash_label1.setText('/')
        slash_label1.setFont(QFont('Montserrat', 10, QFont.Bold))

        slash_label2 = QLabel(self)
        slash_label2.setText('/')
        slash_label2.setFont(QFont('Montserrat', 10, QFont.Bold))

        add_button = QPushButton(self)
        add_button.setText('Add')
        add_button.setStyleSheet('background-color: #E2FEFF')
        add_button.clicked.connect(add_info('h', 'g', 'g', 'g', 'g'))


        grid = QGridLayout(self)
        grid.addWidget(first_name, 0, 0)
        grid.addWidget(get_first_name, 0, 1)
        grid.addWidget(last_name, 1, 0)
        grid.addWidget(get_last_name, 1, 1)
        grid.addWidget(birth_date, 3, 0)
        grid.addWidget(get_month, 3, 1)
        grid.addWidget(slash_label1, 3, 2)
        grid.addWidget(get_day, 3, 3)
        grid.addWidget(slash_label2, 3, 4)
        grid.addWidget(get_year, 3, 5)
        grid.addWidget(add_button, 4, 1)
        self.setLayout(grid)


    def event(self, event):
        if event.type() == QEvent.WindowStateChange and self.isMinimized():
            self.setWindowFlags(self.windowFlags() & ~Qt.Tool)
            self.tray_icon.show()
            return True
        else:
            return super(Example, self).event(event)

    def restore_window(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.tray_icon.hide()
            self.showNormal()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()