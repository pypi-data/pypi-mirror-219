from .utils import MODBUS_SLAVE_ADDR, PORT, BAUDRATE, Communicator
import modbus_tk.defines as cst
import time

ADAPTER_MODBUS_CONFIG_SR_RUN = 55
ADAPTER_MODBUS_CONFIG_SR_CMD = 56
ADAPTER_MODBUS_BIT_SR_CMD_READ = 34


class SpeechRecognizer(object):
    """语音识别模块

    Examples
    --------
    >>> sr = SpeechRecognizer()
    >>> sr.get_cmd()
    >>> sr.reply(0, 0x01)
    """

    def __init__(self, port=PORT, baudrate=BAUDRATE):
        self._rtu = Communicator.instance(port=port, baudrate=baudrate)
        self._master = self._rtu.master

    def get_cmd(self):
        """获取语音识别模块的指令
        
        Returns:
            int: 0: 没有识别到语音指令，1: 分拣积木，2: 码垛，3: 垃圾分拣，4: 停止运行
        """
        retry = 5
        cmd = 0
        while retry > 0:
            try:
                self._master.execute(MODBUS_SLAVE_ADDR,
                                     cst.WRITE_SINGLE_COIL,
                                     ADAPTER_MODBUS_BIT_SR_CMD_READ,
                                     output_value=1)
                break
            except:
                retry -= 1
        if retry == 0:
            return cmd
        time.sleep(0.2)
        try:
            cmd, = self._master.execute(MODBUS_SLAVE_ADDR,
                                        cst.READ_HOLDING_REGISTERS,
                                        ADAPTER_MODBUS_CONFIG_SR_CMD, 1)
        except:
            pass
        return cmd

    def reply(self, running_flag, task):
        """回复语音识别模块

        Args:
            running_flag (int): 0: 开始运行，1: 运行中，2: 停止运行
            task (int): 1: 积木分拣，2: 码垛，3: 垃圾分拣
        """
        output_value = running_flag * 0x100 + task
        retry = 5
        while retry > 0:
            try:
                self._master.execute(MODBUS_SLAVE_ADDR,
                                     cst.WRITE_SINGLE_REGISTER,
                                     ADAPTER_MODBUS_CONFIG_SR_RUN,
                                     output_value=output_value)
                break
            except:
                retry -= 1
