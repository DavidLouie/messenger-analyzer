import json
from datetime import datetime
from person import Person


class MessageParser:

    def __init__(self, filepath, username):
        with open(filepath) as data_file:
            self.data = json.load(data_file)
        self.people = []
        self.people.append(Person(username))
        self.dates = []

    def parse(self):
        for p in self.data["participants"]:
            new_p = Person(p)
            self.people.append(new_p)

        for m in self.data["messages"]:
            s_name = m["sender_name"]
            self.dates.append(m["timestamp"])
            day = datetime.fromtimestamp(m["timestamp"]).strftime("%A")

            for p in self.people:
                if p.get_name() == s_name:
                    p.total += 1
                    p.inc_day(day)
                    if "content" in m:
                        num_words = len(str.split(m["content"]))
                        p.inc_words(num_words)
                    if "photos" in m:
                        p.inc_photos()
                    if "sticker" in m:
                        p.inc_stickers()
                    if "gifs" in m:
                        p.inc_gifs()
                    break
        self.dates.sort()

    def pretty_print(self):
        for p in self.people:
            p.pretty_print()

    def get_people(self):
        return self.people

    def get_dates(self):
        return self.dates


