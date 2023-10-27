# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '_NotificationWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_NotificationWidget(object):
    def setupUi(self, NotificationWidget):
        if not NotificationWidget.objectName():
            NotificationWidget.setObjectName(u"NotificationWidget")
        NotificationWidget.resize(200, 39)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NotificationWidget.sizePolicy().hasHeightForWidth())
        NotificationWidget.setSizePolicy(sizePolicy)
        NotificationWidget.setMinimumSize(QSize(200, 0))
        NotificationWidget.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout = QVBoxLayout(NotificationWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.message_label = QLabel(NotificationWidget)
        self.message_label.setObjectName(u"message_label")
        sizePolicy.setHeightForWidth(self.message_label.sizePolicy().hasHeightForWidth())
        self.message_label.setSizePolicy(sizePolicy)
        self.message_label.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(11)
        self.message_label.setFont(font)
        self.message_label.setTextFormat(Qt.AutoText)
        self.message_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.message_label)


        self.retranslateUi(NotificationWidget)

        QMetaObject.connectSlotsByName(NotificationWidget)
    # setupUi

    def retranslateUi(self, NotificationWidget):
        NotificationWidget.setWindowTitle(QCoreApplication.translate("NotificationWidget", u"ClipIt - Notification", None))
        self.message_label.setText("")
    # retranslateUi

