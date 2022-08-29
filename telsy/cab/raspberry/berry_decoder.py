'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Cab v29.08.2022
Ing. Elmer Rocha Jaime
'''


def ecg_wave(data):  # 0x01
    ''' Returns the waveforms of the ECG signal '''
    # data[0] : I lead
    # data[1] : II lead
    # data[2] : III lead
    # data[3] : aVR lead
    # data[4] : aVL lead
    # data[5] : aVF lead
    # data[6] : V lead

    # I,II…V are the wave amplitude equal to
    # LeadI, LeadII…LeadV, range is 0-250
    # Package rate is 250 packages/second
    ###########################################################################
    # i_lead = data[0]
    ii_lead = data[1]
    # iii_lead = data[2]
    # avr_lead = data[3]
    # avl_lead = data[4]
    # avf_lead = data[5]
    # v_lead = data[6]
    ###########################################################################
    return str(ii_lead)


def ecg_parameters(data):  # 0x02
    ''' Returns the ECG parameters '''
    # data[0] : ECG Status
    # data[1] : Heart Rate
    # data[2] : Respiration Rate
    # data[3] : ST Level
    # data[4] : Arrythmia code

    # ECG Status
    # BIT0： ECG signal intensity
    # 0 normal
    # 1 weak
    # BIT1： lead status
    # 0 normal
    # 1 lead off
    # BIT3-BIT2：ECG wave gain
    # 00： x0.25 gain
    # 01： x0.5 gain
    # 10： x1 gain
    # 11： x2 gain
    # BIT5-BIT4：ECG filter mode
    # 00： operation mode
    # 01： monitor mode
    # 10： diagnose mode
    # BIT7-BIT6：ECG lead mode
    # 01 Lead3 mode, sampling Lead II (measure RA-LL，driving by LA)
    # 11 Lead5 mode, default settings during module power on

    # Heart Rate
    # Range is 0-250，unit：beat/second

    # Respiration Rate
    # Range is 0-250，unit：beat/second

    # ST Level
    # Signed char，range is -100 - +100,
    # equal to –1mV - +1mV，eg：-75 means
    # -0.75mV，+55 means +0.55mV

    # Arrythmia code
    # Code ARR
    # 0x00 ANALYSIS
    # 0x01 NORMAL
    # 0x02 ASYSTOLE
    # 0x03 VFIB/VTAC
    # 0x04 R ON T
    # 0x05 MULTI PVCS
    # 0x06 COUPLE PVCS
    # 0x07 PVC
    # 0x08 BIGERMINY
    # 0x09 TRIGERMINY
    # 0x0A TACHYCARDIA
    # 0x0B BRADYCARDIA
    # 0x0C MISSED BEATS
    ###########################################################################
    # ecg_status = data[0]
    # hear_rate = data[1]
    respiration_rate = data[2]
    # st_level = data[3]
    # arrythmia_code = data[4]
    ###########################################################################
    return str(respiration_rate)


def nibp(data):  # 0x03
    ''' Returns de NIBP results (systolic, diastolic and mean pressure) '''
    # data[0] : NIBP Status
    # data[1] : Cuff Pressure
    # data[2] : Systolic Pressure
    # data[3] : Mean Pressure
    # data[4] : Diastolic Pressure

    # NIBP Status
    # BIT1-BIT0：NIBP Patient mode
    # 00： adult mode
    # 01： child mode
    # 10： neonate mode
    # BIT5-BIT2：NIBP Test Result
    # 0000 Test Finished（normal test）
    # 0001 During test
    # 0010 Test Stopped
    # 0011 Over pressure protected
    # 0100 cuff is too loose or unattached
    # 0101 Test time out
    # 0110 Test error occure
    # 0111 Disturb found during test
    # 1000 test result is out of range
    # 1001 module is initializing
    # 1010 module initiallized
    # BIT7-BIT6： reserved bits

    # Cuff Pressure
    # real cuff pressure = data[1] x 2，unit：mmHg

    # Systolic Pressure
    # range is 0-250，unit：mmHg

    # Mean Pressure
    # range is 0-250，unit：mmHg

    # Diastolic Pressure
    # range is 0-250，unit：mmHg

    # When module status is initializing,
    # any operation command about NIBP will be ignored by module.

    # The Sys/Mean/Dia pressure is meaningful only if
    # NIBP test result is 0000 Test Finished(normal test).

    # 3C : 0011 1100
    ###########################################################################
    status = (data[0] & 0x3C) >> 2
    # cuff = data[1]
    sys = data[2]
    mean = data[3]
    dia = data[4]
    ###########################################################################
    return str(status)+'*'+str(sys)+'S'+str(dia)+'S'+str(mean)


def spo2(data):  # 0x04
    ''' Returns the SPO2 parameters '''
    # data[0] : SPO2 Status
    # data[1] : SPO2
    # data[2] : Pulse Rate

    # SPO2 Status
    # 0x00 normal
    # 0x01 sensor is off
    # 0x02 no finger insert
    # 0x03 searching pulse signal
    # 0x04 searching pulse signal is time out

    # SPO2
    # SPO2 saturation value, range is 0-100，
    # If SPO2 Status is not 0x00(normal),
    # the value is invalid and always be 127(0x7F)

    # Pulse Rate
    # range is 0~250，If SPO2 Status is not 0x00(normal), the value is invalid and always be 255(0xFF)
    ###########################################################################
    spo2 = data[1]
    pr = data[2]
    ###########################################################################
    return str(spo2)+'S'+str(pr)


def temperature(data):  # 0x05
    ''' Returns the temperature value '''
    # data[0] : TEMP Status
    # data[1] : TEMP Integral
    # data[2] : TEMP Decimal

    # TEMP Status
    # 0x00 normal
    # 0x01 TEMP sensor is off

    # TEMP Integral
    # Temperature Integral part, range is 0-45

    # TEMP Decimal
    # Temperature Decimal part, range is 0-9

    # Calculate
    # Real temperature = TEMP Integral + （TEMP Decimal/10）
    # eg：if TEMP Integral = 37，and TEMP Decimal = 5
    # then the real temperatue = 37.5，unit：ºC（centidegree)

    # If TEMP Status is not 0x00(normal)，then the
    # TEMP Integral and TEMP Decimal are both equal to 0 (invalid value)
    ###########################################################################
    temp = data[1] + (data[2]/10)
    ###########################################################################
    return str(temp)


def spo2_wave(data):  # 0xFE
    ''' Returns the waveform of the SPO2 signal '''
    # data[0] : SPO2 Wave amplitude

    # SPO2 Wave amplitude, that is SPO2 Plethymography
    # value，range is 0-100
    ###########################################################################
    return data[0]

def spo2_wave(data):  # 0xFE
    ''' Returns the waveform of the SPO2 signal '''
    # data[0] : SPO2 Wave amplitude

    # SPO2 Wave amplitude, that is SPO2 Plethymography
    # value，range is 0-100
    ###########################################################################
    return data[0]

def respiration_wave(data):  # 0xFF
    ''' Returns the waveform of the respiration '''
    # data[0] : RESP Wave amplitude
    # RESP Wave amplitude，that is RESP Plethymography
    # value，range is 0-250
    ###########################################################################
    return data[0]
