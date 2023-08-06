from .utils import get_crc, MODBUS_SLAVE_ADDR, PORT, BAUDRATE, Communicator
import modbus_tk.defines as cst
import atexit


class AirPump():

    def __init__(self, port=PORT, baudrate=BAUDRATE) -> None:
        self._bit_addr_suck = 32
        self._bit_addr_release = 33
        self._reg_addr_timeout = 54
        self._rtu = Communicator.instance(port=port, baudrate=baudrate)
        self._master = self._rtu.master
        self.timeout = 10000
        self.state = 'release'
        self.release()
        atexit.register(self.release)

    def suck(self, timeout=10000):
        if timeout != self.timeout:
            self.timeout = int(timeout)
            try:
                self._master.execute(MODBUS_SLAVE_ADDR,
                                     cst.WRITE_SINGLE_REGISTER,
                                     self._reg_addr_timeout,
                                     output_value=self.timeout)
                self.state = 'suck'
            except:
                pass
        try:
            self._master.execute(MODBUS_SLAVE_ADDR,
                                 cst.WRITE_SINGLE_COIL,
                                 self._bit_addr_suck,
                                 output_value=1)
        except:
            pass

    def release(self):
        try:
            self._master.execute(MODBUS_SLAVE_ADDR,
                                 cst.WRITE_SINGLE_COIL,
                                 self._bit_addr_release,
                                 output_value=1)
            self.state = 'release'
        except:
            pass

    def act(self, action):
        if action == 'suck':
            self.suck()
        elif action == 'release':
            self.release()
        else:
            raise ValueError(f"Unknow action: {action}")

    def get_state(self):
        return self.state
