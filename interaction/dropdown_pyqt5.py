import sys
import time
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.centralwidget = QWidget(self)
        self.gridlayout = QGridLayout(self.centralwidget)
        # x, y, w, h
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT5 drop down menu demo")

        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip('Leave The App')
        exitAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Fruit')
        fileMenu.addAction(exitAction)

        self.home()

    def home(self):
        btn = QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.minimumSizeHint())

        extractAction = QAction('Flee the Scene', self)
        extractAction.triggered.connect(self.close_application)

        self.toolBar = self.addToolBar("Exit application")
        self.toolBar.addAction(extractAction)

        checkBox = QCheckBox('Enlarge Window', self)
        checkBox.stateChanged.connect(self.enlarge_window)

        self.progress = QProgressBar(self)

        self.btn = QPushButton("Download",self)
        self.btn.clicked.connect(self.download)

        self.fruitChoice = QLabel("Current fruit: Pear", self)

        dropdown = QComboBox(self)
        dropdown.addItem("Pear")
        dropdown.addItem("Apple")
        dropdown.addItem("Banana")
        dropdown.addItem("Grape")
        dropdown.addItem("Blueberry")
        dropdown.addItem("Strawberry")

        dropdown.activated[str].connect(self.fruit_choice)

        # pack everything in a grid layout for convenience
        self.gridlayout.addWidget(checkBox, 0, 0, 1, 2)
        self.gridlayout.addWidget(QLabel('Progress'), 0, 2, 1, 1)
        self.gridlayout.addWidget(self.progress, 1, 2, 1, 4)
        self.gridlayout.addWidget(self.btn, 2, 2, 1, 1)
        self.gridlayout.addWidget(self.fruitChoice, 3, 1, 1, 2)
        self.gridlayout.addWidget(dropdown, 4, 1, 1, 1)

        self.setCentralWidget(self.centralwidget)

        self.show()


    def fruit_choice(self, text):
        self.fruitChoice.setText('Current fruit: ' + text)


    def download(self):
        self.completed = 0

        while self.completed < 100:
            self.completed += 0.001
            self.progress.setValue(int(self.completed))
            QApplication.processEvents()



    def enlarge_window(self, state):
        if state == Qt.Checked:
            self.setGeometry(50,50, 1000, 600)
        else:
            self.setGeometry(50, 50, 500, 300)


    def close_application(self):
        choice = QMessageBox.question(self, 'Close Application',
                                            "You sure?",
                                            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Leaving now")
            sys.exit()
        else:
            pass



def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()
