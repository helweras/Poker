from turtledemo.penrose import start
from StatRoom import Room
from Table import TableRabbit
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QHBoxLayout, QFrame
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
        self.cards = []

    def get_card(self, card):
        self.cards.append(card)


class GuiPoker(QWidget):
    def __init__(self):
        super().__init__()
        # Списки одноименные с аргументами стола
        self.hand = []
        self.flop = []
        self.turn = []
        self.river = []

        self.table = TableRabbit()
        self.stat_room = None
        # колода в которой каждая масть это отдельный список карт
        self.card_list = self.create_mast()

        self.frame_list = []

        self.push_card_button = []

        self.button_card_list = []
        self.main_button_list = []
        self.anim_list = []
        self.setWindowTitle('Poker')
        self.setGeometry(100, 100, 800, 600)
        self.create_main_button()
        self.create_card_btn()
        self.create_hand_frame()
        self.create_frame_table()
        self.get_lime_frame()

    @staticmethod
    def create_mast():
        """Метод создает колоду в которой каждая масть это отдельный список карт"""
        return [[(mast, nominal) for nominal in range(2, 15)] for mast in range(4)]

    def create_main_button(self):
        """Метод создает 4 основные кнопки с названием мастей и располагает их на экране"""
        offset = 0
        font = QFont("Arial", 20)
        for i, name in enumerate(('♠', '♣', '♥', '♦')):
            main_btn = MainPushButton(name, self, i)
            main_btn.setGeometry(50 + offset, 10, 35, 60)
            main_btn.setFont(font)
            main_btn.setStyleSheet('padding: 20px, 10px')
            main_btn.setChecked(False)
            main_btn.clicked.connect(self.open_close)
            self.main_button_list.append(main_btn)
            offset += 50

    def create_card_btn(self):
        """Метод создает кнопки карт"""
        for i, mast in enumerate(self.card_list):
            for card in mast:
                btn = CardPushButton(str(card[-1]), self, card)
                btn.setCheckable(False)
                btn.setGeometry(50, 50, 36, 60)
                btn.clicked.connect(self.draw_card)
                btn.hide()
                main_button = self.main_button_list[i]
                main_button.get_card(btn)
                self.button_card_list.append(btn)

    def draw_card(self):
        """Метод для добавляет card нажатой кнопки поочередно в:
        self.hand
        self.flop
        self.turn
        self.river
        Деактивирует нажатые кнопки, после добавления ривера блокирует все кнопки карт"""
        clicked_button = self.sender()
        clicked_button.hide()
        add_list = self.hand
        if len(self.hand) == 2:
            add_list = self.flop
        if len(self.flop) == 3:
            add_list = self.turn
        if self.turn:
            add_list = self.river
            for card in self.button_card_list:
                card.setEnabled(False)
        add_list.append(clicked_button.card)
        self.push_card_button.append(clicked_button)
        count = len(self.push_card_button)
        self.get_lime_frame(count)


    def create_hand_frame(self):
        offset = 0
        for i in range(2):
            frame = QFrame(self)
            frame.setGeometry(350 + offset, 50, 36, 60)
            frame.setFrameShape(QFrame.Box)
            frame.setStyleSheet("background-color: transparent; border: 2px solid #000000;")
            offset += 50
            self.frame_list.append(frame)

    def create_frame_table(self):
        offset = 0
        for i in range(5):
            frame = QFrame(self)
            frame.setGeometry(275 + offset, 130, 36, 60)
            frame.setFrameShape(QFrame.Box)
            frame.setStyleSheet("background-color: transparent; border: 2px solid #000000;")
            offset += 50
            self.frame_list.append(frame)

    def get_lime_frame(self, count=0):
        try:
            if count == 7:
                self.frame_list[count - 1].setStyleSheet("background-color: transparent; border: 2px solid #000000;")

                return
            frame = self.frame_list[count]
            frame.setStyleSheet("background-color: transparent; border: 3px solid #00FF00;")
            if count >= 1:
                self.frame_list[count-1].setStyleSheet("background-color: transparent; border: 2px solid #000000;")
        except Exception as e:
            print(e)

    def open_close(self):
        """Метод вызывает анимацию раскрытия и скрыия карт  в зависимости от состояния кнопки масти"""
        try:
            clicked_button = self.sender()
            flag = clicked_button.isChecked()
            if flag:
                self.animation_close(clicked_button)
            else:
                self.animation_open(clicked_button)
        except Exception as e:
            print(e)

    def animation_open(self, clicked: MainPushButton):
        """Метод анимации раскрытия кнопок карт"""
        try:
            offset = QPoint(0, 35)
            clicked_button = clicked
            clicked_button.setCheckable(True)
            clicked_button.lower()
            for count, btn_card in enumerate(clicked_button.cards):
                strat_pos = clicked_button.pos()
                btn_card.show()
                anim = QPropertyAnimation(btn_card, b"pos", self)
                anim.setDuration(200)
                anim.setStartValue(strat_pos)
                anim.setEndValue(strat_pos + offset * (count + 1))
                anim.start()
                self.anim_list.append(anim)
        except Exception as e:
            print(e)

    def animation_close(self, clicked: MainPushButton):
        """Метод анимации закрытия карт кнопок"""
        try:
            clicked_button = clicked
            clicked_button.setCheckable(False)
            for count, btn_card in enumerate(clicked_button.cards):
                start_pos = btn_card.pos()
                end_pos = clicked_button.pos()
                anim = QPropertyAnimation(btn_card, b"pos", self)
                anim.setStartValue(start_pos)
                anim.setDuration(200)
                anim.setEndValue(end_pos)
                btn_card.lower()
                anim.start()
                self.anim_list.append(anim)
            # for btn_card in self.button_list[clicked_button.mast]:
            #     btn_card.hide()
        except Exception as e:
            print(e)


# class CardPushButton(QPushButton):
#     def __init__(self):
#         super().__init__()


app = QApplication([])
poker = GuiPoker()
poker.show()
app.exec_()
