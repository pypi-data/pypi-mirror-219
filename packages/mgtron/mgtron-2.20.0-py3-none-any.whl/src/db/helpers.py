"""Helper functions regarding the database for the GUI."""

import dearpygui.dearpygui as dpg
import json
import logging
import sqlite3
from datetime import datetime
import pathlib

from .models import get_sql_save_names
from .models import get_sql_details
from .models import delete_sql_save_data
from .models import save_to_database


ROOT = pathlib.Path(__file__).resolve().parent.parent

# dd/mm/YY H:M:S
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
DB_PATH = pathlib.Path(ROOT / "db" / "mgtron_db.db")

loggey = logging.getLogger(name=__name__)


FREQ: dict[str, int] = {
    "chan_1": 0,
    "chan_2": 3,
    "chan_3": 6,
    "chan_4": 9,
    "chan_5": 12,
    "chan_6": 15,
    "chan_7": 18,
    "chan_8": 21,
}

POWS: dict[str, int] = {
    "chan_1": 1,
    "chan_2": 4,
    "chan_3": 7,
    "chan_4": 10,
    "chan_5": 13,
    "chan_6": 16,
    "chan_7": 19,
    "chan_8": 22,
}

BANDS: dict[str, int] = {
    "chan_1": 2,
    "chan_2": 5,
    "chan_3": 8,
    "chan_4": 11,
    "chan_5": 14,
    "chan_6": 17,
    "chan_7": 20,
    "chan_8": 23,
}

NAME: dict[str, int] = {
    "chan_1": 24,
    "chan_2": 25,
    "chan_3": 26,
    "chan_4": 27,
    "chan_5": 28,
    "chan_6": 29,
    "chan_7": 30,
    "chan_8": 31,
}


def live_refresh(alias: list[str]):
    """For as many aliases passed in, remove from the dpg registry."""
    loggey.debug(msg=f"{live_refresh.__name__}()")

    for i in dpg.get_aliases():
        for j in alias:
            if i.__contains__(j):
                dpg.remove_alias(alias=i)
                loggey.debug(f"Removed alias: {i}")
                loggey.debug(msg=f"Removed alias: {i}")


def get_save_data() -> list[dict[str, str]]:
    """Get the save data."""
    return [
        {
            "save_name": dpg.get_value(item="save_custom_input"),
            "power": dpg.get_value(f"power_{channel}"),
            "bandwidth": dpg.get_value(f"bandwidth_{channel}"),
            "frequency": dpg.get_value(f"freq_{channel}"),
            "date": dt_string,
        }
        for channel in range(1, 9)
    ]


def quick_save(sender, app_data, user_data) -> None:
    """Save the present inputs of the fields."""
    prelim_data: list[dict[str, dict[str, str]]] = [
        {
            f"channel {channel}": {
                "Power": dpg.get_value(f"power_{channel}"),
                "Bandwidth": dpg.get_value(f"bandwidth_{channel}"),
                "Frequency": dpg.get_value(f"freq_{channel}"),
                "Date": dt_string,
            },
        }
        for channel in range(1, 9)
    ]

    with open(file=f"{ROOT}/db/quick_save.json", mode="w") as file:
        file.write(json.dumps(obj=prelim_data, indent=2))
        loggey.info("Save Complete")


def quick_load(sender, app_data, user_data) -> None:
    """Load the last daved data."""
    saved_data: list = []

    # print(f"\nsending: {sender}")
    # print(f"app_data: {app_data}")
    # print(f"user_data: {user_data}\n")

    try:
        loggey.info("Opening the quick save file: quick_save.json")
        with open(file=f"{ROOT}/db/quick_save.json") as file:
            saved_data = json.loads(file.read())
            [
                (
                    dpg.set_value(
                        item=f"power_{channel}",
                        value=saved_data[channel -
                                         1][f"channel {channel}"]["Power"],
                    ),
                    dpg.set_value(
                        item=f"bandwidth_{channel}",
                        value=saved_data[channel -
                                         1][f"channel {channel}"]["Bandwidth"],
                    ),
                    dpg.set_value(
                        item=f"freq_{channel}",
                        value=saved_data[channel -
                                         1][f"channel {channel}"]["Frequency"],
                    ),
                )
                for channel in range(1, 9)
            ]
            loggey.info("Quick load complete")

    except SystemError:
        loggey.error("No saved data found")
        return


def custom_save() -> None:
    """Save config w/ a custom name."""
    loggey.debug("%s() executed", custom_save.__name__)

    try:
        save_data = get_save_data()

    except (
            TypeError,
            IndexError,
            KeyError,
            AttributeError,
            ValueError,
    ):
        loggey.warning(msg=f"database failure | {custom_save.__name__}()")

    # Clear input and close input
    dpg.set_value(item="save_custom_input", value="")
    dpg.configure_item(item="modal_save", show=False)

    save_to_database(
        input_data=save_data,
        db_path=DB_PATH
    )


