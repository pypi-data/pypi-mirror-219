"""Make remote API calls to find Bluetooth device names."""


from datetime import datetime
from typing import Callable

import json
import time
import logging
import requests
import tabulate 
tabulate.PRESERVE_WHITESPACE = True
from decouple import config

from colorama import Fore as F

import dearpygui.dearpygui as dpg

from .ble_data import ble_data_complete
from ..globals.helpers import disble_select_btns

from ..globals.helpers import enable_select_btns
from ..globals.helpers import BLE_BTNS_LIST


loggei = logging.getLogger(name=__name__)

R = F.RESET


# Blue Button Theme
with dpg.theme() as blue_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 255, 255))  # BLUE
# Orange Button Theme
with dpg.theme() as orng_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 165, 0, 255))  # ORANGE


def get_device_name(mac: str) -> dict:
    """Make the remote API call to get the device name."""
    api_key: str = config("API_KEY")

    url = "https://mac-address-lookup1.p.rapidapi.com/static_rapid/mac_lookup/"

    # print(f"mac: {mac}")
    querystring = {"query": mac}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "mac-address-lookup1.p.rapidapi.com"
    }

    response = requests.get(
        url,
        headers=headers,
        params=querystring,
        timeout=5,
    )

    # print(json.dumps(response.json(), indent=4))

    return response.json()


def bluetooth_scan_jam(sender) -> None:
    """Scan the local bluetooth channels and jam them."""
    loggei.info(msg="BLE method called")

    # Disable the buttons that should not be used during the scan
    disble_select_btns(*BLE_BTNS_LIST, _dpg=dpg)

    try:
        # Conditional lgic to determine if the scan is in progress
        if dpg.get_item_theme(item=sender) == orng_btn_theme:
            dpg.bind_item_theme(
                item="mssn_bluetooth_scan",
                theme=blue_btn_theme,
            )

            dpg.configure_item(
                item=sender,
                label="  BLUETOOTH\n   SCAN",
            )
            loggei.debug(msg="Bluetooth scan button disabled")

            # Delete the open bluetooth scan window
            dpg.delete_item(item="12")
            loggei.debug(msg="Bluetooth scan window deleted")

            # Re-enable the buttons that were disabled
            enable_select_btns(*BLE_BTNS_LIST, _dpg=dpg)

        else:

            # Launch the window that will show the bluetooth information
            dpg.bind_item_theme(
                item=sender,
                theme=orng_btn_theme,
            )
            dpg.configure_item(
                item=sender,
                label="  BLUETOOTH\n   SCAN",
            )
            loggei.debug(msg="Bluetooth scan button enabled")

            with dpg.window(
                tag="12",
                no_scrollbar=True,
                no_collapse=True,
                no_resize=True,
                no_title_bar=True,
                no_move=True,
                pos=(0, 0),
                width=880,
                height=735,
            ):
                with dpg.child_window(
                    tag="ble_labels",
                    pos=(0, 0),
                    width=880,
                    height=715,
                ):
                    dpg.add_text(
                        default_value=" " * 7 + "MAC" + " " * 7 + "|" +
                        " " * 4 +
                        "MANUFACTURER" + " " * 3 + "|" + " " +
                        "RSSI" + " "  + "|" + " " * 2 + "DATE",
                        label="BLUETOOTH LIST",
                    )
                    dpg.add_text(
                        default_value='-'*89
                    )

                with dpg.child_window(
                    tag="ble_list",
                    no_scrollbar=False,
                    pos=(0, 60),
                    width=880,
                    height=680,
                ):

                    # Get the BLE dict information and print to GUI
                    all_data: dict = ble_data_complete()
                    converted_data = []
                    for i in all_data:
                        new_list = []
                        new_list.append(i[0])
                        new_list.append(i[1][0])
                        new_list.append(i[1][1])
                        new_list.append(f" {datetime.now().strftime('%H:%M:%S')}")

                        converted_data.append(new_list)

                    for i in converted_data:
                        mac_diff = 18 - len(i[1])
                        if len(i[0]) < 18:
                            i[0] += " " * mac_diff
                        dpg.add_text(
                            # tag=i[1],  # Causes issue on re-scan
                            default_value=tabulate.tabulate(
                                [i],
                                stralign="left",
                                tablefmt="plain",
                                ),
                        )
                        dpg.add_text(
                            default_value=" "
                        )

    except SystemError:
        loggei.error(msg="Bluetooth scan window not found")
        return


