from monitorcontrol.monitorcontrol import get_monitors, PBP, InputSource
import enum
import time
import sys

@enum.unique
class Mons(enum.Enum):
    U4025QW = 'U4025QW'
    U3821DW = 'U3821DW'

monitors = None

def set_key_value (key: int, value: int) :
    print(f'setting key={key}, value={value}')


def get_monitor(model, refresh=True):
    global monitors
    if monitors == None:
        monitors = get_monitors()

    try:
        for monitor in monitors:
            with monitor:
                try:
                    if monitor.get_model() == model:
                        return monitor
                except Exception as e:
                    print('  e=' + str(e))
        raise Exception('No monitor found with model ' + model)
    except Exception as e:
        print('e=' + str(e))
        monitors == None
        if not refresh:
            return get_monitor(model, False)
        raise e

    raise Exception(f"No monitor found with model {model}")



def print_vpc () :
    print('print_vpc()')
    monitors =  get_monitors()
    print(f'Number of monitors: {len(monitors)}')
    if monitors == None:
        monitors = get_monitors()
    for monitor in monitors:
        with monitor:
            print('monitor=' + str(monitor))
            try:
                capabilities = monitor.get_vcp_capabilities()
                if capabilities['model'] != 'U4025QW':
                    continue
                print(f'capabilities: {capabilities}')
                return
            except Exception as e:
                print(f'Error: {e}')
                continue

def set_input_source (mon: Mons, input_source: InputSource):
    print('set_input_source mon=' + mon.value + ' input_source=' + str(input_source))

    monitor = get_monitor(mon.value)
    with monitor:
        try:
            current_input_source = monitor.get_input_source()
            if (current_input_source.value == input_source.value):
                print(f'  already on input source {input_source}')
                return
            print(f'  changing input source from {current_input_source} to {input_source} for monitor {mon}')
            monitor.set_input_source(input_source)
            time.sleep(3)
            return
        except Exception as e:
            print(f'  warning: {e}')

def set_pbp_mode (mon: Mons, mode: str, sub_input: InputSource):
    print('set_pbp_mode mon=' + mon.value + ' mode=' + mode + ' sub_input=' + str(sub_input))

    monitor = get_monitor(mon.value)
    with monitor:
        try:
            current_mode = monitor.get_pbp()
            mode_value = getattr(PBP, mode.upper())
            if current_mode == mode_value:
                print(f'  already in mode {mode_value}')
            else:
                print('  set_pbp mode from ' + str(current_mode) + ' to ' + str(mode_value))
                monitor.set_pbp(mode)
                time.sleep(3)

            if mode == 'OFF':
                return
            print(f'  checking sub_input for mode {mode}')
            try:
                current_sub_input = monitor.get_sub_input()
            except Exception as e:
                monitor = get_monitor(mon.value)
                current_sub_input = monitor.get_sub_input()
            print(f'  current_sub_input=${current_sub_input}')
            if (current_sub_input != sub_input):
                print(f'  setting sub_input=${sub_input}')
                monitor.set_sub_input(sub_input)

            return
        except Exception as e:
            print(f'  warning: {e}')


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
            set_pbp_mode(Mons.U4025QW, 'OFF', None)
            set_input_source(Mons.U3821DW, InputSource.USB_C)
            set_input_source(Mons.U4025QW, InputSource.THUNDERBOLT)
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
