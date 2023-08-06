"""Helper functions for the GUI. Intended design is functional programming."""

import os
import configparser
import threading
import logging
import pathlib
import platform

import subprocess
import sys
from typing import Callable
from datetime import datetime

from colorama import Fore as F

import dearpygui.dearpygui as dpg
from ..gui.interface import Megatron
from ..gui.interface import format_output

from ..db.helpers import check_and_load_config

R = F.RESET
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
WORKING = ROOT / "src" / "gui"


# datetime object containing current date and time
now = datetime.now()

loggey = logging.getLogger(name=__name__)

loggey.info(msg="class Megatron instatiated")
data_vehicle: Megatron = Megatron()

dpg.create_context()
loggey.info(msg="Remote colors initialized")


# Green Button Theme
with dpg.theme() as grn_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 255, 0, 255))  # GREEN
# Red Button Theme
with dpg.theme() as red_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0, 255))  # RED
# Blue Button Theme
with dpg.theme() as blue_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 255, 255))  # BLUE
# Grey Button Theme
with dpg.theme() as grey_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (105, 105, 105, 255))  # GREY
# Orange Button Theme
with dpg.theme() as orng_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 165, 0, 255))  # ORANGE

# load the intial contents of the database for comparison upon new save
loggey.info(msg="initial loading database")


def device_names() -> list[str]:
    """Use a bash script to list connected microarchitectures."""
    if platform.system().lower != "windows":
        # Avoid crashing program if there are no devices detected
        try:
            listing_script = [
                # f'#!/bin/bash\n'
                f'for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev | grep "ACM"); do\n'
                f'(syspath={"${sysdevpath%/dev}"}\n'
                f'devname={"$(udevadm info -q name -p $syspath)"}\n'
                f'[[ {"$devname"} == "bus/"* ]] && exit\n'
                f'eval "$(udevadm info -q property --export -p $syspath)"\n'
                f'[[ -z "$ID_SERIAL" ]] && exit\n'
                f'echo "/dev/$devname - $ID_SERIAL"\n'
                f") done"
            ]
            devices: subprocess.CompletedProcess[str] = subprocess.run(
                args=listing_script,
                shell=True,
                stdout=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                capture_output=False,
                check=True,
            )
        except TypeError:
            loggey.warning(
                msg=f"No devices detected | {device_names.__name__}")
            devices = subprocess.CompletedProcess(
                args="",
                returncode=1,
                stdout="",
                stderr="",
            )

    _devices: list = list(
        devices.stdout.strip().split(
            sep="\n"))  # type: ignore

    loggey.info(msg=f"Devices found: {_devices} | {device_names.__name__}")

    # If there is only one device skip the hooplah
    if len(_devices) == 1:
        return _devices
    return sorted(_devices)


DEVICE: list[str] = device_names()


def card_state(channel: int) -> None:
    """Get the present state of the card."""
    # Refresh indicators; this grants state of the card
    card_stats = get_card_status()

    try:  # If the card is not connected, then skip
        card_stats["power"][channel - 1]
    except IndexError:
        dpg.set_value(
            item=f"power_{channel}_indicator",
            value="N/A",
        )
        dpg.set_value(
            item=f"bandwidth_{channel}_indicator",
            value="N/A",
        )

        return

    # Power state
    if int(
        dpg.get_value(item=f"power_{channel}"),
    ) != int(card_stats["power"][channel - 1]):
        dpg.set_value(
            item=f"power_{channel}_indicator",
            value=f"{int(card_stats['power'][channel-1])} pwr",
        )

    # frquency state
    if int(
        dpg.get_value(item=f"freq_{channel}"),
    ) != int(card_stats["freq"][channel - 1]):
        dpg.set_value(
            item=f"frequency_{channel}_indicator",
            value=f"{card_stats['freq'][channel-1]} MHz",
        )

    # bandwidth state
    if int(
        dpg.get_value(item=f"bandwidth_{channel}"),
    ) != int(card_stats["bw"][channel - 1]):
        dpg.set_value(
            item=f"bandwidth_{channel}_indicator",
            value=f"{int(card_stats['bw'][channel-1])} %",
        )

    # Clear the card state if field is the same as the input
    if int(
        dpg.get_value(item=f"power_{channel}"),
    ) == int(card_stats["power"][channel - 1]):
        dpg.configure_item(
            item=f"power_{channel}_indicator",
            default_value="",
        )

    if int(
        dpg.get_value(item=f"freq_{channel}"),
    ) == int(card_stats["freq"][channel - 1]):
        dpg.configure_item(
            item=f"frequency_{channel}_indicator",
            default_value="",
        )

    if int(
        dpg.get_value(item=f"bandwidth_{channel}"),
    ) == int(card_stats["bw"][channel - 1]):
        dpg.configure_item(
            item=f"bandwidth_{channel}_indicator",
            default_value="",
        )


