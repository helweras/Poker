from Gui import GuiPoker
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication([])
    poker = GuiPoker()
    poker.show()
    app.exec_()