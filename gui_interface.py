import sys
import threading

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from listener import Listener


class MyGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 200, 400, 200)
        self.setMinimumSize(400, 200)
        self.setMaximumSize(500, 300)
        self.setWindowTitle('Personal')
        self.__add_menu__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.listener = Listener()
        self.voice_analyser = VoiceAnalyser(self.listener)
        self.setCentralWidget(self.voice_analyser)
        self.started = False

    def __add_menu__(self):
        start_action = QAction('&Start', self)
        start_action.setShortcut('Ctrl+S')
        start_action.triggered.connect(self.start_action_trigger)

        stop_action = QAction('&Stop', self)
        stop_action.setShortcut('Ctrl+Shift+S')
        stop_action.triggered.connect(self.stop_action_trigger)

        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.exit_action_trigger)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')

        file_menu.addAction(start_action)
        file_menu.addAction(stop_action)
        file_menu.addAction(exit_action)

    def start_action_trigger(self):
        print('Start Action Triggered')
        if not self.started:
            self.started = True
            self.listener.start()

    def stop_action_trigger(self):
        print('Stop Action Trigger')
        if self.started:
            self.started = False
            self.listener.stop()
            self.voice_analyser.stop_thread()

    def exit_action_trigger(self):
        print('Exit Action Trigger')
        if self.started:
            self.stop_action_trigger()
            self.close()


class VoiceAnalyser(QWidget):
    def __init__(self, listen: Listener):
        super().__init__()
        self.listener = listen
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_title('Voice Analysis')

        self.xdata = np.linspace(0, 2 * np.pi, 1024)  # Update xdata size to match incoming data size
        self.ydata = np.zeros_like(self.xdata)

        self.thread = threading.Thread(target=self.update_plot)
        self.thread.start()

    def update_plot(self):
        try:
            while True:
                data = self.listener.get_voice_level()
                self.ydata = np.roll(self.ydata, -len(data))
                self.ydata[-len(data):] = data

                self.ax.clear()
                self.ax.set_xlabel('Time')
                self.ax.set_ylabel('Amplitude')
                self.ax.set_title('Voice Analysis')

                self.ax.plot(self.xdata, self.ydata, '-')

                self.canvas.draw()
        except Exception as e:
            print(e)

    def stop_thread(self):
        self.thread.stop()


def start():
    app = QApplication(sys.argv)
    gui = MyGui()
    gui.show()
    sys.exit(app.exec_())