def start_up_card_state() -> None:
    """Specialized function to display card state at startup."""
    # Refresh indicators; this grants state of the card
    card_stats = get_card_status()

    for i in range(1, 9):
        try:  # If the card is not connected, then skip
            card_stats["power"][i - 1]
        except (IndexError, KeyError):
            dpg.set_value(
                item=f"power_{i}_indicator",
                value="N/A",
            )
            dpg.set_value(
                item=f"bandwidth_{i}_indicator",
                value="N/A",
            )

            continue

        # check if the input value is different from the card state
        if int(dpg.get_value(item=f"power_{i}")) != int(
                card_stats["power"][i - 1]):
            dpg.set_value(
                item=f"power_{i}_indicator",
                value=f"{int(card_stats['power'][i-1])} pwr",
            )

        if int(dpg.get_value(item=f"freq_{i}")) != int(
                card_stats["freq"][i - 1]):
            dpg.set_value(
                item=f"frequency_{i}_indicator",
                value=f"{card_stats['freq'][i-1]} MHz",
            )

        if int(dpg.get_value(item=f"bandwidth_{i}")) != int(
                card_stats["bw"][i - 1]):
            dpg.set_value(
                item=f"bandwidth_{i}_indicator",
                value=f"{int(card_stats['bw'][i-1])} %",
            )


def return_teensy(device_list: list[str] = DEVICE) -> dict[str, str]:
    """Return the device path and serial of the name Teensy."""
    teensy_info: dict[str, str] = {}

    # Initial process the device names
    device = [device.split(sep="_") for device in device_list]

    # filter and return only Teensy devices
    desired_device = [device for device in device if "Teensy" in device[0]]

    # Create the dictionary of the Teensy path and serial number
    for _i, val in enumerate(desired_device):
        teensy_info[val[-1]] = val[0].split(sep="-")[0]

    # if teensy_info == {}:
    #     loggey.error(msg="No Teensy device found")
    #     return {"0": "0"}

    return teensy_info


def get_device_path_from_serial_number() -> str:
    """Get the device path from the serial number."""
    loggey.debug(msg=f"{get_device_path_from_serial_number.__name__}()")

    # Get the serial number from the GUI
    try:
        serial_number: str = str(dpg.get_value(
            item="device_indicator"
        )).split(sep=":")[
            1
        ]
    except IndexError:
        loggey.error(
            msg=f"No serial number found "
            f"|{get_device_path_from_serial_number.__name__}()"
        )
        return "/dev/ttyACM0"

    # Get the list of devices in a list of dictionaries
    devices = return_teensy(DEVICE).items()

    # Loop through the list of devices and compare to serial number
    for device in devices:
        if int(device[0]) == int(serial_number):
            device_path = device[1]
            loggey.debug(msg=f"Device path: {device_path}")

            loggey.info(
                f"Device path: {device_path} |"
                f" {get_device_path_from_serial_number.__name__}()"
            )

            return device_path

    return "No Match"


TEENSY_DETAILS: dict = return_teensy()


def compare_device_serial_to_config(serial_num: str) -> bool:
    """Compare the selected serial to the serial in the config."""
    # Get the device serial number directly from the GUI

    # Get the list of devices in a list of dictionaries
    parser, _ = read_config(file=f"{WORKING}/_configs/card_config.ini")

    devices = []

    try:
        devices: list[int] = [
            int(parser["mgtron"][f"card_{i}"]) for i in range(1, 9)]
    except (KeyError, ValueError):
        loggey.warning(msg="No serial number found or invalid serial number")

    # Loop through the list of devices and compare to serial number
    for device in devices:
        if device == int(serial_num):
            serial_number = device
            loggey.debug(
                msg=f"Serial Number: {serial_number} matched |"
                f" {compare_device_serial_to_config.__name__}()"
            )
            return True

    return False


def validate_user_input(
    channel: int
):
    """Ensure the input fields respond as expected."""
    power_input = dpg.get_value(item=f"power_{channel}")
    band_input = dpg.get_value(item=f"bandwidth_{channel}")
    freq_input = dpg.get_value(item=f"freq_{channel}")
    is_power_valid = True
    is_band_valid = True
    is_freq_valid = True
    forbidden = ["*", "!", "@", "#", "$", "%", "^", "&", "*",
                 "(", ")", "_", "+", "=", """/""", "-", "?", ".."]

    # Checks if user input is blank, or has invalid characters
    for invalid in forbidden:
        match power_input, invalid:
            case ("", invalid):
                dpg.set_value(item=f"power_{channel}", value="0")
            case (power_string, invalid) if invalid in power_string:
                dpg.set_value(item=f"power_{channel}", value="0")
                is_power_valid = False
        match band_input, invalid:
            case ("", invalid):
                dpg.set_value(item=f"bandwidth_{channel}", value="0")
            case (band_string, invalid) if invalid in band_string:
                dpg.set_value(item=f"bandwidth_{channel}", value="0")
                is_band_valid = False
        match freq_input, invalid:
            case ("", invalid):
                dpg.set_value(item=f"freq_{channel}", value="50")
            case (freq_string, invalid) if invalid in freq_string:
                dpg.set_value(item=f"freq_{channel}", value="50")
                is_freq_valid = False

    # Checks if user inputs numbers past max value or below minimum value
    match is_power_valid, int(dpg.get_value(item=f"power_{channel}")):
        case (True, value) if value > 100:
            dpg.set_value(item=f"power_{channel}", value="100")
        case (True, value) if value < 0:
            dpg.set_value(item=f"power_{channel}", value="0")
    match is_band_valid, int(dpg.get_value(item=f"bandwidth_{channel}")):
        case (True, value) if value > 100:
            dpg.set_value(item=f"bandwidth_{channel}", value="100")
        case (True, value) if value < 0:
            dpg.set_value(item=f"bandwidth_{channel}", value="0")
    match is_freq_valid, float(dpg.get_value(item=f"freq_{channel}")):
        case (True, value) if value > 6400:
            dpg.set_value(item=f"freq_{channel}", value="6400")
        case (True, value) if value < 50:
            dpg.set_value(item=f"freq_{channel}", value="50")


