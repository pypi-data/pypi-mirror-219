"""Helper functions for wifi business of the GUI."""

import os
import pathlib
from ..globals.helpers import WIFI_BTNS_LIST
from ..globals.helpers import enable_select_btns
from ..globals.helpers import disble_select_btns
from .scanning import post_ssid
from .scanning import freqs_and_sigs
from .scanning import threaded_scan
from .scanning import find_signals_and_frequencies
from .scanning import convert_signal_to_rssi
from ..gui.helpers import callstack_helper
import logging
from typing import Callable
import dearpygui.dearpygui as dpg
from colorama import Fore as F
import yaml
import tabulate
tabulate.PRESERVE_WHITESPACE = True


loggei = logging.getLogger(name=__name__)

R = F.RESET


# Blue Button Theme
with dpg.theme() as blue_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 255, 255))  # BLUE
# Orange Button Theme
with dpg.theme() as orng_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 165, 0, 255))  # ORANGE
# Grey Button Theme
with dpg.theme() as grey_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, ("128", "128", "128", 255))  # GREY
# Red Button Theme
with dpg.theme() as red_btn_theme, dpg.theme_component(dpg.mvAll):
    dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0, 255))  # RED


def convert_data(data):
    """Convert the data from a list of dictionaries to a list of lists."""
    loggei.debug("%s()", convert_data.__name__)

    if not data:
        return []
    keys = list(data[0].keys())
    result = []
    # Order the keys
    keys = ["ssid", "bssid", "channel", "frequency",  "signal", "security"]

    for dictionary in data:
        values = [dictionary[key] for key in keys]
        result.append(values)

    return result


def wifi_scan_jam(sender) -> None:
    """Scan the local wifi channels and jam them."""
    loggei.info(msg="Scan jammer method called")

    colwidth_delineate = 4
    wifi_button_width = 669

    disble_select_btns(*WIFI_BTNS_LIST, _dpg=dpg)
    #  Determine if the scan is in progress; toggle button

    if dpg.get_item_theme(item=sender) == orng_btn_theme:
        dpg.bind_item_theme(
            item="mssn_scan_jam",
            theme=blue_btn_theme,  # WTF Only hard-coding the color works; Blue
        )
        loggei.debug(msg="WiFi scan button disabled")

        try:
            # Delete the open WiFi scan window
            dpg.configure_item(item=129, show=False, modal=False)
            dpg.configure_item(item="128", show=False, modal=False)

            # Makes no sense why configure first is needed to delete
            dpg.delete_item(item=129)
            dpg.delete_item(item="128")

            dpg.delete_item(item="wifi_scan_window")
            os.remove("wifi_scan_results.yml")

            loggei.debug(msg="WiFi scan window deleted")
        except (SystemError, FileNotFoundError) as err:
            loggei.warning("WiFi scan btn: %s", err)
        finally:
            enable_select_btns(*WIFI_BTNS_LIST, _dpg=dpg)

    else:
        # Turn the button Orange
        dpg.bind_item_theme(
            item=sender,
            theme=orng_btn_theme,
        )

        delete_scan_aliases()

        scan_window(colwidth_delineate, wifi_button_width)

        loggei.debug(msg="WiFi scan jammer method finished")


def delete_scan_aliases(alias_file="wifi_scan_aliases.yml") -> None:
    """Delete the wifi scan aliases."""
    loggei.info("%s()", delete_scan_aliases.__name__)

    try:
        # Read the contents of the YAML file
        with open(alias_file, "r") as read_file:
            alias_data = yaml.load(
                stream=read_file,
                Loader=yaml.FullLoader
            )

            [dpg.delete_item(item=i) for i in alias_data]
            loggei.debug(msg="WiFi scan aliases deleted")

    except (yaml.parser.ParserError, FileNotFoundError):
        loggei.error(
            "%s() failed to read alias file",
            wifi_scan_jam.__name__
        )

    try:
        os.remove(alias_file)  # Delete the file
        loggei.debug(msg="WiFi scan alias file deleted")
    except FileNotFoundError:
        loggei.error(
            "%s() failed to delete alias file",
            wifi_scan_jam.__name__
        )