def custom_load(sender, app_data=None, user_data=None) -> None:
    """Load config /w a custom name."""
    loggey.info("%s() executed", custom_load.__name__)

    # print(f"\nsender: {sender}")

    loggey.debug(msg="Attempting to load custom save data")

    custom_load_to_sql: list[str] = []
    try:
        custom_load_to_sql = get_sql_save_names()
    except sqlite3.DatabaseError:
        loggey.warning(msg="No custom save file found")
    init_save_data_length = custom_load_to_sql.__len__()

    live_refresh(alias=["load",])
    loggey.info(msg=f"Sender: {sender}")
    with dpg.window(
            modal=True,
            popup=True,
            tag="modal_loaded",
            pos=(
                0,  # dpg.get_viewport_client_width() // 2 - 100,
                0,  # dpg.get_viewport_client_height() // 2 - 100,
            ),
    ):
        {
            (
                dpg.add_menu_item(
                    parent="modal_loaded",
                    label=unique,
                    tag=f"load_{itera + init_save_data_length}",
                    callback=load_chosen,
                    user_data=(unique, itera + init_save_data_length),
                ),
            )
            # if {sender, }.union({"custom_load_button", 220})  # set theory
            # else (
            #     dpg.add_menu_item(
            #         parent="modal_delete",
            #         label=unique,
            #         callback=delete_chosen,
            #         user_data=(unique, itera + init_save_data_length),
            #         tag=f"delete_{itera + init_save_data_length}",
            #         show=True,
            #     )
            # )
            for itera, unique in enumerate(custom_load_to_sql, start=0)
        }
        dpg.add_button(
            label="Close",
            parent="modal_loaded",
            tag="close_modal_loaded",
            callback=lambda: dpg.configure_item(
                item="modal_loaded", show=False),
        )


def load_chosen(
        sender=None, app_data=None, user_data: tuple[str, int] = ("", 0)
) -> None:
    """Take in the chosen file to be loaded to the input fields of the gui."""
    loggey.info(f"{load_chosen.__name__}() executed")

    _custom_load = get_sql_details(save_name=user_data[0])
    _ret_data: tuple = _custom_load

    _ = [
        (
            dpg.set_value(item=f"freq_{itera}",
                          value=_ret_data[FREQ[f"chan_{itera}"]]),
            dpg.set_value(
                item=f"power_{itera}", value=_ret_data[POWS[f"chan_{itera}"]]
            ),
            dpg.set_value(
                item=f"bandwidth_{itera}",
                value=_ret_data[BANDS[f"chan_{itera}"]]
            ),
        )
        for itera in range(1, 9)
    ]


def delete_chosen(
        sender=None,
        app_data=None,
        user_data: tuple[str, int] = (str(), int()),
) -> None:
    """Delete a saved file."""
    # Get the list of saved objects
    _custom_load = get_sql_save_names()
    init_save_data_length = _custom_load.__len__()
    live_refresh(alias=["delete",])

    with dpg.window(
            modal=True,
            popup=True,
            tag="modal_delete",
            pos=(
                0,  # dpg.get_viewport_client_width() // 2 - 100,
                0,  # dpg.get_viewport_client_height() // 2 - 100,
            ),
    ):
        [
            dpg.add_menu_item(
                parent="modal_delete",
                label=unique,
                callback=delete_it,
                user_data=(unique, itera + init_save_data_length),
                tag=f"delete_{itera + init_save_data_length}",
                show=True,
            )
            for itera, unique in enumerate(_custom_load, start=0)
        ]
        dpg.add_button(
            label="Close",
            parent="modal_delete",
            tag="close_modal_delete",
            callback=lambda: dpg.configure_item(
                item="modal_delete", show=False),
        )

    loggey.info(
        f"Live update of delete and load menu items complete\
            | {delete_chosen.__name__}()"
    )


def delete_it(
        sender=None,
        app_data=None,
        user_data: tuple[str, int] = (str(), int()),
) -> None:
    """Delete the chosen database item."""
    loggey.debug(msg=f"{delete_it.__name__}() executed")

    # print(f"Sender: {sender}")
    # print(f"App data: {app_data}")
    # print(f"User data: {user_data[0]}")

    # Delete the selected item from the database
    delete_sql_save_data(save_name=user_data[0], db_path=DB_PATH)


def check_and_load_config(button_name: str) -> dict[str, list]:
    """Check database for config button as the name of the saved config."""
    loggey.debug(msg=f"{check_and_load_config.__name__}()")
    config_data: dict[str, list] = {}

    # Check the sql database for the name of the button
    save_names = get_sql_save_names()

    # Remove new lines and rejoin sentence; this is ! robust
    button_name = button_name.replace("  ", " ").replace("\n", "")

    loggey.info(f"DB names: {save_names}")
    loggey.info(f"Button name: '{button_name}'")

    if button_name in save_names:
        loggey.debug(f"Button name: {button_name} found in DB")

        # Get the config from the database
        config = get_sql_details(save_name=button_name)

        loggey.debug(config)

        # Get the channel, frequency, power, and bandwidth
        channel: list[int] = [int(i) for i in range(1, 9)]
        frequency: list[float] = [
            float(config[FREQ[
                f"chan_{i}"]]) for i, _ in enumerate(FREQ, start=1)
        ]
        power: list[int] = [
            int(config[POWS[
                f"chan_{i}"]]) for i, _ in enumerate(POWS, start=1)
        ]
        bandwidth: list[int] = [
            int(config[BANDS[
                f"chan_{i}"]]) for i, _ in enumerate(BANDS, start=1)
        ]

        # Store the config in a dictionary
        config_data: dict[str, list] = {
            "channel": channel,
            "freq": frequency,
            "power": power,
            "bw": bandwidth,
        }

    return config_data
