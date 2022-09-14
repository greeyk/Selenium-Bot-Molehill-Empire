import atexit
from imperium.constants import plants_id
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import sys, time


from imperium.imperium import Imperium


plant = []

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        global check_boxes
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('bot_gui2.ui', self)

        check_boxes = [self.C1, self.C2, self.C3, self.C4, self.C5, self.C6, self.C7, self.C8, self.C9, self.C10,
                       self.C11, self.C12, self.C13, self.C14, self.C15, self.C16]
        for c in check_boxes:
            c.stateChanged.connect(self.plants_number)

        self.thread = {}
        self.Start.clicked.connect(self.start_worker_1)
        self.Start.clicked.connect(self.read_variables)
        self.Stop.clicked.connect(self.stop_worker_1)
        self.Stop.setEnabled(False)

    def read_variables(self):
        global login
        global password
        global server
        global sleep

        login = self.Login.text()
        password = self.Password.text()
        server = str(self.Server.currentText())
        sleep = int(self.Sleep.currentText())*60

    def append_list(self, index):
        global plant

        plant.append(plants_id[index])
        plant = list(dict.fromkeys(plant))
        return plant

    def remove_from_list(self, index):
        try:
            plant.remove(plants_id[index])
        except:
            pass
        return plant

    def plants_number(self):
        for idx, i in enumerate(check_boxes):
            if i.isChecked():
                self.append_list(idx)
            else:
                self.remove_from_list(idx)
        print(plant)

    def start_worker_1(self):
        self.thread[1] = ThreadClass(parent=None, index=1)
        self.thread[1].start()
        #self.thread[1].any_signal.connect(self.my_function)
        self.Start.setEnabled(False)
        self.Stop.setEnabled(True)

    def stop_worker_1(self):
        self.thread[1].stop()
        self.Start.setEnabled(True)

    def close_event(self):
        ThreadClass.bot.quit()


class ThreadClass(QtCore.QThread):
    #any_signal = QtCore.pyqtSignal(int)
    bot = Imperium()

    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.is_running = True

    def run(self):
        print('Starting thread...', self.index)

        self.bot.land_first_page()
        self.bot.try_login(login, password, server)
        try:
            self.bot.accept_cookies()
        except:
            pass
        time.sleep(1)

        while True:
            try:
                self.bot.closing_windows()
            except:
                pass

            try:
                self.bot.harvesting()
            except Exception as e:
                print('Harvesting error -----' + str(e))

            try:
                self.bot.planting(*plant)
            except Exception as e:
                print('Planting Error -----' + str(e))

            try:
                self.bot.watering()
            except Exception as e:
                print('Watering error -----' + str(e))

            try:
                self.bot.selling()
            except Exception as e:
                print('Selling error -----' + str(e))

            time.sleep(2)
            self.bot.refreshing()
            time.sleep(sleep)

            try:
                self.bot.try_login_again(login, password)
                print("Logged again")
            except:
                pass

    def stop(self):
        self.is_running = False
        print('Stopping thread...', self.index)
        self.terminate()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    ret = app.exec_()
    atexit.register(mainWindow.close_event())
    sys.exit(ret)