def callstack_helper(
    channel: int,
    freq_value: float = float(),
    pwr_value: int = int(),
    bw_value: int = int(),
):
    """Send the command to the microcontroller."""
    loggey.info(msg=f"{callstack_helper.__name__}() executed")

    dpg.bind_item_theme(
        item=f"stats_{channel}",
        theme=orng_btn_theme,
    )

    loggey.info(f"Channel {channel} Information Sent")

    data_vehicle.change_power(
        channel=channel,
        power_level=convert_power(dpg.get_value(f"power_{channel}")),
        PORT=get_device_path_from_serial_number(),
    )

    data_vehicle.change_bandwidth(
        channel=channel,
        percentage=dpg.get_value(f"bandwidth_{channel}"),
        PORT=get_device_path_from_serial_number(),
    )

    data_vehicle.change_freq(
        channel=channel,
        frequency=dpg.get_value(f"freq_{channel}"),
        PORT=get_device_path_from_serial_number(),
    )

    loggey.info("Ready for next command.\n")

    # Automatically turn the indicators green after command is sent
    # if the power level is zero turn the indicator from green to grey
    [
        dpg.bind_item_theme(
            item=f"stats_{channel}",
            theme=grn_btn_theme,
        )
        if dpg.get_value(f"power_{channel}")
        else dpg.bind_item_theme(
            item=f"stats_{channel}",
            theme=grey_btn_theme,
        ),
    ]
    no_power()


def send_vals(sender, app_data, user_data) -> None:
    """Relational connection between GUI and Megatron class."""
    loggey.info(msg=f"{send_vals.__name__}() executed")

    match user_data:
        case 1:
            validate_user_input(channel=1)
            callstack_helper(channel=1)
        case 2:
            validate_user_input(channel=2)
            callstack_helper(channel=2)
        case 3:
            validate_user_input(channel=3)
            callstack_helper(channel=3)
        case 4:
            validate_user_input(channel=4)
            callstack_helper(channel=4)
        case 5:
            validate_user_input(channel=5)
            callstack_helper(channel=5)
        case 6:
            validate_user_input(channel=6)
            callstack_helper(channel=6)
        case 7:
            validate_user_input(channel=7)
            callstack_helper(channel=7)
        case 8:
            validate_user_input(channel=8)
            callstack_helper(channel=8)
        case _:
            loggey.warning("Unrecognized GUI report of a channel: \n")
            loggey.debug(
                f"Sender: {sender}\n"
                f"App data: {app_data}\n"
                f"User data: {user_data}\n",
            )


def reset_button(sender, app_data, user_data) -> None:
    """Reset all channel power levels to zero."""
    loggey.info("Kill All command Sent")

    try:
        [
            dpg.bind_item_theme(f"stats_{i+1}", orng_btn_theme)
            for i in range(8)
        ]

        data_vehicle.reset_board(
            PORT=get_device_path_from_serial_number(),
        )

        # Automatically turn the indicators grey after power levels are zero
        [
            (
                dpg.bind_item_theme(
                    f"stats_{i+1}",
                    grey_btn_theme),
            )
            for i in range(8)
        ]

    except SystemError as err:
        loggey.error("interupted wifi scan or %s", err)

    loggey.info("Ready for next command.\n")


def send_all_channels(
        sender=None,
        app_data: tuple[Callable[[None], None]] = None,
        user_data=None,
) -> None:
    """Send the data from all channels at once."""
    loggey.debug("%s() executed", send_all_channels.__name__)

    WIFI_SCAN_WIN: str = "128"
    BLE_SCAN_WIN: str = "12"

    loggey.info("sender: %s", sender)
    loggey.info("app_data: %s", app_data)
    loggey.info("user_data: %s", user_data)

    if dpg.does_alias_exist(alias=WIFI_SCAN_WIN):
        # print("Calling wifi_factory")
        user_data[0](app_data=callstack_helper)

    elif dpg.does_alias_exist(alias=BLE_SCAN_WIN):
        # print("ble button pressed")
        user_data[1](callstack_helper)

    else:
        # print("no special case")

        for i in range(1, 9):
            validate_user_input(channel=i)

        # This broke when in a for loop
        callstack_helper(channel=1)
        callstack_helper(channel=2)
        callstack_helper(channel=3)
        callstack_helper(channel=4)
        callstack_helper(channel=5)
        callstack_helper(channel=6)
        callstack_helper(channel=7)
        callstack_helper(channel=8)

    no_power()

    loggey.info("Ready for next command.\n")


def auto_fill_freq(
        freq_val: float = 0.0,
        freq_constant: float = 5.0,
) -> None:
    """Auto fill the frequency column based on the first input."""
    _ = [
        dpg.set_value(
            item=f"freq_{i}",
            value=(
                abs(
                    float(dpg.get_value(f"freq_{i-2}"))
                    - float(dpg.get_value(f"freq_{i-1}"))
                )
                + float(dpg.get_value(f"freq_{i-1}"))
            )
            if float(dpg.get_value(item=f"freq_{i}")) <= 6400
            else 6400.00,
        )
        for i in range(3, 9)
        if not freq_constant
    ]

    _ = [
        dpg.set_value(
            item=f"freq_{i}",
            value=freq_val + freq_constant * (i - 1)
        )
        for i in range(1, 9)
        if freq_constant
    ]


