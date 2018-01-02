
from bokeh.plotting import figure, output_file, show
from FadingStatistics import FadingStatistics
from bokeh.layouts import gridplot

from data import debug_events

tests = [3]

for test in range(len(tests)):

    raw_data = debug_events[tests[test]]

    x = [i for i in range(len(raw_data))]

    hours_per_day = 24
    cycle_size = hours_per_day

    cyclic_stats = [FadingStatistics(14, 0.10) for i in range(cycle_size)]
    cycle_history = []

    hour0_x = []
    hour0_y = []
    hour0_avg = []

    for i in range(len(raw_data)):

        raw_value = raw_data[i]

        cycle_stat = cyclic_stats[i%cycle_size]
        cycle_stat.update(raw_value)
        cycle_history.append(cycle_stat.mean())

        # For illustration, show data points for one cycle
        if i%cycle_size == 0:
            hour0_x.append(i)
            hour0_y.append(raw_value)
            hour0_avg.append(cycle_stat.mean())

    # output to static HTML file
    output_file("lines.html")

    p = figure(title="Fig.2a - Raw Data", width=1200, height=400, x_axis_label='hours', y_axis_label='counts')
    p2 = figure(title="Fig.2b - Cyclic Averages", width=1200, height=400, x_axis_label='hours', y_axis_label='counts')
    p3 = figure(title="Fig.2c - Superimposed", width=1200, height=400, x_axis_label='hours', y_axis_label='counts')

    p.line(x, raw_data, line_width=2, color="blue", legend="raw data")
    p.triangle(hour0_x, hour0_y, size=7, color="firebrick", alpha=1.0, legend="hour-0")

    p2.line(x, cycle_history, line_width=2, color="green", line_dash=[8,2], legend="cyclic avg")
    p2.triangle(hour0_x, hour0_avg, size=7, color="firebrick", alpha=1.0, legend="hour-0")

    p3.line(x, raw_data, line_width=2, color="blue", legend="raw data")
    p3.line(x, cycle_history, line_width=2, color="green", line_dash=[8,2], legend="cyclic avg")

    show(gridplot([[p], [p2], [p3]]))
