import argparse
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os

sns.set(
    style="darkgrid",
    rc={
        "figure.facecolor": "#252629", 
        "axes.facecolor": "#252629",    
        "grid.color": "#8F929E",        

        "figure.figsize": (7.2, 4.45),
        "xtick.labelsize": 16,
        "ytick.labelsize": 16,
        "font.size": 15,
        "figure.autolayout": True,
        "axes.titlesize": 16,
        "axes.labelsize": 17,
        "lines.linewidth": 2,
        "lines.markersize": 6,
        "legend.fontsize": 15,
        "text.color": "white",      
        "xtick.color": "white",         
        "ytick.color": "white",         
        "axes.labelcolor": "white",     
        "axes.edgecolor": "white",      
    },
)
colors = sns.color_palette("colorblind", 4)
dashes_styles = cycle(["-", "-.", "--", ":"])
sns.set_palette(colors)
colors = cycle(colors)


def moving_average(interval, window_size):
    if window_size == 1:
        return interval
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, "same")


def plot_df(df, color, xaxis, yaxis, ma=1, label=""):
    df[yaxis] = pd.to_numeric(df[yaxis], errors="coerce") 

    mean = df.groupby(xaxis).mean()[yaxis]
    std = df.groupby(xaxis).std()[yaxis]
    if ma > 1:
        mean = moving_average(mean, ma)
        std = moving_average(std, ma)

    x = df.groupby(xaxis).mean().index.values

    # Debugging output to check shapes
    print(f"Shape of x: {x.shape}")
    print(f"Shape of mean: {mean.shape}")
    print(f"Shape of std: {std.shape}")

    plt.plot(x, mean, label=label, color=color, linestyle=next(dashes_styles))
    plt.fill_between(x, mean + std, mean - std, alpha=0.25, color=color, rasterized=True)


if __name__ == "__main__":
    prs = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="""Plot Traffic Signal Metrics"""
    )
    prs.add_argument("-f", nargs=2, required=True, help="Two measures files representing first and last epoch\n")
    prs.add_argument("-l", nargs=2, default=None, help="File's legends\n")
    prs.add_argument("-t", type=str, default="", help="Plot title\n")
    prs.add_argument("-yaxis", type=str, default="system_total_waiting_time", help="The column to plot.\n")
    prs.add_argument("-xaxis", type=str, default="step", help="The x axis.\n")
    prs.add_argument("-ma", type=int, default=1, help="Moving Average Window.\n")
    prs.add_argument("-sep", type=str, default=",", help="Values separator on file.\n")
    prs.add_argument("-xlabel", type=str, default="Time step (s)", help="X axis label.\n")
    prs.add_argument("-ylabel", type=str, default="Total waiting time (s)", help="Y axis label.\n")
    prs.add_argument("-output", type=str, default=None, help="PDF output filename.\n")

    args = prs.parse_args()
    
    if len(args.f) != 2:
        raise ValueError("Exactly two input files are required.")

    labels = args.l if args.l is not None else ["First Epoch", "Last Epoch"]
    
    plt.figure()

    # Plot the first file (light blue)
    df1 = pd.read_csv(os.path.abspath(args.f[0]), sep=args.sep)
    plot_df(df1, xaxis=args.xaxis, yaxis=args.yaxis, label=labels[0], color=next(colors), ma=args.ma)

    # Plot the second file (dark blue)
    df2 = pd.read_csv(os.path.abspath(args.f[1]), sep=args.sep)
    plot_df(df2, xaxis=args.xaxis, yaxis=args.yaxis, label=labels[1], color=next(colors), ma=args.ma)

    plt.title(args.t)
    plt.ylabel(args.ylabel)
    plt.xlabel(args.xlabel)
    plt.ylim(bottom=0)
    plt.legend()

    if args.output is not None:
        output_path = os.path.abspath(args.output + ".pdf")
        plt.savefig(output_path, bbox_inches="tight")

    plt.show()
