"""Box plot module."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .style import custom_template, format_title


def boxplot(
    data_frame: pd.DataFrame,
    x_axis: str,
    y_axis: str,
    title: str,
    subtitle: str | None = None,
    outliers: bool = True,
    **kwargs,
) -> go.Figure:
    """Create a box plot.

    Args:
        data_frame (pd.DataFrame): DataFrame to plot.
        x_axis (str): Column to use as x axis.
        y_axis (str): Column to use as y axis.
        title (str): Title of the plot.
        subtitle (str, optional): Subtitle of the plot. Defaults to None.
        outliers (bool, optional): Show outliers. Defaults to True.
        **kwargs: Keyword arguments to pass to plotly.graph_objects.Box.

    Returns:
        go.Figure: Box plot figure.
    """
    fig = go.Figure()
    for x_value in data_frame[x_axis].unique():
        y_values = data_frame[data_frame[x_axis] == x_value][y_axis]

        boxpoints = "outliers" if outliers else False

        fig.add_trace(
            go.Box(
                x=data_frame[data_frame[x_axis] == x_value][x_axis],
                y=y_values,
                name=str(x_value),
                boxpoints=boxpoints,
                **kwargs,
            )
        )

    fig.update_layout(
        title=format_title(title, subtitle=subtitle),
        template=custom_template,
        width=800,
        height=400,
        showlegend=False,
    )
    fig.update_xaxes(title_text=x_axis)
    fig.update_yaxes(title_text=y_axis)
    return fig
