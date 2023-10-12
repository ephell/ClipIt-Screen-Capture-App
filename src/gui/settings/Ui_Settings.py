# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Settings.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from .check_boxes.record_microphone_audio_check_box import RecordMicrophoneAudioCheckBox
from .check_boxes.record_speaker_audio_check_box import RecordSpeakerAudioCheckBox

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(450, 140)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Settings.sizePolicy().hasHeightForWidth())
        Settings.setSizePolicy(sizePolicy)
        Settings.setMinimumSize(QSize(450, 140))
        Settings.setMaximumSize(QSize(450, 140))
        self.verticalLayout = QVBoxLayout(Settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.captures_dir_path_group_box = QGroupBox(Settings)
        self.captures_dir_path_group_box.setObjectName(u"captures_dir_path_group_box")
        self.horizontalLayout = QHBoxLayout(self.captures_dir_path_group_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.dir_path_line_edit = QLineEdit(self.captures_dir_path_group_box)
        self.dir_path_line_edit.setObjectName(u"dir_path_line_edit")
        self.dir_path_line_edit.setFocusPolicy(Qt.NoFocus)
        self.dir_path_line_edit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.dir_path_line_edit)

        self.browse_button = QPushButton(self.captures_dir_path_group_box)
        self.browse_button.setObjectName(u"browse_button")

        self.horizontalLayout.addWidget(self.browse_button)


        self.verticalLayout.addWidget(self.captures_dir_path_group_box)

        self.audio_preferences_group_box = QGroupBox(Settings)
        self.audio_preferences_group_box.setObjectName(u"audio_preferences_group_box")
        self.horizontalLayout_2 = QHBoxLayout(self.audio_preferences_group_box)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.record_speaker_audio_check_box = RecordSpeakerAudioCheckBox(self.audio_preferences_group_box)
        self.record_speaker_audio_check_box.setObjectName(u"record_speaker_audio_check_box")
        self.record_speaker_audio_check_box.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.record_speaker_audio_check_box)

        self.record_microphone_audio_checkbox = RecordMicrophoneAudioCheckBox(self.audio_preferences_group_box)
        self.record_microphone_audio_checkbox.setObjectName(u"record_microphone_audio_checkbox")

        self.horizontalLayout_2.addWidget(self.record_microphone_audio_checkbox)


        self.verticalLayout.addWidget(self.audio_preferences_group_box)


        self.retranslateUi(Settings)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Settings", None))
        self.captures_dir_path_group_box.setTitle(QCoreApplication.translate("Settings", u"Captures Directory Path", None))
        self.browse_button.setText(QCoreApplication.translate("Settings", u"Browse", None))
        self.audio_preferences_group_box.setTitle(QCoreApplication.translate("Settings", u"Audio Preferences", None))
        self.record_speaker_audio_check_box.setText(QCoreApplication.translate("Settings", u"Record Speaker Audio", None))
        self.record_microphone_audio_checkbox.setText(QCoreApplication.translate("Settings", u"Record Microphone Audio", None))
    # retranslateUi
