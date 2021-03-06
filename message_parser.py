import json
from datetime import datetime
from person import Person


class MessageParser:

    def __init__(self, filepath, username):
        with open(filepath) as data_file:
            self.data = json.load(data_file)
        self.people = []
        self.people.append(Person(username))

    def parse(self):
        for p in self.data["participants"]:
            new_p = Person(p)
            self.people.append(new_p)

        for m in self.data["messages"]:
            s_name = m["sender_name"]
            day = datetime.fromtimestamp(m["timestamp"]).strftime("%A")

            for p in self.people:
                if p.get_name() == s_name:
                    p.total += 1
                    p.days[day] += 1
                    p.dates.append(m["timestamp"])
                    if "content" in m:
                        num_words = len(str.split(m["content"]))
                        p.words += num_words
                    if "photos" in m:
                        p.photos += 1
                    if "sticker" in m:
                        p.stickers += 1
                    if "gifs" in m:
                        p.gifs += 1
                    break
        for p in self.people:
            p.dates.sort()

    def pretty_print(self):
        for p in self.people:
            p.pretty_print()


