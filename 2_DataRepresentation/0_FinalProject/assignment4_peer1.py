% matplotlib
notebook

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pandas.tseries.offsets import MonthEnd, MonthBegin
from matplotlib.widgets import Button
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib.ticker import StrMethodFormatter
from matplotlib.lines import Line2D
import math


def draw_graph(year):
    ax1.cla()
    ax2.cla()
    ax1.set_title("Kineret Water Level VS Monthly Rainfall\n" + str(year))
    rainfall_year_df = rainfall_df[rainfall_df["Date"].dt.year == year]
    rainfall_year_df["Date"] = rainfall_year_df["Date"] - MonthBegin(1)
    waterlevel_year_df = waterlevel_df[waterlevel_df["Date"].dt.year == year]
    ax1.bar(rainfall_year_df["Date"].values, rainfall_year_df["Rain"], width=31, align="edge", color="c")
    ax2.plot(waterlevel_year_df["Date"], waterlevel_year_df["Level"], color="red", label=" Water Level")
    custom_lines = [Line2D([0], [0], color="c", lw="1"),
                    Line2D([0], [0], color="red", )]
    legend = ax1.legend(custom_lines, ['Rain Fall', 'Water Level)'])
    legend.get_lines()[0].set_linewidth(8)
    ax1.xaxis.set_major_locator(MonthLocator())
    ax1.xaxis.set_major_formatter(DateFormatter("%b"))
    ax2.yaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}'))  # 2 decimal places
    ax1.set_ylabel("Rainfall (mm)")
    ax2.set_ylabel("Water Level (mm from 'red line')")
    ax1.tick_params(top=False, right=False, left=False, bottom=False)
    ax2.tick_params(top=False, right=False, left=False, bottom=False)
    for spine in ax1.spines.values():
        spine.set_visible(False)
    for spine in ax2.spines.values():
        spine.set_visible(False)
    plt.show()


year = 1975

# ----------------------Clean Rain Data----------------------------------------------
rainfall_df = pd.read_csv("Har Meron.csv")
rainfall_df = rainfall_df[["Date", "Monthly Rainfall (mm)"]]
rainfall_df.columns = ["Date", "Rain"]
rainfall_df["Date"] = rainfall_df["Date"].str.slice_replace(-2, -2,
                                                            "19")  # add year (19) to date before converting to dt
rainfall_df["Date"] = pd.to_datetime(rainfall_df["Date"])  # .dt.to_period("M")
rainfall_df["Date"] = rainfall_df["Date"] + MonthEnd(1)
rainfall_df["Rain"] = pd.to_numeric(rainfall_df["Rain"])
rainfall_df["Month"] = rainfall_df["Date"].dt.month
target_df = rainfall_df.copy()
average_rain_df = rainfall_df.groupby("Month").agg("mean").reset_index()
record_to_insert = pd.DataFrame({"Month": [8], "Rain": [0]})
average_rain_df = pd.concat([average_rain_df.iloc[:7], record_to_insert, average_rain_df.iloc[7:]],
                            ignore_index=True).reset_index(drop=True)

# -------------add averaged data for missing months
target_index = 0
for source_index, row in rainfall_df.iterrows():
    # print(source_index)
    current_month = target_index + 1 - ((math.ceil((target_index + 1) / 12)) - 1) * 12
    current_year = 1969 + int((target_index) / 12)
    while (rainfall_df["Date"][source_index].month > current_month) or (
            rainfall_df["Date"][source_index].year > current_year):
        new_row = pd.DataFrame({"Date": [target_df["Date"][target_index - 1] + pd.DateOffset(months=1)],
                                "Month": [current_month],
                                "Rain": [average_rain_df.iloc[current_month - 1]["Rain"]]})
        target_df = pd.concat([target_df.iloc[:target_index], new_row, target_df.iloc[target_index:]]).reset_index(
            drop=True)
        target_index += 1
        current_month = target_index + 1 - ((math.ceil((target_index + 1) / 12)) - 1) * 12
        current_year = 1969 + int((target_index) / 12)
    target_index += 1
rainfall_df = target_df.copy()

# ----------------------Clean miflas Data---------------------------
waterlevel_df = pd.read_excel("miflas.xls")[["Date", "Level"]]
waterlevel_df["Date"] = pd.to_datetime(waterlevel_df["Date"])
waterlevel_df = waterlevel_df[waterlevel_df["Date"].dt.year < 1999]  # .set_index("Date")

# -----------------------Create plot axes-------------------------
fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()
plt.subplots_adjust(top=0.89)

# -----------------------Create Buttons-------------------------
next_button_ax = plt.axes([0.8, 0.9, 0.1, 0.05])
next_button = Button(ax=next_button_ax, color="white", hovercolor="grey", label="Next")
prev_button_ax = plt.axes([0.13, 0.9, 0.1, 0.05])
prev_button = Button(ax=prev_button_ax, color="white", hovercolor="grey", label="Prev")


def next_year(event):
    global year
    year += 1
    ax1.set_title(year)
    draw_graph(year)


next_button.on_clicked(next_year)


def prev_year(event):
    global year
    year -= 1
    ax1.set_title(year)
    draw_graph(year)


prev_button.on_clicked(prev_year)

draw_graph(year)


