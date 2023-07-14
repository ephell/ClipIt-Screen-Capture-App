# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MediaPlayerControls.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QVBoxLayout,
    QWidget)

from ._render_and_save_button import RenderAndSaveButton
from . import resource_rc
from . import resource_rc

class Ui_MediaPlayerControls(object):
    def setupUi(self, MediaPlayerControls):
        if not MediaPlayerControls.objectName():
            MediaPlayerControls.setObjectName(u"MediaPlayerControls")
        MediaPlayerControls.resize(362, 160)
        self.central_layout = QVBoxLayout(MediaPlayerControls)
        self.central_layout.setObjectName(u"central_layout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.play_button = QPushButton(MediaPlayerControls)
        self.play_button.setObjectName(u"play_button")
        icon = QIcon()
        icon.addFile(u":/icons/play.png", QSize(), QIcon.Normal, QIcon.Off)
        self.play_button.setIcon(icon)
        self.play_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.play_button)

        self.pause_button = QPushButton(MediaPlayerControls)
        self.pause_button.setObjectName(u"pause_button")
        icon1 = QIcon()
        icon1.addFile(u":/icons/pause.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pause_button.setIcon(icon1)
        self.pause_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.pause_button)

        self.reset_button = QPushButton(MediaPlayerControls)
        self.reset_button.setObjectName(u"reset_button")
        icon2 = QIcon()
        icon2.addFile(u":/icons/reset.png", QSize(), QIcon.Normal, QIcon.Off)
        self.reset_button.setIcon(icon2)
        self.reset_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.reset_button)

        self.render_and_save_button = RenderAndSaveButton(MediaPlayerControls)
        self.render_and_save_button.setObjectName(u"render_and_save_button")
        icon3 = QIcon()
        icon3.addFile(u":/icons/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.render_and_save_button.setIcon(icon3)
        self.render_and_save_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.render_and_save_button)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.volume_slider_icon_label = QLabel(MediaPlayerControls)
        self.volume_slider_icon_label.setObjectName(u"volume_slider_icon_label")
        self.volume_slider_icon_label.setMinimumSize(QSize(30, 30))
        self.volume_slider_icon_label.setMaximumSize(QSize(30, 30))
        self.volume_slider_icon_label.setPixmap(QPixmap(u":/icons/volume_slider_icon.png"))
        self.volume_slider_icon_label.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.volume_slider_icon_label)

        self.volume_slider = QSlider(MediaPlayerControls)
        self.volume_slider.setObjectName(u"volume_slider")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volume_slider.sizePolicy().hasHeightForWidth())
        self.volume_slider.setSizePolicy(sizePolicy)
        self.volume_slider.setMinimumSize(QSize(135, 0))
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.volume_slider)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.central_layout.addLayout(self.verticalLayout_2)


        self.retranslateUi(MediaPlayerControls)

        QMetaObject.connectSlotsByName(MediaPlayerControls)
    # setupUi

    def retranslateUi(self, MediaPlayerControls):
        MediaPlayerControls.setWindowTitle(QCoreApplication.translate("MediaPlayerControls", u"Media Player Controls", None))
        self.play_button.setText("")
        self.pause_button.setText("")
        self.reset_button.setText("")
        self.render_and_save_button.setText("")
        self.volume_slider_icon_label.setText("")
    # retranslateUi

