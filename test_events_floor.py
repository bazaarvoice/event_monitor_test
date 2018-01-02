
from bokeh.plotting import figure, output_file, show
from FadingStatistics import FadingStatistics
import math

from data import debug_events

tests = [5]

def compress_signal(raw_value, trend_stats):
    COMPRESSION_FACTOR = 3.0

    normalized_value = raw_value - trend_stats.mean()
    compression_limit = COMPRESSION_FACTOR * trend_stats.deviation()
    if compression_limit < 0.0001:
        return raw_value

    compressed_value = math.atan(normalized_value / compression_limit) * compression_limit
    return trend_stats.mean() + compressed_value

for test in range(len(tests)):
    EXCEPTION_DEVIATION_LIMIT = 3.0

    raw_data = debug_events[tests[test]]

    x = [i for i in range(len(raw_data))]

    hours_per_day = 24
    cycle_size = hours_per_day

    cyclic_stats = [FadingStatistics(14, 0.10) for i in range(cycle_size)]
    cycle_history = []
    cycle_deviation_high_history = []
    cycle_deviation_low_history = []

    trend_stats = FadingStatistics(hours_per_day*21, 0.10)
    trend_history = []
    trend_deviation_high_history = []
    trend_deviation_low_history = []

    compressed_history = []

    exception_x = []
    exception_y = []

    for i in range(len(raw_data)):

        raw_value = raw_data[i]
        trend_stats.update(raw_value)
        trend_history.append(trend_stats.mean())

        compressed_value = compress_signal(raw_value, trend_stats)
        compressed_history.append(compressed_value)

        cycle_stat = cyclic_stats[i%cycle_size]
        cycle_stat.update(compressed_value)
        cycle_history.append(cycle_stat.mean())

        # Signal bounds; if the signal runs outside of these limits, flag an exception
        cyclic_value = cycle_stat.mean()
        # Choosing rails can be tricky; the standard deviation goes wide on an event, and the signal model tends to be fussy;
        # so let's choose an average between the two.
        cycle_deviation_limit = (abs((cyclic_value - trend_stats.mean())) + trend_stats.deviation()) * 0.5 * EXCEPTION_DEVIATION_LIMIT
        cycle_deviation_high_history.append(cyclic_value + cycle_deviation_limit)
        cycle_deviation_low_history.append(cyclic_value - cycle_deviation_limit)

        # Enforce an event floor of 3% of the signal model
        floor = cyclic_value * 0.03
        if cycle_deviation_low_history[i] < floor:
            cycle_deviation_low_history[i] = floor

        if raw_value > cycle_deviation_high_history[i] or raw_value < cycle_deviation_low_history[i]:
            exception_x.append(i)
            exception_y.append(raw_value)

    # output to static HTML file
    output_file("lines.html")

    p = figure(title="Fig.6 - Event Limits Floor", width=1200, height=400, x_axis_label='hours', y_axis_label='counts')

    p.line(x, raw_data, line_width=1, color="blue", legend="raw data")
    p.line(x, cycle_history, line_width=2, color="green", line_dash=[8,2], legend="cyclic avg")

    p.line(x, cycle_deviation_high_history, line_width=1, color="red", legend="upper bound")
    p.line(x, cycle_deviation_low_history, line_width=1, color="red", legend="lower bound")

    p.triangle(exception_x, exception_y, size=7, color="firebrick", legend="exceptional")

    show(p)
