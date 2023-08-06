# 0.0.4
import time
import serial
import scipy
import pandas as pd
import pkg_resources
import os

# 備忘：lineの内訳
# オンボード計算がFalseのとき→ [ピークの位置(4Byte), アンプ量(4Byte)]*チャンネル数 + [温度(℃*100)(2Byte), 空(2Byte), 不明(計4Byte)] + ["Ende"(4Byte)]
# →出力は8×チャンネル数+12byte
class FBGcom:
    def __init__(self):
        self._ser: serial.serialwin32.Serial = None
        self.FBG_num = 0
        self.WL_ranges = []
        self._iniPath = pkg_resources.resource_filename('myFBGcommunication', 'params.ini')
        if os.path.isfile(self._iniPath):
            self._params = pd.read_csv(self._iniPath, header=None, index_col=0)
        else:
            self._iniPath = 'params.ini'
            if not os.path.isfile(self._iniPath):
                self._make_default_paramsfile()
            self._params = pd.read_csv(self._iniPath, header=None, index_col=0)
        self._FBG_width = float(self._params.loc['FBG_width', 1])   # nano m
        self._integration_time = float(self._params.loc['integration_time', 1])
        self._Averaging = int(self._params.loc['Averaging', 1])
        self._on_boradCalculation = bool(self._params.loc['on_boradCalc', 1])
        self._defaultTemp = float(self._params.loc['defaultTemp', 1])

    def init(self, COM):
        try:
            self._ser = serial.Serial(COM, baudrate=3000000,
                                bytesize=serial.EIGHTBITS,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                timeout=0.001)
        except serial.serialutil.SerialException:
            return -1

        self.auto_setting()
        self.set_param()
        return 1


    def auto_setting(self):
        # ----FBGセンサの検出-----
        spectrum_raw = b''
        WLL_raw = b''
        self._ser.write(b's>')
        time.sleep(0.1)
        while len(spectrum_raw) != 2052:
            spectrum_raw = spectrum_raw + self._ser.read_all()
        spectrum = [int.from_bytes(spectrum_raw[i*2:i*2+2], byteorder='little') for i in range(1024)]
        spectrum[0:3] = [spectrum[3]]*3
        _peaks, _ = scipy.signal.find_peaks(spectrum, height=10000, distance=10)
        self.FBG_num = len(_peaks)
        if self.FBG_num == 0:
            return -1
        self._ser.write(b'WLL>')  # Get wavelength of pixels list
        time.sleep(0.1)
        while len(WLL_raw) != 4100:
            WLL_raw = WLL_raw + self._ser.read_all()
        # --バイナリで出てくる全波長の変換--
        WLL = [int.from_bytes(WLL_raw[i*4:i*4+4], byteorder='little') for i in range(1024)]
        # --ピーク値の波長--
        self._FBG_wavelength = [WLL[i] for i in _peaks]

        # ----アクティブチャンネルの設定-----
        for i, nowFBG_wavelength in enumerate(self._FBG_wavelength):
            # 各チャンネルの検出範囲を設定
            now_WL_range = [int(nowFBG_wavelength - (self._FBG_width * 10000) / 2), int(nowFBG_wavelength + (self._FBG_width * 10000) / 2)]
            self.WL_ranges.append(now_WL_range)
            send = 'Ke,' + str(i) + ',' + str(now_WL_range[0]) + ',' + str(now_WL_range[1]) + '>'
            self._ser.write(send.encode())
            time.sleep(0.01)
        # チャンネル数の設定
        send = 'KA,' + str(self.FBG_num) + '>'
        time.sleep(0.01)
        self._ser.write(send.encode())
        return 1

    def set_param(self, FBG_width=None, integration_time=None, Averaging=None, on_boradCalculation=None, defaultTemp=None, WL_range=False):
        self._params = pd.read_csv(self._iniPath, header=None, index_col=0)
        if FBG_width == None:
            self._FBG_width = float(self._params.loc['FBG_width', 1])   # nano m
        else:
            self._FBG_width = FBG_width
        if integration_time == None:
            self._integration_time = float(self._params.loc['integration_time', 1])
        else:
            self._integration_time = integration_time
        if Averaging == None:
            self._Averaging = int(self._params.loc['Averaging', 1])
        else:
            self._Averaging = Averaging
        if on_boradCalculation == None:
            self._on_boradCalculation = bool(self._params.loc['on_boradCalc', 1])
        else:
            self._on_boradCalculation = on_boradCalculation
        if defaultTemp == None:
            self._defaultTemp = float(self._params.loc['defaultTemp', 1])
        else:
            self._defaultTemp = defaultTemp
        # if WL_range:
        #     self.WL_ranges
        self._params.to_csv(self._iniPath, header=None)

        # 露光時間，平均化処理のパラメータ設定
        send = 'iz,' + str(int(self._integration_time * 1000000)) + '>'
        time.sleep(0.01)
        self._ser.write(send.encode())

        send = 'm,' + str(self._Averaging) + '>'
        self._ser.write(send.encode())
        time.sleep(0.01)
        self._ser.write(b'LED,1>')
        time.sleep(0.01)
        self._ser.write(b'a>')
        for i in range(self.FBG_num):
            send = 'OBsType,' + str(i) + ',' + '0' + '>'
            self._ser.write(send.encode())
        self._ser.write(b'OBN>')  # zero Temp/strain
        time.sleep(0.01)
        send = 'OBsaT0,' + str(int(self._defaultTemp*100)) + '>'
        self._ser.write(send.encode())  # 全チャネルに同じT0値を設定
        time.sleep(0.01)
        send = 'OBB,' + str(int(self._on_boradCalculation)) + '>'
        self._ser.write(send.encode())
        time.sleep(0.01)

        self._ser.write(b'P>')
        while self._ser.readline() != b'':
            pass

    def read(self, Targets):
        tmp_line = b''
        data_len = 8 * self.FBG_num + 12
        dataOK = False
        while not dataOK:
            line = tmp_line
            tmp_line = b''
            self._ser.write(b'P>')
            while len(line) < data_len:
                time.sleep(0.001)
                line = line + self._ser.read_all()
                self._ser.write(b'P>')
            if len(line) == data_len:
                if line[-4:-1] == b'End':
                    dataOK = True
                else:
                    print('CHECK1')
            elif len(line) > data_len:
                ende_idx = line.find(b'Ende')
                tmp_line = line[ende_idx + 4:len(line)]
                if ende_idx != data_len - 4:
                    line = line[-data_len:]
                else:
                    tmp_line = line[ende_idx + 4:len(line)]
                    line = line[0:ende_idx + 4]
                    dataOK = True
        if self._on_boradCalculation:
            now_data = [int.from_bytes(line[8 * i:8 * i + 4], byteorder='little', signed=True)/10000 for i in Targets]
        else:
            now_data = [int.from_bytes(line[8 * i:8 * i + 4], byteorder='little', signed=True) for i in Targets]
        return now_data

    def read_all(self):
        now_data = self.read(range(self.FBG_num))
        return now_data

    def _make_default_paramsfile(self):
        _paramas = [['FBG_width',3.0], ['integration_time',0.05], ['Averaging',1],['on_boradCalc',True],['defaultTemp',21]]
        pd.DataFrame(_paramas, columns=None).to_csv('params.ini', index=None, header=None)
