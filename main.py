import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import axes

import numpy as np

import csv
from enum import Enum
import random


def read_data(
    file_names: list[str],
    columns_to_read: list[int],
    start_index: float = 1,
    end_index: float = 1002,
) -> list[int]:
    data = []
    for file_name in file_names:
        with open(f"openfoam_data/{file_name}", newline="") as csvfile:
            file_reader = csv.reader(csvfile, delimiter=",")
            reader_data = list(file_reader)

            for column in columns_to_read:
                column_data = []

                for row in range(start_index, end_index):
                    column_data.append(reader_data[row][column])
                data.append(column_data)

    return data


def set_up_axes(
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
    x_velocity_U_5 = 0


if __name__ == "__main__":
    figure, ax = plt.subplots()

    all_file_names = ["U_5_data.csv"]
    # Read from the 10th column from every csv file which corresponds to the y-coordinate of the cavity flow model
    horizontal_axis = read_data(
        file_names=[file_name for file_name in all_file_names], columns_to_read=[10]
    )[0]

    selected_data = read_data(
        file_names=[file_name for file_name in all_file_names],
        columns_to_read=[property.value for property in physicalProperties],
    )

    set_up_axes(ax=ax, title="Lid-Driven Cavity Flow Data")

    all_markers = [".", ",", "o", "^", "v", "s", "D"]
    all_line_styles = ["-", "--", "-.", ":"]
    all_colors = [
        "#278AEB",
        "#4B7096",
        "#676B48",
        "#6B4A48",
        "#D6EB28",
        "#EB3428",
        "#90EB2F",
    ]

    # sample a list of random and unique indices from all_colors so no two plots have the same color
    colors_random_indices = random.sample(range(0, len(all_colors)), len(all_colors))

    for i, property in enumerate(physicalProperties):
        # markers_random_index = random.randrange(0, len(all_markers))
        # line_styles_random_index = random.randrange(0, len(all_line_styles))
        ax.plot(
            horizontal_axis,
            selected_data[i],
            (
                # f"{all_markers[markers_random_index]}"
                # f"{all_line_styles[line_styles_random_index]}"
                f"{all_colors[colors_random_indices[i]]}"
            ),
            lw=2,
            label=property.name,
        )

    ax.legend(frameon=True)

    plt.xlabel("position")
    plt.ylabel("magnitude of velocity")

    plt.savefig("C:/Users/23shaang/Desktop/CFD-Data-main/image/plot.png")
