from StatRoom import Room
from Table import TableRabbit
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject, QPropertyAnimation, QPoint
from PyQt5.QtGui import QFont


class CardPushButton(QPushButton):
    def __init__(self, name, parent, card):
        super().__init__(name, parent)
        self.card = card



class MainPushButton(QPushButton):
    def __init__(self, name, parent, mast):
        super().__init__(name, parent)
        self.mast = mast


class GuiPoker(QWidget):
    def __init__(self):
        super().__init__()
        self.card_list = []
        self.button_list = []
        self.main_button_list = []
        self.anim_list = []
        self.setWindowTitle('Poker')
        self.setGeometry(100, 100, 800, 600)
        self.create_mast()
        self.create_main_button()
        self.create_card_btn()

    def create_mast(self):
        x = [(mast, nominal) for mast in range(4)
             for nominal in range(2, 15)]
        mast = []
        for card in x:
            mast.append(card)
            if card[-1] == 14:
                self.card_list.append(mast)
                mast = []

    def create_main_button(self):
        offset = 0
        font = QFont("Arial", 20)
        for i, name in enumerate(('♠', '♣', '♥', '♦')):
            main_btn = MainPushButton(name, self, i)
            main_btn.setGeometry(50 + offset, 10, 35, 60)
            main_btn.setFont(font)
            main_btn.setStyleSheet('padding: 20px, 10px')
            print(main_btn.mast)
            main_btn.clicked.connect(lambda :self.animation())
            self.main_button_list.append(main_btn)
            offset += 50

    def button_clicked(self):
        clicked_button = self.sender()  # <-- вот здесь
        print(f"Нажата кнопка с текстом: {clicked_button.text()}, {clicked_button.mast}")

    def create_card_btn(self):
        offset = 0
        for i, mast in enumerate(self.card_list):
            mast_list = []
            for card in mast:
                btn = CardPushButton(str(card[-1]), self, card)
                btn.setGeometry(50 + offset, 50, 35, 60)
                btn.hide()
                mast_list.append(btn)
            self.button_list.append(mast_list)
            offset += 100

    def animation(self):
        try:
            offset = QPoint(0, 35)
            clicked_button = self.sender()
            for count, btn_card in enumerate(self.button_list[clicked_button.mast]):
                strat_pos = self.main_button_list[i].pos()
                btn_card.show()
                anim = QPropertyAnimation(btn_card, b"pos", self)
                anim.setDuration(200)
                anim.setStartValue(strat_pos)
                anim.setEndValue(strat_pos + offset * (count + 1))
                anim.start()
                self.anim_list.append(anim)
        except Exception as e:
            print(e)

# class CardPushButton(QPushButton):
#     def __init__(self):
#         super().__init__()


app = QApplication([])
poker = GuiPoker()
poker.show()
app.exec_()