def auto_fill_power() -> None:
    """Auto fill the power column based on the first input."""
    power_1 = dpg.get_value(item="power_1")

    # Ensure power_1 is greater than 0 and less than 100
    if int(power_1) <= 0:
        power_1 = 0
    elif int(power_1) >= 100:
        power_1 = 100

    _ = [
        dpg.set_value(item=f"power_{i}", value=power_1)
        for i in range(1, 9)
    ]


def auto_fill_bandwidth() -> None:
    """Auto fill the bandwidth column based on the first input."""
    bandwidth_1 = dpg.get_value(item="bandwidth_1")

    # Ensure bandwidth_1 is greater than 0 and less than 100
    if int(bandwidth_1) <= 0:
        bandwidth_1 = 0
    elif int(bandwidth_1) >= 100:
        bandwidth_1 = 100

    _ = [
        dpg.set_value(
            item=f"bandwidth_{i}",
            value=bandwidth_1,
        )
        for i in range(1, 9)
    ]


def change_inputs(sender, app_data, user_data) -> None:
    """Use the mouse wheel to change the field inputs."""
    loggey.info("app data: %s", app_data)
    loggey.info("user data: %s", user_data)
    loggey.info("sender: %s", sender)

    if dpg.is_item_focused(item="power_1"):
        loggey.debug(dpg.get_value("power_1"))


def read_config(file: str) -> tuple[configparser.ConfigParser, list[str]]:
    """Read the config file and return the contents."""
    devices = DEVICE
    parser = configparser.ConfigParser()
    parser.read(filenames=file, encoding="utf-8")
    loggey.info(msg=f"file {file} read | {read_config.__name__}()")

    return parser, devices


def auto_send(sender, app_data, user_data) -> None:
    """Set a flag to indicate when mission buttons should auto send."""
    loggey.debug(msg=f"{auto_send.__name__}()")

    loggey.info("sender: %s", sender)
    loggey.info("app_data: %s", app_data)
    loggey.info("user_data: %s", user_data)

    # Set the button to green
    dpg.bind_item_theme(
        theme=grn_btn_theme if not dpg.get_item_theme(
            item=sender) == grn_btn_theme else None,
        item=sender,
    )

    global AUTO_SEND_FLAG

    # Set the flag
    AUTO_SEND_FLAG = dpg.get_item_theme(
        item=sender) == grn_btn_theme

    loggey.debug(msg=f"Auto send flag: {AUTO_SEND_FLAG}")


def mission(sender, app_data, user_data) -> None:
    """Mission alpha user facing button configuration."""
    name = sender.split("\n")[0].lower()

    label_name = dpg.get_item_configuration(item=sender)['label']

    # Capture only the first part of the button name
    loggey.info(msg="{}() executed".format(sender.split("\n")[0]))

    # Check against the database for the name of the config button as the name
    # of the saved config
    input_vals: dict[str, list] = check_and_load_config(button_name=label_name)

    try:
        # Check if the config file exists and if it does, read it
        parser, _ = read_config(
            file=f"{WORKING}/_configs/{mission.__name__ + '_' + name}.ini"
        )

        [
            (
                dpg.set_value(
                    item=f"freq_{config}",
                    value=float(parser["freq"][f"freq_{config}"])
                    if not input_vals
                    else input_vals["freq"][config - 1],
                ),
                dpg.set_value(
                    item=f"power_{config}",
                    value=int(parser["power"][f"power_{config}"])
                    if not input_vals
                    else input_vals["power"][config - 1],
                ),
                dpg.set_value(
                    item=f"bandwidth_{config}",
                    value=int(
                        parser["bandwidth"][f"bw_{config}"]
                        if not input_vals
                        else input_vals["bw"][config - 1]
                    ),
                ),
            )
            for config in range(1, 9)
        ]

        loggey.debug(msg="Send all flag checking")

        global AUTO_SEND_FLAG

        # If SEND_AUTO_FLAG then SEND_ALL
        if AUTO_SEND_FLAG:
            loggey.info(msg=f"auto send flag: {AUTO_SEND_FLAG}")
            send_all_channels()
        else:
            loggey.info(msg=f"auto send flag: {AUTO_SEND_FLAG}")

    except (KeyError, SystemError, NameError) as an_error:
        loggey.warning(msg=f"Error: {an_error}")


def kill_channel(sender, app_data, user_data: int) -> None:
    """Kill channel w/out resetting power on user facing screen."""
    loggey.debug("%s() executed", kill_channel.__name__)

    PORT = get_device_path_from_serial_number()

    data_vehicle.change_power(
        channel=user_data,
        power_level=0,
        PORT=PORT
    )

    dpg.bind_item_theme(
        item=sender,
        theme=grey_btn_theme)


