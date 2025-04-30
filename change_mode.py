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


def get_monitor(mon: Mons, refresh=True):
    # print(f'get_monitor model={mon} refresh={refresh}')
    monitors = get_monitors()

    try:
        for monitor in monitors:
            with monitor:
                try:
                    if monitor.get_model() == mon:
                        return monitor
                except Exception as e:
                    print('  e=' + str(e))
        raise Exception(f'  [get_monitor] No monitor found with model {mon}')
    except Exception as e:
        print('  [get_monitor] e=' + str(e))
        if not refresh:
            return get_monitor(mon, False)
        raise e


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

def set_pbp_mode (mon: Mons, mode: PBP):
    print(f'set_pbp_mode mon={mon.value} mode={mode}')
    monitor = get_monitor(mon.value)
    with monitor:
        try:
            current_mode = monitor.get_pbp()
            if current_mode == mode:
                print(f'  already in mode {mode}')
            else:
                print(f'  set_pbp mode from {current_mode} to {mode}')
                monitor.set_pbp(mode)
                time.sleep(8)

            return
        except Exception as e:
            print(f'  warning: {e}')

def set_sub_input (sub_input):
    print(f'set_sub_input sub_input={sub_input}')
    # current_sub_input = monitor.get_sub_input()
    # print(f'  current_sub_input=${current_sub_input}')
    # if (current_sub_input != sub_input):
    #     print(f'  setting sub_input=${sub_input}')
    #     monitor.set_sub_input(sub_input)

##### SPLIT SCREEN #####
def main ():
    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] + ' [split|fun|work]')
        return

    match sys.argv[1]:
        case 'split':
            set_input_source(Mons.U4025QW, InputSource.THUNDERBOLT)
            set_pbp_mode(Mons.U4025QW, 'PBP_FIFTY_FIFTY')
        case 'fun':
            set_pbp_mode(Mons.U4025QW, PBP.OFF)
            set_input_source(Mons.U3821DW, InputSource.USB_C)
            set_input_source(Mons.U4025QW, InputSource.THUNDERBOLT)
        case 'work':
            set_pbp_mode(Mons.U4025QW, PBP.PBP_FIFTY_FIFTY)
            set_input_source(Mons.U3821DW, InputSource.DP1)
            set_input_source(Mons.U4025QW, InputSource.DP1)
        case _:
            raise Exception('Invalid mode: ' + sys.argv[1])
    print(f'switched to {sys.argv[1]} mode')

if __name__ == '__main__':
    main()

# set_key_value()
