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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

from ._crop_button.crop_button import CropButton
from ._render_and_save_button.render_and_save_button import RenderAndSaveButton
from ._upload_button.upload_button import UploadButton
from ._volume_button.volume_button import VolumeButton
from . import resource_rc

class Ui_MediaPlayerControls(object):
    def setupUi(self, MediaPlayerControls):
        if not MediaPlayerControls.objectName():
            MediaPlayerControls.setObjectName(u"MediaPlayerControls")
        MediaPlayerControls.resize(494, 190)
        self.horizontalLayout = QHBoxLayout(MediaPlayerControls)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_4 = QSpacerItem(136, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

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

        self.volume_button = VolumeButton(MediaPlayerControls)
        self.volume_button.setObjectName(u"volume_button")
        icon3 = QIcon()
        icon3.addFile(u":/icons/volume_slider_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.volume_button.setIcon(icon3)
        self.volume_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.volume_button)

        self.crop_button = CropButton(MediaPlayerControls)
        self.crop_button.setObjectName(u"crop_button")
        icon4 = QIcon()
        icon4.addFile(u":/icons/crop.png", QSize(), QIcon.Normal, QIcon.Off)
        self.crop_button.setIcon(icon4)
        self.crop_button.setIconSize(QSize(30, 30))
        self.crop_button.setCheckable(True)

        self.horizontalLayout.addWidget(self.crop_button)

        self.render_and_save_button = RenderAndSaveButton(MediaPlayerControls)
        self.render_and_save_button.setObjectName(u"render_and_save_button")
        icon5 = QIcon()
        icon5.addFile(u":/icons/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.render_and_save_button.setIcon(icon5)
        self.render_and_save_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.render_and_save_button)

        self.upload_button = UploadButton(MediaPlayerControls)
        self.upload_button.setObjectName(u"upload_button")
        icon6 = QIcon()
        icon6.addFile(u":/icons/upload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.upload_button.setIcon(icon6)
        self.upload_button.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.upload_button)

        self.horizontalSpacer_5 = QSpacerItem(135, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


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

