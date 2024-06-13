import matplotlib  # type: ignore
import matplotlib as mpl  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import matplotlib.ticker as ticker  # type: ignore
from matplotlib import axes  # type: ignore

import numpy as np  # type: ignore

import csv
from typing import Optional, Union
from enum import Enum


def read_data(
    file_name: str,
    columns_to_read: list[int],
    start_index: float = 1,
    end_index: float = 1002,
) -> list[int]:
    data = []

    with open(f"data/{file_name}", newline="") as csvfile:
        file_reader = csv.reader(csvfile, delimiter=",")
        reader_data = list(file_reader)

        for column in columns_to_read:
            column_data = []
            for row in range(start_index, end_index):
                column_data.append(reader_data[row][column])
            data.append(column_data)

    return data


def setup_axes(
    ax: axes,
    title: str,
    x_lower_limit: float = None,
    x_upper_limit: float = None,
    y_lower_limit: float = None,
    y_upper_limit: float = None,
) -> None:
    ax.grid(True)
    ax.axis("equal")

    ax.xaxis.set_major_locator(ticker.MaxNLocator(10))
    ax.xaxis.set_minor_locator(ticker.MaxNLocator(50))
    ax.xaxis.set_ticks_position("bottom")

    ax.yaxis.set_major_locator(ticker.MaxNLocator(10))
    ax.yaxis.set_minor_locator(ticker.MaxNLocator(50))
    ax.yaxis.set_ticks_position("left")

    if None not in (x_lower_limit, x_upper_limit):
        ax.set_xlim(x_lower_limit, x_upper_limit)

    if None not in (y_lower_limit, y_upper_limit):
        ax.set_ylim(y_lower_limit, y_upper_limit)

    ax.text(
        0.5,
        1.05,
        title,
        horizontalalignment="center",
        transform=ax.transAxes,
        fontsize=20,
        fontname="Calibri",
        color="tab:blue",
    )


class physicalProperties(Enum):
    Ux = 0          # velocity (x-component)
    Uy = 1          # velocity (y-component)
    epsilon = 3     # rate of diffusion of turbulent kinetic energy
    k = 4           # turbulent kinetic energy
    p = 6           # pressure
    arc_length = 8  # probably something related to postprocessing?


if __name__ == "__main__":
    figure, ax = plt.subplots()
    # # compile a list of all milliseconds between 0s and 10s so that we can plot it against the properties
    # time = np.linspace(
    #     0, 1001, 1001
    # )

    time = read_data("data_U_5.csv", [9])[0]

    selected_data = read_data(
        "data_U_5.csv",
        [property.value for property in physicalProperties],
    )

    setup_axes(ax, "Lid-Driven Cavity Flow Data", 0, 1002)

    all_line_styles = ["-", "--", "-.", ":"]
    all_colors = ["b", "g", "r", "c", "m", "y", "k"]

    for i, property in enumerate(physicalProperties):
        ax.plot(
            time,
            selected_data[i],
            f"{all_line_styles[np.random.randint(0, 3)]}{all_colors[np.random.randint(0, 6)]}",
            lw=2,
            label=property.name,
        )

    ax.legend(frameon=True)

    plt.xlabel("time")
    plt.ylabel("value")

    plt.savefig("C:/Users/nicol/Desktop/CFD Data/image/plot.png")
