import plotly.graph_objects as go

lex_color = "#A6A00C"


def human_display(
    amount: float, with_decimal=True, shorten=True, unit: str = ""
) -> str:
    """
    Return
    """
    result = None
    if shorten:
        if abs(amount) >= 1e9:
            if abs(amount) < 1e11:
                result = f"{amount/1e9:,.2f} Mds {unit}"
            else:
                result = f"{amount/1e9:,.0f} Mds {unit}"
        elif abs(amount) >= 1e6:
            if abs(amount) < 1e8:
                result = f"{amount/1e6:,.2f} M{unit}"
            else:
                result = f"{amount/1e6:,.0f} M{unit}"
        elif abs(amount) >= 1e4:
            result = f"{amount/1e3:,.2f} k{unit}"
    if with_decimal and result is None:
        result = f"{amount:,.2f} {unit}"
    elif result is None:
        result = f"{amount:,.0f} {unit}"
    return result.replace(",", " ").replace(".", ",")


def in_euros(amount: float, with_decimal=True, shorten=True) -> str:
    return human_display(amount, with_decimal, shorten, unit="€")


def get_x_data(df):
    # Quantile numbering
    if "quantile_index" in df.columns:
        if df["quantile_index"].iloc[0] == 0:
            df["quantile_index"] = df["quantile_index"] + 1
        x_data = df["quantile_index"]
    else:
        x_data = df.index
    return x_data


def plot_distribution(
    data1,
    data2=None,
    data3=None,
    replace_num_quantile_by_bound: bool = False,
    log: bool = False,
    title: str = None,
):
    """
    data1 = {
        "df": df_decile_rfr_2020,
        "trace_name": "POTE 2020",
        "col_to_plot": {
            "y": "bucket_mean",
            "width": "bucket_count",
            "y_lib": "Moyenne",
        },
    }
    """
    df = data1["df"]
    df2 = df3 = None
    width_factor = 1
    if data2 is not None:
        df2 = data2["df"]
        width_factor = 2
    if data3 is not None:
        df3 = data3["df"]
        width_factor = 3
    if len(df) == 10:
        decile_or_quantile = "décile"
    elif len(df) == 100:
        decile_or_quantile = "centile"
    else:
        decile_or_quantile = "ERROR"

    # Build width of bar
    common_bucket_size = df[data1["col_to_plot"]["width"]].quantile(q=0.5)
    common_bucket_size
    df["width"] = 0.8 / width_factor
    df.loc[df[data1["col_to_plot"]["width"]] > common_bucket_size + 1, "width"] = (
        1 / width_factor
    )
    df.loc[df[data1["col_to_plot"]["width"]] < common_bucket_size - 1, "width"] = (
        0.2 / width_factor
    )
    x_data = get_x_data(df)

    if replace_num_quantile_by_bound:
        bar_text = df["bucket_count"].round()
    else:
        bar_text = [f"{in_euros(val)}" for val in df.lower_bound.to_list()]

    data_to_plot = [
        go.Bar(
            x=x_data,
            y=df[data1["col_to_plot"]["y"]].to_list(),
            text=bar_text,
            width=df["width"].to_list(),
            name=data1.get("trace_name")
            # marker_color=lex_color
        )
    ]
    if df2 is not None:
        if replace_num_quantile_by_bound:
            bar_text = df2["bucket_count"].round()
        else:
            bar_text = [f"{in_euros(val)}" for val in df2.lower_bound.to_list()]
        data_to_plot.append(
            go.Bar(
                x=x_data,
                y=df2[data2["col_to_plot"]["y"]].to_list(),
                text=bar_text,
                width=df["width"].to_list(),
                name=data2.get("trace_name"),
            )
        )
    if df3 is not None:
        if replace_num_quantile_by_bound:
            bar_text = df3["bucket_count"].round()
        else:
            bar_text = [f"{in_euros(val)}" for val in df3.lower_bound.to_list()]
        data_to_plot.append(
            go.Bar(
                x=x_data,
                y=df3[data3["col_to_plot"]["y"]].to_list(),
                text=bar_text,
                width=df["width"].to_list(),
                name=data3.get("trace_name"),
            )
        )

    fig = go.Figure(data=data_to_plot)
    if title:
        fig.update_layout(title=title)
    if log:
        fig.update_yaxes(type="log")
        fig.add_annotation(
            xref="x domain",
            yref="y domain",
            # The arrow head will be 25% along the x axis, starting from the left
            x=0.01,
            # The arrow head will be 40% along the y axis, starting from the bottom
            y=0.94,
            text="<b>Attention</b> : échelle logarithmique !",
            showarrow=False,
        )

    if replace_num_quantile_by_bound:
        _ = fig.update_traces(
            # text = bucket_count,
            hovertemplate="Nombre de foyer : %{text:,.0f}<br>"
            + "Frontière basse : %{x}<br>"
            + f"{data1['col_to_plot'].get('y_lib')}"
            + ": %{y:,.0f} €<br>",
        )
        _ = fig.update_layout(
            xaxis=dict(
                title="Montant minimum de la tranche",
                tickmode="array",
                tickvals=x_data,
                ticktext=[f"{in_euros(val)}" for val in df.lower_bound.to_list()],
            )
        )
    else:
        _ = fig.update_traces(
            hovertemplate=decile_or_quantile
            + " : %{x}<br>"
            + "Frontière basse : %{text}<br>"
            + f"{data1['col_to_plot'].get('y_lib')}"
            + ": %{y:,.0f} €<br>",
        )
        _ = fig.update_layout(
            xaxis=dict(
                title="Numéro de " + decile_or_quantile,
                tickmode="linear",
            ),
            yaxis=dict(title="Euros"),  # , rangemode="tozero"
        )
    # Update plot sizing
    fig.update_layout(
        height=700,
        autosize=True,
        template="plotly_white",
    )
    fig.update_traces(marker_line_color=lex_color, marker_line_width=2)
    _ = fig.update_layout(hovermode="x unified")

    return fig.show()


