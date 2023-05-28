
#!/usr/bin/env python3

import subprocess
def get_water_temp():
    # Read Temperature
    tempread = subprocess.check_output(['cat', '/sys/bus/w1/devices/28-0307979413a9/w1_slave'], encoding='utf-8')

    # Extract the temperature value and format it
    temp = float(tempread.split('=')[-1])/1000
    temp_formatted = '{:.2f}'.format(temp)

    # Output
    print(f"Water Temperature Is {temp_formatted}°C")

if __name__ == "__main__":  
    get_water_temp()