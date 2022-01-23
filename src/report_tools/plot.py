import argparse
import pandas as pd
import plotly.express as px
import os


def getDf(filename):
    df = pd.read_csv(filename, delimiter="\t")
    df["size"] = df["size"].apply(str)
    df["noise"] = df["noise"].apply(str)
    df.loc[df["size"] == "1", "size"] = "01"
    df.loc[df["size"] == "5", "size"] = "05"
    df = df.groupby(["compressor", "size", "noise"]).apply(lambda x: x["correct"].sum()/len(x)).reset_index()
    df.columns = ["compressor", "size", "noise", "correct"]
    return df


def full(df, output, title, correctLabel):
    fig = px.scatter_3d(df,
        x = "noise",
        y = "size",
        color = "compressor",
        z = "correct",
        title = title,
        labels = {"size": "Size (s)", "noise": "Noise", "compressor": "Compressor", "correct": correctLabel})
    try:
        os.makedirs(os.path.dirname(output), exist_ok=True)
    except:
        pass
    fig.write_html(output)


def size(df, output, title, correctLabel):
    fig = px.line(df,
        x = "noise",
        color = "compressor",
        y = "correct",
        title = title,
        labels = {"noise": "Noise", "compressor": "Compressor", "correct": correctLabel},
        markers = True)
    try:
        os.makedirs(os.path.dirname(output), exist_ok=True)
    except:
        pass
    fig.write_html(output)


def noise(df, output, title, correctLabel):
    fig = px.line(df,
        x = "size",
        color = "compressor",
        y = "correct",
        title = title,
        labels = {"size": "Size (s)", "compressor": "Compressor", "correct": correctLabel},
        markers = True)
    try:
        os.makedirs(os.path.dirname(output), exist_ok=True)
    except:
        pass
    fig.write_html(output)


def main(args):
    # Graphs with how correct the songs found are
    df = getDf(args.data)
    df["correct"] = df["correct"]*100
    full(df,
        f"{args.full_prefix}.html",
        "Percentage of correctly found songs",
        "Correct (%)")
    size(df.loc[df["size"] == str(args.size)],
        f"{args.size_prefix}.html",
        f"Percentage of correctly found songs with size={args.size}s",
        "Correct (%)")
    noise(df.loc[df["noise"] == str(args.noise)],
        f"{args.noise_prefix}.html",
        f"Percentage of correctly found songs with noise={args.noise}",
        "Correct (%)")
    
    # Graphs that show if similar songs are found (classical genre only)
    df = getDf(args.classical_data)
    full(df,
        f"{args.full_prefix}Classical.html",
        "Average number of classical songs found in the top 4 results",
        "Songs")
    size(df.loc[df["size"] == str(args.size)],
        f"{args.size_prefix}Classical.html",
        f"Average number of classical songs found in the top 4 results with size={args.size}s",
        "Songs")
    noise(df.loc[df["noise"] == str(args.noise)],
        f"{args.noise_prefix}Classical.html",
        f"Average number of classical songs found in the top 4 results with noise={args.noise}",
        "Songs")
    
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="File with data for the graphs (generated by datagen.py)", required=True)
    parser.add_argument("--classical-data", help="File with data for the graphs (generated by datagen.py)", required=True)
    parser.add_argument("--full-prefix", help="File prefix to output the full graph", required=True)
    parser.add_argument("--size-prefix", help="File prefix to output the size graph", required=True)
    parser.add_argument("--noise-prefix", help="File prefix to output the noise graph", required=True)
    parser.add_argument("--size", help="Size to use for the size graph", default="01")
    parser.add_argument("--noise", help="Noise to use for the noise graph", default=0.1)
    args = parser.parse_args()
    main(args)