def plot_quantile(
    df,
    df2=None,
    df3=None,
    col_to_plot: dict = {
        "x": "rfr",
        "y": "irpp",
        "x_lib": "Revenu fiscal de référence",
        "y_lib": "Impôt",
    },
    replace_num_quantile_by_bound: bool = False,
    log: bool = False,
    title: str = None,
):
    if len(df) == 10:
        decile_or_quantile = "décile"
    elif len(df) == 100:
        decile_or_quantile = "centile"
    else:
        decile_or_quantile = "ERROR"

    width = 0.8
    if df2 is not None:
        width = 0.5
        if df3 is not None:
            width = 0.3

    data_to_plot = [
        go.Bar(
            x=df.index + 1,
            y=df[col_to_plot["y"]].to_list(),
            width=width,
            # marker_color=lex_color
        )
    ]
    if df2 is not None:
        data_to_plot.append(
            go.Bar(
                x=df2.index + 1,
                y=df2[col_to_plot["y"]].to_list(),
                width=width,
            )
        )
    if df3 is not None:
        data_to_plot.append(
            go.Bar(
                x=df3.index + 1,
                y=df2[col_to_plot["y"]].to_list(),
                width=width,
            )
        )

    fig = go.Figure(data=data_to_plot)
    if title:
        fig.update_layout(title=title)
    if log:
        fig.update_yaxes(type="log")
        fig.add_annotation(
            xref="x domain",
            yref="y domain",
            # The arrow head will be 25% along the x axis, starting from the left
            x=0.01,
            # The arrow head will be 40% along the y axis, starting from the bottom
            y=0.94,
            text="<b>Attention</b> : échelle logarithmique !",
            showarrow=False,
        )

    if replace_num_quantile_by_bound:
        _ = fig.update_traces(
            text=df["count"],
            hovertemplate="Nombre de foyer : %{text:,.0f}<br>"
            + "Frontière haute : %{x}<br>"
            + f"{col_to_plot.get('y_lib')}"
            + ": %{y:,.0f} €<br>",
        )
        _ = fig.update_layout(
            xaxis=dict(
                title="Montant minimum de la tranche",
                tickmode="array",
                tickvals=df.index,
                ticktext=[f"{in_euros(val)}" for val in df[col_to_plot["x"]].to_list()],
            )
        )
    else:
        _ = fig.update_traces(
            text=[f"{in_euros(val)}" for val in df[col_to_plot["x"]].to_list()],
            hovertemplate=decile_or_quantile
            + " : %{x}<br>"
            + "Frontière haute : %{text}<br>"
            + f"{col_to_plot.get('y_lib')}"
            + ": %{y:,.0f} €<br>",
        )
        _ = fig.update_layout(
            xaxis=dict(
                title="Numéro de " + decile_or_quantile,
                tickmode="linear",
            ),
            yaxis=dict(title="Euros"),  # , rangemode="tozero"
        )
    # Update plot sizing
    fig.update_layout(
        height=700,
        autosize=True,
        template="plotly_white",
    )
    fig.update_traces(marker_line_color=lex_color, marker_line_width=2)
    _ = fig.update_layout(hovermode="x unified")

    return fig.show()
