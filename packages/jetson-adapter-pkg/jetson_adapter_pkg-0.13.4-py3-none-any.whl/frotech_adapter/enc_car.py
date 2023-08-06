from .utils import get_crc, PORT, BAUDRATE, Communicator
import modbus_tk.defines as cst
import atexit

ENABLE_ADDR = 1
SPEED_ADDR = 10
ROTATE_ADDR = 11
PID_ENABLE_ADDR = 14
LEFT_UP_WHEEL_ADDR = 114
RIGHT_UP_WHEEL_ADDR = 115
LEFT_DOWN_WHEEL_ADDR = 116
RIGHT_DOWN_WHEEL_ADDR = 117

MODBUS_SLAVE_ADDR = 1


class Car():

    def __init__(self, port=PORT, baudrate=BAUDRATE) -> None:
        self._rtu = Communicator.instance(port=port, baudrate=baudrate)
        self._master = self._rtu.master
        atexit.register(self.stop)

    def enable_pid(self, enable):
        if enable:
            enable = 1
        else:
            enable = 0
        try:
            self._master.execute(MODBUS_SLAVE_ADDR,
                                 cst.WRITE_SINGLE_REGISTER,
                                 PID_ENABLE_ADDR,
                                 output_value=enable)
        except:
            pass

    def set_wheel_speed(self, lu, ru, ld, rd):
        """设置4个轮子的速度

        Args:
            lu (int): 左上轮子速度
            ru (int): 右上轮子速度
            ld (int): 左下轮子速度
            rd (int): 右下轮子速度
        """
        lu = max(min(lu, 1000), -1000)
        ru = max(min(ru, 1000), -1000)
        ld = max(min(ld, 1000), -1000)
        rd = max(min(rd, 1000), -1000)
        lu = int(lu) & 0xffff
        ru = int(ru) & 0xffff
        ld = int(ld) & 0xffff
        rd = int(rd) & 0xffff

        pdu = bytearray([
            MODBUS_SLAVE_ADDR, cst.WRITE_MULTIPLE_REGISTERS,
            0, LEFT_UP_WHEEL_ADDR, 0, 4, 8, (lu >> 8) & 0xff, lu & 0xff,
            (ru >> 8) & 0xff, ru & 0xff, (ld >> 8) & 0xff, ld & 0xff,
            (rd >> 8) & 0xff, rd & 0xff
        ])

        cmd = pdu + get_crc(pdu)
        self._master._serial.write(cmd)
        # try:
        #     self._master.execute(MODBUS_SLAVE_ADDR,
        #                          cst.WRITE_MULTIPLE_REGISTERS,
        #                          LEFT_UP_WHEEL_ADDR,
        #                          output_value=[lu, ru, ld, rd])
        # except:
        #     pass

    def set_velocity(self, x, y, w):
        """设置速度

        Args:
            x (float): x速度，单位 m/s
            y (float): y速度，单位 m/s
            w (float): w速度，单位 rad/s
        """
        x = int(x * 100) & 0xffff
        w = int(w * 100) & 0xffff
        try:
            self._master.execute(MODBUS_SLAVE_ADDR,
                                 cst.WRITE_MULTIPLE_REGISTERS,
                                 SPEED_ADDR,
                                 output_value=[x, w])
        except:
            pass

    def forward(self, x):
        """设置前进速度

        Args:
            x (float): 前进速度，单位 m/s
        """
        x = int(x * 100) & 0xffff
        try:
            self._master.execute(MODBUS_SLAVE_ADDR,
                                 cst.WRITE_SINGLE_REGISTER,
                                 SPEED_ADDR,
                                 output_value=x)
        except:
            pass

    def rotate(self, w):
        """设置旋转速度

        Args:
            w (float): 旋转速度，单位 rad/s
        """
        w = int(w * 100) & 0xffff
        try:
            self._master.execute(MODBUS_SLAVE_ADDR,
                                 cst.WRITE_SINGLE_REGISTER,
                                 SPEED_ADDR,
                                 output_value=w)
        except:
            pass

    def stop(self):
        self.onoff(0)

    def onoff(self, on):
        on = 1 if on else 0
        for _ in range(5):
            try:
                self._master.execute(MODBUS_SLAVE_ADDR,
                                     cst.WRITE_SINGLE_REGISTER,
                                     SPEED_ADDR,
                                     output_value=on)
            except:
                pass
            else:
                break
