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
This module has all for simplify work with scraping.
"""

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import track
import os

class Scraper:
    """The handler of web connection."""
    def __init__(self, HEADERS, POSTER_PATH="posters"):
        """Initialising the connection information."""
        self.HEADERS, self.POSTER_PATH = HEADERS, POSTER_PATH
        self.mkdir(self.POSTER_PATH)

    def mkdir(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)

    def file_exist(self, path):
        if os.path.isfile(path):
            return True
        return False

    def get_anime(self, url, GETPOSTER = False):
        """
        Return None if response is not 200.
        Otherwise, return [url, title, status].
        """
        response = requests.get(url, headers=self.HEADERS)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.content, 'html.parser')
        data = soup.find('div', class_='rcol', style = 'width:701px; padding:0 0 0 6px;')
        # Getting Title
        title = data.find('h2').get_text(strip=True)
        # Getting Status
        str_find = "\nСерій: "
        str_current = data.get_text()
        str_current = str_current[str_current.find(str_find)+len(str_find):]
        status = str_current[:str_current.find('\n')]
        # Poster
        poster_url = "https://anitube.in.ua" + soup.find('span', class_="story_post").find('img').get('src')
        poster_path = f"{self.POSTER_PATH}/{poster_url.split('/')[-1]}"
        if GETPOSTER and not self.file_exist(poster_path):
            console = Console()
            with console.status("[yellow]Downloading...[/]"):
                img = requests.get(poster_url)
                with open(poster_path,'wb') as file:
                    file.write(img.content)
                console.print(f"[green][DONWLOADED][/] The poster for \"{title}\"")
        return [url, title, status, poster_path]