def bluetooth_defeat(callstack_helper: Callable[[int,], None]) -> None:
    """Generate the Bluetooth frequencies."""
    loggei.info(msg="SCANNING...")

    try:
        dpg.delete_item(item="12")
    except SystemError:
        loggei.error(msg="Bluetooth scan window not found")
        loggei("quitting")
        return

    # Find the bluetooth signals and their frequencies
    bluetooth_blocker_init: list[tuple[int, int, int]] = [
        (2402, 100, 20),
        (2426, 100, 20),
        (2480, 100, 20),
        (2426, 0, 20),
        (2410, 100, 100),
        (2430, 100, 100),
        (2450, 100, 100),
        (2470, 100, 100),
    ]

    _ = [  # Set the values of the bluetooth frequencies
        (
            dpg.set_value(
                item=f"freq_{i}",
                value=float(vals[0]) if isinstance(vals[0], int) else 50.0,
            ),
            dpg.set_value(
                item=f"power_{i}",
                value=vals[1] if int(vals[0]) != 50 else 0,
            ),
            dpg.set_value(
                item=f"bandwidth_{i}",
                value=vals[2],
            ),
            loggei.info("Bluetooth frequency set in GUI: %s", vals),

            # Automatically send the command to the MGTron board
            callstack_helper(channel=i),
        )
        # if hardware_ids
        for i, vals in enumerate(bluetooth_blocker_init, start=1)
    ]

    seconds = 3
    loggei.info("Transmitting for %s seconds...", seconds)

    # loop for 3 seconds without sleep
    t_end = time.time() + seconds

    # Give an opportunity to stop the transmission
    while time.time() < t_end:
        if dpg.is_item_clicked(
                item="Stop_all_channels"
        ):
            loggei.warning(msg="Scan jam stopper clicked")

            return

    loggei.debug("intitial ble transmission complete")
    bluetooth_blocker_post: list[tuple[int, int, int]] = [
        (2402, 100, 20),
        (2426, 100, 20),
        (2480, 100, 20),
        (2426, 0, 20),
        (2410, 0, 20),
        (2430, 0, 20),
        (2450, 0, 20),
        (2470, 0, 20),
    ]

    _ = [  # Set channels 0 thru 5 to power = 0
        (
            dpg.set_value(
                item=f"freq_{i}",
                value=float(vals[0]) if isinstance(vals[0], int) else 50.0,
            ),
            dpg.set_value(
                item=f"power_{i}",
                value=vals[1] if int(vals[0]) != 50 else 0,
            ),
            dpg.set_value(
                item=f"bandwidth_{i}",
                value=vals[2],
            ),
            loggei.debug("Bluetooth frequency set in GUI: %s", vals),

            # Automatically send the command to the MGTron board
            callstack_helper(channel=i),
        )
        # if hardware_ids
        for i, vals in enumerate(bluetooth_blocker_post, start=1)
    ]

    enable_select_btns(*BLE_BTNS_LIST, _dpg=dpg)

    # Set the bluetooth button to be blue
    dpg.bind_item_theme(item="mssn_bluetooth_scan", theme=blue_btn_theme)

    try:
        dpg.delete_item(item="12")
    except SystemError:
        loggei.error(msg="Bluetooth scan window not found")

    loggei.info(msg="Bluetooth yam complete")
