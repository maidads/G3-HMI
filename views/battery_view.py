from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal


class BatteryBarWidget(QtWidgets.QWidget):
    """Widget that displays battery level as colored bars"""

    def __init__(self, steps=5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )

        # Define class parameters
        self._padding = 5
        self._bar_solid_percent = 0.6
        self.n_steps = steps
        self._value = 0  # Store the value internally

        # Define the fixed saturation level (75%)
        self._saturation = 0.75

        # Base colors for the gradient: top (green) to bottom (red)
        self._base_colors = [
            '#ff0000',  # Red (bottom)
            '#ff7f00',  # Orange
            '#ffff00',  # Yellow
            '#7fff00',  # Green-yellow
            '#00ff00',  # Green (top)
        ]

        # Apply saturation to create the adjusted colors
        self.steps = []
        for color_hex in self._base_colors:
            color = QtGui.QColor(color_hex)
            h, s, l, a = color.getHslF()
            s = min(1.0, s * self._saturation)  # Apply 75% saturation
            color.setHslF(h, s, l, a)
            self.steps.append(color.name())

        # Background color
        self._background_color = QtGui.QColor("#0C495D")

    def sizeHint(self):
        return QtCore.QSize(40, 120)

    def set_value(self, value):
        self._value = value
        self.update()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        brush = QtGui.QBrush()
        brush.setColor(self._background_color)
        brush.setStyle(Qt.BrushStyle.SolidPattern)

        # Draw rounded background rectangle
        path = QtGui.QPainterPath()
        rect = QtCore.QRectF(0, 0, self.width(), self.height())
        path.addRoundedRect(rect, 10, 10)
        painter.fillPath(path, brush)

        # Define our canvas.
        d_height = self.height() - (self._padding * 2)
        d_width = self.width() - (self._padding * 2)

        # Draw the bars.
        step_size = d_height / self.n_steps
        bar_height = int(step_size * self._bar_solid_percent)
        bar_spacer = int(step_size * (1 - self._bar_solid_percent) / 2)

        # Calculate the number of steps to draw based on the current value
        n_steps_to_draw = int(self._value / 100.0 * self.n_steps)

        for n in range(n_steps_to_draw):
            # Make sure we don't go out of index range for the steps list
            color_index = min(n, len(self.steps) - 1)
            brush.setColor(QtGui.QColor(self.steps[color_index]))

            y_pos = int(self._padding + d_height - ((1 + n) * step_size) + bar_spacer)

            # Create rounded rectangle for each bar
            bar_path = QtGui.QPainterPath()
            bar_rect = QtCore.QRectF(
                self._padding,
                y_pos,
                d_width,
                bar_height
            )
            bar_path.addRoundedRect(bar_rect, 5, 5)  # 5px corner radius
            painter.fillPath(bar_path, brush)

        painter.end()


class BatteryView(QtWidgets.QWidget):
    """Main view for the battery monitor"""

    # Signal for user interactions
    powerToggleRequested = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout()

        # Battery level visual indicator
        self._bar = BatteryBarWidget(steps=5)
        layout.addWidget(self._bar)

        # Status label
        self._status_label = QtWidgets.QLabel("Battery Status: Initializing...")
        layout.addWidget(self._status_label)

        # Control button for mock batteries
        self._power_button = QtWidgets.QPushButton("🔌 Toggle Power")
        self._power_button.clicked.connect(self._on_power_toggle)
        layout.addWidget(self._power_button)

        self.setLayout(layout)
        self.resize(160, 300)
        self.setWindowTitle("Battery Monitor")

    def update_display(self, battery_state):
        """Update the view with new battery information"""
        percent = battery_state["percent"]
        plugged = battery_state["plugged"]

        # Update the bar
        self._bar.set_value(percent)

        # Update status label
        status_text = f"Battery: {percent:.1f}% "
        status_text += "🔌 Charging" if plugged else "🔋 Discharging"
        self._status_label.setText(status_text)

    def _on_power_toggle(self):
        """Handle power toggle button click"""
        self.powerToggleRequested.emit()

    def show_critical_warning(self):
        """Show a warning when battery level is critical"""
        QtWidgets.QMessageBox.warning(
            self,
            "Battery Low",
            "⚠️ Warning: Battery level is critically low!",
            QtWidgets.QMessageBox.StandardButton.Ok
        )