def scan_window(colwidth_delineate, wifi_button_width) -> None:
    """Create a window to display the scan results."""
    loggei.info("%s()", scan_window.__name__)

    with dpg.window(
        tag=129,
        no_scrollbar=False,
        no_collapse=True,
        no_resize=True,
        no_title_bar=True,
        no_move=True,
        modal=True,
        pos=(0, 50),
        width=880,
        height=675,
    ):

        dpg.configure_item(item=129, show=False)

        # Get the WiFi dict information and print to GUI
        all_data: list[dict[str, str]] = threaded_scan(
            _dpg=dpg,
            linux_data=find_signals_and_frequencies
        )
        dpg.configure_item(item=129, show=True, modal=False)

        all_data = convert_signal_to_rssi(all_data)

        new_data = convert_data(all_data)  # Converts to list of lists
        fill_scan_result(
            converted_data=new_data,
            colwidth_delineate=colwidth_delineate,
            wifi_button_width=wifi_button_width,
        )

        [
            loggei.info("convert scan result: %s", i)
            for i in new_data
        ]

    with dpg.window(
        tag="128",
        pos=(0, -50),
        width=880,
        height=40,
        no_resize=True,
        no_scrollbar=True,
        no_collapse=True,
        no_title_bar=True,
        no_move=True,
    ):
        headers = ["SSID", "MAC", "CH", "FREQ", "SIGNAL", "SECURITY"]

        dpg.add_text(

            default_value=" "*5 + "|" + " "*12 + headers[0] + " "*17 +
            "|" + " " * 8 +
            headers[1] + " " * 5 + "| " + headers[2] + " " * 3 + "|" + " " * 2 +
            headers[3] + " " * 2 + "| " + headers[4] + " " + "| " +
            headers[5] + " " * 2 + "|",

            color=(200, 138, 218, 255),  # Purple
            label="WIFI LIST",
            pos=(0, 58),
        )
    return


def fill_scan_result(
        converted_data: list[list],
        colwidth_delineate: int,
        wifi_button_width: int,
) -> None:
    """Fill the scan results window with the data."""
    loggei.info("%s()", fill_scan_result.__name__)

    for i in (converted_data):

        # Before so length can be calculated
        if len(i[0]) == 0:
            i[0] = f"SSID_{i[1]}"

        ssid_difference = 32 - len(i[0])
        channel_diff = 4 - len(i[2])
        signal_diff = 3 - len(i[4])

        if len(i[0]) < 32:
            i[0] += " " * ssid_difference
        if len(i[2]) < 4:
            i[2] += " " * channel_diff
        if len(i[4]) < 3:
            i[4] += " " * signal_diff
        if len(i[5]) == 0:
            i[5] = "Open"

        temp_list = []
        temp_list.append(i)

        dpg.add_button(
            tag=i[1],  # Causes issue on re-scan unless deleted
            parent=129,
            label=tabulate.tabulate(
                [i],
                stralign="left",
                tablefmt="plain",
                maxcolwidths=[
                    None,
                    None,
                    None,
                    None,
                    None,
                    4,
                ]),
            width=880,
            height=60,
            callback=indicate_tagged_results,
            user_data=(i, i[1]),
        )

        with open("wifi_scan_aliases.yml", "a") as outfile:
            yaml.dump(
                data={i[1]: i[0]},
                stream=outfile,
            )


def indicate_tagged_results(sender, app_data, user_data: list[str]) -> None:
    """Change the color of the sender."""
    loggei.debug("%s()", indicate_tagged_results.__name__)

    loggei.info("User data: %s", user_data)

    # Make a toggle of the selected buttons
    if dpg.get_item_theme(item=sender) == blue_btn_theme:
        # Turn the button green
        dpg.bind_item_theme(
            item=sender,
            theme=None,
        )
    else:
        # Turn the button blue
        dpg.bind_item_theme(
            item=sender,
            theme=blue_btn_theme,
        )

    # Turn user_data into a dict with user_data[0] as the key
    user_datas = {
        user_data[0][0]: {
            "MAC": user_data[0][1],
            "CH": user_data[0][2],
            "FREQ": user_data[0][3].split(" ")[0],
            "SIGNAL": user_data[0][4],
            "SECURITY": user_data[0][5],
        }
    }

    # all_tags: list = [i for i in user_data[1][1]]

    # [print(f"{F.YELLOW}All tags:{R}: {i}") for i in all_tags]

    # print(f"{F.YELLOW}Converted data:{R}: {user_data[1]}")

    # Write the data to a yml file
    with open("wifi_scan_results.yml", "a") as outfile:
        yaml.dump(
            data=user_datas,
            stream=outfile,
        )

    loggei.debug("%s() exiting", indicate_tagged_results.__name__)


