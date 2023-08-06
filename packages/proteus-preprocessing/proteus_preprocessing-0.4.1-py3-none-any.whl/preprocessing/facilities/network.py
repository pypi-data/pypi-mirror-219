import json
import os

import numpy as np
import pandas as pd


def preprocess(download_func, output_source, network, **_):
    df = get_raw_network_dataframe(download_func, output_source, network)

    unique_counts = df.groupby(["Elevation", "Lat", "Long"]).transform("nunique")
    df["num_connections"] = unique_counts["BranchEquipment"]
    network_number = list(df["Network"].unique())

    network = {}
    for n in range(len(network_number)):
        network[n + 1] = {}
        network[n + 1]["branches"] = df[df["Network"] == network_number[n]]["BranchEquipment"].unique().tolist()
        network[n + 1]["measured_distance"] = np.concatenate(
            [df[df["BranchEquipment"] == b]["MeasuredDistance"].values for b in network[n + 1]["branches"]]
        ).tolist()
        network[n + 1]["numbers"] = np.cumsum(
            [len(df[df["BranchEquipment"] == b]["MeasuredDistance"].values) for b in network[n + 1]["branches"]]
        ).tolist()

    save_processed_network_json(output_source, network)


def get_raw_network_dataframe(download_func, output_source, network):
    download_func(network, output_source.uri)
    input_file_name = os.path.join(output_source.uri, network)
    return pd.read_csv(input_file_name)


def save_processed_network_json(output_source, network):
    output_file_name = os.path.join(output_source.uri, "network.json")
    with open(output_file_name, "w") as output_file:
        json.dump(network, output_file)
