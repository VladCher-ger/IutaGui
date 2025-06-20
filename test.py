
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QCalendarWidget, QTimeEdit, QDialog, 
                            QDialogButtonBox, QHBoxLayout)
from PyQt6.QtCore import QDateTime, QTime, QDate

class DateTimeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date and Time")
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Calendar widget for date selection
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumDate(QDate(2023, 1, 1))
        self.calendar.setMaximumDate(QDate(2023, 12, 31))
        
        # Time edit with custom settings
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Time:"))
        
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime(12, 0))  # Default to noon
        self.time_edit.setTimeRange(QTime(8, 0), QTime(18, 0))  # 8AM-6PM
        
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

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        self.datetime_btn = QPushButton("Select Date and Time")
        self.datetime_btn.clicked.connect(self.show_dialog)
        
        self.result_label = QLabel("No date/time selected")
        
        layout.addWidget(self.datetime_btn)
        layout.addWidget(self.result_label)
        self.setLayout(layout)
        self.setWindowTitle('Custom DateTime Picker')
        self.show()
        
    def show_dialog(self):
        dialog = DateTimeDialog(self)
        if dialog.exec():
            datetime = dialog.get_datetime()
            self.result_label.setText(
                f"Selected: {datetime.toString('yyyy-MM-dd HH:mm')}"
            )

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()