def return_indicated_results() -> dict[str, dict[str, str]]:
    """Check which buttons are red and return the data."""
    loggei.debug("%s()", return_indicated_results.__name__)

    # Read the contents of the yml file
    selected_scan_results = yaml.load(
        stream=open("wifi_scan_results.yml", "r"),
        Loader=yaml.FullLoader,
    )

    os.remove("wifi_scan_results.yml")

    alias_dict: dict[str, dict[str, str]] = dict()

    # Get all of the alias themes
    for iterite, color in enumerate(selected_scan_results.items(), start=1):
        if dpg.get_item_theme(color[1]["MAC"]):
            alias_dict.update({color[0]: color[1]})

    # print(f"\n{F.YELLOW}Aliases: {R}{alias_dict}")
    # print(f"{F.YELLOW}Selected scan results: {R}{selected_scan_results}")

    return alias_dict


def activate_wifi_chase() -> None:
    """Send all the requisite information to the MGTron board."""
    loggei.debug("%s()", activate_wifi_chase.__name__)

    user_data: dict[str, dict[str, str]] = return_indicated_results()

    ssid: list[str] = list(user_data.keys())

    # print(f"{F.YELLOW}SSID to search: {R}{ssid}")

    try:
        dpg.delete_item(item=129)
        dpg.delete_item(item="128")
    except SystemError as e:
        loggei.error("System error: %s", e)

    channel_list: list[int] = discern_avail_channels(dpg)

    loggei.info("Channel list: %s", channel_list)

    # If there are no channels available, then all available
    if not channel_list:
        channel_list: list[int] = [1, 2, 3, 4, 5, 6, 7, 8]

    count: int = 4  # len(user_data.keys())

    tracker = 0
    while tracker != count:

        if tracker >= 1:

            try:
                dpg.delete_item(item=129)
                dpg.delete_item(item="128")
            except SystemError as e:
                loggei.error("System error: %s", e)

                # print(f"{F.CYAN}New scan: {tracker + 1}{R}")
                # Get the chase frequencies
                chase_freqs: list[float] = threaded_scan(
                    _dpg=dpg,
                    linux_data=post_ssid,
                    ssid=ssid
                )

                # print("\nChase freqs:", set(chase_freqs))
        else:

            chase_freqs: list[float] = [
                float(i.get("FREQ")) for i in user_data.values()
            ]

            # print("\nChase freqs:", set(chase_freqs))

        disable_scanning_mode(enable_btns=False)

        # Take advantage of the dedup characteristics of a set
        chase_freqs: set[float] = set(chase_freqs)

        # Chase three times
        chase(
            chase_freqs=chase_freqs,
            channel_list=channel_list
        )

        tracker += 1

    disable_scanning_mode(enable_btns=True)
    # Change the mssn_scan_jam button to blue
    dpg.bind_item_theme(
        item="mssn_scan_jam",
        theme=blue_btn_theme,
    )


def chase(
        chase_freqs: set[float],
        channel_list: list[int]
) -> None:
    """Chase the WiFi signal."""
    loggei.info("%s()", chase.__name__)

    [
        (
            dpg.set_value(
                item=f"freq_{ij}",
                value=freq if isinstance(
                    freq, float
                ) else 50.0
            ),
            dpg.set_value(
                item=f"power_{ij}",
                value=100 if int(freq) != 50 else 0
            ),
            dpg.set_value(
                item=f"bandwidth_{ij}",
                value=10 if int(freq) != 50 else 0
            ),
            loggei.info(
                "Frequency, in sig strength order, discovered: %s", ij
            ),
            # Automatically send the command to the MGTron board
            callstack_helper(channel=ij),
        )
        for ij, freq in enumerate(chase_freqs, start=1)
    ]

    dpg.configure_item(
        item="mssn_scan_jam",
        label="WIFI",
    )


