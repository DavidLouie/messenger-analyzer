from message_parser import MessageParser
from person import Person
import colorsys
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.backends.backend_pdf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta


# create bar chart of message frequency by day of the week
def freq_by_day(person):
    fig = plt.figure()
    objects = ('Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun')
    y_pos = np.arange(len(objects))
    freq = person.days.values()
    plt.bar(y_pos, freq, align='center', alpha=0.8, color=col_map[person.get_name()])
    plt.xticks(y_pos, objects)
    plt.ylabel('Frequency')
    plt.title(person.get_name() + ' message frequency by weekday')
    return fig


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


# produce indices of labels from a list of dates
def create_ind(d_list):
    return range(0, len(d_list), len(d_list) // 5)


# produce 5 or 6 evenly spaced labels from a list of dates
def create_labels(d_list):
    gap = len(d_list) // 5
    labels = [d_list[0], d_list[gap], d_list[2 * gap],
              d_list[3 * gap], d_list[4 * gap], d_list[5 * gap - 1]]
    return labels


# create bar chart of message frequency for a person on each day over the dataset
def freq_chrono(person):
    fig = plt.figure()
    date_list = convert_timestamps(person.dates)
    y_pos = np.arange(len(date_list))
    freq = count_timestamps(person.dates, len(date_list))
    plt.bar(y_pos, freq, align='center', alpha=0.8, color=col_map[person.get_name()])

    # produce 5 or 6 evenly spaced x-axis labels
    plt.xticks(create_ind(date_list), create_labels(date_list))

    plt.ylabel('Frequency')
    plt.title(person.get_name() +' message frequency')
    return fig


# create bar chart of total message frequency across the dataset
def freq_chrono_total(people):
    combined_p = Person('Total')
    timestamps = []
    for p in people:
        timestamps.extend(p.dates)
    timestamps.sort()
    combined_p.dates = timestamps
    return freq_chrono(combined_p)


# create stacked bar chart of message frequency over the dataset
def freq_chrono_stacked(people):
    fig = plt.figure()
    combined_ts = []
    for p in people:
        combined_ts.extend(p.dates)
    date_list = convert_timestamps(combined_ts)

    x_ind = np.arange(len(date_list))
    width = 0.35

    # sort people by number of messages to produce a prettier graph
    people.sort(key=lambda p: p.total, reverse=True)

    # plot the first person to set the bottom correctly for following people
    first_p = people[0]
    prev = count_timestamps(first_p.dates, len(date_list))
    plt.bar(x_ind, prev, width,
            color=col_map[first_p.get_name()],
            label=first_p.get_name())

    # plot the rest of the people, skipping the first person
    iter_people = iter(people)
    next(iter_people)
    for p in iter_people:
        p_date_freq = count_timestamps(p.dates, len(date_list))
        plt.bar(x_ind, p_date_freq, width, bottom=prev,
                color=col_map[p.get_name()],
                label=p.get_name())
        prev = list(map(sum,  zip(prev, p_date_freq)))

    # produce 5 or 6 evenly spaced x-axis labels
    plt.xticks(create_ind(date_list), create_labels(date_list))

    plt.ylabel('Messages per day')
    plt.title('Messages per day by person')
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    return fig


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
    colors = get_colors(len(people) + 1)
    objects = {}
    for i in range(0, len(people)):
        p = people[i]
        objects[p.get_name()] = colors[i]
    objects['Total'] = colors[len(people)]      # color of combined data
    return objects


# bar chart of average usage of a stat determined by func by person
def freq_non_word(people, func, message_type):
    # create plot
    fig, ax = plt.subplots()
    bar_width = 0.1
    opacity = 0.8

    # sort people by stat
    people.sort(key=lambda p: func(p), reverse=True)

    for i in range(0, len(people)):
        p = people[i]
        p_data = (func(p))
        plt.bar(i*bar_width, p_data, bar_width,
                alpha=opacity,
                color=col_map[p.get_name()],
                label=p.get_name())

    plt.xlabel(message_type)
    plt.ylabel('Average number of occurrences per message')
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.tight_layout()

    return fig


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

    return fig


if __name__ == "__main__":
    output_pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
    m_p = MessageParser('/home/david/Documents/Personal_Projects/facebookData/messages/dontmebro_08776cf081/message.json', 'David Louie')
    m_p.parse()
    col_map = _assign_colors(m_p.people)
    plot1 = freq_by_day(m_p.people[0])
    output_pdf.savefig(plot1)
    plot2 = freq_chrono(m_p.people[2])
    output_pdf.savefig(plot2)
    plot3 = freq_chrono_total(m_p.people)
    output_pdf.savefig(plot3)
    plot4 = freq_chrono_stacked(m_p.people)
    output_pdf.savefig(plot4, bbox_inches="tight")
    plot5 = freq_non_word(m_p.people, Person.get_stick_avg, 'Stickers')
    output_pdf.savefig(plot5, bbox_inches="tight")
    plot6 = freq_non_word(m_p.people, Person.get_photos_avg, 'Photos')
    output_pdf.savefig(plot6, bbox_inches="tight")
    plot7 = freq_non_word(m_p.people, Person.get_gifs_avg, 'Gifs')
    output_pdf.savefig(plot7, bbox_inches="tight")
    plot8 = produce_table(m_p.people)
    output_pdf.savefig(plot8)
    #m_p.pretty_print()
    output_pdf.close()