def device_finder(user_data: int = int()) -> None:
    """Filter all connected devices and present only Teensy devices."""
    loggey.info(msg=f"{device_finder.__name__}() executed")

    teensy_info: dict[str, str] = {}

    # Initial process the device names
    device = [device.split(sep="_") for device in device_names()]

    # filter and return only Teensy devices
    desired_device = [device for device in device if "Teensy" in device[0]]
    loggey.info(msg=f"Devices filtered check: {desired_device} |"
                f"{device_names.__name__}")

    # Create the dictionary of the Teensy path and serial number
    for _i, val in enumerate(desired_device):
        teensy_info[val[-1]] = val[0].split(sep="-")[0]
    loggey.info(msg=f"Teensy info: {teensy_info} | {device_names.__name__}")
    # Can only choose a 'Teensy' device
    for _i, dev in enumerate(teensy_info, start=1):
        # * Source of truth for chosen device
        if user_data == dev:
            # Set the device indicator to the chosen device
            dpg.set_value(
                item="device_indicator",
                value=f"Device:{dev}",
            )

            # Disappear the menu after choosing a device
            dpg.configure_item(item="modal_device_config", show=False)

            # Turn the card select button green when you switch devices
            # and turn the other buttons blue
            (
                dpg.bind_item_theme(
                    item=f"card_{_i}", theme=grn_btn_theme
                ),
                [
                    dpg.bind_item_theme(

                        item=f"card_{_j}",
                        theme=blue_btn_theme,
                    )
                    for _j, _ in enumerate(dev, start=1)
                    if _j != _i and dpg.does_item_exist(item=f"card_{_j}")
                ],
            ) if compare_device_serial_to_config(
                serial_num=str(
                    dpg.get_value(
                        item="device_indicator")).split(
                    sep=":")[1]
            ) else dpg.bind_item_theme(
                # Theoretically, this should never happen
                item=f"card_{_i}",
                theme=grey_btn_theme,
            )

    device_refresh()
    return desired_device


def populate_right_side_buttons() -> list[bool]:
    """Detect if up to eight Teensy devices are connected."""
    # Get the number of connected devices
    num_devices = device_finder().__len__()

    match num_devices:
        # If there are less than 1 device connected, return False
        case x if x < 1:
            return [False]

        # If there are more than 8 devices connected, return True
        # case x if x > 8:
            # return [True]

        # If there are less than 8 devices connected, populate the buttons
        case _:
            # Return true for each device connected and false until 8
            truth = [True] * num_devices
            false = [False] * (8 - len(truth))

            # Append the false values to the truth values
            truth.extend(false)

            # Return the list of booleans
            return truth


def device_refresh(sender=None, app_data=None, user_data=None) -> None:
    """Update the present status of the card."""
    card_stats = get_card_status()

    for i in range(1, 9):
        try:
            if str(
                    dpg.get_value(item=f"power_{i}"),
            ) != str(card_stats["power"][i - 1]):
                dpg.set_value(
                    item=f"power_{i}",
                    value=rev_convert_power(int(card_stats["power"][i - 1])),
                )
                dpg.bind_item_theme(
                    item=f"stats_{i}",
                    theme=grey_btn_theme) if str(
                    dpg.get_value(item=f"power_{i}")
                ) == "0" else dpg.bind_item_theme(
                    item=f"stats_{i}", theme=grn_btn_theme
                )

            if str(
                    dpg.get_value(item=f"freq_{i}"),
            ) != str(card_stats["freq"][i - 1]):
                dpg.set_value(
                    item=f"freq_{i}",
                    value=float(card_stats["freq"][i - 1]),
                )

            if str(
                    dpg.get_value(item=f"bandwidth_{i}"),
            ) != str(card_stats["bw"][i - 1]):
                dpg.set_value(
                    item=f"bandwidth_{i}",
                    value=int(card_stats["bw"][i - 1]),
                )

        except IndexError:
            loggey.warning(msg=f"Index error in {device_refresh.__name__}()")
            dpg.set_value(item=f"power_{i}", value="")
            dpg.set_value(item=f"freq_{i}", value="")
            dpg.set_value(item=f"bandwidth_{i}", value="")
            dpg.bind_item_theme(
                item=f"stats_{i}",
                theme=grey_btn_theme)


def fill_config():
    """Automatically fill the config file with devices detected."""
    parser, devices = read_config(file=f"{WORKING}/_configs/card_config.ini")
    devices = TEENSY_DETAILS
    serial_list = list(devices.keys())
    loggey.info(msg="Populating config file with detected devices")
    loggey.info(msg=f"Devices: {devices}")
    loggey.info(msg=f"length of device: {len(devices)}")
    [
        serial_list.append(str(0)) for _ in range(8 - len(serial_list))
    ]
    try:

        # Ensure eight spots in the config file are filled in if there are
        # not eight devices
        # {
        #     "0": "0" for i in range(8 - len(devices))
        # }
        loggey.info(msg=(devices))
        # Automatically fill in an empty config file
        # parser["mgtron"] = {
        #     f"card_{i+1}": str(dev.split(sep="_")[-1])
        #     for i, dev in enumerate(devices) if len(
        #         str(dev.split(sep="_")[-1])
        #     ) <= 8
        # }
        parser["mgtron"] = {
            f"card_{i+1}": str(dev.split(sep="_")[-1]) if len(
                str(dev.split(sep="_")[-1])) <= 8 else str(0)
            for i, dev in enumerate(serial_list)
        }

        with open(
                file=f"{WORKING}/_configs/card_config.ini",
                mode="w"
        ) as config_file:
            parser.write(config_file)
            loggey.info(msg="Config file has been automatically filled")

    except (KeyError, IndexError):
        loggey.warning(msg="Config file error")
        with open(
                file=f"{WORKING}/_configs/card_config.ini",
                mode="w"
        ) as config_file:
            config_file.write("[mgtron]\n")
            config_file.write("card_1=\n")
            fill_config()


