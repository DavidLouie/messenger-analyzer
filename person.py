class Person:

    def __init__(self, name):
        self._name = name   # never changed once set here
        self.days = {
            'Monday': 0,
            'Tuesday': 0,
            'Wednesday': 0,
            'Thursday': 0,
            'Friday': 0,
            'Saturday': 0,
            'Sunday': 0
        }
        self.total = 0
        self.words = 0
        self.stickers = 0
        self.gifs = 0
        self.photos = 0

    def inc_day(self, day):
        self.days[day] += 1

    def inc_words(self, num_words):
        self.words += num_words

    def inc_stickers(self):
        self.stickers += 1

    def inc_gifs(self):
        self.gifs += 1

    def inc_photos(self):
        self.photos += 1

    def pretty_print(self):
        print(self._name)
        for day, num in self.days.items():
            print("    " + day + ": " + str(num))
           # self.total += num
        print("  Total: " + str(self.total))
        print("  Words: " + str(self.words))
        print("    Avg WPM: " + str(self.get_words_avg()))
        print("  Stickers: " + str(self.stickers))
        print("     Avg SPM: " + str(self.get_stick_avg()))
        print("  Gifs: " + str(self.gifs))
        print("     Avg GPM: "  + str(self.get_gifs_avg()))
        print("  Photos: " + str(self.photos))
        print("     Avg PPM: " + str(self.get_photos_avg()))

    def get_days(self):
        return self.days

    def get_name(self):
        return self._name

    def get_words_avg(self):
        return self.words / self.total

    def get_stick_avg(self):
        return self.stickers / self.total

    def get_gifs_avg(self):
        return self.gifs / self.total

    def get_photos_avg(self):
        return self.photos / self.total

