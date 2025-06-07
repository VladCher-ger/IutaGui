from Guiresource import colorpalette 
from PyQt6 import QtWidgets
import gui
from dataManager import DataManager


class MainApplication(gui.MainWindow):

    def __init__(self):
        super().__init__()
        self.init_gui()
        self.datamanager =  DataManager()
        



        self.init_actions()
        self.plotListing = []
    def init_actions(self):

        self.LoadData.pressed.connect(self.loadNewData)
        self.ResetPlot.pressed.connect(self.clearPlot)
        self.list.itemDoubleClicked.connect(self.plotItem)

    def loadNewData(self):

        self.datamanager.load_data()

        if not self.datamanager.data is None:
        
            self.list.clear()
            self.list.addItems(self.datamanager.data.head())

    def clearPlot(self):
        self.plotListing = []
        self.plotWidget.clearPlot()
    def onItemClicked(self):

        self.list.itemDoubleClicked.connect(self.plotItem)

    def plotItem(self, Item):
        if Item.text() in self.plotListing:
            return
        self.plotListing.append(Item.text())
        self.plotWidget.plot(self.datamanager.data[Item.text()], Item.text())



    
if __name__ == "__main__":
 
    app = QtWidgets.QApplication([])
    main = MainApplication()
    
    dark_palette = colorpalette.dark_palette()
    app.setStyle('Fusion')
    app.setPalette(dark_palette)
    app.setApplicationDisplayName("Demo")

    main.showMaximized()
    app.exec()
