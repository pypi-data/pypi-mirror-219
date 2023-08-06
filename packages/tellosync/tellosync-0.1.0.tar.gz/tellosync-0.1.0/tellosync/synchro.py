import serial
import time
import platform

class Synchro:
    def __init__(self, port:int, numSynchros: int=0) -> None:
        self.ser = serial.Serial()
        self.ser.baudrate = 19200
        self.ser.timeout = 2.0
        
        match (platform.system()):
            case "Windows":
                self.ser.port = f"COM{port}"
            case "Linux":
                self.ser.port = f"/dev/ttyUSB{port}"
            case "Darwin":
                self.ser.port = f"/dev/tty.usbmodem{port}"
            case _:
                self.ser.port = f"COM{port}"

        self.numSynchros = numSynchros
    
    def open(self) -> bool:
        try:
            self.ser.open()
            time.sleep(3.0)
            return True
        except serial.SerialException as e:
            print(e)
            return False

    def close(self) -> None:
        self.ser.close()

    def selfIsReady(self) -> None:
        self.ser.write(b"READY")
    
    def waitSync(self) -> bool:
        result = self.ser.readline().decode("Ascii").strip()
        return result == "SYNCED"
    
    def unsync(self) -> None:
        self.ser.write(b"UNSYNC")
    
    def resync(self) -> None:
        self.ser.write(b"RESYNC")
    
    def start(self) -> None:
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.ser.write(b"START")
        time.sleep(1.0)

        self.ser.write(str(self.numSynchros).encode("Ascii"))
        time.sleep(1.0)
    
    def finished(self) -> None:
        self.ser.write(b"FINISH")
