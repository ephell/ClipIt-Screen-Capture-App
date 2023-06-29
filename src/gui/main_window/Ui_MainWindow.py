# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(214, 134)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.select_area_button = QPushButton(self.centralwidget)
        self.select_area_button.setObjectName(u"select_area_button")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_area_button.sizePolicy().hasHeightForWidth())
        self.select_area_button.setSizePolicy(sizePolicy)
        self.select_area_button.setMinimumSize(QSize(180, 0))
        self.select_area_button.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.select_area_button)

        self.start_recording_button = QPushButton(self.centralwidget)
        self.start_recording_button.setObjectName(u"start_recording_button")
        sizePolicy.setHeightForWidth(self.start_recording_button.sizePolicy().hasHeightForWidth())
        self.start_recording_button.setSizePolicy(sizePolicy)
        self.start_recording_button.setMinimumSize(QSize(180, 0))
        self.start_recording_button.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.start_recording_button)

        self.stop_recording_button = QPushButton(self.centralwidget)
        self.stop_recording_button.setObjectName(u"stop_recording_button")
        sizePolicy.setHeightForWidth(self.stop_recording_button.sizePolicy().hasHeightForWidth())
        self.stop_recording_button.setSizePolicy(sizePolicy)
        self.stop_recording_button.setMinimumSize(QSize(180, 0))
        self.stop_recording_button.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.stop_recording_button)

        self.open_editor_button = QPushButton(self.centralwidget)
        self.open_editor_button.setObjectName(u"open_editor_button")
        sizePolicy.setHeightForWidth(self.open_editor_button.sizePolicy().hasHeightForWidth())
        self.open_editor_button.setSizePolicy(sizePolicy)
        self.open_editor_button.setMinimumSize(QSize(180, 0))
        self.open_editor_button.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.open_editor_button)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ClipIt", None))
        self.select_area_button.setText(QCoreApplication.translate("MainWindow", u"Select Area", None))
        self.start_recording_button.setText(QCoreApplication.translate("MainWindow", u"Start Recording", None))
        self.stop_recording_button.setText(QCoreApplication.translate("MainWindow", u"Stop Recording", None))
        self.open_editor_button.setText(QCoreApplication.translate("MainWindow", u"Open Editor", None))
    # retranslateUi

