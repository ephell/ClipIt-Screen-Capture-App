# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

from .audio_preferences.record_microphone_audio_check_box import RecordMicrophoneAudioCheckBox
from .audio_preferences.record_speaker_audio_check_box import RecordSpeakerAudioCheckBox
from .captures_directory.browse_button import BrowseButton
from .captures_directory.line_edit import CapturesDirectoryLineEdit
from .hotkeys.screenshot.line_edit import ScreenshotLineEdit
from .hotkeys.screenshot.status_label import ScreenshotStatusLabel
from .hotkeys.start_stop_recording.line_edit import StartStopRecordingLineEdit
from .hotkeys.start_stop_recording.status_label import StartStopRecordingStatusLabel

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        if not SettingsWindow.objectName():
            SettingsWindow.setObjectName(u"SettingsWindow")
        SettingsWindow.resize(425, 270)
        SettingsWindow.setMinimumSize(QSize(425, 270))
        SettingsWindow.setMaximumSize(QSize(425, 270))
        self.verticalLayout = QVBoxLayout(SettingsWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.captures_dir_group_box = QGroupBox(SettingsWindow)
        self.captures_dir_group_box.setObjectName(u"captures_dir_group_box")
        self.horizontalLayout = QHBoxLayout(self.captures_dir_group_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.captures_dir_line_edit = CapturesDirectoryLineEdit(self.captures_dir_group_box)
        self.captures_dir_line_edit.setObjectName(u"captures_dir_line_edit")
        self.captures_dir_line_edit.setFocusPolicy(Qt.NoFocus)
        self.captures_dir_line_edit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.captures_dir_line_edit)

        self.browse_button = BrowseButton(self.captures_dir_group_box)
        self.browse_button.setObjectName(u"browse_button")

        self.horizontalLayout.addWidget(self.browse_button)


        self.verticalLayout.addWidget(self.captures_dir_group_box)

        self.audio_preferences_group_box = QGroupBox(SettingsWindow)
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

        self.hotkeys_group_box = QGroupBox(SettingsWindow)
        self.hotkeys_group_box.setObjectName(u"hotkeys_group_box")
        self.verticalLayout_5 = QVBoxLayout(self.hotkeys_group_box)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.screenshot_label = QLabel(self.hotkeys_group_box)
        self.screenshot_label.setObjectName(u"screenshot_label")

        self.verticalLayout_2.addWidget(self.screenshot_label)

        self.start_stop_recording_label = QLabel(self.hotkeys_group_box)
        self.start_stop_recording_label.setObjectName(u"start_stop_recording_label")

        self.verticalLayout_2.addWidget(self.start_stop_recording_label)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.screenshot_line_edit = ScreenshotLineEdit(self.hotkeys_group_box)
        self.screenshot_line_edit.setObjectName(u"screenshot_line_edit")
        self.screenshot_line_edit.setMinimumSize(QSize(0, 27))
        self.screenshot_line_edit.setMaximumSize(QSize(16777215, 27))

        self.verticalLayout_3.addWidget(self.screenshot_line_edit)

        self.start_stop_recording_line_edit = StartStopRecordingLineEdit(self.hotkeys_group_box)
        self.start_stop_recording_line_edit.setObjectName(u"start_stop_recording_line_edit")
        self.start_stop_recording_line_edit.setMinimumSize(QSize(0, 27))
        self.start_stop_recording_line_edit.setMaximumSize(QSize(16777215, 27))
        self.start_stop_recording_line_edit.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.start_stop_recording_line_edit)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(9)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.screenshot_status_label = ScreenshotStatusLabel(self.hotkeys_group_box)
        self.screenshot_status_label.setObjectName(u"screenshot_status_label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.screenshot_status_label.sizePolicy().hasHeightForWidth())
        self.screenshot_status_label.setSizePolicy(sizePolicy)
        self.screenshot_status_label.setMinimumSize(QSize(10, 10))
        self.screenshot_status_label.setMaximumSize(QSize(10, 10))

        self.verticalLayout_6.addWidget(self.screenshot_status_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.verticalLayout_4.addLayout(self.verticalLayout_6)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.start_stop_recording_status_label = StartStopRecordingStatusLabel(self.hotkeys_group_box)
        self.start_stop_recording_status_label.setObjectName(u"start_stop_recording_status_label")
        sizePolicy.setHeightForWidth(self.start_stop_recording_status_label.sizePolicy().hasHeightForWidth())
        self.start_stop_recording_status_label.setSizePolicy(sizePolicy)
        self.start_stop_recording_status_label.setMinimumSize(QSize(10, 10))
        self.start_stop_recording_status_label.setMaximumSize(QSize(10, 10))

        self.verticalLayout_7.addWidget(self.start_stop_recording_status_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.verticalLayout_4.addLayout(self.verticalLayout_7)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 2)

        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.hotkeys_group_box)


        self.retranslateUi(SettingsWindow)

        QMetaObject.connectSlotsByName(SettingsWindow)
    # setupUi

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(QCoreApplication.translate("SettingsWindow", u"SettingsWindow", None))
        self.captures_dir_group_box.setTitle(QCoreApplication.translate("SettingsWindow", u"Captures Directory", None))
        self.browse_button.setText(QCoreApplication.translate("SettingsWindow", u"Browse", None))
        self.audio_preferences_group_box.setTitle(QCoreApplication.translate("SettingsWindow", u"Audio Preferences", None))
        self.record_speaker_audio_check_box.setText(QCoreApplication.translate("SettingsWindow", u"Record Speaker Audio", None))
        self.record_microphone_audio_checkbox.setText(QCoreApplication.translate("SettingsWindow", u"Record Microphone Audio", None))
        self.hotkeys_group_box.setTitle(QCoreApplication.translate("SettingsWindow", u"Hotkeys", None))
        self.screenshot_label.setText(QCoreApplication.translate("SettingsWindow", u"Screenshot", None))
        self.start_stop_recording_label.setText(QCoreApplication.translate("SettingsWindow", u"Start/Stop Recording", None))
    # retranslateUi

