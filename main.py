from pandas import plotting
from Guiresource import colorpalette 
from PyQt6 import QtWidgets
import gui
from dataManager import DataManager
from PyQt6.QtCore import QDate,QTime
from pandas import to_datetime

from tkinter.filedialog import asksaveasfilename

class MainApplication(gui.MainWindow):

    def __init__(self):
        super().__init__()
        self.init_gui()

        self.datamanager =  DataManager()
        

        self.init_actions()
        self.initVaribales()
    
    def init_actions(self):
        
        self.StoreSelection.pressed.connect(self.StoreSelectedData)

        self.LoadData.pressed.connect(self.loadNewData)
        self.ResetPlot.pressed.connect(self.clearPlot)
        self.list.itemDoubleClicked.connect(self.plotItem)

        self.datetime_btn.clicked.connect(self.show_dialog)
        self.datetime_btn_end.clicked.connect(self.show_dialog_end)
    
    def initVaribales(self):
        self.plotListing = []

        self.datetime_start = QDate.currentDate()
        self.datetime_end = QDate.currentDate()

        self.datetime_start_global = QDate.currentDate()
        self.datetime_end_global =QDate.currentDate()




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


            self.datetime_start_global = self.datetime_start
            self.datetime_end_global =self.datetime_end 

            print(self.datetime_end )

            self.StoreSelection.show()

            self.datetime_btn.show()
            self.result_label.show()
            self.datetime_btn_end.show()
            self.result_label_end.show()

            self.clearPlot()

            


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
        
        self.plotListing.append(Item)

        self.updatePlot()

    def updatePlot(self):   
        self.clearPlotSoft()
        temp_data = self.datamanager.data

        temp_data = temp_data[(temp_data.index > self.datetime_start) & (temp_data.index < self.datetime_end)]

        for Item in self.plotListing:
            self.plotWidget.plot(temp_data[Item.text()], Item.text())

    def show_dialog(self):
        self.dialog = gui.DateTimeDialog(self)
        
        self.dialog.time_edit.setTime(self.convertTimestamp(self.datetime_start_global))
        if self.dialog.exec():
            datetime = self.dialog.get_datetime()
            self.datetime_start= datetime.toString('yyyy-MM-dd HH:mm:ss')

            self.result_label.setText(
            f"Start: {datetime.toString('yyyy-MM-dd HH:mm')}"
        )   
        if self.datamanager:
            self.updatePlot()
    
    def show_dialog_end(self):
        self.dialog_end = gui.DateTimeDialog(self)

        self.dialog_end.time_edit.setTime(self.convertTimestamp(self.datetime_end_global))

        if self.dialog_end.exec():
            datetime = self.dialog_end.get_datetime()
            self.datetime_end = datetime.toString('yyyy-MM-dd HH:mm:ss')
            self.result_label_end.setText(
                f"End: {datetime.toString('yyyy-MM-dd HH:mm')}"
            )
            if self.datamanager:
                self.updatePlot()   

    def StoreSelectedData(self):

        safepath = asksaveasfilename()
        safepath = safepath.removesuffix('.csv')
        temp_data = self.datamanager.data

        temp_data = temp_data[(temp_data.index > self.datetime_start) & (temp_data.index < self.datetime_end)]
        print(safepath)

        with open(safepath+'.csv', 'w') as f:
            # Write separator row (adjust the pattern as needed)
            f.write('Sep=,'  + '\n')
            # Write the DataFrame
            temp_data.to_csv(f,index=False,sep=',',lineterminator='\n')

        if len(self.plotListing):

            with open(safepath+'_selection.csv', 'w') as f:
                # Write separator row (adjust the pattern as needed)
                f.write('Sep=,'  + '\n')
                # Write the DataFrame
                savelist = ["DAQ","Date","Time", ] + [i.text() for i in self.plotListing] 
                
                print(savelist)
                temp_data.to_csv(f,index=False,sep=',',lineterminator='\n', columns=savelist)




    def convertTimestamp(self, ts):
        hour = ts.hour
        minute = ts.minute
        second = ts.second      

        return QTime(hour, minute, second) 
    
if __name__ == "__main__":
 
    app = QtWidgets.QApplication([])
    main = MainApplication()
    
    dark_palette = colorpalette.dark_palette()
    app.setStyle('Fusion')
    app.setPalette(dark_palette)
    app.setApplicationDisplayName("Demo")

    main.showMaximized()
    app.exec()
