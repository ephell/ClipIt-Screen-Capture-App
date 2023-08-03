# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MediaItemTimeEdits.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QWidget)

from ._time_edit import TimeEdit

class Ui_MediaItemTimeEdits(object):
    def setupUi(self, MediaItemTimeEdits):
        if not MediaItemTimeEdits.objectName():
            MediaItemTimeEdits.setObjectName(u"MediaItemTimeEdits")
        MediaItemTimeEdits.resize(178, 47)
        self.horizontalLayout_2 = QHBoxLayout(MediaItemTimeEdits)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.left_handle_time_edit = TimeEdit(MediaItemTimeEdits)
        self.left_handle_time_edit.setObjectName(u"left_handle_time_edit")

        self.horizontalLayout.addWidget(self.left_handle_time_edit)

        self.separator_label = QLabel(MediaItemTimeEdits)
        self.separator_label.setObjectName(u"separator_label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.separator_label.sizePolicy().hasHeightForWidth())
        self.separator_label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.separator_label.setFont(font)

        self.horizontalLayout.addWidget(self.separator_label)

        self.right_handle_time_edit = TimeEdit(MediaItemTimeEdits)
        self.right_handle_time_edit.setObjectName(u"right_handle_time_edit")

        self.horizontalLayout.addWidget(self.right_handle_time_edit)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(MediaItemTimeEdits)

        QMetaObject.connectSlotsByName(MediaItemTimeEdits)
    # setupUi

    def retranslateUi(self, MediaItemTimeEdits):
        MediaItemTimeEdits.setWindowTitle(QCoreApplication.translate("MediaItemTimeEdits", u"Form", None))
        self.left_handle_time_edit.setDisplayFormat(QCoreApplication.translate("MediaItemTimeEdits", u"HH:mm:zzz", None))
        self.separator_label.setText(QCoreApplication.translate("MediaItemTimeEdits", u"-", None))
        self.right_handle_time_edit.setDisplayFormat(QCoreApplication.translate("MediaItemTimeEdits", u"HH:mm:zzz", None))
    # retranslateUi

