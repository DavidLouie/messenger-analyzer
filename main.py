from message_parser import MessageParser
from person import Person
import colorsys
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta

# create bar chart of message frequency by day of the week
def freq_by_day(person):
    objects = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    y_pos = np.arange(len(objects))
    freq = person.get_days().values()
    plt.bar(y_pos, freq, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Frequency')
    plt.title(person.get_name() + ' message frequency by weekday')
    plt.show()

# convert list of sorted timestamps into a list of days ranging from the first to the last
def convert_timestamps(timestamps):
    first_day = datetime.fromtimestamp(timestamps[0]).date()
    last_day = datetime.fromtimestamp(timestamps[len(timestamps)-1]).date()
    delta = last_day - first_day
    date_list = [first_day + timedelta(days=x) for x in range(0, delta.days + 1)]
    return date_list

# create a list of message frequencies where the index corresponds to the index in the date_list
def count_timestamps(timestamps, n):
    freq = [0]*n
    first_day = datetime.fromtimestamp(timestamps[0]).date()
    for ts in timestamps:
        cur_day = datetime.fromtimestamp(ts).date()
        delta = cur_day - first_day
        freq[delta.days] += 1
    return freq

# create bar chart of message frequency on each day over the dataset
def freq_chrono(timestamps):
    date_list = convert_timestamps(timestamps)
    y_pos = np.arange(len(date_list))
    freq = count_timestamps(timestamps, len(date_list))
    plt.bar(y_pos, freq, align='center', alpha=0.5)

    # produce 6 evenly spaced x-axis labels
    gap = len(date_list) // 5
    ind = range(0, len(date_list), gap)
    labels = [date_list[0], date_list[gap], date_list[2*gap], date_list[3*gap], date_list[4*gap], date_list[5*gap]]
    plt.xticks(ind, labels)

    plt.ylabel('Frequency')
    plt.title('Chronological message frequency by weekday')
    plt.show()

# generate num_colors unique colors
def get_colors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors


# assign each person a unique color to display in the graph
def _assign_colors(people):
    colors = get_colors(len(people))
    objects = {}
    for i in range(0, len(people)):
        p = people[i]
        objects[p.get_name()] = colors[i]
    return objects


# bar chart of average usage of a stat determined by func by person
def freq_non_word(people, color_map, func, message_type):
    # create plot
    plt.subplots()
    bar_width = 0.1
    opacity = 0.8

    # sort people by stat
    people.sort(key=lambda x: func(x), reverse=True)
    for i in range(0, len(people)):
        p = people[i]
        p_data = (func(p))
        plt.bar(i*bar_width, p_data, bar_width,
                alpha=opacity,
                color=color_map[p.get_name()],
                label=p.get_name())

    plt.xlabel(message_type)
    plt.ylabel('Average number of occurrences per message')
    plt.legend()
    plt.tight_layout()

    plt.show()

# create table ranking people by number of messages, with number of words and words per message listed
def produce_table(people):
    fig, ax = plt.subplots()

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    # sort people by num messages and compile into table
    people.sort(key=lambda p: p.total, reverse=True)
    clust_data = []
    for p in people:
        p_data = [p.get_name(), p.total, p.words, round(p.get_words_avg(), 1)]
        clust_data.append(p_data)

    collabel=("Person", "Number of messages", "Number of words", "Average words per message")
    ax.table(cellText=clust_data, colLabels=collabel, loc='center')

    plt.show()


if __name__ == "__main__":
    m_p = MessageParser('/home/david/Documents/Personal_Projects/facebookData/messages/dontmebro_08776cf081/message.json', 'David Louie')
    m_p.parse()
    # freq_by_day(m_p.get_people()[0])
    # freq_chrono(m_p.get_dates())
    # color_map = _assign_colors(m_p.get_people())
    # freq_non_word(m_p.get_people(), color_map, Person.get_stick_avg, 'Stickers')
    # freq_non_word(m_p.get_people(), color_map, Person.get_photos_avg, 'Photos')
    # freq_non_word(m_p.get_people(), color_map, Person.get_gifs_avg, 'Gifs')
    produce_table(m_p.get_people())
    m_p.pretty_print()





