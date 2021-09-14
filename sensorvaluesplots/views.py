from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter


def index(request):
    x_data = [
        -1, 1, 2, 4, 5
    ]

    y_data = [
        (1 / (x ** 2)) for x in x_data
    ]

    plot_div = plot(
        [
            Scatter(
                x=x_data,
                y=y_data,
                mode='markers+lines+text',
                name='test1',
                opacity=1,
                marker_color='green',
            ),
            Scatter(
                x=x_data,
                y=[5, 15, 25, 35, 45, 55],
                mode='markers+lines+text',
                name='test2',
                opacity=1,
                marker_color='blue',
            ),
            Scatter(
                # x=[10, 20, 30, 40, 50], andere abszisse -> zweite linie im plot
                x=x_data,
                y=[1, 12, 22, 32, 42, 52],
                mode='markers+lines+text',
                name='<a href="/admin"> testlink</a>',
                opacity=1,
                marker_color='red',
            ),
        ],
        output_type='div')
    return render(request, "sensorvaluesplots/index.html", context={'plot_div': plot_div})

