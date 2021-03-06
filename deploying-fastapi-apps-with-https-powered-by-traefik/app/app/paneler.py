from pathlib import Path

import holoviews as hv
import hvplot.pandas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import panel as pn
from matplotlib.backends.backend_agg import FigureCanvas
from matplotlib.figure import Figure

current_file = Path(__file__)

if current_file.parent.resolve() == Path("/app/app"):
    data_path = Path("/data/datatraining.txt")
else:
    data_path = current_file.parent.parent / "data/datatraining.txt"

data = pd.read_csv(data_path)
data["date"] = data.date.astype("datetime64[ns]")
data = data.set_index("date")


def mpl_plot(avg, highlight):
    fig = Figure()
    FigureCanvas(fig)  # not needed in mpl >= 3.1
    ax = fig.add_subplot()
    avg.plot(ax=ax)
    if len(highlight):
        highlight.plot(style="o", ax=ax)
    return fig


def find_outliers(variable="Temperature", window=30, sigma=10, view_fn=mpl_plot):
    avg = data[variable].rolling(window=window).mean()
    residual = data[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = np.abs(residual) > std * sigma
    return view_fn(avg, avg[outliers])


kw = dict(window=(1, 60), variable=sorted(list(data.columns)), sigma=(1, 20))


tap = hv.streams.PointerX(x=data.index.min())


def hvplot2(avg, highlight):
    line = avg.hvplot(height=300, width=500)
    outliers = highlight.hvplot.scatter(color="orange", padding=0.1)
    tap.source = line
    return (line * outliers).opts(legend_position="top_right")


@pn.depends(tap.param.x)
def table(x):
    index = np.abs((data.index - x).astype(int)).argmin()
    return data.iloc[index]


app = pn.interact(find_outliers, view_fn=hvplot2, **kw)

row = pn.Row(
    pn.Column("## Room Occupancy\nHover over the plot for more information.", app[0]),
    pn.Row(app[1], table),
)

row.servable()
