from monitorcontrol.monitorcontrol import get_monitors, InputSource

def set_input_source (monitorModel, inputSourceValue) :
    for monitor in get_monitors():
        with monitor:
            try:
                capabilities = monitor.get_vcp_capabilities()
                if capabilities['model'] != monitorModel:
                    continue
                current_input_source = monitor.get_input_source()
                print(f'current input source: name={current_input_source.name} value=' + str(current_input_source.value))
                if (current_input_source.value == inputSourceValue):
                    print(f'Already on input source {inputSourceValue}')
                    continue
                print(f'Changing input source from {current_input_source} to {inputSourceValue} for monitor {monitorModel}')
                monitor.set_input_source(inputSourceValue)
            except Exception as e:
                print(f'Error: {e}')
                continue

set_input_source('U4025QW', InputSource.THUNDERBOLT) ## 25 == 0x19 == THUNDERBOLT
set_input_source('U3821DW', InputSource.USB_C) ## 27 == 0x1B == USB-C
