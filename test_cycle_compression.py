
from bokeh.plotting import figure, output_file, show
from FadingStatistics import FadingStatistics
from bokeh.layouts import gridplot
import math

from data import debug_events

tests = [0]

def compress_signal(raw_value, trend_stats):
    COMPRESSION_FACTOR = 3.0

    normalized_value = raw_value - trend_stats.mean()
    compression_limit = COMPRESSION_FACTOR * trend_stats.deviation()
    if compression_limit < 0.0001:
        return raw_value

    compressed_value = math.atan(normalized_value / compression_limit) * compression_limit
    return trend_stats.mean() + compressed_value

for test in range(len(tests)):

    raw_data = debug_events[tests[test]]

    x = [i for i in range(len(raw_data))]

    hours_per_day = 24
    cycle_size = hours_per_day

    cyclic_stats = [FadingStatistics(14, 0.10) for i in range(cycle_size)]
    cycle_history = []

    trend_stats = FadingStatistics(hours_per_day*21, 0.10)
    trend_history = []

    compressed_history = []

    cyclic_compressed_stats = [FadingStatistics(14, 0.10) for i in range(cycle_size)]
    cycle_compressed_history = []

    for i in range(len(raw_data)):

        raw_value = raw_data[i]
        trend_stats.update(raw_value)
        trend_history.append(trend_stats.mean())

        cycle_stat = cyclic_stats[i%cycle_size]
        cycle_stat.update(raw_value)
        cycle_history.append(cycle_stat.mean())

        compressed_value = compress_signal(raw_value, trend_stats)
        compressed_history.append(compressed_value)

        cycle_compressed_stat = cyclic_compressed_stats[i%cycle_size]
        cycle_compressed_stat.update(compressed_value)
        cycle_compressed_history.append(cycle_compressed_stat.mean())

    # output to static HTML file
    output_file("lines.html")

    p = figure(title="Fig.4a - Un-Compressed", width=1200, height=400, x_axis_label='hours', y_axis_label='counts')
    p2 = figure(title="Fig.4b - Compressed", width=1200, height=400, x_axis_label='hours', y_axis_label='counts')

    p.line(x, raw_data, line_width=2, color="blue", legend="raw data")
    p.line(x, cycle_history, line_width=2, color="green", line_dash=[8,2], legend="cyclic avg")

    p2.line(x, raw_data, line_width=1, color="blue", line_dash=[2,2], legend="raw data")
    p2.line(x, compressed_history, line_width=2, color="black", legend="compressed data")
    p2.line(x, cycle_compressed_history, line_width=2, color="green", line_dash=[8,2], legend="cyclic avg")

    show(gridplot([[p], [p2]]))
