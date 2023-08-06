"""Matplotlib plotting backend."""

import datetime
from typing import Optional, List, Set

import numpy as np

from temporian.implementation.numpy.data.event_set import EventSet, IndexType
from temporian.implementation.numpy.data.plotter import (
    Options,
    Style,
    is_uniform,
    get_num_plots,
    auto_style,
)


def plot_matplotlib(
    evsets: List[EventSet],
    indexes: List[IndexType],
    features: Set[str],
    options: Options,
):
    import matplotlib.pyplot as plt
    from matplotlib.cm import get_cmap

    colors = get_cmap("tab10").colors

    px = 1 / plt.rcParams["figure.dpi"]

    num_plots = get_num_plots(evsets, indexes, features, options)

    fig, axs = plt.subplots(
        num_plots,
        figsize=(
            options.width_px * px,
            options.height_per_plot_px * num_plots * px,
        ),
        squeeze=False,
    )

    # Actual plotting
    plot_idx = 0
    for index in indexes:
        if plot_idx >= num_plots:
            # Too much plots are displayed already.
            break

        # Index of the next color to use in the plot.
        color_idx = 0

        for evset in evsets:
            if plot_idx >= num_plots:
                break

            title = " ".join(
                [f"{k}={v}" for k, v in zip(evset.schema.index_names(), index)]
            )

            evset_features = evset.schema.feature_names()
            display_features = [f for f in evset_features if f in features]

            xs = evset.data[index].timestamps
            uniform = is_uniform(xs)

            plot_mask = np.full(len(xs), True)
            if options.min_time is not None:
                plot_mask = plot_mask & (xs >= options.min_time)
            if options.max_time is not None:
                plot_mask = plot_mask & (xs <= options.max_time)
            if options.max_points is not None and len(xs) > options.max_points:
                # Too many timestamps. Only keep the fist ones.
                plot_mask = plot_mask & (
                    np.cumsum(plot_mask) <= options.max_points
                )

            xs = xs[plot_mask]

            if evset.schema.is_unix_timestamp:
                # Matplotlib understands datetimes.
                xs = [
                    datetime.datetime.fromtimestamp(x, tz=datetime.timezone.utc)
                    for x in xs
                ]

            if len(display_features) == 0:
                # There is not features to plot. Instead, plot the timestamps.
                _matplotlib_sub_plot(
                    ax=axs[plot_idx, 0],
                    xs=xs,
                    ys=np.zeros(len(xs)),
                    options=options,
                    color=colors[color_idx % len(colors)],
                    name="[sampling]",
                    is_unix_timestamp=evset.schema.is_unix_timestamp,
                    title=title,
                    style=Style.vline,
                )
                # Only print the index / title once
                title = None

                color_idx += 1
                plot_idx += 1

            for display_feature in display_features:
                feature_idx = evset_features.index(display_feature)

                if plot_idx >= num_plots:
                    # Too much plots are displayed already.
                    break

                ys = evset.data[index].features[feature_idx][plot_mask]
                if options.style == Style.auto:
                    effective_stype = auto_style(uniform, xs, ys)
                else:
                    effective_stype = options.style

                _matplotlib_sub_plot(
                    ax=axs[plot_idx, 0],
                    xs=xs,
                    ys=ys,
                    options=options,
                    color=colors[color_idx % len(colors)],
                    name=display_feature,
                    is_unix_timestamp=evset.schema.is_unix_timestamp,
                    title=title,
                    style=effective_stype,
                )

                # Only print the index / title once
                title = None

                color_idx += 1
                plot_idx += 1

    fig.tight_layout()
    return fig


def _matplotlib_sub_plot(
    ax,
    xs,
    ys,
    options: Options,
    color,
    name: str,
    is_unix_timestamp: bool,
    title: Optional[str],
    style: Style,
    **wargs,
):
    """Plots "(xs, ys)" on the axis "ax"."""

    import matplotlib.ticker as ticker

    if style == Style.line:
        mat_style = {}  # Default
    elif style == Style.marker:
        mat_style = {"marker": "2", "linestyle": "None"}
    elif style == Style.vline:
        mat_style = {"marker": "|", "linestyle": "None"}
    else:
        raise ValueError("Non implemented style")

    ax.plot(xs, ys, lw=0.5, color=color, **mat_style, **wargs)
    if options.min_time is not None or options.max_time is not None:
        args = {}
        if options.min_time is not None:
            args["left"] = (
                datetime.datetime.fromtimestamp(
                    options.min_time, tz=datetime.timezone.utc
                )
                if is_unix_timestamp
                else options.min_time
            )
        if options.max_time is not None:
            args["right"] = (
                datetime.datetime.fromtimestamp(
                    options.max_time, tz=datetime.timezone.utc
                )
                if is_unix_timestamp
                else options.max_time
            )
        ax.set_xlim(**args)

    ax.xaxis.set_tick_params(labelsize=8)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
    ax.xaxis.set_minor_locator(ticker.NullLocator())

    ax.set_ylabel(name, size=8)
    ax.yaxis.set_tick_params(labelsize=8)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(5))
    ax.yaxis.set_minor_locator(ticker.NullLocator())

    ax.grid(lw=0.4, ls="--", axis="x")
    if title:
        ax.set_title(title, fontsize=8)
