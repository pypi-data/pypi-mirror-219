"""This module is used to scan for wifi signals and their frequencies."""

import time
import itertools
import logging
import requests
import subprocess
from pathlib import Path
from typing import Callable
from typing import Any

from colorama import Fore as F

from ..globals.helpers import ThreadWithReturnValue
# from ..globals.helpers import enable_select_btns
# from ..globals.helpers import WIFI_BTNS_LIST


loggey = logging.getLogger(__name__)

R = F.RESET
PATH = Path(__file__).parent.parent.parent


def find_signals_and_frequencies(port: int | None) -> list[dict]:
    """Use the linux host to scan for wifi signals and frequencies."""
    loggey.debug(
        msg=f"Scanning for wifi signals and frequencies |"
        f" {find_signals_and_frequencies.__name__}"
    )
    port: int = 8081

    try:
        output: list[dict] = requests.get(
            url=f"http://localhost:{port}/base_scan",
            headers={"Content-Type": "application/json"},
            timeout=8,
        )

        if output.status_code != 200:
            loggey.error(
                msg=f"Failed to scan for wifi signals and frequencies |"
                f" {find_signals_and_frequencies.__name__}"
            )
            loggey.error(
                msg=f"Status code: {output.status_code} |"
                f" {find_signals_and_frequencies.__name__}"
            )
    except requests.exceptions.ConnectionError as err:
        loggey.error(
            msg=f"WiFi API not running |"
            f" {find_signals_and_frequencies.__name__}"
        )
        loggey.error(
            msg=f"Error: {err} | {find_signals_and_frequencies.__name__}"
        )

    return output.json()


def post_ssid(ssid: list[str]) -> list[float]:
    """Send the SSID that is to be searched and recieve the frequency."""
    loggey.debug(
        "Posting SSID to API | %s", post_ssid.__name__
    )

    port: int = 8081
    timeout = 13
    end_point: str = "select_scan"

    # Post request to the API
    try:
        output: float = requests.post(
            url=f"http://localhost:{port}/{end_point}",
            headers={"Content-Type": "application/json"},
            json={"ssid": ",".join(ssid)},
            timeout=timeout,
        )

        if output.status_code != 200:
            loggey.error(
                msg=f"API failure | {post_ssid.__name__}"
            )
            loggey.error(
                msg=f"Status code: {output.status_code} |"
                f" {post_ssid.__name__}"
            )

            return [0.0]
    except requests.exceptions.ConnectionError as err:
        loggey.error(
            msg=f"WiFi API not running | {post_ssid.__name__}"
        )
        loggey.error(
            msg=f"Error: {err} | {post_ssid.__name__}"
        )
        return [0.0]

    loggey.warning(f"{F.GREEN}Frequency: {output.json()}{R}")

    return output.json()


def threaded_scan(
        _dpg,
        linux_data: Callable[
            [list | None],
            list[dict | float]
        ],
        ssid: list[float] | None = None,
) -> list[dict]:
    """Scan for wifi signals and frequencies in a thread."""
    loggey.debug(
        "Scanning for wifi signals and frequencies | %s",
        threaded_scan.__name__
    )

    show_word: str = "SCANNING" if not ssid else "CHASING"

    linux_data = ThreadWithReturnValue(
        target=linux_data,
        args=(ssid if ssid else None,),
    )

    linux_data.start()

    linux_data = threaded_print(
        _dpg=_dpg,
        linux_data=linux_data,
        message=show_word,
    )

    linux_data = linux_data.join()

    return linux_data


def threaded_print(
        _dpg: object,
        linux_data: ThreadWithReturnValue,
        message: str,
) -> ThreadWithReturnValue:
    """Handle the printing during scans."""
    loggey.debug(
        "Printing during scans | %s", threaded_print.__name__
    )

    if message != "SCANNING":
        # Turn the text of the scanning button to "SCANNING"
        _dpg.configure_item(
            tag="scan_btn",
            item="mssn_scan_jam",
            label=message,
        )

        sleep_delay: float = 0.5
        count = 0
        while linux_data.is_alive():
            time.sleep(sleep_delay)
            count += 1
            _dpg.configure_item(
                item="mssn_scan_jam",
                label=message + "." * count
            )
            count = 0 if count > 3 else count

        try:
            _dpg.delete_item(item=129)
        except SystemError:
            loggey.warning(
                "Window already removed | %s", threaded_scan.__name__
            )

        return linux_data

    with _dpg.window(
        tag="wifi_scan_window",
        no_scrollbar=True,
        no_collapse=True,
        no_resize=True,
        no_title_bar=True,
        no_move=True,
        modal=True,
        pos=(0, 0),
        width=880,
        height=735,
    ):

        _dpg.add_text(
            parent="wifi_scan_window",
            pos=(
                _dpg.get_item_width(item="wifi_scan_window") / 2 - 50,
                _dpg.get_item_height(item="wifi_scan_window") / 2 - 50
            ),
            tag="scan_text",
            default_value=message,
        )

        sleep_delay: float = 0.5
        count = 0
        while linux_data.is_alive():
            time.sleep(sleep_delay)
            count += 1
            _dpg.configure_item(
                parent="wifi_scan_window",
                item="scan_text",
                default_value=message + "." * count
            )
            count = 0 if count > 3 else count
        _dpg.delete_item(item="wifi_scan_window")

    return linux_data


