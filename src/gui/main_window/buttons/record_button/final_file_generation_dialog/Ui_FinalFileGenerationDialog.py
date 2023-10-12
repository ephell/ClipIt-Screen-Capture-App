# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FinalFileGenerationDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QProgressBar, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_FinalFileGenerationDialog(object):
    def setupUi(self, FinalFileGenerationDialog):
        if not FinalFileGenerationDialog.objectName():
            FinalFileGenerationDialog.setObjectName(u"FinalFileGenerationDialog")
        FinalFileGenerationDialog.resize(500, 121)
        self.verticalLayout = QVBoxLayout(FinalFileGenerationDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.main_widget_frame = QFrame(FinalFileGenerationDialog)
        self.main_widget_frame.setObjectName(u"main_widget_frame")
        self.main_widget_frame.setFrameShape(QFrame.StyledPanel)
        self.main_widget_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.main_widget_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.status_message_frame_layout = QHBoxLayout()
        self.status_message_frame_layout.setObjectName(u"status_message_frame_layout")
        self.status_message_h_left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.status_message_frame_layout.addItem(self.status_message_h_left_spacer)

        self.status_message_label = QLabel(self.main_widget_frame)
        self.status_message_label.setObjectName(u"status_message_label")
        font = QFont()
        font.setPointSize(15)
        font.setBold(False)
        self.status_message_label.setFont(font)

        self.status_message_frame_layout.addWidget(self.status_message_label)

        self.status_message_h_right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.status_message_frame_layout.addItem(self.status_message_h_right_spacer)


        self.verticalLayout_4.addLayout(self.status_message_frame_layout)

        self.progress_bar_frame = QFrame(self.main_widget_frame)
        self.progress_bar_frame.setObjectName(u"progress_bar_frame")
        self.progress_bar_frame.setFrameShape(QFrame.StyledPanel)
        self.progress_bar_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.progress_bar_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 9, 0, 0)
        self.progress_bar_frame_layout = QVBoxLayout()
        self.progress_bar_frame_layout.setObjectName(u"progress_bar_frame_layout")
        self.progress_bar = QProgressBar(self.progress_bar_frame)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setMinimumSize(QSize(0, 35))
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.progress_bar_frame_layout.addWidget(self.progress_bar)


        self.verticalLayout_2.addLayout(self.progress_bar_frame_layout)


        self.verticalLayout_4.addWidget(self.progress_bar_frame)


        self.verticalLayout.addWidget(self.main_widget_frame)


        self.retranslateUi(FinalFileGenerationDialog)

        QMetaObject.connectSlotsByName(FinalFileGenerationDialog)
    # setupUi

    def retranslateUi(self, FinalFileGenerationDialog):
        FinalFileGenerationDialog.setWindowTitle(QCoreApplication.translate("FinalFileGenerationDialog", u"Generating Final File", None))
        self.status_message_label.setText(QCoreApplication.translate("FinalFileGenerationDialog", u"(2/3) Merging speaker and microphone audio ... ", None))
    # retranslateUi

