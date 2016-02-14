import datetime
import tarfile
import json
import os

import pandas
import numpy as np
import matplotlib.pyplot as plt

from database import Imageboard, Post
from plot import plot_weekday, plot_hour
from plot import plot_last_days, plot_last_week, plot_last_year


FILEDIR = "out"


def compress_file(filename):
    filepath = os.path.join(FILEDIR, filename)
    with tarfile.open(os.path.join(FILEDIR, "{}.tar.xz".format(filename[:-4])), "w:xz") as tar:
        tar.add(filepath)
    os.remove(filepath)


def work_on_everything():
    for imageboard in Imageboard.select():
        for board in imageboard.boards:
            series = pandas.Series([post.post_id for post in board.data], index=[post.timestamp for post in board.data])

            # Apply tz info and convert to local tz
            series = series.tz_localize('UTC')
            series = series.tz_convert('Europe/Berlin')

            # Resample and interpolate missing values
            series = series.resample('1min').interpolate()

            series_diff = series.diff()

            # Save complete data set as csv file
            filename = "all_{}.csv".format(board.board)
            series_diff.to_csv(os.path.join(FILEDIR, filename))
            compress_file(filename)

            weekdays = series_diff.groupby(series_diff.index.weekday)
            weekdays_out = [(int(weekday[0]), float(weekday[1].mean().round(2))) for weekday in weekdays]
            with open(os.path.join(FILEDIR, "weekday_{}.json".format(board.board)), "w") as outfile:
                json.dump(weekdays_out, outfile)
            weekdays_series = pandas.Series([weekday[1].mean() for weekday in weekdays],
                                            index=[weekday[0] for weekday in weekdays])
            plot_weekday(weekdays_series, "post distribution per weekday on /{}/".format(board.board),
                         os.path.join(FILEDIR, "weekday_{}.png".format(board.board)))

            hours = series_diff.groupby(series_diff.index.hour)
            hours_out = [(int(hour[0]), float(hour[1].mean().round(2))) for hour in hours]
            with open(os.path.join(FILEDIR, "hour_{}.json".format(board.board)), "w") as outfile:
                json.dump(hours_out, outfile)
            hours_series = pandas.Series(np.roll([hour[1].mean() for hour in hours], -6),
                                         index=np.roll([hour[0] for hour in hours], -6))
            plot_hour(hours_series, "post distribution per hour on /{}/".format(board.board),
                      os.path.join(FILEDIR, "hour_{}.png".format(board.board)))


def last_days():
    days_data = []
    days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=2)
    for imageboard in Imageboard.select():
        for board in imageboard.boards:
            data = board.data.select().where(Post.timestamp >= days_ago)
            series = pandas.Series([post.post_id for post in data], index=[post.timestamp for post in data])

            # Apply tz info and convert to local tz
            series = series.tz_localize('UTC')
            series = series.tz_convert('Europe/Berlin')

            # Resample and interpolate missing values
            series = series.resample('1min').interpolate()

            series_diff = series.diff()

            filename = "last_days_{}.csv".format(board.board)
            series_diff.to_csv(os.path.join(FILEDIR, filename))
            compress_file(filename)

            series_mean = pandas.rolling_mean(series_diff, 90)
            days_data.append((board.board, series_mean))
    plot_last_days(days_data, "last 48 hours", os.path.join(FILEDIR, "last_days.png"))


def last_week():
    week_data = []
    week_ago = datetime.datetime.utcnow() - datetime.timedelta(weeks=1)
    for imageboard in Imageboard.select():
        for board in imageboard.boards:
            data = board.data.select().where(Post.timestamp >= week_ago)
            series = pandas.Series([post.post_id for post in data], index=[post.timestamp for post in data])

            # Apply tz info
            series = series.tz_localize('UTC')
            series = series.tz_convert('Europe/Berlin')

            # Resample and interpolate missing values
            series = series.resample('1min').interpolate()

            series_diff = series.diff()

            filename = "last_week_{}.csv".format(board.board)
            series_diff.to_csv(os.path.join(FILEDIR, filename))
            compress_file(filename)

            series_mean = pandas.rolling_mean(series_diff, 140)
            week_data.append((board.board, series_mean))
    plot_last_week(week_data, "last 7 days", os.path.join(FILEDIR, "last_week.png"))


def last_year():
    year_data = []
    year_ago = datetime.datetime.utcnow() - datetime.timedelta(days=365)
    for imageboard in Imageboard.select():
        for board in imageboard.boards:
            data = board.data.select().where(Post.timestamp >= year_ago)
            series = pandas.Series([post.post_id for post in data], index=[post.timestamp for post in data])

            # Apply tz info
            series = series.tz_localize('UTC')
            series = series.tz_convert('Europe/Berlin')

            # Resample and interpolate missing values
            series = series.resample('1min').interpolate()

            series_diff = series.diff()
            series_diff = series_diff.resample('1H', how='mean')

            #filename = "last_year_{}.csv".format(board.board)
            #series_diff.to_csv(os.path.join(FILEDIR, filename))
            #compress_file(filename)

            series_mean = pandas.rolling_mean(series_diff, 168)
            year_data.append((board.board, series_mean))
    plot_last_year(year_data, "last year on krautchan", os.path.join(FILEDIR, "last_year.png"))


def write_html():
    import jinja2

    template_loader = jinja2.FileSystemLoader(searchpath="templates/")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("index.html")

    output = template.render(last_update=datetime.datetime.now(), boards=['b', 'int', 'vip'])
    with open(os.path.join(FILEDIR, "index.html"), "w") as outfile:
        outfile.write(output)


if __name__ == '__main__':
    plt.style.use('ggplot')
    plt.xkcd()

    work_on_everything()
    last_days()
    last_week()
    last_year()

    write_html()

