import sys

# f strings require python 3.6
assert sys.version_info >= (3, 6), "f strings require python 3.6"
# incomplete list of VCP codes from the MCCS specification
_VCP_CODE_DEFINTIONS = {
    "image_factory_default": {
        "name": "restore factory default image",
        "value": 0x04,
        "type": "wo",
        "function": "nc",
    },
    "image_luminance": {
        "name": "image luminance",
        "value": 0x10,
        "type": "rw",
        "function": "c",
    },
    "image_contrast": {
        "name": "image contrast",
        "value": 0x12,
        "type": "rw",
        "function": "c",
    },
    "image_color_preset": {
        "name": "image color preset",
        "value": 0x14,
        "type": "rw",
        "function": "nc",
    },
    "active_control": {
        "name": "active control",
        "value": 0x52,
        "type": "ro",
        "function": "nc",
    },
    "input_select": {
        "name": "input select",
        "value": 0x60,
        "type": "rw",
        "function": "nc",
    },
    "image_orientation": {
        "name": "image orientation",
        "value": 0xAA,
        "type": "ro",
        "function": "nc",
    },
    "display_power_mode": {
        "name": "display power mode",
        "value": 0xD6,
        "type": "rw",
        "function": "nc",
    },

    ## dell specific??
    "volume": {
        "name": "volume",
        "value": 0x62,
        "type": "rw",
        "function": "nc", ## not sure what this does
    },
    "mute": {
        "name": "mute",
        "value": 0x8D,
        "type": "rw",
        "function": "nc",
    },
    "PBP": {
        "name": "picture by picture",
        "value": 0xE9,
        "type": "rw",
        "function": "nc",
    },
    "swap_usb": {
        "name": "swap usb",
        "value": 0xF7,
        "type": "wo",
        "function": "nc",
    },
    "swap_input": {
        "name": "swap input",
        "value": 0xE5,
        "type": "wo",
        "function": "nc",
    },
    "sub_input": {
        "name": "sub input",
        # "value": 0xE8, ## 232
        "value": 0xE8,
        "type": "rw",
        "function": "nc",
    }

}


class VCPCode:
    """
    Virtual Control Panel code.  Simple container for the control
    codes defined by the VESA Monitor Control Command Set (MCCS).

    This should be used by getting the code from
    :py:meth:`get_vcp_code_definition()`

    Args:
        name: VCP code name.

    Raises:
        KeyError: VCP code not found.
    """

    def __init__(self, name: str):
        self.definition = _VCP_CODE_DEFINTIONS[name]

    def __repr__(self) -> str:
        return (
            "virtual control panel code definition. "
            f"value: {self.value} "
            f"type: {self.type}"
            f"function: {self.function}"
        )

    @property
    def name(self) -> int:
        """Friendly name of the code."""
        return self.definition["name"]

    @property
    def value(self) -> int:
        """Value of the code."""
        return self.definition["value"]

    @property
    def type(self) -> str:
        """Type of the code."""
        return self.definition["type"]

    @property
    def function(self) -> str:
        """Function of the code."""
        return self.definition["function"]

    @property
    def readable(self) -> bool:
        """Returns true if the code can be read."""
        if self.type == "wo":
            return False
        else:
            return True

    @property
    def writeable(self) -> bool:
        """Returns true if the code can be written."""
        if self.type == "ro":
            return False
        else:
            return True
