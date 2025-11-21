import plotly.graph_objects as go

def plot_forecast(history, forecast_df, history_weeks=52):

    # ------------------------------------------
    # Limit history to last N weeks (default 52)
    # ------------------------------------------
    history = history.tail(history_weeks)

    fig = go.Figure()

    # ------------------------------------------
    # HISTORY (last 52 weeks)
    # ------------------------------------------
    fig.add_trace(go.Scatter(
        x=history.index,
        y=history["y"],
        mode="lines",
        name="History",
        line=dict(color="rgba(80,80,80,0.8)", width=2)
    ))

    # ------------------------------------------
    # FORECAST MEAN
    # ------------------------------------------
    fig.add_trace(go.Scatter(
        x=forecast_df.index,
        y=forecast_df["mean"],
        mode="lines",
        name="Forecast",
        line=dict(color="rgba(30, 90, 255, 1)", width=3)
    ))

    # ------------------------------------------
    # CONFIDENCE INTERVAL BAND
    # ------------------------------------------
    fig.add_trace(go.Scatter(
        x=forecast_df.index,
        y=forecast_df["upper_90"],
        mode="lines",
        name="Upper 90%",
        line=dict(width=0),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df.index,
        y=forecast_df["lower_90"],
        mode="lines",
        name="90% CI",
        fill="tonexty",
        fillcolor="rgba(30, 90, 255, 0.15)",
        line=dict(width=0)
    ))

    # ------------------------------------------
    # Layout adjustments
    # ------------------------------------------
    fig.update_layout(
        title="<b>Weekly Revenue Forecast (Next 26 Weeks)</b>",
        xaxis_title="Week",
        yaxis_title="Revenue (€)",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=30, r=30, t=80, b=30)
    )

    return fig
