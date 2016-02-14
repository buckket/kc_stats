import pytz

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def _create_chart():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    return fig, ax


def _apply_labels(ax, title):
    ax.set_title(title)
    ax.set_ylabel("posts per minute")
    ax.set_xlabel("bython powered - made by loom in 2016", fontsize=6)


def _enable_ticks(ax):
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()


def _scale_and_save(ax, fig, filename):
    ax.autoscale()
    fig.tight_layout()
    fig.savefig(filename)


def plot_weekday(series, title, filename):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    fig, ax = _create_chart()

    # Apply labels
    _apply_labels(ax, title)

    # Enable left and bottom ticks
    _enable_ticks(ax)

    # Plot
    ax.bar(range(len(series.index)), series, align='center')

    # Adjust ticks and labels
    ax.set_xticks(range(len(weekdays)))
    ax.set_xticklabels(weekdays)

    _scale_and_save(ax, fig, filename)


def plot_hour(series, title, filename):
    fig, ax = _create_chart()

    # Apply labels
    _apply_labels(ax, title)

    # Enable left and bottom ticks
    _enable_ticks(ax)

    # Plot
    ax.bar(range(len(series.index)), series, align='center')

    # Adjust ticks and labels
    ax.set_xticks(range(len(series.index)))
    ax.set_xticklabels(series.index)

    _scale_and_save(ax, fig, filename)


def plot_last_days(data, title, filename):
    tz = pytz.timezone("Europe/Berlin")
    fig_all, ax_all = _create_chart()

    # Apply labels
    _apply_labels(ax_all, title)

    # Enable left and bottom ticks
    _enable_ticks(ax_all)

    # Modify x-axis for proper styling
    ax_all.xaxis_date()
    x_hours = mdates.HourLocator(interval=4, tz=tz)
    x_format = mdates.DateFormatter('%H:%M', tz=tz)
    ax_all.xaxis.set_major_formatter(x_format)
    ax_all.xaxis.set_major_locator(x_hours)
    ax_all.minorticks_on()

    # Plot
    for series in data:
        ax_all.plot(series[1].index, series[1], label="/{}/".format(series[0]))

    ax_all.legend(loc=0, fancybox=True)

    _scale_and_save(ax_all, fig_all, filename)


def plot_last_week(data, title, filename):
    tz = pytz.timezone("Europe/Berlin")
    fig_all, ax_all = _create_chart()

    # Apply labels
    _apply_labels(ax_all, title)

    # Enable left and bottom ticks
    _enable_ticks(ax_all)

    # Modify x-axis for proper styling
    ax_all.xaxis_date()
    x_days = mdates.DayLocator(interval=1, tz=tz)
    x_format = mdates.DateFormatter('%a', tz=tz)
    ax_all.xaxis.set_major_formatter(x_format)
    ax_all.xaxis.set_major_locator(x_days)
    ax_all.minorticks_off()

    # Plot
    for series in data:
        ax_all.plot(series[1].index, series[1], label="/{}/".format(series[0]))

    # ax_all.legend(loc=0, fancybox=True)

    _scale_and_save(ax_all, fig_all, filename)


def plot_last_year(data, title, filename):
    tz = pytz.timezone("Europe/Berlin")
    fig_all, ax_all = _create_chart()

    # Apply labels
    _apply_labels(ax_all, title)

    # Enable left and bottom ticks
    _enable_ticks(ax_all)

    # Modify x-axis for proper styling
    ax_all.xaxis_date()
    x_months = mdates.MonthLocator(interval=1, tz=tz)
    x_format = mdates.DateFormatter('%b', tz=tz)
    ax_all.xaxis.set_major_formatter(x_format)
    ax_all.xaxis.set_major_locator(x_months)
    ax_all.minorticks_off()

    # Plot
    for series in data:
        ax_all.plot(series[1].index, series[1], label="/{}/".format(series[0]))

    ax_all.legend(loc=0, fancybox=True)

    _scale_and_save(ax_all, fig_all, filename)
