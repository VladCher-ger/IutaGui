
from PyQt6 import QtWidgets, QtCore, QtGui

from PyQt6.QtCore import QEvent, QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QDateTime, QTime, QDate
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QDateTimeEdit,
    QDialogButtonBox,
    QDialog,
    QCalendarWidget,
    QTimeEdit,
    QPushButton
    
    
)

import numpy as np

from Guiresource import colorpalette 
from Guiresource.matplotFigure import PlotCanvas


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_gui()
    
    def init_gui(self): 
        ##### window init

        


        MainLayout = QtWidgets.QHBoxLayout()
        RightGraphlayout = QtWidgets.QVBoxLayout()
        RightGraphlayoutTopPart = QtWidgets.QHBoxLayout()

        LeftLayout = QtWidgets.QVBoxLayout()

        ButtonLayout1 = QtWidgets.QGridLayout()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        central_widget = QWidget()
        # This container holds the window contents, so we can style it.
        central_widget.setObjectName("Container")
        central_widget.setStyleSheet(
            """#Container {
            background: qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #594174 stop:0.5 #8D095E stop:1 #07AF3B);
            border-radius: 5px;
        }
        QPushButton { background-color: #594174 }
        QPushButton:hover { background-color: qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #594174 stop:1 #8D095E) }
        QPushButton:pressed { background-color: qlineargradient(x1:0 y1:0, x2:1 y2:1,  stop:0 #8D095E stop:1 #07AF3B) }
        """
        )
        self.title_bar = CustomTitleBar(self)

        self.customize_graphs()
        self.define_buttons()
        self.define_list()

        #self.make_logo()

        MainLayout.setContentsMargins(11, 11, 11, 11)

        centra_widget_layout = QVBoxLayout()
        centra_widget_layout.setContentsMargins(0, 0, 0, 0)
        centra_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        centra_widget_layout.addWidget(self.title_bar)
        
        
        #LogoLayout_demo.addWidget(self.Logo_demo,)

        ButtonLayout1.addWidget(self.LoadData,0,0)
        ButtonLayout1.addWidget(self.ResetPlot,0,1)

        RightGraphlayout.addWidget(self.plotWidget)

        LeftLayout.addLayout(ButtonLayout1)

        layout = QVBoxLayout()
        
        self.datetime_btn = QPushButton("Select Start time")
        self.datetime_btn.clicked.connect(self.show_dialog)
        
        self.result_label = QLabel("No date/time selected")

        self.datetime_btn_end = QPushButton("End Start time")
        self.datetime_btn_end.clicked.connect(self.show_dialog_end)
        
        self.result_label_end = QLabel("No date/time selected")

        layout.addWidget(self.datetime_btn)
        layout.addWidget(self.result_label)
        layout.addWidget(self.datetime_btn_end)
        layout.addWidget(self.result_label_end)

        LeftLayout.addLayout(layout)

        LeftLayout.addWidget(self.list)
        

        MainLayout.addLayout(LeftLayout)
        MainLayout.addLayout(RightGraphlayout)
        

 
        centra_widget_layout.addLayout(MainLayout)

        central_widget.setLayout(centra_widget_layout)

        self.setCentralWidget(central_widget)

    def define_list(self):

        self.list = QtWidgets.QListWidget()
        self.list.setFixedWidth(300)


    def define_buttons(self):

        self.LoadData = QtWidgets.QPushButton("Load data")
        self.ResetPlot = QtWidgets.QPushButton("Reset plot")



        self.LoadData.setFixedSize(QSize(150,100))
        self.ResetPlot.setFixedSize(QSize(150,100))

        self.LoadData.setFont(QtGui.QFont("Times", 14))
        self.ResetPlot.setFont(QtGui.QFont("Times", 14))

    def show_dialog(self):
        self.dialog = DateTimeDialog(self)
        if self.dialog.exec():
            datetime = self.dialog.get_datetime()
            self.datetime_start= datetime.toString('yyyy-MM-dd HH:mm:ss')

            self.result_label.setText(
                f"Start: {datetime.toString('yyyy-MM-dd HH:mm')}"
            )
    def show_dialog_end(self):
        self.dialog_end = DateTimeDialog(self)
        if self.dialog_end.exec():
            datetime = self.dialog_end.get_datetime()
            self.datetime_end = datetime.toString('yyyy-MM-dd HH:mm:ss')
            self.result_label_end.setText(
                f"End: {datetime.toString('yyyy-MM-dd HH:mm')}"
            )

    def customize_graphs(self):
        
        self.plotWidget = PlotCanvas(self, width=8, height=6)


    def changeEvent(self, event):
        
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
            
        super().changeEvent(event)
        event.accept()

    def window_state_changed(self, state):
        self.title_bar.normal_button.setVisible(state == Qt.WindowState.WindowMaximized)
        self.title_bar.max_button.setVisible(state != Qt.WindowState.WindowMaximized)

        

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()





class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initial_pos = None
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setSpacing(2)
        
        

        # Min button
        title_bar_layout.addStretch()
        self.min_button = QToolButton(self)
        min_icon = QIcon()
        min_icon.addFile("./Icons/min.svg")
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().showMinimized)

        # Max button
        self.max_button = QToolButton(self)
        max_icon = QIcon()
        max_icon.addFile("./Icons/max.svg")
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window().showMaximized)

        # Close button
        self.close_button = QToolButton(self)
        close_icon = QIcon()
        close_icon.addFile("./Icons/close.svg")  # Close has only a single state.
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        # Normal button
        self.normal_button = QToolButton(self)
        normal_icon = QIcon()
        normal_icon.addFile("./Icons/max.svg")
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)
        # Add buttons
        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            # button.setAlignment(Qt.AlignmentFlag.AlignTop)
            button.setFixedSize(QSize(20, 20))
            button.setStyleSheet(
                """QToolButton {
                    border: none;
                    padding: 2px;
                }
                """
            )
            title_bar_layout.addWidget(button)

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)
        
class DateTimeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date and Time")
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Calendar widget for date selection
        self.calendar = QCalendarWidget()

        
        # Time edit with custom settings
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Time:"))
        
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setTime(QTime(12, 0))  # Default to noon
        
        
        time_layout.addWidget(self.time_edit)
        time_layout.addStretch()
        
        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(self.calendar)
        layout.addLayout(time_layout)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_datetime(self):
        return QDateTime(
            self.calendar.selectedDate(),
            self.time_edit.time()
        )
if __name__ == "__main__":

    

    app = QtWidgets.QApplication([])
    main = MainWindow()
    
    dark_palette = colorpalette.dark_palette()
    app.setStyle('Fusion')
    app.setPalette(dark_palette)
    app.setApplicationDisplayName("Demo")

    main.show()
    app.exec()
