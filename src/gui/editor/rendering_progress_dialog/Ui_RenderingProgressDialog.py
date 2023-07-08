# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RenderingProgressDialog.ui'
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
    QLabel, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_RenderingProgressDialog(object):
    def setupUi(self, RenderingProgressDialog):
        if not RenderingProgressDialog.objectName():
            RenderingProgressDialog.setObjectName(u"RenderingProgressDialog")
        RenderingProgressDialog.resize(500, 166)
        self.verticalLayout = QVBoxLayout(RenderingProgressDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.main_widget_frame = QFrame(RenderingProgressDialog)
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

        self.close_button_frame = QFrame(self.main_widget_frame)
        self.close_button_frame.setObjectName(u"close_button_frame")
        self.close_button_frame.setFrameShape(QFrame.StyledPanel)
        self.close_button_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.close_button_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.close_button_frame_h_layout = QHBoxLayout()
        self.close_button_frame_h_layout.setObjectName(u"close_button_frame_h_layout")
        self.close_button_frame_h_layout.setContentsMargins(-1, 9, -1, -1)
        self.close_button_h_left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.close_button_frame_h_layout.addItem(self.close_button_h_left_spacer)

        self.close_button = QPushButton(self.close_button_frame)
        self.close_button.setObjectName(u"close_button")
        self.close_button.setEnabled(False)
        self.close_button.setMinimumSize(QSize(100, 30))

        self.close_button_frame_h_layout.addWidget(self.close_button)

        self.close_button_h_right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.close_button_frame_h_layout.addItem(self.close_button_h_right_spacer)


        self.horizontalLayout_2.addLayout(self.close_button_frame_h_layout)


        self.verticalLayout_4.addWidget(self.close_button_frame)


        self.verticalLayout.addWidget(self.main_widget_frame)


        self.retranslateUi(RenderingProgressDialog)

    # setupUi

    def retranslateUi(self, RenderingProgressDialog):
        RenderingProgressDialog.setWindowTitle(QCoreApplication.translate("RenderingProgressDialog", u"Rendering And Saving", None))
        self.status_message_label.setText(QCoreApplication.translate("RenderingProgressDialog", u"Rendering and saving ...", None))
        self.close_button.setText(QCoreApplication.translate("RenderingProgressDialog", u"Close", None))
    # retranslateUi

