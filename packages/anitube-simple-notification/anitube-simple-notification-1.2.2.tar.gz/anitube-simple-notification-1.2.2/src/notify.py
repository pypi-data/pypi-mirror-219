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
This module has all for simplify work with notifications.
"""

from notifypy import Notify

class Notification:
    """The handler of notification."""
    def __init__(self, title, message, icon_path=""):
        """Initialising the notification information."""
        self.title, self.message, self.icon_path = title, message, icon_path

    def send(self):
        """Send the notification."""
        notification = Notify()
        notification.title = self.title
        notification.message = self.message
        notification.icon = self.icon_path
        notification.send()
