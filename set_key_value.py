from monitorcontrol import get_monitors
import time

def set_key_value (key: int, value: int) :
    print(f'setting key={key}, value={value}')

def print_vpc () :

    monitors =  get_monitors()
    print(f'Number of monitors: {len(monitors)}')
    for monitor in get_monitors():
        with monitor:
            print('monitor=' + str(monitor))
            try:
                capabilities = monitor.get_vcp_capabilities()
                if capabilities['model'] != 'U4025QW':
                    continue
                # if capabilities['model'] == 'U3821DW':
                #     continue
                print(f'capabilities: {capabilities}')
                return
            #     print('monitor=' + capabilities['model'] + ', current input source=' + str(monitor.get_input_source()))
            #     # print(f'name: ${capabilities.name}')
            #     # monitor.set_input_source('DP1')
            except Exception as e:
                print(f'Error: {e}')
                continue


print_vpc()




# set_key_value()