def disable_scanning_mode(enable_btns: bool = True) -> None:
    """Disable the wifi scanning mode."""
    loggei.info("%s()", disable_scanning_mode.__name__)

    # Disable the open wifi window
    try:
        dpg.configure_item(item=129, show=False, modal=False)
        dpg.configure_item(item="128", show=False, modal=False)

        dpg.delete_item(item=129)
        dpg.delete_item(item="128")
    except SystemError:
        loggei.warning(msg="WiFi window already closed")

    # Make the wifi button blue
    dpg.bind_item_theme(
        item="mssn_scan_jam",
        theme=blue_btn_theme,
    )

    enable_select_btns(*WIFI_BTNS_LIST, _dpg=dpg) if enable_btns else None


def wifi_kill_all(callstack_helper: Callable[[int, ], None]) -> None:
    """Insert and auto send the top eight scanned channels."""
    loggei.info(msg="Scan jammer method called")

    loggei.info(msg="SCANNING...")

    data = threaded_scan(_dpg=dpg, linux_data=find_signals_and_frequencies)

    # Disable the open wifi window
    try:
        dpg.configure_item(item=129, show=False, modal=False)
        dpg.configure_item(item="128", show=False, modal=False)

        dpg.delete_item(item=129)
        dpg.delete_item(item="128")
    except SystemError:
        loggei.warning(msg="WiFi window already closed")

    freq_and_strength: dict[int, float] = freqs_and_sigs(data, short_list=True)

    loggei.warning(msg=f"Freq & Strength sorted: {freq_and_strength}")

    _ = [
        (
            dpg.set_value(
                item=f"freq_{i}", value=float(freq) if isinstance(
                    freq, float
                ) else 50.0
            ),
            dpg.set_value(
                item=f"power_{i}",
                value=100 if int(freq) != 50 else 0),
            dpg.set_value(
                item=f"bandwidth_{i}",
                value=10 if int(freq) != 50 else 0),
            loggei.debug(
                msg=f"Frequency, in sig strength order, discovered: {freq}"
            ),
            # Automatically send the command to the MGTron board
            callstack_helper(channel=i),
        )
        for i, freq in enumerate(freq_and_strength.values(), start=1)
    ]

    enable_select_btns(*WIFI_BTNS_LIST, _dpg=dpg)

    # Stop looping scan jam if 'KILL ALL' is pressed and hovered over
    # (return if dpg.is_item_clicked(item="Stop_all_channels")),

    # Make the wifi button blue
    dpg.bind_item_theme(
        item="mssn_scan_jam",
        theme=blue_btn_theme,
    )

    loggei.debug(msg="Scan jammer method finished")


def discern_avail_channels(_dpg: dpg) -> list[int]:
    """Determine which channel is available and return the channel number."""
    loggei.debug("%s()", discern_avail_channels.__name__)

    # Get all of the indicator colors
    indicator_color: list = [
        _dpg.get_item_theme(item=f"stats_{i}") for i in range(1, 9)
    ]

    loggei.info("Indicator color: %s", indicator_color)

    grey_theme = 30
    # Find out what channel numbers are available
    free_channels = indicator_color.count(grey_theme)

    loggei.info("Free channels: %s", free_channels)

    if not free_channels:
        loggei.warning(msg="No wifi channels available")
        return []

    # Transform all grey indicies to True and the rest to False
    indicator_color = [
        color == grey_theme for color in indicator_color
    ]

    loggei.info("Indicator color: %s", indicator_color)

    # Keep track of the indices as the channel numbers to the new list
    channel_numbers = [
        i for i, color in enumerate(indicator_color, start=1) if color
    ]

    loggei.info("Channel numbers returned: %s", channel_numbers)

    return channel_numbers


def wifi_factory(
        sender=None,
        app_data: Callable[[int, ], None] = None,
        user_data=None
) -> None:
    """Take in the request and discern the appropriate wifi action."""
    loggei.debug("%s()", wifi_factory.__name__)

    WIFI_BTN_SELECT_YAML = pathlib.Path("wifi_scan_results.yml")

    # Check if the wifi button select yaml file exists
    if not pathlib.Path.exists(WIFI_BTN_SELECT_YAML):
        loggei.info("calling wifi_kill_all()")
        wifi_kill_all(app_data)

    else:
        loggei.info("calling wifi_chase()")
        activate_wifi_chase()


def main():
    """Run the main program."""
    loggei.info(msg="Main method called")

    return_indicated_results()


if __name__ == "__main__":
    main()
