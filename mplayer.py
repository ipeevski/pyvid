#!/usr/bin/env python3
import mpv
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class VideoPlayer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MainWindow")
        self.resize(1024, 768)

        self.centralWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.playlistView = QListView(self.centralWidget)
        self.playlistView.setAcceptDrops(True)
        self.playlistView.setProperty("showDropIndicator", True)
        self.playlistView.setDragDropMode(QAbstractItemView.DropOnly)
        self.playlistView.setAlternatingRowColors(True)
        self.playlistView.setUniformItemSizes(True)
        self.playlistView.setObjectName("playlistView")
        self.verticalLayout.addWidget(self.playlistView)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.currentTimeLabel = QLabel(self.centralWidget)
        self.currentTimeLabel.setMinimumSize(QSize(80, 0))
        self.currentTimeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.currentTimeLabel.setObjectName("currentTimeLabel")
        self.horizontalLayout_4.addWidget(self.currentTimeLabel)
        self.timeSlider = QSlider(self.centralWidget)
        self.timeSlider.setOrientation(Qt.Horizontal)
        self.timeSlider.setObjectName("timeSlider")
        self.horizontalLayout_4.addWidget(self.timeSlider)
        self.totalTimeLabel = QLabel(self.centralWidget)
        self.totalTimeLabel.setMinimumSize(QSize(80, 0))
        self.totalTimeLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.totalTimeLabel.setObjectName("totalTimeLabel")
        self.horizontalLayout_4.addWidget(self.totalTimeLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.previousButton = QPushButton(self.centralWidget)
        self.previousButton.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap("images/control-skip-180.png"), QIcon.Normal, QIcon.Off)
        self.previousButton.setIcon(icon)
        self.previousButton.setObjectName("previousButton")
        self.horizontalLayout_5.addWidget(self.previousButton)
        self.playButton = QPushButton(self.centralWidget)
        self.playButton.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("images/control.png"), QIcon.Normal, QIcon.Off)
        self.playButton.setIcon(icon1)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_5.addWidget(self.playButton)
        self.pauseButton = QPushButton(self.centralWidget)
        self.pauseButton.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap("images/control-pause.png"), QIcon.Normal, QIcon.Off)
        self.pauseButton.setIcon(icon2)
        self.pauseButton.setObjectName("pauseButton")
        self.horizontalLayout_5.addWidget(self.pauseButton)
        self.stopButton = QPushButton(self.centralWidget)
        self.stopButton.setText("")
        icon3 = QIcon()
        icon3.addPixmap(QPixmap("images/control-stop-square.png"), QIcon.Normal, QIcon.Off)
        self.stopButton.setIcon(icon3)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_5.addWidget(self.stopButton)
        self.nextButton = QPushButton(self.centralWidget)
        self.nextButton.setText("")
        icon4 = QIcon()
        icon4.addPixmap(QPixmap("images/control-skip.png"), QIcon.Normal, QIcon.Off)
        self.nextButton.setIcon(icon4)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout_5.addWidget(self.nextButton)
        self.viewButton = QPushButton(self.centralWidget)
        self.viewButton.setText("")
        icon5 = QIcon()
        icon5.addPixmap(QPixmap("images/application-image.png"), QIcon.Normal, QIcon.Off)
        self.viewButton.setIcon(icon5)
        self.viewButton.setCheckable(True)
        self.viewButton.setObjectName("viewButton")
        self.horizontalLayout_5.addWidget(self.viewButton)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.label = QLabel(self.centralWidget)
        self.label.setText("")
        self.label.setPixmap(QPixmap("images/speaker-volume.png"))
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.volumeSlider = QSlider(self.centralWidget)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setProperty("value", 100)
        self.volumeSlider.setOrientation(Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.horizontalLayout_5.addWidget(self.volumeSlider)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 484, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFIle = QMenu(self.menuBar)
        self.menuFIle.setObjectName("menuFIle")
        self.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)
        self.open_file_action = QAction(self)
        self.open_file_action.setObjectName("open_file_action")
        self.menuFIle.addAction(self.open_file_action)
        self.menuBar.addAction(self.menuFIle.menuAction())

        self.retranslateUi(self)

        self.container = QWidget(self.centralWidget)
        # self.setCentralWidget(self.container)
        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.container.setAttribute(Qt.WA_NativeWindow)
        self.container.setMinimumSize(QSize(800,600))
        self.player = mpv.MPV(
                # wid=str(int(self.container.winId())),
                input_default_bindings=True,
                input_vo_keyboard=True,
                vo='opengl', # You may not need this
                log_handler=print)
        self.player.fullscreen = True

    def play(self, file):
        self.player.play(file)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Failamp"))
        self.currentTimeLabel.setText(_translate("MainWindow", "0:00"))
        self.totalTimeLabel.setText(_translate("MainWindow", "0:00"))
        self.menuFIle.setTitle(_translate("MainWindow", "FIle"))
        self.open_file_action.setText(_translate("MainWindow", "Open file..."))

    def keyPressEvent(self, event):
        key = event.key()
        # Commands: https://mpv.io/manual/stable/#command-interface
        self.player.command('keypress', chr(key))

        # self.player.command('frame-step')

        # if key == Qt.Key_Left:
        #     print('Left Arrow Pressed')


app = QApplication(sys.argv)

# This is necessary since PyQT stomps over the locale settings needed by libmpv.
# This needs to happen after importing PyQT before creating the first mpv.MPV instance.
import locale
locale.setlocale(locale.LC_NUMERIC, 'C')
win = VideoPlayer()
win.show()
win.play(sys.argv[1])
sys.exit(app.exec_())
