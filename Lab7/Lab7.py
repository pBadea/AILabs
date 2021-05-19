
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

class Lab7:
    
    # set the flag is_sample_data to true to plot "sample_number" samples
    def init_google_drive_data(self, is_sample_data = False, sample_number = 1000):
        auth.authenticate_user()
        gauth = GoogleAuth()
        gauth.credentials = GoogleCredentials.get_application_default()
        drive = GoogleDrive(gauth)
        link = 'https://drive.google.com/open?id=19ETpfj6iQMvWsidI7UdChuJhSImKziIb'
        fluff, id = link.split('=')
        downloaded = drive.CreateFile({'id':id}) 
        downloaded.GetContentFile('Filename.csv')  
        self.data_frame = pd.read_csv('Filename.csv', usecols =["Adjusted Passenger Count","Month", "Year"], squeeze = True)
        if(is_sample_data):
            self.data = np.array(l7.data_frame.sample(sample_number).values)
        else:
            self.data = np.array(self.data_frame.values)


    # plot data and use kmeans 
    def plot_clustered_data(self):
        x_arr = []
        y_arr = []
        for elem in self.data:
            elem[2] = l7.convert_month_string_to_number(elem[2])
            x_arr.append(elem[0])
            y_arr.append(elem[2]/12 + elem[1])

        plt.xlabel('Passanger Count')
        plt.ylabel('Year')
        kmeans = KMeans(n_clusters=5)
        kmeans.fit(self.data)
        plt.scatter(x_arr,y_arr, c=kmeans.labels_, cmap='rainbow')
        plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], color='black', marker='v' )
        plt.show()

    def convert_month_string_to_number(self,s):
        if(s == 'January'):
            return 0
        if(s == 'February'):
            return 1
        if(s == 'March'):
            return 2
        if(s == 'April'):
            return 3
        if(s == 'May'):
            return 4
        if(s == 'June'):
            return 5
        if(s == 'July'):
            return 6
        if(s == 'August'):
            return 7
        if(s == 'September'):
            return 8
        if(s == 'October'):
            return 9
        if(s == 'November'):
            return 10
        if(s == 'December'):
            return 11
        else:
            return -1

l7 = Lab7()
l7.init_google_drive_data(True,300)
l7.plot_clustered_data()
