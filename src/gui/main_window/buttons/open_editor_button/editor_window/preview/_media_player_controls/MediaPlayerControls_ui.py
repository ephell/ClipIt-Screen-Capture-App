# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MediaPlayerControls.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from ._crop_button.crop_button import CropButton
from ._render_and_save_button.render_and_save_button import RenderAndSaveButton
from ._upload_button.upload_button import UploadButton
from ._volume_button.volume_button import VolumeButton
from . import media_player_controls_icons_rc

class Ui_MediaPlayerControls(object):
    def setupUi(self, MediaPlayerControls):
        if not MediaPlayerControls.objectName():
            MediaPlayerControls.setObjectName(u"MediaPlayerControls")
        MediaPlayerControls.resize(653, 78)
        MediaPlayerControls.setMinimumSize(QSize(0, 78))
        MediaPlayerControls.setMaximumSize(QSize(16777215, 78))
        self.verticalLayout_2 = QVBoxLayout(MediaPlayerControls)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_4 = QSpacerItem(80, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.button_frame = QFrame(MediaPlayerControls)
        self.button_frame.setObjectName(u"button_frame")
        self.button_frame.setMinimumSize(QSize(425, 0))
        self.button_frame.setMaximumSize(QSize(425, 16777215))
        self.button_frame.setFrameShape(QFrame.StyledPanel)
        self.button_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.button_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.play_button = QPushButton(self.button_frame)
        self.play_button.setObjectName(u"play_button")
        icon = QIcon()
        icon.addFile(u":/icons/play.png", QSize(), QIcon.Normal, QIcon.Off)
        self.play_button.setIcon(icon)
        self.play_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.play_button)

        self.pause_button = QPushButton(self.button_frame)
        self.pause_button.setObjectName(u"pause_button")
        icon1 = QIcon()
        icon1.addFile(u":/icons/pause.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pause_button.setIcon(icon1)
        self.pause_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.pause_button)

        self.reset_button = QPushButton(self.button_frame)
        self.reset_button.setObjectName(u"reset_button")
        icon2 = QIcon()
        icon2.addFile(u":/icons/reset.png", QSize(), QIcon.Normal, QIcon.Off)
        self.reset_button.setIcon(icon2)
        self.reset_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.reset_button)

        self.volume_button = VolumeButton(self.button_frame)
        self.volume_button.setObjectName(u"volume_button")
        icon3 = QIcon()
        icon3.addFile(u":/icons/volume_slider_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.volume_button.setIcon(icon3)
        self.volume_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.volume_button)

        self.crop_button = CropButton(self.button_frame)
        self.crop_button.setObjectName(u"crop_button")
        self.crop_button.setStyleSheet(u"")
        icon4 = QIcon()
        icon4.addFile(u":/icons/crop.png", QSize(), QIcon.Normal, QIcon.Off)
        self.crop_button.setIcon(icon4)
        self.crop_button.setIconSize(QSize(30, 30))
        self.crop_button.setCheckable(True)

        self.horizontalLayout.addWidget(self.crop_button)

        self.render_and_save_button = RenderAndSaveButton(self.button_frame)
        self.render_and_save_button.setObjectName(u"render_and_save_button")
        icon5 = QIcon()
        icon5.addFile(u":/icons/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.render_and_save_button.setIcon(icon5)
        self.render_and_save_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.render_and_save_button)

        self.upload_button = UploadButton(self.button_frame)
        self.upload_button.setObjectName(u"upload_button")
        icon6 = QIcon()
        icon6.addFile(u":/icons/upload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.upload_button.setIcon(icon6)
        self.upload_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.upload_button)


        self.horizontalLayout_3.addWidget(self.button_frame, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.horizontalSpacer_5 = QSpacerItem(80, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.retranslateUi(MediaPlayerControls)

        QMetaObject.connectSlotsByName(MediaPlayerControls)
    # setupUi

    def retranslateUi(self, MediaPlayerControls):
        MediaPlayerControls.setWindowTitle(QCoreApplication.translate("MediaPlayerControls", u"Media Player Controls", None))
        self.play_button.setText("")
        self.pause_button.setText("")
        self.reset_button.setText("")
        self.volume_button.setText("")
        self.crop_button.setText("")
        self.render_and_save_button.setText("")
        self.upload_button.setText("")
    # retranslateUi

