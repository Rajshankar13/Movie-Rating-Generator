import sys

from PySide2.QtWidgets import QApplication, QMessageBox

from gui.App import App

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
