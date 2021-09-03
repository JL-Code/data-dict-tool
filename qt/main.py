import sys
import pkg_resources
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

# 参考：https://www.bilibili.com/video/BV1wZ4y1G7Ur?from=search&seid=10558608980613499134&spm_id_from=333.337.0.0
# https://github.com/horychen/emachinery/tree/pypi-tut-video

class CustomWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        path = "ui/uic_load.ui"
        filepath = pkg_resources.resource_filename(__name__, path)
        try:
            self.ui = loadUi(filepath, self)
        except ModuleNotFoundError as e:
            print(str(e))
        except Exception as e:
            raise e

        self.ui.pushButton.setText("按钮")
        self.setWindowTitle("标题：UIC")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomWidget()
    window.show()
    sys.exit(app.exec_())
