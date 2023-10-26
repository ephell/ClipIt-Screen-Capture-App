# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '_notification_widget.ui'
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
        NotificationWidget.resize(227, 54)
        self.verticalLayout = QVBoxLayout(NotificationWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.notification_text = QLabel(NotificationWidget)
        self.notification_text.setObjectName(u"notification_text")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.notification_text.setFont(font)

        self.verticalLayout.addWidget(self.notification_text, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.retranslateUi(NotificationWidget)

        QMetaObject.connectSlotsByName(NotificationWidget)
    # setupUi

    def retranslateUi(self, NotificationWidget):
        NotificationWidget.setWindowTitle(QCoreApplication.translate("NotificationWidget", u"ClipIt - Notification", None))
        self.notification_text.setText(QCoreApplication.translate("NotificationWidget", u"Starting", None))
    # retranslateUi

