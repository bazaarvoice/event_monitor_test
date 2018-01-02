
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

    noise_history = []

    for i in range(len(raw_data)):

        cycle_stat = cyclic_stats[i%cycle_size]

        raw_value = raw_data[i]
        cycle_stat.update(raw_value)
        cycle_history.append(cycle_stat.mean())

        noise_history.append(raw_value - cycle_stat.mean())


    # output to static HTML file
    output_file("lines.html")

    p = figure(title="Fig.3 - Noise", width=1200, height=400, x_axis_label='hours', y_axis_label='counts')

    p.line(x, raw_data, line_width=2, color="blue", legend="raw data")
    p.line(x, cycle_history, line_width=2, color="green", line_dash=[8,2], legend="cyclic avg")
    p.line(x, noise_history, line_width=2, color="firebrick", legend="noise")

    show(p)
