#!/usr/bin/python3
# Plot a question's views over time from database
# Usage: ./se.plot.py <log_name> <Url>

import sys
import json
import math
import datetime
import calendar
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def sig(num, digits=2):
    return ("{0:." + str(digits) + "g}").format(num) if abs(num) < 10**digits else str(int(num))


def add_date(src, years=0, months=0, days=0):
    "Add a number of years, months, days to date object"

    # Calculate new years and month
    new_y, new_m = src.year, src.month
    new_y += (new_m + months - 1) // 12 + years
    new_m = (new_m + months - 1) % 12 + 1

    # Replace years and month in date and limit days if month comes up short (like February has 28 days)
    new_d = min(calendar.monthrange(new_y, new_m)[-1], src.day)
    date = src.replace(year=new_y, month=new_m, day=new_d)

    # Add and days in
    if days:
        date += datetime.timedelta(days=days)
    return date


def get_views(filename, site, question):
    dates = []
    views = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = json.loads(line)
            date = datetime.datetime.fromtimestamp(line[0])
            if site in line[1] and question in line[1][site]:
                count = int(line[1][site][question])
                dates.append(date)
                views.append(count)
    return dates, views


def print_views(dates, views, left, right):
    "Print out data for LibreOffice Calc viewing"
    print('\n')
    print(str(left).ljust(16), '\t', right)
    for date, view in zip(dates, views):
        print(date, '\t', sig(view))


def bin_weekly(dates, views_list, days=7):
    "Bin views into weekly increments."
    delta = datetime.timedelta(days=days)
    end_date = dates[-1]
    end_views = views_list[-1]
    weekly_dates = [end_date]
    weekly_views = []

    # Go thru in reverse order so the the last date is the same in both graphs
    for date, views in zip(reversed(dates), reversed(views_list)):
        if end_date - date >= delta or (date == weekly_dates[0] and end_date - date >= delta * 0.7):
            weekly_dates.append(weekly_dates[-1] - delta)
            increase = end_views - views
            # Adjust the numbers if more or less than a whole week
            adj = (end_date - date) / delta
            increase /= adj
            weekly_views.append(increase)
            end_views = views
            end_date = date


    weekly_dates.pop(-1)
    weekly_dates.reverse()
    weekly_views.reverse()
    return weekly_dates, weekly_views


def format_axis(ax, dates, views):

    # Strip removes and hours, minutes... off dates
    strip = lambda date: datetime.datetime(date.year, date.month, date.day)

    # Generate major tics every month or year
    start = strip(dates[0])                 # Start date
    end = strip(dates[-1])                  # End date
    length = (dates[-1] - dates[0]).days    # Number of days between them
    tics = []                               # Set major tics
    print('length =', length)


    if length < 90:
        print('short')
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m-%d'))
        tics = [start, end]
    elif length < 365 * 3:
        print('medium')
        # Add major tics every month
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%y-%m'))
        date = datetime.datetime(start.year, start.month, 1)
        while date < end:
            if date > start:
                tics.append(date)
            date = add_date(date, months=1)
    else:
        print('long')
        # Add major tics every year
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%y-%m'))
        date = datetime.datetime(start.year, 1, 1)
        while date < end:
            if date > start:
                tics.append(date)
            date = add_date(date, years=1)


    ax.set_xticks(tics)


    # Set limits to conform to first and last date
    ax.set_xlim(start, end)

    # Set minor ticks to days or months
    if length < 100:
        ax.xaxis.set_minor_locator(matplotlib.dates.DayLocator(interval=1))
    else:
        # Set Minor ticks to months
        ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))

    # Set the y tics
    start = int(min(views))
    end = max(views)
    end = int(end + 1) if end % 1 else int(end)
    scale = math.log(end - start, 10) if end - start > 1 else 1
    major = int(10 ** int(scale - 1))
    while True:
        tics = list(range(start, end + major, major))
        if len(tics) <= 10:
            break
        major *= 2
    ax.set_yticks(tics)

    # Set the minor tics
    if len(tics) > 2:
        minors = tics[1] - tics[0]
        if minors > 20:
            minors = 10
        if minors > 1:
            ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(n=minors))



def get_tics(start, end):
    "Try to find well spaced integer tics between start and end"
    if end - start <= 5:
        return list(range(start, end + 1))
    candidates = []
    for divisions in range(2, 8):
        interval = (end - start) // divisions
        tics = list(range(end, start, -interval))
        gap = (tics[-1] - start) / interval
        score = gap - (len(tics) / 10)**2
        tics = [start] + list(reversed(tics))
        candidates.append([score, tics])
        # print(round(score,1), interval, tics, '\n')
    # print('\n')
    candidates.sort()
    return candidates[-1][-1]


def main():
    if len(sys.argv[1:]) >= 2:
        filename = sys.argv[1]
        url = sys.argv[2]

    elif len(sys.argv[1:]) >= 1:
        filename = 'se.views.out'
        url = sys.argv[1]
    else:
        filename = 'se.views.out'
        url = input("Input a url to graph: ")

    site = url.split('/')[2].split('.')[0]
    question = url.split('/')[4]

    dates, views = get_views(filename, site, question)


    # Truncate view if given max number of days
    '''
    truncate = None
    if truncate:
        dates = dates[-truncate:]
        views = views[-truncate:]
    '''


    if len(dates) <= 2:
        print("Insufficient data found to make graph")
        return

    print_views(dates, views, 'Date:', 'Views Total:')
    if len(dates) >= 2:
        print("\nAverage Views per day:", \
        sig((views[-1] - views[0]) / ((dates[-1] - dates[0]).total_seconds() / 86400)))

    weekly_dates, weekly_views = bin_weekly(dates, views)
    if len(weekly_dates) >= 3:
        print_views(weekly_dates, weekly_views, 'Date:', "Normalized Weekly Views:")
        fig, (ax1, ax2) = plt.subplots(1, 2)
        format_axis(ax2, weekly_dates, weekly_views)

        ax2.set_title('Normalized Weekly Views')
        ax2.plot(weekly_dates, weekly_views)
        if len(weekly_dates) >= 2:
            print("\nAverage Views per week:", sig(sum(weekly_views) / len(weekly_views)))

    else:
        fig, ax1 = plt.subplots()

    format_axis(ax1, dates, views)
    ax1.set_title('Total Views')
    ax1.plot(dates, views)

    fig.suptitle('Views on ' + ' '.join((site.title(), "Question", question)))
    plt.show()


if __name__ == "__main__":
    main()
