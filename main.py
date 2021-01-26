#!/usr/bin/python
# -*- coding:utf-8 -*-


import time
import ADS1256
import RPi.GPIO as GPIO
from losantmqtt import Device

try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()

    # Construct device
    device = Device("60104ece5749350006d2e0fd", "213699ae-314a-408e-bd0f-7b496fec009d", "b3623a4b632cb3cb3c80c39eee0f9fe9f2fb3c13990300021b941d01aa61c07c")
    def on_command(device, command):
    print("Command received.")
    print(command["name"])
    print(command["payload"])

    # Listen for commands.
    device.add_event_observer("command", on_command)

    # Connect to Losant.
    device.connect(blocking=False)

    while(True):

        ADC_Value = ADC.ADS1256_GetAll() # READING all Values

        # prepare results
        res1 = ADC_Value[0]*5.0/0x7fffff
        res2 = ADC_Value[1]*5.0/0x7fffff
        res3 = ADC_Value[2]*5.0/0x7fffff
        res4 = ADC_Value[3]*5.0/0x7fffff

        # Print current values
        print ("0 ADC = %lf"%(res1)
        print ("1 ADC = %lf"%(res2)
        print ("2 ADC = %lf"%(res3)
        print ("3 ADC = %lf"%(ADC_Value[3]))
        print ("3 ADC = %lf"%(ADC_Value[3]*5.0))
        print ("3 ADC = %lf"%(ADC_Value[3]*5.0/0x7fffff))
        #    print ("4 ADC = %lf"%(ADC_Value[4]*5.0/0x7fffff))
        #    print ("5 ADC = %lf"%(ADC_Value[5]*5.0/0x7fffff))
        #    print ("6 ADC = %lf"%(ADC_Value[6]*5.0/0x7fffff))
        #    print ("7 ADC = %lf"%(ADC_Value[7]*5.0/0x7fffff))
        print ("\33[9A")

        # Send values to cloud
        device.loop()
        if device.is_connected():
            device.send_state({"mass1": ADC_Value[0]*5.0, "mass2": ADC_Value[1]*5.0, "mass3": ADC_Value[2]*5.0, "mass4": ADC_Value[3]*5.0})

        #Pause
        time.sleep(1)



except :
    GPIO.cleanup()
    print ("\r\nProgram end     ")
    exit()
