from pandas import plotting
from Guiresource import colorpalette 
from PyQt6 import QtWidgets
import gui
from dataManager import DataManager
from PyQt6.QtCore import QDate
from pandas import to_datetime

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


    def date_change(self):
        print("Hi")

    def loadNewData(self):

        self.datamanager.load_data()

        if not self.datamanager.data is None:
        
            self.list.clear()
            self.list.addItems(self.datamanager.data.head())

            print(self.datamanager.data.index[0])

            
            

            self.result_label.setText(f"Start: {self.datamanager.data.index[0]}")
            self.result_label_end.setText(f"End: {self.datamanager.data.index[-1]}")

            self.datetime_start = self.datamanager.data.index[0]
            self.datetime_end = self.datamanager.data.index[-1]





    def clearPlot(self):
        self.plotListing = []
        self.plotWidget.clearPlot()

    def clearPlotSoft(self):
        
        self.plotWidget.clearPlot()
    def onItemClicked(self):

        self.list.itemDoubleClicked.connect(self.plotItem)

    def plotItem(self, Item):
        if Item.text() in self.plotListing:
            return
        self.clearPlotSoft()
        self.plotListing.append(Item)

        print(self.datetime_start,self.datetime_end)
        start = to_datetime(self.datetime_start)
        end = to_datetime(self.datetime_end)
    
        temp_data = self.datamanager.data

        temp_data = temp_data[(temp_data.index > self.datetime_start) & (temp_data.index < self.datetime_end)]

        for Item in self.plotListing:
            self.plotWidget.plot(temp_data[Item.text()], Item.text())


    
if __name__ == "__main__":
 
    app = QtWidgets.QApplication([])
    main = MainApplication()
    
    dark_palette = colorpalette.dark_palette()
    app.setStyle('Fusion')
    app.setPalette(dark_palette)
    app.setApplicationDisplayName("Demo")

    main.showMaximized()
    app.exec()
