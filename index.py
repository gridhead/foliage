from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, time, requests, json
from PyQt5.uic import loadUiType

ui,_=loadUiType('foliage.ui')

class MainApp(QMainWindow,ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.title = 'Foliage by t0xic0der'
        self.setupUi(self)
        self.handle_buttons()

    def handle_buttons(self):
        self.btn_get.clicked.connect(self.fetch_weather)
        self.btn_abt.clicked.connect(self.display_about)

    def fetch_weather(self):
        apikey = self.oapi_text.text()
        locale = self.city_text.text()
        try:
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "appid=" + apikey + "&q=" + locale
            response = requests.get(complete_url)
            data = response.json()
            if str(data["cod"])== "404":
                self.label_city.setText("City not found!")
                self.label_coor.setText("Error 404 : Please check the location and try again")
            if str(data["cod"])== "401":
                self.label_city.setText("Invalid API key!")
                self.label_coor.setText("Error 401 : Please check the API key and try again")
            if str(data["cod"])=="400":
                self.label_city.setText("No location provided!")
                self.label_coor.setText("Error 400 : Please provide a location and try again")
            else:
                prim = data["main"]
                main_avg_temp = prim["temp"]
                main_pressure = prim["pressure"]
                main_humidity = prim["humidity"]
                main_min_temp = prim["temp_min"]
                main_max_temp = prim["temp_max"]
                if "sea_level" in prim:
                    main_sea_prez = prim["sea_level"]
                else:
                    main_sea_prez = 0
                if "grnd_level" in prim:
                    main_gnd_prez = prim["grnd_level"]
                else:
                    main_gnd_prez = 0
                gust = data["wind"]
                main_spd_wind = gust["speed"]
                main_dir_wind = gust["deg"]
                clem = data["weather"][0]
                main_weat_pri = clem["main"]
                main_weat_des = clem["description"]
                loca = data["coord"]
                main_lon_city = loca["lon"]
                main_lat_city = loca["lat"]
                syst = data["sys"]
                main_ret_time = syst["message"]
                main_org_coun = syst["country"]
                main_sun_rise = syst["sunrise"]
                main_sun_sate = syst["sunset"]
                main_tzd_data = data["timezone"]
                mtzdata=time.strftime("%H%M",time.localtime(main_tzd_data))
                sunrise=time.strftime("%H%M",time.localtime(main_sun_rise))
                sunsate=time.strftime("%H%M",time.localtime(main_sun_sate))
                main_nam_city = data["name"]
                loca_base=main_nam_city+", "+main_org_coun
                loca_prec="Lat:"+str(main_lat_city)+", Lon:"+str(main_lon_city)
                self.label_city.setText(str(loca_base))
                self.label_coor.setText(str(loca_prec))
                self.val_wind_spd.setText(str(main_spd_wind))
                self.val_wind_dir.setText(str(round(main_dir_wind,2)))
                self.val_prez_avg.setText(str(round(main_pressure,2)))
                self.val_prez_sea.setText(str(int(main_sea_prez)))
                self.val_prez_gnd.setText(str(int(main_gnd_prez)))
                self.val_temp_avg.setText(str(round(main_avg_temp-273,1)))
                self.val_tkel_avg.setText(str(round(main_avg_temp,2))+"K")
                self.val_temp_min.setText(str(round(main_min_temp-273,1)))
                self.val_temp_max.setText(str(round(main_max_temp-273,1)))
                self.val_clim_pri.setText(str(main_weat_pri))
                self.val_clim_sec.setText(str(main_weat_des))
                self.val_humidity.setText(str(main_humidity))
                self.val_sola_tzd.setText(str(mtzdata))
                self.val_sola_ris.setText(str(sunrise))
                self.val_sola_set.setText(str(sunsate))
        except Exception as e:
            print(e)
            self.label_city.setText("Unable to fetch!")
            self.label_coor.setText("Please check your internet connection and try again")

    def display_about(self):
        self.label_city.setText("Foliage")
        self.label_coor.setText("by t0xic0der")
        self.oapi_text.clear()
        self.city_text.clear()

def main():
    app=QApplication(sys.argv)
    QFontDatabase.addApplicationFont("fonts/AkzidenzGroteskLight.ttf")
    window=MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()