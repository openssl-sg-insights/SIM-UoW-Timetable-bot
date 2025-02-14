#! /usr/bin/env python3
# -*- coding: utf-8 -*-
##
#   Copyright (C) 2018 JING KAI TAN
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
#   License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##
# Class message for retrival of timetable.
##
from Models.classes import IndividualClassStructure
import datetime
import calendar
import arrow


class MessageTimetable:
    GITHUB_URL = (
        "https://github.com/xlanor/SIM-UoW-Timetable-bot/blob/master/DISCLAIMER.md"
    )

    def __init__(self, cur_week: str, last_sync_date: str):
        self.__cur_week = cur_week
        self.__last_sync_date = last_sync_date
        # prepares a nested list of lists.
        self.__class_list = []
        for i in range(7):
            # adds 7 empty arrays.
            self.__class_list.append([])

    def add_class_list(
        self, class_numeric_day: int, class_object: IndividualClassStructure
    ):
        self.__class_list[class_numeric_day].append(class_object)

    def get_message(self):
        message_array = [f"📈Timetable for the week of *{self.__cur_week}*\n"]
        message_array.append(
            f"🔃 This timetable was last synced on *{self.__last_sync_date}*\n"
        )
        message_array.append(
            f"By using this bot, you agree to the terms and conditions stated in the [DISCLAIMER.md]({MessageTimetable.GITHUB_URL}) on github\n\n"
        )
        for i in range(7):
            message_array.append(f"󠁳📅 *{calendar.day_name[i]}*\n")
            if len(self.__class_list[i]) == 0:
                message_array.append("📌-\n")
                message_array.append("```\n")
                message_array.append("You have no classes for this day!")
                message_array.append("```\n")
            else:
                for class_object in self.__class_list[i]:
                    message_array.append(class_object.get_formatted_text())
                    message_array.append("\n")
            message_array.append("\n")
        return "".join(message_array)

    def get_today(self):
        local = arrow.utcnow().to("Asia/Singapore")
        local_day = local.format("dddd")
        local_date = local.format("DD/MM/YYYY")
        message_array = [f"📈Timetable for {local_day}, *{local_date}*\n"]
        message_array.append(
            f"🔃 This timetable was last synced on *{self.__last_sync_date}*\n"
        )
        message_array.append(
            f"By using this bot, you agree to the terms and conditions stated in the [DISCLAIMER.md]({MessageTimetable.GITHUB_URL}) on github\n\n"
        )
        # the class list should only have 1 day here.
        numeric_day_to_get = datetime.datetime.today().weekday()
        message_array.append(f"󠁳📅 *{local_day}*\n")
        if len(self.__class_list[numeric_day_to_get]) == 0:
            message_array.append("📌-\n")
            message_array.append("```\n")
            message_array.append("You have no classes for this day!")
            message_array.append("```\n")
        else:
            for class_object in self.__class_list[numeric_day_to_get]:
                message_array.append(class_object.get_formatted_text())
                message_array.append("\n")
        message_array.append("\n")
        return "".join(message_array)

    def get_fucked(self):
        message_array = [f"📈Fucked up classes for the week of *{self.__cur_week}*\n"]
        message_array.append(
            f"🔃 This timetable was last synced on *{self.__last_sync_date}*\n"
        )
        message_array.append(
            f"By using this bot, you agree to the terms and conditions stated in the [DISCLAIMER.md]({MessageTimetable.GITHUB_URL}) on github\n\n"
        )
        # By defintion,
        fucked_time = datetime.datetime.strptime("09:00", "%H:%M").time()
        total_fucked = 0
        for i in range(7):
            for class_object in self.__class_list[i]:
                fucked_counter = 0
                start_time = class_object.start_time
                if i < 5:
                    if start_time.time() < fucked_time:
                        if fucked_counter == 0:
                            message_array.append(f"󠁳📅 *{calendar.day_name[i]}*\n")
                        fucked_counter += 1
                        total_fucked += 1
                        message_array.append(class_object.get_formatted_text())
                        message_array.append("\n")
                else:
                    if fucked_counter == 0:
                        message_array.append(f"󠁳📅 *{calendar.day_name[i]}*\n")
                    fucked_counter += 1
                    total_fucked += 1
                    message_array.append(class_object.get_formatted_text())
                    message_array.append("\n")

                if fucked_counter != 0:
                    message_array.append("\n")

        if total_fucked == 0:
            message_array.append("You have no fucked up classes this week!")
        return "".join(message_array)
