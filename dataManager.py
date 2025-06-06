import pandas as pd
from tkinter.filedialog import askopenfilename


class DataManager():

    def __init__(self):

        pass

    def load_data(self, filename = None):
        self.data = None
        if not filename:
           filename = askopenfilename(initialdir="./Data/")

        print(filename)
        if not filename:
            return
 
        self.data = pd.read_csv(filename, sep=",", skiprows=1)

        self.data.columns = self.data.columns.str.strip()

        # Convert date and time columns to datetime
        # Note: The date format in the file appears to be 0-1-1 which is invalid,
        # so we'll create a proper datetime from the time column assuming current date
        self.data['DateTime'] = pd.to_datetime(self.data['Time'], format='%H:%M:%S')
        self.data['DateTime'] = self.data['DateTime'].apply(lambda dt: dt.replace(year=pd.Timestamp.now().year, 
                                                                  month=pd.Timestamp.now().month, 
                                                                  day=pd.Timestamp.now().day))

        # Set DateTime as index
        self.data.set_index('DateTime', inplace=True)

        # Drop the original Date and Time columns
        self.data.drop(['Date', 'Time'], axis=1, inplace=True)

       

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    DataClass = DataManager()
    DataClass.load_data("./Data/Messungen_Oel_Bochum.CSV")
    
    data = DataClass.data

    lightIntensity = data["Light Intensity (lux)"]
    plt.plot( lightIntensity)
    plt.show()

