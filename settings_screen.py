# .\settings_screen.py
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QSpinBox, QComboBox, QFormLayout, QTabWidget,
                             QCheckBox, QMessageBox)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSignal

class SettingsScreen(QWidget):
    """
    Settings screen for configuring system parameters.
    """

    # Signal when screen is closed
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("Settings")
        
        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#B0E0E6'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Default settings
        self.settings = {
            "warning_threshold": 75,
            "critical_threshold": 85,
            "update_interval": 15,  # minutes
            "fullscreen": True,
            "sensors": {
                "Sensor 1": {"enabled": True, "max_level": 100, "offset": 0},
                "Sensor 2": {"enabled": True, "max_level": 100, "offset": 0},
                "Sensor 3": {"enabled": True, "max_level": 100, "offset": 0}
            }
        }

        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """Creates the settings screen UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Top bar with back and save buttons
        top_bar_layout = QHBoxLayout()
        
        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(80, 30)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """)
        back_btn.clicked.connect(self.go_back)
        top_bar_layout.addWidget(back_btn)
        
        top_bar_layout.addStretch()
        
        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.setFixedSize(120, 30)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ECC71;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #27AE60; }
        """)
        save_btn.clicked.connect(self.save_settings)
        top_bar_layout.addWidget(save_btn)
        
        main_layout.addLayout(top_bar_layout)

        # Title
        title = QLabel("System Settings")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #f0f0f0;
                border: 1px solid #cccccc;
                padding: 8px 16px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
        """)

        # Create tabs
        alarm_tab = self.create_alarm_tab()
        general_tab = self.create_general_tab()
        sensor_tab = self.create_sensor_tab()
        
        self.tab_widget.addTab(alarm_tab, "Alarm Settings")
        self.tab_widget.addTab(general_tab, "General Settings")
        self.tab_widget.addTab(sensor_tab, "Sensor Settings")

        main_layout.addWidget(self.tab_widget)

    def create_alarm_tab(self):
        """Creates the alarm settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setSpacing(15)

        # Section title
        section_title = QLabel("Alarm Thresholds (%)")
        section_title.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(section_title)

        # Form for thresholds
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignLeft)
        form_layout.setVerticalSpacing(10)
        form_layout.setHorizontalSpacing(20)

        # Warning level
        warning_label = QLabel("Warning Level:")
        self.warning_spin = QSpinBox()
        self.warning_spin.setRange(10, 95)
        self.warning_spin.setSuffix("%")
        self.warning_spin.setFixedWidth(100)
        form_layout.addRow(warning_label, self.warning_spin)

        # Critical level
        critical_label = QLabel("Critical Level:")
        self.critical_spin = QSpinBox()
        self.critical_spin.setRange(20, 99)
        self.critical_spin.setSuffix("%")
        self.critical_spin.setFixedWidth(100)
        form_layout.addRow(critical_label, self.critical_spin)

        # Link the spin boxes: critical must be > warning
        self.warning_spin.valueChanged.connect(
            lambda val: self.critical_spin.setMinimum(val + 1))
        self.critical_spin.valueChanged.connect(
            lambda val: self.warning_spin.setMaximum(val - 1))

        layout.addLayout(form_layout)
        layout.addStretch()
        
        return tab

    def create_general_tab(self):
        """Creates the general settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setSpacing(15)

        # Update settings section
        update_title = QLabel("Update Settings")
        update_title.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(update_title)

        update_form = QFormLayout()
        update_form.setLabelAlignment(Qt.AlignLeft)
        update_form.setFormAlignment(Qt.AlignLeft)
        update_form.setVerticalSpacing(10)
        update_form.setHorizontalSpacing(20)

        interval_label = QLabel("Data Update Interval:")
        self.update_spin = QSpinBox()
        self.update_spin.setRange(1, 120)
        self.update_spin.setSuffix(" min")
        self.update_spin.setFixedWidth(100)
        update_form.addRow(interval_label, self.update_spin)
        
        layout.addLayout(update_form)
        
        # Display settings section
        display_title = QLabel("Display Settings")
        display_title.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(display_title)
        
        self.fullscreen_check = QCheckBox("Start in fullscreen mode")
        layout.addWidget(self.fullscreen_check)
        
        layout.addStretch()
        
        return tab

    def create_sensor_tab(self):
        """Creates the sensor settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setSpacing(15)

        # Sensor selection
        sensor_layout = QHBoxLayout()
        config_label = QLabel("Configure Sensor:")
        self.sensor_combo = QComboBox()
        self.sensor_combo.setFixedWidth(150)
        self.sensor_combo.addItems(list(self.settings["sensors"].keys()))
        self.sensor_combo.currentTextChanged.connect(self.update_sensor_ui_fields)
        sensor_layout.addWidget(config_label)
        sensor_layout.addWidget(self.sensor_combo)
        sensor_layout.addStretch()
        layout.addLayout(sensor_layout)

        # Sensor parameters section
        params_title = QLabel("Sensor Parameters")
        params_title.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(params_title)

        # Enable checkbox
        self.sensor_enabled = QCheckBox("Enable this sensor")
        layout.addWidget(self.sensor_enabled)

        # Form for sensor settings
        sensor_form = QFormLayout()
        sensor_form.setLabelAlignment(Qt.AlignLeft)
        sensor_form.setFormAlignment(Qt.AlignLeft)
        sensor_form.setVerticalSpacing(10)
        sensor_form.setHorizontalSpacing(20)

        # Max level
        max_level_label = QLabel("Max Physical Level:")
        self.max_level_spin = QSpinBox()
        self.max_level_spin.setRange(10, 1000)
        self.max_level_spin.setSuffix(" cm")
        self.max_level_spin.setFixedWidth(100)
        sensor_form.addRow(max_level_label, self.max_level_spin)

        # Offset
        offset_label = QLabel("Reading Offset:")
        self.offset_spin = QSpinBox()
        self.offset_spin.setRange(-100, 100)
        self.offset_spin.setSuffix(" cm")
        self.offset_spin.setFixedWidth(100)
        sensor_form.addRow(offset_label, self.offset_spin)

        layout.addLayout(sensor_form)
        
        # Calibration button
        calibrate_btn = QPushButton("Calibrate Sensor")
        calibrate_btn.setFixedWidth(120)
        calibrate_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """)
        calibrate_btn.clicked.connect(self.calibrate_sensor)
        layout.addWidget(calibrate_btn)
        
        layout.addStretch()
        
        return tab

    def load_settings(self):
        """Loads values from settings into UI fields"""
        try:
            # Alarm tab
            self.warning_spin.setValue(self.settings["warning_threshold"])
            self.critical_spin.setValue(self.settings["critical_threshold"])
            self.warning_spin.valueChanged.emit(self.settings["warning_threshold"])
            self.critical_spin.valueChanged.emit(self.settings["critical_threshold"])

            # General tab
            self.update_spin.setValue(self.settings["update_interval"])
            self.fullscreen_check.setChecked(self.settings["fullscreen"])

            # Sensor tab
            if self.sensor_combo.count() > 0:
                self.update_sensor_ui_fields(self.sensor_combo.currentText())
        except KeyError as e:
            print(f"Warning: Missing setting key during load: {e}")
        except Exception as e:
            print(f"Error loading settings into UI: {e}")

    def update_sensor_ui_fields(self, sensor_name):
        """Updates sensor settings fields when selection changes"""
        if sensor_name in self.settings["sensors"]:
            sensor_config = self.settings["sensors"][sensor_name]
            try:
                self.sensor_enabled.setChecked(sensor_config["enabled"])
                self.max_level_spin.setValue(sensor_config["max_level"])
                self.offset_spin.setValue(sensor_config["offset"])
            except KeyError as e:
                print(f"Warning: Missing setting key for sensor '{sensor_name}': {e}")
            except Exception as e:
                print(f"Error updating sensor UI fields for '{sensor_name}': {e}")

    def save_settings(self):
        """Saves the current UI field values to settings"""
        try:
            # Save alarm settings
            self.settings["warning_threshold"] = self.warning_spin.value()
            self.settings["critical_threshold"] = self.critical_spin.value()

            # Save general settings
            self.settings["update_interval"] = self.update_spin.value()
            self.settings["fullscreen"] = self.fullscreen_check.isChecked()

            # Save current sensor settings
            current_sensor_name = self.sensor_combo.currentText()
            if current_sensor_name in self.settings["sensors"]:
                sensor_config = self.settings["sensors"][current_sensor_name]
                sensor_config["enabled"] = self.sensor_enabled.isChecked()
                sensor_config["max_level"] = self.max_level_spin.value()
                sensor_config["offset"] = self.offset_spin.value()

            print("Settings saved:", self.settings)
            QMessageBox.information(self, "Settings Saved",
                                   "Your settings have been saved.")

        except Exception as e:
            print(f"Error saving settings: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")

    def go_back(self):
        """Closes the settings screen"""
        if self.parent_window:
            self.parent_window.showFullScreen()
        self.close()

    def calibrate_sensor(self):
        """Placeholder for sensor calibration process"""
        sensor_name = self.sensor_combo.currentText()
        QMessageBox.information(self, "Calibration",
                               f"Calibration procedure for '{sensor_name}' would start here.")

    def closeEvent(self, event):
        """Handles window close event"""
        self.closed.emit()
        super().closeEvent(event)


# Test code
if __name__ == "__main__":
    app = QApplication(sys.argv)
    settings = SettingsScreen()
    settings.showFullScreen()
    sys.exit(app.exec_())