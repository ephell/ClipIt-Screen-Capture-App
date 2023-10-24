# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QSizePolicy, QVBoxLayout, QWidget)

from .buttons.open_capture_folder_button.open_capture_folder_button import OpenCaptureFolderButton
from .buttons.open_editor_button.open_editor_button import OpenEditorButton
from .buttons.record_button.record_button import RecordButton
from .buttons.screenshot_button.screenshot_button import ScreenshotButton
from .buttons.settings_button.settings_button import SettingsButton
from . import main_window_button_icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(320, 170)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(320, 170))
        MainWindow.setMaximumSize(QSize(320, 170))
        MainWindow.setStyleSheet(u"")
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(self.central_widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.capture_duration_label = QLabel(self.central_widget)
        self.capture_duration_label.setObjectName(u"capture_duration_label")
        font = QFont()
        font.setPointSize(32)
        font.setBold(True)
        self.capture_duration_label.setFont(font)

        self.verticalLayout_2.addWidget(self.capture_duration_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.separator_line = QFrame(self.central_widget)
        self.separator_line.setObjectName(u"separator_line")
        self.separator_line.setMinimumSize(QSize(272, 3))
        self.separator_line.setMaximumSize(QSize(272, 3))
        self.separator_line.setStyleSheet(u"background-color: gray;")
        self.separator_line.setFrameShape(QFrame.HLine)
        self.separator_line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.separator_line, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.button_frame = QFrame(self.central_widget)
        self.button_frame.setObjectName(u"button_frame")
        self.button_frame.setFrameShape(QFrame.StyledPanel)
        self.button_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.button_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.record_button = RecordButton(self.button_frame)
        self.record_button.setObjectName(u"record_button")
        self.record_button.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.record_button)

        self.screenshot_button = ScreenshotButton(self.button_frame)
        self.screenshot_button.setObjectName(u"screenshot_button")
        self.screenshot_button.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.screenshot_button)

        self.open_editor_button = OpenEditorButton(self.button_frame)
        self.open_editor_button.setObjectName(u"open_editor_button")
        self.open_editor_button.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.open_editor_button)

        self.open_capture_folder_button = OpenCaptureFolderButton(self.button_frame)
        self.open_capture_folder_button.setObjectName(u"open_capture_folder_button")
        self.open_capture_folder_button.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.open_capture_folder_button)

        self.settings_button = SettingsButton(self.button_frame)
        self.settings_button.setObjectName(u"settings_button")
        self.settings_button.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.settings_button)


        self.verticalLayout_3.addWidget(self.button_frame)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(2, 1)
        MainWindow.setCentralWidget(self.central_widget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ClipIt", None))
        self.capture_duration_label.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.record_button.setText("")
        self.screenshot_button.setText("")
        self.open_editor_button.setText("")
        self.open_capture_folder_button.setText("")
        self.settings_button.setText("")
    # retranslateUi

