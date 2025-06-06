from PyQt6 import QtWidgets, QtCore, QtGui
def dark_palette():

    # creats the dark mode color palette for the gui

    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(53, 53, 53))

    dark_palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColorConstants.White)

    dark_palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(25, 25, 25))

    dark_palette.setColor(QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(53, 53, 53))

    dark_palette.setColor(QtGui.QPalette.ColorRole.ToolTipBase, QtGui.QColorConstants.White)

    dark_palette.setColor(QtGui.QPalette.ColorRole.ToolTipText, QtGui.QColorConstants.White)

    dark_palette.setColor(QtGui.QPalette.ColorRole.Text, QtGui.QColorConstants.White)

    dark_palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(89, 65, 116))

    dark_palette.setColor(QtGui.QPalette.ColorRole.ButtonText, QtGui.QColorConstants.White)

    dark_palette.setColor(QtGui.QPalette.ColorRole.BrightText, QtGui.QColorConstants.Red)

    dark_palette.setColor(QtGui.QPalette.ColorRole.Link, QtGui.QColor(42, 130, 218))

    dark_palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(42, 130, 218))

    dark_palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColorConstants.Black)



    return dark_palette
