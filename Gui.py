from turtledemo.penrose import start
from StatRoom import Room
from Table import TableRabbit
import sys
from random import choice
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtCore import pyqtSignal, QObject, QPropertyAnimation, QPoint, QTimer, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QCursor


class MyTimer(QTimer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.func_for_connect = None

    def get_func(self, func):
        self.func_for_connect = func


class CardPushButton(QPushButton):
    leave_signal = pyqtSignal(object)
    input_signal = pyqtSignal(object)

    def __init__(self, name, parent, card):
        super().__init__(name, parent)
        self.card = card
        self.default_pos = None
        self.offset = QPoint(0, 35)
        self.mast, self.nominal = self.card
        self.frame_position = None
        self.index = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_cursor)
        self.timer.start(1000)
        self.mast_str = ''
        self.setObjectName("MyGradientButton")

        self.is_hovered = False

    def __str__(self):
        return f'карта ---- {self.card}'

    def setting_style(self, colors):
        font = QFont("Chiller", 12)
        color1, color2 = colors if self.isChecked() else colors[::-1]
        self.setFont(font)
        self.setStyleSheet(f"""
                    QPushButton#MyGradientButton {{
                        background-color: qlineargradient(
                            spread:pad, x1:0, y1:0, x2:0, y2:1,
                            stop:0 {color1},
                            stop:1 {color2}
                        );
                        border: none;
                        color: black;
                        
                    }}
                    QPushButton#MyGradientButton:pressed {{
                        background-color: qlineargradient(
                            spread:pad, x1:0, y1:0, x2:0, y2:1,
                            stop:0 {color1},
                            stop:1 {color2}
                        );
                        color: white;
                        
                    }}
                """)

    def get_fr_pos(self, pos):
        self.frame_position = pos

    def get_index(self, index):
        self.index = index

    def check_cursor(self):
        if not self.underMouse() and self.isChecked() and self.is_hovered:
            print(self)

    def leaveEvent(self, event):
        self.leave_signal.emit(self)  # передаём виджет в главное окно
        super().leaveEvent(event)

    def enterEvent(self, event):
        self.input_signal.emit(self)
        super().enterEvent(event)

    def check_hover(self):
        if not self.isChecked():
            self.raise_()
        self.is_hovered = True


class MainPushButton(QPushButton):
    def __init__(self, name, parent, mast):
        super().__init__(name, parent)
        self.mast = mast
        self.cards = []
        self.color_collection = None
        self.toggled.connect(self.setting_style)
        self.setter_color = ('#F5F5F5', '#3F888F')
        self.setObjectName("MyGradientButton")

        self.is_paint = False

    def get_card(self, card):
        self.cards.append(card)

    def get_color_collection(self, cc):
        self.color_collection = cc

    def set_color(self):
        if self.color_collection:
            colors = choice(self.color_collection)
        else:
            colors = ('#F5F5F5', '#3F888F')
        self.setter_color = colors

    def paint(self):
        if not self.is_paint:
            self.is_paint = True
            for btn in self.cards:
                btn.color = self.setter_color
                btn.setting_style(self.setter_color)

    def setting_style(self):
        font = QFont("Arial", 20)
        color1, color2 = self.setter_color if self.isChecked() else self.setter_color[::-1]
        self.setFont(font)
        self.setStyleSheet(f"""
                    QPushButton#MyGradientButton {{
                        background-color: qlineargradient(
                            spread:pad, x1:0, y1:0, x2:0, y2:1,
                            stop:0 {color1},
                            stop:1 {color2}
                        );
                        border: none;
                        color: black;
                    }}
                    QPushButton#MyGradientButton:pressed {{
                        background-color: qlineargradient(
                            spread:pad, x1:0, y1:0, x2:0, y2:1,
                            stop:0 {color1},
                            stop:1 {color2}
                        );
                        color: white;
                    }}
                """)


class CardFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.card_button = False

    def __str__(self):
        return 'Моя рамка'

    def get_card(self, button: CardPushButton):
        self.card_button = button


class LimeFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent; border: 5px solid #00FF00;")


class LabelPlayers(QLabel):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.count = 2
        self.set_style()

    def refresh(self):
        self.count = 2
        self.setText(f'{self.count}')

    def set_style(self):
        font = QFont('Chiller', 11)
        self.setFont(font)


