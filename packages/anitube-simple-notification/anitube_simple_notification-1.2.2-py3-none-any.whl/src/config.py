##########################################################################
# Copyright (C) 2022-2023 Kostiantyn Klochko <kklochko@protonmail.com>   #
#                                                                        #
# This file is part of Anitube Simple Notification.                      #
#                                                                        #
# Anitube Simple Notification is free software: you can redistribute     #
# it and/or modify it under the terms of the GNU General Public          #
# License as published by the Free Software Foundation, either version   #
# 3 of the License, or (at your option) any later version.               #
#                                                                        #
# Anitube Simple Notification is distributed in the hope that it will    #
# be useful, but WITHOUT ANY WARRANTY; without even the implied          #
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See   #
# the GNU General Public License for more details.                       #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with Anitube Simple Notification. If not, see                    #
# <https://www.gnu.org/licenses/>.                                       #
##########################################################################

"""
This module has all for simplify work with the toml configuration file.
"""

from rich.console import Console
import tomli
from pathlib import PosixPath

class Config:
    @staticmethod
    def config_validation(config: dict) -> bool:
        """Return False if config is invalid. Empty values is valid."""
        validations = {
            "POSTERS": lambda v: isinstance(v, bool),
            "WAITING_PERIOD": lambda v: isinstance(v, int) and v >= 0,
            "URLS": lambda l: isinstance(l, list) and len(l) == len(list(filter(str,l))),
        }
        return all(validations.get(k, lambda x: False)(v) for (k, v) in config.items())

    @staticmethod
    def config_validation_detail(config: dict) -> dict:
        """Return a dict where key is a field and value is valid status."""
        validations = {
            "POSTERS": lambda v: isinstance(v, bool),
            "WAITING_PERIOD": lambda v: isinstance(v, int) and v >= 0,
            "URLS": lambda l: isinstance(l, list) and
            len(list(filter(lambda v: isinstance(v,str), l))) and
            len(list(filter(lambda v: v.startswith("https://anitube.in.ua/"), l)))
            #len(l) == len(list(filter(str,l))),
        }
        return {k:validations.get(k, lambda x: False)(v) for (k, v) in config.items()}

    @staticmethod
    def config_validation_error(config: dict):
        """Show error and remove invalid fields."""
        validation = Config.config_validation_detail(config)
        if not validation.pop("POSTERS", True):
            Console().print(f"[red][ERROR] Please, POSTER must be false or true.[/]")
            del config["POSTERS"]
        if not validation.pop("WAITING_PERIOD", True):
            Console().print(
                ''.join(["[red][ERROR] ",
                         "Please, WAITING_PERIOD must be an integer that greater",
                         "than zero or equals to.[/]"]))
            del config["WAITING_PERIOD"]
        if not validation.pop("URLS", True):
            Console().print(
                "".join(["[red][ERROR] Please, URLS must be a list of strings"
                         "which ones are page urls of anitube.in.ua.[/]"]))
            del config["URLS"]

    @staticmethod
    def get_config(config_path:PosixPath, console:Console) -> dict:
        """
        Read the configuration file and return dict as configuration.
        The configuration file must be in the application folder.
        """
        config = {}
        try:
            with open(config_path, "rb") as file:
                config = tomli.load(file)
        except FileNotFoundError:
            console.print(f"[red][ERROR] Please, create configuration file.[/]")
            console.print(f"[yellow][ERROR] The configuration file path: {config_path}.[/]")
        except tomli.TOMLDecodeError:
            console.print(f"[red][ERROR] Please, check configuration file for correctness.[/]")
        Config.config_validation_error(config)
        return config
