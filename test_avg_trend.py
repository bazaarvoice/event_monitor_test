
from bokeh.plotting import figure, output_file, show
from FadingStatistics import FadingStatistics

from data import debug_events

tests = [3]

for test in range(len(tests)):

    raw_data = debug_events[tests[test]]

    x = [i for i in range(len(raw_data))]

    hours_per_day = 24

    # Different fading window statistics for averages, plus history arrays for display purposes
    trend_1day_stats = FadingStatistics(hours_per_day*1, 0.10)
    trend_1day_history = []

    trend_7day_stats = FadingStatistics(hours_per_day*7, 0.10)
    trend_7day_history = []

    trend_21day_stats = FadingStatistics(hours_per_day*21, 0.10)
    trend_21day_history = []

    for i in range(len(raw_data)):

        raw_value = raw_data[i]
        trend_1day_stats.update(raw_value)
        trend_7day_stats.update(raw_value)
        trend_21day_stats.update(raw_value)

        trend_1day_history.append(trend_1day_stats.mean())
        trend_7day_history.append(trend_7day_stats.mean())
        trend_21day_history.append(trend_21day_stats.mean())


    # output to static HTML file
    output_file("lines.html")

    p = figure(title="Fig.1 - Raw Data and Trending Averages", width=1200, height=400, x_axis_label='hours', y_axis_label='counts')

    p.line(x, raw_data, line_width=2, color="blue", legend="raw data")

    p.line(x, trend_1day_history, line_width=2, color="green", line_dash=[2,2], legend="1-day avg")
    p.line(x, trend_7day_history, line_width=2, color="green", line_dash=[4,4], legend="7-day avg")
    p.line(x, trend_21day_history, line_width=2, color="green", line_dash=[8,2], legend="21-day avg")

    show(p)