class GuiPoker(QWidget):
    """Класс основного окна графического приложения"""

    def __init__(self):
        super().__init__()
        # Списки одноименные с аргументами стола
        self.hand = []
        self.flop = []
        self.turn = []
        self.river = []

        self.fonts = (
            "Comic Sans MS", "Segoe Print", "Segoe Script", "Lucida Handwriting",
            "Arial Rounded MT Bold", "Gabriola",
            "Georgia", "Verdana"

        )
        self.collection_color = {0: (), 1: (), 2: (('#DDBEC3', '#CC0605'), ('#EAE6CA', '#B44C43')), 3: ()}

        self.table = TableRabbit(hand=self.hand, flop=self.flop, turn=self.turn, river=self.river)
        self.stat_room = Room(self.table)  # Атрибут StatRoom

        # колода в которой каждая масть это отдельный список карт
        self.card_list = self.create_mast()

        # Список рамок (QFrame или наследованные от них)
        self.frame_list = []

        # Список из кнопок карт
        self.button_card_list = []

        # Список из кнопок мастей
        self.main_button_list = []

        # Список анимаций
        self.anim_list = []

        # Параметры окна
        self.setWindowTitle('Poker')
        self.setGeometry(100, 100, 800, 650)

        # Методы необходимые при создании основного окна
        self.create_main_button()
        self.create_card_btn()
        self.lime_frame = self.create_lime_frame()
        self.create_hand_frame()
        self.create_frame_table()
        self.calculate_button = self.create_calculate_button()
        self.refresh_button = self.create_refresh_button()
        self.label_text = self.create_label_text_players()
        self.count_players_label = self.create_label_players()
        self.up_btn, self.down_btn = self.create_up_button(), self.create_down_button()
        self.winrate_label = self.create_winrate_label()
        self.count_comb_label = self.create_comb_rate_label()

        self.timer_on_card = self.create_timer()
        self.timer_leave_card = self.create_timer()

    # Создание колоды
    @staticmethod
    def create_mast():
        """Метод создает колоду в которой каждая масть это отдельный список карт"""
        return [[(mast, nominal) for nominal in range(2, 15)] for mast in range(4)]

    @staticmethod
    def between_widget(midl: CardPushButton, und: CardPushButton = None, up: CardPushButton = None):
        if not und:
            midl.stackUnder(up)
        elif not up:
            und.stackUnder(midl)
        else:
            midl.stackUnder(up)
            und.stackUnder(midl)

    @staticmethod
    def reset_z_btn_card(main: MainPushButton):
        """Метод для восстановления порядка отрисовки карт для определенной масти"""

        for card in main.cards:
            card.raise_()
        if not main.isChecked():
            main.raise_()

    def raise_card(self, widget: CardPushButton):
        """Метод который, присоединяет функцию поднятия карты к таймеру self.timer_on_card"""
        self.timer_on_card.timeout.connect(widget.check_hover)
        self.timer_on_card.start(100)

    def take_seat(self, widget: CardPushButton):
        """Метод отключает метод поднятия карты от таймера и восстанавливает порядок отрисовки карт"""
        try:
            self.timer_on_card.timeout.disconnect(widget.check_hover)
            if widget.pos() != widget.default_pos and widget.is_hovered:
                widget.is_hovered = False
                b = widget.mast
                main_btn = self.main_button_list[b]
                self.reset_z_btn_card(main_btn)
        except Exception as e:
            print(e, 'take_seat')

    # -------------- Создание виджетов -----------------

    # Создание кнопок мастей
    def create_main_button(self):
        """Метод создает 4 основные кнопки с названием мастей и располагает их на экране"""
        offset = 0
        for i, name in enumerate(('♠', '♣', '♥', '♦')):
            main_btn = MainPushButton(name, self, i)
            main_btn.setGeometry(50 + offset, 10, 35, 60)
            main_btn.get_color_collection(self.collection_color[i])
            main_btn.set_color()
            main_btn.setCheckable(True)
            main_btn.clicked.connect(self.open_close)
            main_btn.setting_style()
            self.main_button_list.append(main_btn)
            offset += 50

    # Создание кнопки расчет
    def create_calculate_button(self):
        """Метод создает кнопку 'Расчет'"""
        font = QFont('Segoe Print', 11)
        calcul_btn = QPushButton('Расчет', self)
        calcul_btn.setGeometry(550, 180, 90, 60)
        calcul_btn.setFont(font)
        calcul_btn.clicked.connect(self.calculate)
        return calcul_btn

    # Создание кнопок карт
    def create_card_btn(self):
        """Метод создает кнопки карт"""
        ico = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K',
               14: 'A'}
        mast_str = ('♠', '♣', '♥', '♦')
        for i, mast in enumerate(self.card_list):
            for card in mast:
                nominal = ico[card[-1]]
                btn = CardPushButton(f'{nominal} {mast_str[i]}', self, card)
                btn.setCheckable(True)
                btn.setGeometry(50, 50, 36, 60)
                btn.setContentsMargins(0, 5, 0, 0)
                btn.clicked.connect(self.draw_card)
                btn.leave_signal.connect(self.take_seat)
                btn.input_signal.connect(self.raise_card)
                btn.hide()
                main_button = self.main_button_list[i]
                main_button.get_card(btn)
                self.button_card_list.append(btn)

    # Создание кнопки Сбросить
    def create_refresh_button(self):
        """Метод создает кнопку Сбросить"""
        font = QFont('Segoe Print', 11)
        refresh = QPushButton('Сбросить', self)
        refresh.setGeometry(550, 100, 90, 60)
        refresh.setFont(font)
        refresh.clicked.connect(self.refresh)
        return refresh

    # Создание кнопки увеличения кол-ва игроков
    def create_up_button(self):
        """Метод создает кнопку увеличения кол-ва игроков"""
        font = QFont('Segoe Print', 13)
        font.setBold(True)
        button = QPushButton('+', self)
        button.setGeometry(620, 330 - 40, 40, 40)
        button.setFont(font)
        button.clicked.connect(self.up_players)
        return button

    # Создание кнопки уменьшения кол-ва игроков
    def create_down_button(self):
        """Создание кнопки уменьшения кол-ва игроков"""
        font = QFont('Segoe Print', 13)
        font.setBold(True)
        button = QPushButton('-', self)
        button.setGeometry(520, 330 - 40, 40, 40)
        button.setFont(font)
        button.clicked.connect(self.down_players)
        return button

    # Создание рамок для карт руки
    def create_hand_frame(self):
        """Создание рамок для карт руки"""
        offset = 0
        for i in range(2):
            frame = CardFrame(self)
            frame.setGeometry(350 + offset, 100, 36, 60)
            frame.setFrameShape(QFrame.Box)
            frame.setAttribute(Qt.WA_TransparentForMouseEvents)
            frame.setStyleSheet("background-color: transparent; border: 1px solid #000000;")
            offset += 50
            self.frame_list.append(frame)

    # Создание зеленой рамки
    def create_lime_frame(self):
        """Создание зеленой рамки"""
        frame = LimeFrame(self)
        frame.setGeometry(350, 100, 36, 60)
        frame.setFrameShape(QFrame.Box)
        frame.lower()
        return frame

    # Создание рамок для карт стола
    def create_frame_table(self):
        """Создание рамок для карт стола"""
        offset = 0
        for i in range(5):
            frame = CardFrame(self)
            frame.setGeometry(275 + offset, 180, 36, 60)
            frame.setFrameShape(QFrame.Box)
            frame.setAttribute(Qt.WA_TransparentForMouseEvents)
            frame.setStyleSheet("background-color: transparent; border: 1px solid #000000;")
            offset += 50
            self.frame_list.append(frame)

    # Создание лейбла с надписью
    def create_label_text_players(self):
        """Создание лейбла с надписью"""
        font = QFont('Segoe Print', 13)
        label = QLabel(self)
        label.setText(f'игроки')
        label.setFont(font)
        label.setGeometry(570, 270, 50, 60)
        label.adjustSize()
        return label

    def create_label_players(self):
        """Создание лейбла с кол-вом игроков"""
        font = QFont('Segoe Print', 13)
        font.setBold(True)
        label = LabelPlayers(parent=self)
        label.setText(f'{label.count}')
        label.setFont(font)
        label.setGeometry(585, 300, 50, 60)
        label.setStyleSheet("background-color: transparent; "
                            "border-top: 1px solid black; "
                            "border-bottom: 1px solid black")
        label.adjustSize()

        return label

    def create_winrate_label(self, percent='0'):
        font = QFont('Segoe Print', 13)
        label = QLabel(self)
        label.setText(f'{percent}%')
        label.setFont(font)
        label.setGeometry(390, 270, 50, 60)
        label.adjustSize()
        return label

    def create_comb_rate_label(self):
        text = self.stat_room.get_string_count_comb()
        font = QFont('Segoe Print', 11)
        label = QLabel(self)
        label.setText(text)
        label.setFont(font)
        label.setGeometry(490, 370, 50, 60)
        label.adjustSize()
        return label

    @staticmethod
    def create_timer():
        timer = QTimer()
        timer.setSingleShot(True)
        return timer

    # ---------- Методы срабатывающие при нажатии -------

    # Метод для открытия и закрытия кнопок карт
    def open_close(self):
        """Метод вызывает анимацию раскрытия и скрытия карт в зависимости от состояния кнопки масти"""
        try:
            clicked_button = self.sender()
            flag = clicked_button.isChecked()
            if not flag:
                self.animation_close(clicked_button)
            else:
                clicked_button.paint()
                self.animation_open(clicked_button)
        except Exception as e:
            print(e)

    def calculate(self):
        """Метод создает стол и комнату и вызывает метод StatRoom.stat_room.up_count
        И выводит результат"""

        players = self.count_players_label.count
        self.table = TableRabbit(players=players, hand=self.hand, flop=self.flop, turn=self.turn, river=self.river)
        self.stat_room = Room(self.table)
        self.stat_room.up_count()
        percent = self.stat_room.chans()
        count_comb = self.stat_room.get_string_count_comb()
        self.winrate_label.setText(f'{percent}%')
        self.winrate_label.adjustSize()
        self.count_comb_label.setText(count_comb)
        self.count_comb_label.adjustSize()

    def refresh(self):
        """Сбрасывает состояние программы до начального"""
        try:
            for card_button in self.button_card_list:
                card_button.setChecked(False)
                card_button.get_index(False)
            for main_card in self.main_button_list:
                main_card.setChecked(True)
                main_card.click()
            for frame in self.frame_list:
                frame.get_card(False)
            self.mario()
            self.jump_lime_frame()
            self.count_players_label.refresh()
            self.winrate_label.setText(f'0%')
            self.stat_room.set_zero_count_comb()
            self.count_comb_label.setText(self.stat_room.get_string_count_comb())
        except Exception as e:
            print(e)

    def draw_card(self):
        """Метод определяет какая кнопка нажата и предает эту кнопку в
        self.animation_for_card"""
        clicked_button = self.sender()
        try:
            self.animation_for_card(clicked_button)

        except Exception as e:
            print(e)

    def animation_for_card(self, btn_card: CardPushButton):
        """Метод определяет состояние нажатия кнопки
        В соответствии с этим выбирает метод:
            True - append_on_a_line
            False - delite_card
        И деактивирует или активирует кнопку расчет на основании результата
        выполнения метода mario"""
        try:
            flag = btn_card.isChecked()
            if flag:
                self.append_on_a_line(btn_card)
            else:
                self.delite_card(btn_card)
            flag_for_cal = self.mario()
            self.calculate_button.setEnabled(flag_for_cal)
        except Exception as e:
            print(f'{e} err in ----- {self.animation_for_card.__name__}')

    def append_on_a_line(self, btn_card: CardPushButton):
        """Добавляет кнопку карты в соответствующую рамку"""
        try:
            for i in range(len(self.frame_list)):
                frame = self.frame_list[i]
                if not frame.card_button:
                    btn_card.get_fr_pos(frame.pos())
                    frame.get_card(btn_card)
                    btn_card.get_index(i)
                    break
                if i == 6:
                    if frame.card_button:
                        return
            self.jump_lime_frame()
            anim = QPropertyAnimation(btn_card, b"pos", self)
            start_pos = btn_card.pos()
            end_pos = btn_card.frame_position
            anim.setDuration(100)
            anim.setStartValue(start_pos)
            anim.setEndValue(end_pos)
            anim.start()
        except Exception as e:
            print(e)

    def delite_card(self, btn_card: CardPushButton):
        """Метод удаляет кнопку карты со стола и вызывает анимацию перехода карты на свое место
        с учетом нажатия кнопки масти"""
        inx = btn_card.card[0]
        flag = self.main_button_list[inx].isChecked()
        if flag:
            end_pos = btn_card.default_pos + btn_card.offset * (btn_card.card[-1] - 1)
        else:
            self.main_button_list[inx].raise_()
            end_pos = btn_card.default_pos

        anim = QPropertyAnimation(btn_card, b"pos", self)
        start_pos = btn_card.pos()
        anim.setDuration(100)
        anim.setStartValue(start_pos)
        anim.setEndValue(end_pos)
        anim.start()
        if btn_card.index is not None:
            i_frame = btn_card.index
            frame = self.frame_list[i_frame]
            frame.get_card(False)
            btn_card.get_index(None)
        self.jump_lime_frame()

    def jump_lime_frame(self):
        """Метод определяющий слот для перемещения зеленой рамки"""
        self.lime_frame.show()
        for i in range(len(self.frame_list)):
            frame = self.frame_list[i]
            if not frame.card_button:
                self.anim_lime_frame(frame)
                break
            if i == 6:
                if frame.card_button:
                    self.lime_frame.hide()

    def anim_lime_frame(self, card_frame: CardFrame):
        """Анимация для перехода зеленой рамки на активный слот"""
        anim = QPropertyAnimation(self.lime_frame, b"pos", self)
        start_pos = self.lime_frame.pos()
        end_pos = card_frame.pos()
        anim.setDuration(100)
        anim.setStartValue(start_pos)
        anim.setEndValue(end_pos)
        anim.start()
        self.lime_frame.lower()

    def get_lime_frame(self, count=0):
        try:
            if count == 7:
                self.frame_list[count - 1].setStyleSheet("background-color: transparent; border: 1px solid #000000;")
                return
            frame = self.frame_list[count]
            frame.setStyleSheet("background-color: transparent; border: 3px solid #00FF00;")
            if count >= 1:
                self.frame_list[count - 1].setStyleSheet("background-color: transparent; border: 1px solid #000000;")
        except Exception as e:
            print(e)

    def animation_open(self, clicked: MainPushButton, durable=200):
        """Метод анимации раскрытия кнопок карт"""
        try:
            offset = QPoint(0, 37)
            clicked_button = clicked
            for count, btn_card in enumerate(clicked_button.cards):
                if btn_card.isChecked():
                    continue
                strat_pos = clicked_button.pos()
                btn_card.is_hovered = False
                btn_card.show()
                btn_card.default_pos = strat_pos
                anim = QPropertyAnimation(btn_card, b"pos", self)
                anim.setDuration(durable)
                anim.setStartValue(strat_pos)
                anim.setEndValue(strat_pos + offset * (count + 1))
                btn_card.raise_()
                anim.start()
                self.anim_list.append(anim)
        except Exception as e:
            print(e, 'animation_open')

    def animation_close(self, clicked: MainPushButton):
        """Метод анимации закрытия карт кнопок"""
        try:
            clicked_button = clicked
            clicked_button.raise_()
            for count, btn_card in enumerate(clicked_button.cards):
                if btn_card.isChecked():
                    continue
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
            print(e, 'animation_close')

    def transform(self):
        """Метод трансформирует атрибуты в нужную форму"""
        if not any(self.hand):
            self.hand = []
        if not any(self.flop):
            self.flop = []
        if not all(self.turn):
            self.turn = []
        if not all(self.river):
            self.river = []

    def check_condition(self):
        """Метод определяет есть ли возможность рассчитать вероятность победы.
        Возвращает False если не выполнены условия для расчета"""
        try:
            if all(self.hand) and all(self.flop):
                lst = [self.hand, self.flop, self.turn, self.river]
                x = True
                for i in lst:
                    if not x:
                        if bool(i):
                            return False
                    if bool(i) is False:
                        x = False
                return True
            return False
        except Exception as e:
            print(e)

    def check_condition2(self):
        """Метод определяет есть ли возможность рассчитать вероятность победы.
        Возвращает False если не выполнены условия для расчета"""
        try:
            if (all(self.hand) or not any(self.hand)) and (all(self.flop) or not any(self.flop)):
                lst = [self.river, self.turn, self.flop, self.hand]
                for i in range(len(lst) - 1):
                    if (any(lst[i]) and all(lst[i])) is True and (any(lst[i + 1]) and all(lst[i + 1])) is False:
                        return False
            else:
                return False
            return True

        except Exception as e:
            print(e)

    def mario(self):
        """Метод приводит к необходимому виду данные для проверки в методе check_condition(),
        а так же вызывает методы self.transform() и
        check_condition()"""
        card_list = []
        for frame in self.frame_list:
            if frame.card_button:
                card = frame.card_button.card
                card_list.append(card)
            else:
                card_list.append(frame.card_button)
        self.hand = card_list[:2]  # Список типа [(3,2), False] - есть одна карта и нет второй
        self.flop = card_list[2:5]
        self.turn = card_list[5:6]
        self.river = card_list[6:]
        self.transform()
        return self.check_condition2()

    def up_players(self):
        if self.count_players_label.count < 8:
            self.count_players_label.count += 1
            count = self.count_players_label.count
            self.count_players_label.setText(f'{count}')
            self.count_players_label.adjustSize()

    def down_players(self):
        if self.count_players_label.count > 2:
            self.count_players_label.count -= 1
            count = self.count_players_label.count
            self.count_players_label.setText(f'{count}')
            self.count_players_label.adjustSize()

# app = QApplication([])
# poker = GuiPoker()
# poker.show()
# app.exec_()
