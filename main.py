# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread, QTime
from playsound import playsound
from datetime import datetime
import time
from functools import partial
from win10toast import ToastNotifier


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()

        loader = QUiLoader()
        self.ui = loader.load('form.ui')
        self.ui.btn_stopwatch_start.clicked.connect(self.startStopWatch)
        self.ui.btn_stopwatch_pause.clicked.connect(self.pauseStopWatch)
        self.ui.btn_stopwatch_stop.clicked.connect(self.stopStopWatch)
        self.ui.btn_record.clicked.connect(self.record)
        # ______________________alarm____________________________________________
        self.ui.btn_addalarm.clicked.connect(self.addalarm)
        # _______________________timer___________________________________________
        self.ui.btn_stopwatch_starttimer.clicked.connect(
            self.startStopWatchtimer)
        self.ui.btn_stopwatch_pausetimer.clicked.connect(
            self.pauseStopWatchtimer)
        self.ui.btn_stopwatch_stoptimer.clicked.connect(
            self.stopStopWatchtimer)

        # _______________________________________________________________________

        self.timer = Timer()

        self.ui.show()

    def pauseStopWatch(self):
        self.timer.terminate()

    def stopStopWatch(self):
        self.timer.terminate()
        self.timer.reset()
        self.ui.lbl_stopwatch.setText("00:00:00")

    def startStopWatch(self):
        self.timer.start()

    def record(self):
        label = QLabel()
        label.setText(widget.ui.lbl_stopwatch.text())
        self.ui.gl_record.addWidget(label)

# ________________Alarm______________
    def addalarm(self):
        self.alarm = Alarm()
        self.alarm.start()


# _______________timer_____________

    def pauseStopWatchtimer(self):
        self.timerr.terminate()

    def stopStopWatchtimer(self):
        self.timerr.terminate()
        self.timerr.reset()
        widget.ui.lbl_stopwatch_timer.setText("00:00:00")

    def startStopWatchtimer(self):
        self.timerr = Timerr(self.ui.spinbox_ht.value(),
                             self.ui.spinbox_mt.value(),
                             self.ui.spinbox_st.value())
        self.timerr.start()


# _________________Stopwatch________________________________________
class Timer(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.h = 00
        self.m = 00
        self.s = 00

    def reset(self):
        self.h = 00
        self.m = 00
        self.s = 00

    def increase(self):
        self.s += 1
        if self.s >= 60:
            self.s = 0
            self.m += 1

        if self.m >= 60:
            self.m = 0
            self.h += 1

    def run(self):
        while True:
            self.increase()
            widget.ui.lbl_stopwatch.setText(f"{self.h}:{self.m}:{self.s}")
            time.sleep(1)
# _____________________________Timer_____________________________________


class Timerr(QThread):
    def __init__(self, h, m, s):
        QThread.__init__(self)
        self.st = h
        self.mt = m
        self.ht = s

    def reset(self):
        self.st = 0
        self.mt = 0
        self.ht = 0

    def decrease(self):

        if self.ht == 0 and self.mt == 0 and self.st == 0:
            return

        if self.st == 0 and self.mt > 0:
            self.st = 59
            self.mt -= 1

        if self.mt == 0 and self.ht > 0:
            self.mt = 59
            self.ht -= 1

        self.st -= 1

    def run(self):
        while True:
            self.decrease()
            widget.ui.lbl_stopwatch_timer.setText(
                f"{self.ht}:{self.mt}:{self.st}")

            time.sleep(1)

# ____________________Alarm____________________________________________________________


class Alarm(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.hour = widget.ui.spinbox_h.value()
        self.minute = widget.ui.spinbox_m.value()
        self.toast = ToastNotifier()

    def run(self):
        while True:
            now = datetime.now()
            now_time = now.strftime("%H:%M:%S")
            time_now = now_time.split(':')
            if self.hour == int(time_now[0]) and self.minute == int(time_now[1]):
                self.toast.show_toast(
                    "Timer ", "wake up", "duration=10")
                playsound("alarm.mp3")

            time.sleep(1)


if __name__ == "__main__":
    app = QApplication([])
    widget = Main()
    sys.exit(app.exec())