@DeprecationWarning
def format_data(
        linux_data: Callable[[], subprocess.CompletedProcess],
        _dpg: Any,
) -> list[dict[str, str]]:
    """Format the data in the subprocess.CompletedProcess object."""
    loggey.debug(
        msg=f"Formatting data | {format_data.__name__}"
    )

    linux_data = threaded_scan(_dpg=_dpg, linux_data=linux_data)

    # Put each line of the output into its own list
    output_list: list[str] = [
        i for i in linux_data.stdout.split(sep="\n") if i != ""
    ]

    formatted_data: list[dict[str, str]] = []

    for data in output_list:
        ssid: str = data.split(sep=":")[0]
        bssid: list[str] = ":".join(
            data.split(sep=":")[1:7]
        )
        channel: str = data.split(sep=":")[7]
        frequency: str = data.split(sep=":")[8]
        signal: str = data.split(sep=":")[9]
        signal = str((int(signal) // 2) - 100)
        signal += " dBm"
        formatted_data.append(
            {
                "ssid": ssid,
                "bssid": bssid,
                "channel": channel,
                "frequency": frequency,
                "signal": signal,
            }
        )

    return formatted_data


def convert_signal_to_rssi(
        output_list: list[dict[str, str]]
) -> list[dict[str, str]]:
    """Convert the signal to RSSI and return all the data."""
    loggey.debug(
        "%s", convert_signal_to_rssi.__name__
    )

    formatted_data: list[dict[str, str]] = []

    for data in output_list:
        data["signal"] = str((int(data["signal"]) // 2) - 100)
        data["signal"] += " dBm"
        formatted_data.append(data)

    return formatted_data


def freqs_and_sigs(
    formatted_data: list[dict[str, str]],
    short_list: bool = False
) -> dict[int, float]:
    """Return a list of frequencies and signals."""
    # zip together the frequencies and signals and allow duplicates
    matched_sigs_and_freqs: dict[int, float] = {

        int(data["signal"]): float(data["frequency"].split(sep=" ")[0])
        for data in formatted_data
    }

    matched_sigs_and_freqs: dict[int, float] = dedup_freqs(
        freq_and_strength=matched_sigs_and_freqs)

    if short_list:
        # reduce the dictionary to the top 8 strongest signals
        top_eight = dict(itertools.islice(
            matched_sigs_and_freqs.items(),
            8
        ))

        # convert the itertools object to a dictionary
        top_eight = dict(enumerate(top_eight.values(), start=1))

        # if the dictionary is not eight items long, fill it with zeros
        if len(top_eight) != 8:
            for i in range(1, 9):
                if i not in top_eight.keys():
                    top_eight[i] = 0.0

            loggey.warning(
                msg=f"Dictionary was not eight items long |"
                f" {freqs_and_sigs.__name__}"
            )

    return matched_sigs_and_freqs if not short_list else top_eight


def dedup_freqs(freq_and_strength: dict[int, float]) -> dict[int, float]:
    """Deduplicate the frequencies of wifi scan results."""
    loggey.debug("%s()", dedup_freqs.__name__)

    freqs_returned: dict[int, float] = dict()

    loggey.info(f"{F.CYAN}init Freq & Strength: {freq_and_strength}{R}")

    for strength, freq in freq_and_strength.items():
        if freq not in freqs_returned.values():
            freqs_returned.update({strength: freq})

    loggey.info(f"{F.CYAN}Freq & Strength deduped: {freqs_returned}{R}")

    return freqs_returned


def main():
    """Run the module as a script."""
    # data = find_signals_and_frequencies()

    # ssid_0 = data[0].get("ssid")

    # print(f"\n{F.CYAN}SSID{R}: {F.YELLOW}{ssid_0}{R}\n")

    # return_val = post_ssid(ssid="CAFO")

    # print(f"\n{F.CYAN}Return_val{R}: {F.BLUE}{return_val}{R}\n")


if __name__ == "__main__":
    main()
