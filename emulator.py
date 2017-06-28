import serial
import serial.tools.list_ports
import struct


class FreematicsEmulator:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def scan(self):
        iterator = serial.tools.list_ports.grep("10C4:EA60")

        elements = 0
        for n, (port, desc, hwid) in enumerate(iterator):
            elements = elements + 1
            path = format(port)

        if elements == 1:
            print("Found device {}".format(path))
            return 1, path
        else:
            print("{} devices found".format(elements))
            return 0

    def connect(self):
        n, path = self.scan()
        if n == 1:
            self.ser = serial.Serial(path, baudrate=38400, timeout=1)
            self.character_echo(0)
            self.sendCMD("ATINF0")
            self.ignition_on()
            self.sendCMD("ATSET 0101=0x00,0x07,0xff,0x00")

    def close(self):
        self.ser.close()

    """
    BEGIN AT* FUNCTIONS
    """

    def sendCMD(self, cmd):
        if self.verbose:
            print("S>", cmd)
        self.ser.write((cmd + "\r").encode('ascii'))
        out = self.ser.readline().decode('ascii').replace('\r', '').strip()
        if self.verbose:
            print("R>", out)
        return out

    def set_pid(self, pid, value):
        """
        ATSET [PID]=[Value]
        ATSET [PID]=[A],[B],[C],[D]...

        Function: setting the value of an OBD-II PID
        Arguments:
            PID: a 4-digit HEX number specifying an OBD-II PID
            Value: the value of the OBD-II PID in decimal or in HEX (raw data)
        Examples:
            ATSET 010C=2000 (setting RPM to 2000)
            ATSET 010C=0x31,0x64 (also setting RPM to 2000 with raw byte data)
        Response: OK or Error
        """
        if type(value) in (list, tuple):
            value = ",".join(map(hex, value))
        cmd = "ATSET {}={}\r".format(pid, value)
        self.sendCMD(cmd)

    def get_pid(self, pid):
        """
        ATGET [PID]

        Function: retrieving the current value of an OBD-II PID
        Argument: a 4-digit HEX number specifying an OBD-II PID
        Response: The raw HEX data of the requested OBD-II PID

        """
        out = self.sendCMD("ATGET {}".format(pid)).split('=')[1]
        if out:
            return int(out, 16)
        return "ERR"

    def reinitialize(self):
        """
        ATZ

        Function: re-initializing the emulator
        Response: the name and version of the emulator
        """

        print("Re-initializing the emulator...")
        return self.sendCMD("ATZ")

    def ignition_on(self):
        """
        ATACC0 / ATACC1

        Function: emulating ignition OFF / ON
        Response: OK
        Note: this does not emulate any voltage change caused by ignition switching
        """
        print("Ignition on")
        return self.sendCMD("ATACC1")

    def ignition_off(self):
        print("Ignition off")
        return self.sendCMD("ATACC0")

    def set_vin(self, value):
        """
        ATSET VIN=[Vehicle Identification Number]

        Function: setting the emulated VIN
        Argument: a 17-digit vehicle identification number
        Response: OK or Error
        """
        return self.sendCMD("ATSET VIN={}".format(value))

    def get_vin(self):
        return self.get_pid("0902")

    def enable_vin(self):
        """
        ATENABLEVIN

        Function: enable VIN
        """
        return self.sendCMD("ATVIN1")

    def disable_vin(self):
        """
        ATDISABLEVIN
        
        Function: disable VIN
        """
        return self.sendCMD("ATVIN0")

    def character_echo(self, on):
        """
        ATE0/ATE1
    
        Function: turning off/on character echoing
        Response: OK
        """
        s = '0'
        if on:
            s = '1'
        return self.sendCMD("ATE{}".format(s))

    def clear_dtc(self):
        """
        ATCLR DTC

        Function: clear all DTC
        """
        return self.sendCMD("ATCLR DTC")

    def set_dtc7(self, codes):
        """
        ATSET DTC7=[OBD-II Trouble Code]

        Function: setting mode 07 DTC (up to 6 separated with comma)
        Argument: a code that identifies a malfunction or failure of a vehicle component (refer to this website)
        Response: OK or Error
        Example: ATSET DTC7=P0105,P0106
        """
        return self.sendCMD("ATSET DTC7={}".format(','.join(codes)))

    def set_dtc(self, codes):
        """
        ATSET DTC=[OBD-II Trouble Code]

        Function: setting mode 03 DTC (up to 6 separated with comma)
        Argument: a code that identifies a malfunction or failure of a vehicle component (refer to this website)
        Response: OK or Error
        Example: ATSET DTC=P0105,P0106
        """
        return self.sendCMD("ATSET DTC={}".format(','.join(codes)))

    def set_protocol(self, protocol):
        """
        ATBUS [Protocol]

        Function: changing the simulated protocol (default is CAN bus 11-bit/500Kbps)
        Argument: a string that specifies the protocol which can be one of the following:
            CAN_11B_500K
            CAN_29B_500K
            CAN_11B_250K
            CAN_29B_250K
            KWP2000_FAST
            KWP2000_5BPS
            ISO9141_2
            J1850_PWM
            J1850_VPW
        Response: OK or Error
        """
        if protocol not in "CAN_11B_500K,CAN_29B_500K,CAN_11B_250K,CAN_29B_250K,KWP2000_FAST,KWP2000_5BPS,ISO9141_2,J1850_PWM,J1850_VPW".split(
                ","):
            raise ValueError("Invalid Protocol: " + protocol)
        return self.sendCMD("ATBUS {}".format(protocol))
        

