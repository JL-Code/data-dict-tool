import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import untitled

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainW = QMainWindow()
    ui = untitled.UIMainWindow()
    ui.setup(mainW)

    mainW.show()

    sys.exit(app.exec_())
