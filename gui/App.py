from PySide2.QtWidgets import QMainWindow

from gui.AppTabWidget import AppTabWidget


class App(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Rating Generator')
        self.setCentralWidget(AppTabWidget(self))
        self.setGeometry(100, 100, 800, 800)

        self.show()
