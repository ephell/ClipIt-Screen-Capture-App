# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from .buttons.screenchot_button.screenshot_button import ScreenshotButton
from .buttons.select_area_button.select_area_button import SelectAreaButton
from .check_boxes.record_microphone_audio_check_box import RecordMicrophoneAudioCheckBox
from .check_boxes.record_speaker_audio_check_box import RecordSpeakerAudioCheckBox

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(409, 391)
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setObjectName(u"central_layout")
        self.video_capture_groupbox = QGroupBox(self.central_widget)
        self.video_capture_groupbox.setObjectName(u"video_capture_groupbox")
        self.video_capture_groupbox_layout = QVBoxLayout(self.video_capture_groupbox)
        self.video_capture_groupbox_layout.setSpacing(6)
        self.video_capture_groupbox_layout.setObjectName(u"video_capture_groupbox_layout")
        self.video_capture_groupbox_layout.setContentsMargins(0, 0, 0, 0)
        self.video_capture_main_frame = QFrame(self.video_capture_groupbox)
        self.video_capture_main_frame.setObjectName(u"video_capture_main_frame")
        self.video_capture_main_frame.setFrameShape(QFrame.StyledPanel)
        self.video_capture_main_frame.setFrameShadow(QFrame.Raised)
        self.viceo_capture_main_frame_layout = QVBoxLayout(self.video_capture_main_frame)
        self.viceo_capture_main_frame_layout.setSpacing(0)
        self.viceo_capture_main_frame_layout.setObjectName(u"viceo_capture_main_frame_layout")
        self.viceo_capture_main_frame_layout.setContentsMargins(9, -1, -1, -1)
        self.video_capture_timer_frame = QFrame(self.video_capture_main_frame)
        self.video_capture_timer_frame.setObjectName(u"video_capture_timer_frame")
        self.video_capture_timer_frame.setFrameShape(QFrame.StyledPanel)
        self.video_capture_timer_frame.setFrameShadow(QFrame.Raised)
        self.video_capture_timer_frame_layout = QHBoxLayout(self.video_capture_timer_frame)
        self.video_capture_timer_frame_layout.setObjectName(u"video_capture_timer_frame_layout")
        self.video_capture_timer_frame_layout.setContentsMargins(-1, 9, -1, 9)
        self.video_capture_timer_left_h_spacer = QSpacerItem(113, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.video_capture_timer_frame_layout.addItem(self.video_capture_timer_left_h_spacer)

        self.video_capture_duration_label = QLabel(self.video_capture_timer_frame)
        self.video_capture_duration_label.setObjectName(u"video_capture_duration_label")
        font = QFont()
        font.setPointSize(23)
        font.setBold(True)
        self.video_capture_duration_label.setFont(font)

        self.video_capture_timer_frame_layout.addWidget(self.video_capture_duration_label)

        self.video_capture_timer_right_h_spacer = QSpacerItem(113, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.video_capture_timer_frame_layout.addItem(self.video_capture_timer_right_h_spacer)


        self.viceo_capture_main_frame_layout.addWidget(self.video_capture_timer_frame)

        self.video_capture_controls_and_settings_container_frame = QFrame(self.video_capture_main_frame)
        self.video_capture_controls_and_settings_container_frame.setObjectName(u"video_capture_controls_and_settings_container_frame")
        self.video_capture_controls_and_settings_container_frame.setFrameShape(QFrame.StyledPanel)
        self.video_capture_controls_and_settings_container_frame.setFrameShadow(QFrame.Raised)
        self.video_capture_controls_and_settings_container_frame_layout = QHBoxLayout(self.video_capture_controls_and_settings_container_frame)
        self.video_capture_controls_and_settings_container_frame_layout.setObjectName(u"video_capture_controls_and_settings_container_frame_layout")
        self.video_capture_controls_and_settings_container_frame_layout.setContentsMargins(0, -1, 0, -1)
        self.video_capture_controls_group_box = QGroupBox(self.video_capture_controls_and_settings_container_frame)
        self.video_capture_controls_group_box.setObjectName(u"video_capture_controls_group_box")
        self.video_capture_controls_group_box_layout = QVBoxLayout(self.video_capture_controls_group_box)
        self.video_capture_controls_group_box_layout.setObjectName(u"video_capture_controls_group_box_layout")
        self.select_area_button = SelectAreaButton(self.video_capture_controls_group_box)
        self.select_area_button.setObjectName(u"select_area_button")

        self.video_capture_controls_group_box_layout.addWidget(self.select_area_button)

        self.start_stop_button_h_layout = QHBoxLayout()
        self.start_stop_button_h_layout.setObjectName(u"start_stop_button_h_layout")
        self.start_button = QPushButton(self.video_capture_controls_group_box)
        self.start_button.setObjectName(u"start_button")

        self.start_stop_button_h_layout.addWidget(self.start_button)

        self.stop_button = QPushButton(self.video_capture_controls_group_box)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setEnabled(False)

        self.start_stop_button_h_layout.addWidget(self.stop_button)


        self.video_capture_controls_group_box_layout.addLayout(self.start_stop_button_h_layout)


        self.video_capture_controls_and_settings_container_frame_layout.addWidget(self.video_capture_controls_group_box)

        self.video_capture_audio_preferences_group_box = QGroupBox(self.video_capture_controls_and_settings_container_frame)
        self.video_capture_audio_preferences_group_box.setObjectName(u"video_capture_audio_preferences_group_box")
        self.video_capture_audio_preferences_group_box_layout = QVBoxLayout(self.video_capture_audio_preferences_group_box)
        self.video_capture_audio_preferences_group_box_layout.setObjectName(u"video_capture_audio_preferences_group_box_layout")
        self.record_speaker_audio_check_box = RecordSpeakerAudioCheckBox(self.video_capture_audio_preferences_group_box)
        self.record_speaker_audio_check_box.setObjectName(u"record_speaker_audio_check_box")
        self.record_speaker_audio_check_box.setEnabled(True)

        self.video_capture_audio_preferences_group_box_layout.addWidget(self.record_speaker_audio_check_box)

        self.record_microphone_audio_checkbox = RecordMicrophoneAudioCheckBox(self.video_capture_audio_preferences_group_box)
        self.record_microphone_audio_checkbox.setObjectName(u"record_microphone_audio_checkbox")

        self.video_capture_audio_preferences_group_box_layout.addWidget(self.record_microphone_audio_checkbox)


        self.video_capture_controls_and_settings_container_frame_layout.addWidget(self.video_capture_audio_preferences_group_box)


        self.viceo_capture_main_frame_layout.addWidget(self.video_capture_controls_and_settings_container_frame)


        self.video_capture_groupbox_layout.addWidget(self.video_capture_main_frame)


        self.central_layout.addWidget(self.video_capture_groupbox)

        self.central_widget_v_spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.central_layout.addItem(self.central_widget_v_spacer)

        self.other_capture_and_miscellaneous_h_layout = QHBoxLayout()
        self.other_capture_and_miscellaneous_h_layout.setObjectName(u"other_capture_and_miscellaneous_h_layout")
        self.other_capture_and_miscellaneous_h_layout.setContentsMargins(-1, -1, -1, 9)
        self.other_capture_group_box = QGroupBox(self.central_widget)
        self.other_capture_group_box.setObjectName(u"other_capture_group_box")
        self.other_capture_group_box_layout = QVBoxLayout(self.other_capture_group_box)
        self.other_capture_group_box_layout.setObjectName(u"other_capture_group_box_layout")
        self.screenshot_button = ScreenshotButton(self.other_capture_group_box)
        self.screenshot_button.setObjectName(u"screenshot_button")

        self.other_capture_group_box_layout.addWidget(self.screenshot_button)

        self.make_a_gif_button = QPushButton(self.other_capture_group_box)
        self.make_a_gif_button.setObjectName(u"make_a_gif_button")

        self.other_capture_group_box_layout.addWidget(self.make_a_gif_button)

        self.other_capture_group_box_v_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.other_capture_group_box_layout.addItem(self.other_capture_group_box_v_spacer)


        self.other_capture_and_miscellaneous_h_layout.addWidget(self.other_capture_group_box)

        self.miscellaneous_group_box = QGroupBox(self.central_widget)
        self.miscellaneous_group_box.setObjectName(u"miscellaneous_group_box")
        self.miscellaneous_group_box_layout = QVBoxLayout(self.miscellaneous_group_box)
        self.miscellaneous_group_box_layout.setObjectName(u"miscellaneous_group_box_layout")
        self.open_editor_button = QPushButton(self.miscellaneous_group_box)
        self.open_editor_button.setObjectName(u"open_editor_button")

        self.miscellaneous_group_box_layout.addWidget(self.open_editor_button)

        self.open_capture_folder_button = QPushButton(self.miscellaneous_group_box)
        self.open_capture_folder_button.setObjectName(u"open_capture_folder_button")

        self.miscellaneous_group_box_layout.addWidget(self.open_capture_folder_button)

        self.open_settings_button = QPushButton(self.miscellaneous_group_box)
        self.open_settings_button.setObjectName(u"open_settings_button")

        self.miscellaneous_group_box_layout.addWidget(self.open_settings_button)


        self.other_capture_and_miscellaneous_h_layout.addWidget(self.miscellaneous_group_box)


        self.central_layout.addLayout(self.other_capture_and_miscellaneous_h_layout)

        MainWindow.setCentralWidget(self.central_widget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ClipIt", None))
        self.video_capture_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Video Capture", None))
        self.video_capture_duration_label.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.video_capture_controls_group_box.setTitle(QCoreApplication.translate("MainWindow", u"Controls", None))
        self.select_area_button.setText(QCoreApplication.translate("MainWindow", u"Select Capture Area", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.video_capture_audio_preferences_group_box.setTitle(QCoreApplication.translate("MainWindow", u"Audio Preferences", None))
        self.record_speaker_audio_check_box.setText(QCoreApplication.translate("MainWindow", u"Record Speaker Audio", None))
        self.record_microphone_audio_checkbox.setText(QCoreApplication.translate("MainWindow", u"Record Microphone Audio", None))
        self.other_capture_group_box.setTitle(QCoreApplication.translate("MainWindow", u"Other Capture", None))
        self.screenshot_button.setText(QCoreApplication.translate("MainWindow", u"Screenshot", None))
        self.make_a_gif_button.setText(QCoreApplication.translate("MainWindow", u"Make a GIF", None))
        self.miscellaneous_group_box.setTitle(QCoreApplication.translate("MainWindow", u"Miscellaneous", None))
        self.open_editor_button.setText(QCoreApplication.translate("MainWindow", u"Open Editor", None))
        self.open_capture_folder_button.setText(QCoreApplication.translate("MainWindow", u"Open Capture Folder", None))
        self.open_settings_button.setText(QCoreApplication.translate("MainWindow", u"Open Settings", None))
    # retranslateUi

