from PyQt4 import QtGui
import sys
# import design
import numpy as np
from emulator import Emulator

"""
class ExampleApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined


def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app
"""

if __name__ == '__main__':
    import time

    e = Emulator()
    e.connect()
    e.clear_dtc()

    e.enable_vin()
    e.set_vin("4" * 17)
    # print("VIN IS SET")
    # e.get_vin()
    e.set_pid("010C", "256")  # RPM
    print(e.get_pid("010C"))
    e.set_pid("010C", "1026")  # RPM
    print(e.get_pid("010C"))
    # print("Determining Active PIDs")
    #
    # print(e.get_pid("0100"))
    # print(e.get_pid("0120"))
    # print(e.get_pid("0140"))
    # print(e.get_pid("0160"))
    # print(e.get_pid("0180"))
    # print(e.get_pid("01A0"))
    # print(e.get_pid("01C0"))
    # print(e.get_pid("0900"))
    # e.set_pid("010D", "100")  # speed
    # e.set_pid("0105", "85")  # Coolant temp
    #
    # import time
    # from itertools import cycle
    #
    # x = np.arange(800)
    # y = np.sin(2 * np.pi * 0.7 * x / 90)
    # c = cycle((y * 10).astype(np.uint8) + 10)
    # try:
    #     while True:
    #         e.set_pid("010D", next(c))
    #         time.sleep(0.1)
    # except Exception as e:
    #     print(e)
    #     pass
    e.close()
