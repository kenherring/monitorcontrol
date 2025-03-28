from monitorcontrol.monitorcontrol import get_monitors, PBP, InputSource
import enum
import time
import sys

@enum.unique
class Mons(enum.Enum):
    U4025QW = 'U4025QW'
    U3821DW = 'U3821DW'

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

def set_input_source (mon: Mons, input_source: InputSource):
    for monitor in get_monitors():
        with monitor:
            try:
                capabilities = monitor.get_vcp_capabilities()
                print('capabilities.model=' + capabilities['model'])
                print ('mon.value=' + mon.value)
                if capabilities['model'] != mon.value:
                    continue

                current_input_source = monitor.get_input_source()
                print(f'current input source: name={current_input_source.name} value=' + str(current_input_source.value))
                if (current_input_source.value == input_source.value):
                    print(f'Already on input source {input_source}')
                    return
                print(f'Changing input source from {current_input_source} to {input_source} for monitor {mon}')
                monitor.set_input_source(input_source)
                time.sleep(3)
                return
            except Exception as e:
                print(f'Error: {e}')
                continue
    print('could not find monitor ' + mon)
    # raise Exception('Monitor not found')

def set_pbp_mode (mon: Mons, mode: str, sub_input: InputSource):
    for monitor in get_monitors():
        with monitor:
            try:
                capabilities = monitor.get_vcp_capabilities()
                if capabilities['model'] != mon.value:
                    continue
                current_mode = monitor.get_pbp()
                print(f'current_pbp=${current_mode}')

                mode_value = mode_value = getattr(PBP, mode.upper())
                if current_mode == mode_value:
                    print(f'Already in mode {mode_value}')
                else:
                    monitor.set_pbp(mode)
                    time.sleep(5)
                    if mode == 'OFF':
                        print('pbp turned off')
                        return
                    new_mode = monitor.get_pbp()
                    print(f'new_pbp=${new_mode}')
                    time.sleep(1)

                # # current_sub_input = monitor.get_sub_input()
                # # print(f'current_sub_input=${current_sub_input}')
                print(f'setting sub_input=${sub_input}')
                monitor.set_sub_input(sub_input)

                return
            except Exception as e:
                print(f'Error: {e}')
                return
    print('could not find monitor ' + mon)
    # raise Exception('Monitor not found')


##### SPLIT SCREEN #####
def main ():
    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] + ' [split|fun|work]')
        return

    match sys.argv[1]:
        case 'split':
            set_input_source(Mons.U4025QW, InputSource.THUNDERBOLT)
            set_pbp_mode(Mons.U4025QW, 'PBP_FIFTY_FIFTY', InputSource.DP1)
        case 'fun':
            set_input_source(Mons.U4025QW, InputSource.THUNDERBOLT)
            set_input_source(Mons.U3821DW, InputSource.USB_C)
            set_pbp_mode(Mons.U4025QW, 'OFF', None)
        case 'work':
            set_pbp_mode(Mons.U4025QW, 'PBP_FIFTY_FIFTY', InputSource.HDMI1)
            set_input_source(Mons.U3821DW, InputSource.DP1)
            set_input_source(Mons.U4025QW, InputSource.DP1)
        case _:
            raise Exception('Invalid mode: ' + sys.argv[1])
    print(f'switched to {sys.argv[1]} mode')

if __name__ == '__main__':
    main()

# set_key_value()