def config_intake() -> None:
    """Read a config file and assign card buttons."""
    parser, devices = read_config(file=f"{WORKING}/_configs/card_config.ini")

    if len(devices) > 1:
        try:
            for dev_count, _ in enumerate(parser["mgtron"], start=1):
                for _, card in enumerate(devices):
                    match card.split(sep="_")[-1] == parser["mgtron"][
                        f"card_{dev_count}"
                    ]:
                        case True if len(card) > 1:
                            dpg.bind_item_theme(
                                item=f"card_{dev_count}",
                                theme=blue_btn_theme,
                            )
                            dpg.configure_item(
                                item=f"card_{dev_count}", enabled=True)
                            loggey.debug(
                                f"{card} is assigned to "
                                f"{parser['mgtron'][f'card_{dev_count}']}"
                            )
                        case False if len(card) == 1:
                            loggey.info(
                                msg="No device filled in on this line "
                                f"{platform.machine()} | "
                                f"{config_intake.__name__}"
                            )
                        case False:
                            loggey.warning(
                                msg="Device ID not detected in order OR "
                                f"not at all on {platform.machine()} | "
                                f"{config_intake.__name__}"
                            )
        except (KeyError, SystemError):
            loggey.warning(
                msg=f"No config file error | {config_intake.__name__}")


def find_bluetooth_and_frequencies() -> bool:
    """Use the linux host to scan for bluetooth signals and frequencies."""
    # send the command: bluetootctl scan on
    subprocess.run(
        ["bluetoothctl", "scan", "on"],
        capture_output=True,
        encoding="utf-8",
        check=False,
    )

    output: subprocess.CompletedProcess = subprocess.run(
        [
            "bluetoothctl",
            "scan",
            "on",
        ],
        capture_output=True,
        encoding="utf-8",
        check=False,
    )

    hardware_column: set[str] = set(output.stdout.split(sep="\n"))

    hardware_ids = {
        int(hardware.split(sep=" ")[0]): int(hardware.split(sep=" ")[-1])
        for hardware in hardware_column
        if hardware != ""
    }

    # print the ordered dictionary
    loggey.info(
        msg=f"Freq and Strength: {hardware_ids} | "
        f"{find_bluetooth_and_frequencies.__name__}"
    )

    return len(hardware_ids) > 0


def card_config(card_number: int = int()) -> None:
    """Read the config file and set the values in the GUI."""
    try:
        parser, _ = read_config(
            file=f"{WORKING}/_configs/card_{card_number}.ini")

        [
            (
                dpg.set_value(
                    item=f"freq_{config}",
                    value=float(parser["freq"][f"freq_{config}"])
                ),
                dpg.set_value(
                    item=f"power_{config}",
                    value=int(parser["power"][f"power_{config}"]),
                ),
                dpg.set_value(
                    item=f"bandwidth_{config}",
                    value=float(parser["bandwidth"][f"bw_{config}"]),
                ),
            )
            for config in range(1, 9)
        ]

    except KeyError:
        loggey.warning(
            msg="Error in reading the config file."
        )

    except SystemError:
        loggey.warning(msg="Invalid data type;  Expected floating point value")


def card_selection(
        sender=None,
        app_data=None,
        user_data: int = int()
) -> None:
    """Load the selected cards prefix when selected."""
    parser, _ = read_config(file=f"{WORKING}/_configs/card_config.ini")

    loggey.info(msg=f"selected card: {user_data} | {card_selection.__name__}")
    loggey.info(msg=parser["mgtron"][f"card_{user_data}"])

    # Manipulate the set to accomplish a loop without the currently selected
    # button
    card_list: set[int] = {1, 2, 3, 4, 5, 6, 7, 8}
    match user_data:
        case 1:
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme
            )
            dpg.set_value(
                item="device_indicator",
                value=f"Device:{parser['mgtron']['card_1']}"
            )
            try:
                device_finder(user_data=int(parser["mgtron"]["card_1"]))
            except ValueError:
                loggey.error(msg="No devices detected")
                dpg.bind_item_theme(
                    item=f"card_{user_data}", theme=red_btn_theme
                )
                return

            # Blue all other active card buttons and make this one green when
            # clicked
            card_list.remove(1)

            # Turn only this button blue
            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=1)
            loggey.info(
                msg=f"Card 1 config loaded | {card_selection.__name__}")

        case 2:
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme
            )
            dpg.set_value(
                item="device_indicator",
                value=f"Device:{parser['mgtron']['card_2']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_2"]))

            card_list.remove(2)

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,
                    )
                    for greyed_card in card_list
                ]

            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=2)
            loggey.info(
                msg=f"Card 2 config loaded | {card_selection.__name__}")

        case 3:
            card_list.remove(3)
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme
            )
            dpg.set_value(
                item="device_indicator",
                value=f"Device:{parser['mgtron']['card_3']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_3"]))

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=3)
            loggey.info(
                msg=f"Card 3 config loaded | {card_selection.__name__}")

        case 4:
            card_list.remove(4)
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme
            )
            dpg.set_value(
                item="device_indicator",
                value=f"Device:{parser['mgtron']['card_4']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_4"]))

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=4)
            loggey.info(
                msg=f"Card 4 config loaded | {card_selection.__name__}")

        case 5:
            card_list.remove(5)
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme
            )
            dpg.set_value(
                item="device_indicator",
                value=f"Device:{parser['mgtron']['card_4']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_4"]))

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=5)
            loggey.info(
                msg=f"Card 5 config loaded | {card_selection.__name__}")

        case 6:
            card_list.remove(6)
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme
            )
            dpg.set_value(
                item="device_indicator",
                value=f"Device:{parser['mgtron']['card_6']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_6"]))

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=6)
            loggey.info(
                msg=f"Card 6 config loaded | {card_selection.__name__}")

        case 7:
            card_list.remove(7)
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme
            )
            dpg.set_value(
                item="device_indicator",
                value=f"Device:{parser['mgtron']['card_7']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_7"]))

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=7)
            loggey.info(
                msg=f"Card 7 config loaded | {card_selection.__name__}")

        case 8:
            card_list.remove(8)
            dpg.bind_item_theme(
                item=f"card_{user_data}", theme=grn_btn_theme
            )
            dpg.set_value(
                item="device_indicator",
                value=f"Device:{parser['mgtron']['card_8']}"
            )
            device_finder(user_data=int(parser["mgtron"]["card_8"]))

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,
                    )
                    for greyed_card in card_list
                ]
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return

            # card_config(card_number=8)
            loggey.info(
                msg=f"Card 8 config loaded | {card_selection.__name__}")

        case _:
            loggey.warning(msg=f"No card selected: {user_data}")
        # card_l
        #           try:ist.remove(user_data)

            try:
                [
                    dpg.bind_item_theme(
                        item=f"card_{greyed_card}",
                        theme=blue_btn_theme,
                    )
                    for greyed_card in card_list
                ]
                loggey.error(
                    msg=f"No card data loaded | {card_selection.__name__}")
            except SystemError:
                loggey.warning(msg="Other cards not found")
                return


