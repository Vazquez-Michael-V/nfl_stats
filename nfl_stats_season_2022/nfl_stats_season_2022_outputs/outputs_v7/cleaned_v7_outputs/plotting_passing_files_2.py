
import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly import offline
import plotly.io as pio


cleaned_files_output_path = r'some_directory\\'
df_passing_compare = pd.read_excel(f'{cleaned_files_output_path}df_passing_compare.xlsx')

print(df_passing_compare.shape)

# Prep the passing yards df.
df_passing_increase = df_passing_compare.loc[df_passing_compare['pass_yds_yoy_eval'] == 'increase'].copy()
df_passing_increase.sort_values(by=['pass_yds_yoy'], ascending=False, inplace=True)

# Prep the td df.
df_td_increase = df_passing_compare.loc[df_passing_compare['td_yoy_eval'] == 'increase'].copy()
df_td_increase.sort_values(by=['td_yoy'], ascending=False, inplace=True)

# Prep the int df.
df_int_increase = df_passing_compare.loc[df_passing_compare['int_yoy_eval'] == 'increase'].copy()
df_int_increase.sort_values(by=['int_yoy'], ascending=False, inplace=True)


# My plotly template.
pio.templates["mvazquez"] = go.layout.Template(
    layout_annotations = [
        dict(
            name = "mvazquez watermark",
            text = "Created by MVazquez",
            # textangle = -30,
            opacity = 0.5,
            font = dict(color = "lightgrey", size = 20),
            xref = "paper",
            yref = "paper",
            x = 0.01,
            y = 0.01,
            showarrow = False            
            )        
        ])

# 3 subplots, passing yards, touchdowns, interceptions.
fig = make_subplots(rows=3, cols=1, row_heights=[800, 500, 500],
                    subplot_titles=("Passing Yards", "Passing Touchdowns", "Interceptions"),
                    vertical_spacing = 0.20)

# Passing traces.
trace_passing_yds_2021 = go.Bar(
    name='2021 Pass Yds',
    x=df_passing_increase['player'],
    y=df_passing_increase['pass_yds_2021'],
    marker_color='rgb(55, 83, 109)'
    # TODO: Need to figure out custom text to show the yoy difference above the bars.
    # TODO: Annotations
    # text=df_passing_increase['pass_yds_yoy'],
    # textposition='outside'
    )

trace_passing_yds_2022 = go.Bar(
    name='2022 Pass Yds',
    x=df_passing_increase['player'],
    y=df_passing_increase['pass_yds_2022'],
    marker_color='rgb(26, 118, 255)'
    )

# Touchdown traces.
trace_tds_2021 = go.Bar(
    name='2021 TD',
    x=df_td_increase['player'],
    y=df_td_increase['td_2021'],
    marker_color='rgb(0, 168, 84)'
    )

trace_tds_2022 = go.Bar(
    name='2022 TD',
    x=df_td_increase['player'],
    y=df_td_increase['td_2022'],
    marker_color='rgb(0, 254, 127)'
    )

# Interception traces.
trace_ints_2021 = go.Bar(
    name='2021 Ints',
    x=df_int_increase['player'],
    y=df_int_increase['int_2021'],
    marker_color='rgb(180, 0, 0)'
    )

trace_ints_2022 = go.Bar(
    name='2022 Ints',
    x=df_int_increase['player'],
    y=df_int_increase['int_2022'],
    marker_color='rgb(255, 63, 63)'
    )

# Add the traces to the appropriate rows and columns.
fig.add_trace(trace_passing_yds_2021, row=1, col=1)
fig.add_trace(trace_passing_yds_2022, row=1, col=1)
fig.add_trace(trace_tds_2021, row=2, col=1)
fig.add_trace(trace_tds_2022, row=2, col=1)
fig.add_trace(trace_ints_2021, row=3, col=1)
fig.add_trace(trace_ints_2022, row=3, col=1)

# Adjust layout and xaxes.
fig.update_layout(
    title_text='Players with YoY Increase in Passing Stats - Seasons 2021 to 2022',
    # barmode='group',
    # xaxis_tickangle=90,
    template = 'plotly_dark+mvazquez'
    )
fig.update_xaxes(row=1, col=1, showticklabels=True,
                 tickangle=45,
                 tickfont=dict(
                     size=12))

# Create HTML file.
offline.plot(fig, filename=f'{cleaned_files_output_path}nfl_stats_passing_yoy_increases.html')
