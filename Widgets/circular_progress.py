from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QColor, QPainter, QPen, QFont, QPaintEvent
from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect



class CircularProgress\
            (QWidget):
    def __init__(self):
        super().__init__()
    
        # Custom Properties
        self.value = 0
        self.width = 200
        self.height = 200
        self.progress_width = 10
        self.progress_rounded_cap = True
        self.max_value = 100
        self.progress_color = QColor("#6B0B4A")
        #text
        self.enable_text = True
        self.font_family = "Segoe UI"
        self.font_size = 12
        self.suffix = "%"
        self.text_color = QColor("#498BD1")
        self.shadow = None  # Initialize here, even with None

        #BG
        self.enable_bg = True
        self.bg_color = QColor("#1F0E33")
    
        # set the default size without the layout
        self.resize(self.width, self.height)

        # Add Drop_shadow
    def add_shadow(self, enable):
        if enable:
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(15)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 80))
            self.setGraphicsEffect(self.shadow)
    #set value
    def set_value(self, value):
        self.value = value
        self.repaint() # render progress



        #paint event. design the circular progression bar

    def paintEvent(self, event: QPaintEvent) -> None:
        #set progress parameters
        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value

        #Painter
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing) #smoother edges when render
        paint.setFont(QFont(self.font_family, self.font_size))

        #Create Rectangle
        rect = QRect(0, 0, self.width, self.height)
        paint.setPen(Qt.PenStyle.NoPen)
        paint.drawRect(rect)

        #PEN
        pen = QPen()
        pen.setWidth(self.progress_width)
        #set round cap.
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        #Enable BG
        if self.enable_bg:
            pen.setColor(QColor(self.bg_color))
            paint.setPen(pen)
            paint.drawArc(int(margin), int(margin), int(width), int(height), 0, 360 * 16)

        #create Arc / circular progression bar
        pen.setColor(QColor(self.progress_color))  # Set the color back to progress_color
        paint.setPen(pen)
        paint.drawArc(int(margin), int(margin), int(width), int(height), -90 * 16, -int(value * 16))

        #Create Text
        pen.setColor(QColor(self.text_color))
        paint.setPen(pen)
        paint.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{self.value}{self.suffix}")

        #END
        paint.end()