def get_card_status() -> dict[str, list]:
    """Grab the status of the card for state tracking."""
    card_data: dict[str, list] = {}

    # Get the path of the presently selected device
    path = get_device_path_from_serial_number()

    try:
        data_vehicle.status(
            PORT=str(path),
        )

        data = format_output(PORT=path)

        loggey.debug(msg=f"raw card status: {data}")

        # Get the channel, frequency, power, and bandwidth
        channel: list[int] = [int(i) for i in data["channel"]]
        frequency: list[float] = [float(i) for i in data["freq"]]
        power: list[float] = [float(i) for i in data["power"]]
        bandwidth: list[float] = [float(i) for i in data["bandwidth"]]

    except IndexError:
        loggey.warning(msg=f"{get_card_status.__name__} failed")
        # Log the line number
        loggey.error(

            msg=f"Line number: {sys.exc_info()[-1].tb_lineno} - No devs found"
        )

        return card_data

    # if not channel:

    card_data["channel"] = channel
    card_data["freq"] = frequency
    card_data["power"] = power
    card_data["bw"] = bandwidth

    return card_data


loggey.debug(msg="EOF")


def reset_status_text(channel: int) -> None:
    """Remove the text above the input fields."""
    # Reset the text above the input after every send command
    dpg.configure_item(item=f"power_{channel}_indicator", show=False)
    dpg.configure_item(item=f"frequency_{channel}_indicator", show=False)
    dpg.configure_item(item=f"bandwidth_{channel}_indicator", show=False)


def db_error(sender=None, app_data=None, user_data=None) -> None:
    """Display a modal popup with the error message."""


def convert_power(power: int) -> int:
    """Map the input from 0 to 100 and convert to 0 to 63."""
    loggey.debug(msg=f"{convert_power.__name__}()")

    loggey.info(msg=f"Power prior to conversion: {power}")
    # Map the input from 0 to 100 and convert to 0 to 63
    try:
        power = int(
            round(
                map_range(
                    x=int(power),
                    in_min=0,
                    in_max=100,
                    out_min=0,
                    out_max=63,
                ),
            ),
        )
    except ValueError:
        loggey.warning(msg=f"{convert_power.__name__} failed")
        # Log the line number
        loggey.error(

            msg=f"Line number: {sys.exc_info()[-1].tb_lineno} - No input found"
        )

        return 0

    loggey.info(msg=f"Power after conversion: {power}")

    # Limit the power to 63
    if power > 63:
        power = 63

    return power


def rev_convert_power(power: int) -> int:
    """Map the input from 0 to 63 and convert to 0 to 100."""
    loggey.debug(msg=f"{rev_convert_power.__name__}()")

    loggey.info(msg=f"Power prior to conversion: {power}")

    # Map the input from 0 to 63 and convert to 0 to 100
    power = int(
        round(
            map_range(
                x=int(power),
                in_min=0,
                in_max=63,
                out_min=0,
                out_max=100,
            ),
        ),
    )

    loggey.info(msg=f"Power after conversion: {power}")

    return power


