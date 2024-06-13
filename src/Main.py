import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Interface.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    main_window.show()
    
    app.exec()