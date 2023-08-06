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
This module has all for simplify work with sqlite3.
"""

import sqlite3

class DataBase:
    """Handler of connection."""
    def __init__(self, PATH: str = "user.db", TABLE: str = "animes"):
        """Initialising the connection information."""
        self.PATH, self.TABLE = PATH, TABLE
        self.create_table(self.TABLE)

    def create_table(self, table):
        """Create a table in the DB."""
        connect = sqlite3.connect(self.PATH)
        cursor = connect.cursor()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table}(id INTEGER PRIMARY KEY, Url TEXT, Title TEXT, Status TEXT, PosterPath TEXT);')
        connect.commit()
        cursor.close()
        connect.close()

    def add_anime(self, url, title, status, poster_path=""):
        """Add entry of a content."""
        connect = sqlite3.connect(self.PATH)
        cursor = connect.cursor()
        data = [url, title, status, poster_path]
        cursor.execute(f'INSERT INTO {self.TABLE}(Url, Title, Status, PosterPath) VALUES(?,?,?,?)', data)
        connect.commit()
        cursor.close()
        connect.close()

    def update_anime_status(self, url, new_status):
        """Add entry of a content."""
        connect = sqlite3.connect(self.PATH)
        cursor = connect.cursor()
        cursor.execute(f"UPDATE {self.TABLE} SET Status = '{new_status}' WHERE Url = '{url}'")
        connect.commit()
        cursor.close()
        connect.close()

    def get_entry(self, url):
        """
        Returns the enties as an list of tuples if exists.
        Otherwise, return [].
        """
        connect = sqlite3.connect(self.PATH)
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM {self.TABLE} WHERE Url = '{url}';")
        data = cursor.fetchall()
        cursor.close()
        connect.close()
        return data

    def add_anime_if(self, url, title, status, poster_path=""):
        """
        Return 0 if not exists.
        Return 1 if the same as the entry in the DB.
        Return -1 if the status is newer than the entry status.
        """
        data = self.get_entry(url)
        # If not exists
        if data == []:
            self.add_anime(url, title, status, poster_path)
            return 0
        # If the same
        if data[0][1:] == (url, title, status, poster_path):
            return 1
        # If the status is newer than the entry status.
        if data[0][3] != status:
            self.update_anime_status(url, status)
            return -1