def map_range(
    x: int,
    in_min: int,
    in_max: int,
    out_min: int,
    out_max: int,
) -> float:
    """Map the input from 0 to 100 and convert to 0 to 63."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def change_card_name(sender, app_data, user_data) -> None:
    """Change the name of the card select button that is currently selected."""
    # Parse the sender to get the card select button
    # by splitting the sender string on the underscore
    card_select_button = sender.split("_")[1]

    card_item = f"card_{card_select_button}"

    # If user selected name is too long, add a new line

    len_cap = 6
    max_cap = 10

    if len(app_data) > len_cap:
        app_data = app_data[:len_cap] + "\n" + app_data[len_cap:]

    # Truncate the name if it is too long
    if len(app_data) > max_cap:
        app_data = app_data[:max_cap]

    # Change the name of the card select button
    dpg.configure_item(item=card_item, label=app_data)


def save_init():
    """Save the current config to the init file."""
    loggey.debug(msg="Saving init file")

    dpg.save_init_file("dpg.ini")


def connect_device(sender, app_data, user_data) -> None:
    """Connect to the device and send the config to the GUI."""
    try:
        # Grab the list of Teensy devices connected
        devices: dict[str, str] = return_teensy(DEVICE)

        if len(devices) == 1:
            dpg.add_menu_item(
                parent="modal_device_config",
                label=f"{devices.popitem()[0].upper()}",
            )

        elif len(devices) > 1:
            [
                (
                    dpg.configure_item(
                        item="modal_device_config",
                        children=[
                            dpg.add_menu_item(
                                parent="modal_device_config",
                                label=f"{device.upper()}",
                                callback=device_finder,
                                user_data=device,
                            )
                        ],
                    )
                )
                for device in devices
            ]
        else:
            pass  # Error handled elsewhere

    except (TypeError, NameError, KeyError, SystemError, ValueError):
        dpg.add_menu_item(
            parent="choose_device",
            label="DEVICE NUMBER: NOT FOUND",
            callback=lambda: dpg.configure_item(
                item="modal_device_config", show=False),
        )
        loggey.error(msg="No device detected")

        [
            dpg.bind_item_theme(
                item=f"stats_{channel}",
                theme=red_btn_theme,
            )
            for channel in range(1, 9)
        ]
        dpg.add_text(
            parent="device_config",
            tag="device_indicator",
            default_value="",
            pos=(5, 35),
        )


def no_power():
    """If the power input field is 0 then turn the stats indicator grey."""
    # loggey.debug(msg=f"{no_power.__name__}()")

    current_power = [
        str(dpg.get_value(item=f"power_{i}")) for i in range(1, 9)]

    for i in range(1, 9):
        dpg.bind_item_theme(
            item=f"stats_{i}",
            theme=grey_btn_theme,
        ) if current_power[
            i - 1
        ].isdigit() and current_power[i - 1] == "0" else None


def numpad(sender, app_data, user_data):
    """Open the numpad for the power input field."""
    loggey.debug(msg=f"{numpad.__name__}()")
    loggey.debug(msg=f"Sender: {sender}")

    if dpg.is_item_focused(item="freq_1") and dpg.is_item_hovered(
        item="freq_1"
    ):

        # Open the numpad
        with dpg.window(
            modal=True,
                pos=(100, 100),
                parent=sender,
                tag="numpad",
                label="NUMPAD",
                show=True,
                width=200,
                height=300,
        ):

            dpg.add_text(
                default_value="Enter Power",
                parent="numpad",
                tag="numpad_text",
                pos=(5, 5),
            )


def launch_ble_server(path: pathlib.Path) -> None:
    """Launch the rust BLE server."""
    loggey.debug(msg=f"{launch_ble_server.__name__}()")
    loggey.info(msg=f"Path: {path}")

    cmd = str(path)

    # Launch the BLE server
    exit_code = os.system(cmd)  # returns the exit code in unix
    # print(f"\nExit code: {exit_code}\n")

    if exit_code != 0:
        loggey.error(msg=f"BLE server in erroneous state: {exit_code}")

    loggey.info(msg="BLE server launched")


def launch_wifi_server(path: pathlib.Path) -> None:
    """Launch the rust WiFi server."""
    loggey.debug(msg=f"{launch_wifi_server.__name__}()")
    loggey.info(msg=f"Path: {path}")

    cmd = str(path)

    # Launch the WiFi server
    exit_code = os.system(cmd)  # returns the exit code in unix
    # print(f"\nExit code: {exit_code}\n")

    if exit_code != 0:
        loggey.error(msg=f"WiFi server in erroneous state: {exit_code}")

    loggey.info(msg="WiFi server launched")


start_server = threading.Thread(
    target=launch_ble_server, args=(f"{ROOT}/src/assets/blueio_rs", ),
)
start_server.daemon = True
start_server.start()

start_server = threading.Thread(
    target=launch_wifi_server, args=(f"{ROOT}/src/assets/wifi_rs", ),
)
start_server.daemon = True
start_server.start()


def tooltips() -> None:
    """Add tooltips to the GUI."""
    loggey.debug(msg=f"{tooltips.__name__}()")

    if not dpg.does_item_exist(item="tooltip"):
        # Tooltip
        with dpg.tooltip(
                tag="tooltip_window",
                parent="mssn_scan_jam"
        ) as wifi_scan_jam_btn:
            # Create the tooltip for every button
            dpg.add_text(
                tag="tooltip",
                parent=wifi_scan_jam_btn,
                default_value="Scan for WiFi networks"
            )

        with dpg.tooltip(
                tag="tooltip_window_1",
                parent="mssn_bluetooth_scan"
        ) as ble_scan_jam_btn:
            dpg.add_text(
                tag="tooltip_1",
                parent=ble_scan_jam_btn,
                default_value="Scan for BLE devices"
            )
    else:
        dpg.delete_item(item="tooltip_window")
        dpg.delete_item(item="tooltip_window_1")


def main():
    """Minor testing throughout development."""
    # if not compressed_data:

    # store the 'freq_dl' column in a df variable
    print(convert_power(40))


if __name__ == "__main__":
    main()
