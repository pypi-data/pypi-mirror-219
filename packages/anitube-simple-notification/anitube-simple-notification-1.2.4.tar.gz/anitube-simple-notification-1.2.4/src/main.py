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
from .db import DataBase
from .scraper import Scraper
from .notify import Notification
from .config import Config
from rich.console import Console
from rich.progress import track
import time
import os
import platformdirs

def main():
    # Const sections.

    # Console initialising
    console = Console()

    APPNAME = "anitube-simple-notification"
    APPAUTHOR = "KKlochko"
    CONFIG_NAME = "config.toml"
    BASE_DIR = os.path.dirname(__file__)
    DATA_DIR = platformdirs.user_data_dir(APPNAME, APPAUTHOR)

    DB_PATH = os.path.join(DATA_DIR, 'user.db')
    POSTERS_PATH = os.path.join(DATA_DIR, 'posters')

    CONFIG_PATH = platformdirs.user_config_path(APPNAME, APPAUTHOR, CONFIG_NAME)

    # check for existing of dirs
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)

    config = Config.get_config(CONFIG_PATH, console)

    # Here you can change testing headers to yours.
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }

    # Default if empty.
    MESSAGE = "New episode."
    WAITING_PERIOD = config.pop('WAITING_PERIOD', 60) # seconds
    POSTERS = config.pop('POSTERS', True) # for use poster as icons of notifications
    urls = config.pop('URLS', [])

    # Initialising objects
    scr = Scraper(HEADERS, POSTERS_PATH)
    db = DataBase(DB_PATH)

    # Checks for new urls in file and add as current state
    # If one of page has updated then notifing.
    # Repeating the checking with the waiting period.
    while True:
        console.print(f"[yellow][DOING][/] Checking for animes [0/{len(urls)}]")
        count = 0
        for url in urls:
            data = scr.get_anime(url, POSTERS)
            if data == None:
                console.print(f"[red][ERROR][/] A conections trouble is occured.")
                continue
            url, title, status, poster_path = data
            console.print(f"[yellow][DOING][/] Checking for \"{title}\" [{count}/{len(urls)}]")
            r = db.add_anime_if(url, title, status, poster_path)
            if r == -1:
                n = Notification(title, MESSAGE, poster_path)
                n.send()
                console.print(f"[blue bold][NOTIFICATION][/] \"{title}\"")
            count+=1
            console.print(f"[green][DONE][/] Checking for \"{title}\" [{count}/{len(urls)}]")
        console.print(f"[yellow][WAITING][/] The next check is after {WAITING_PERIOD} seconds")
        # Sleep while waiting
        for n in track(range(WAITING_PERIOD), description="Waiting..."):
            time.sleep(1)

if __name__ == "__main__":
    main()
