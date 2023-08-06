import json
import os

import h5py
import numpy as np

VARIABLES = [
    "VolumeFlowrateOilStockTank",
    "VolumeFlowrateLiquidStockTank",
    "Pressure",
    "Watercut",
    "VolumeFlowrateOilInSitu",
    "VolumeFlowrateLiquidInSitu",
]


def preprocess(download_func, output_source, base_output_source, input_files, **_):
    network = get_processed_network_json(base_output_source)

    download_raw_flowline_csvs(download_func, output_source, input_files)

    output_networks = []
    for n in range(len(network)):
        network_names = network[list(network.keys())[n]]["branches"]
        outputs = []

        for variable in VARIABLES:
            outputs_array = []

            for input_file in input_files:
                input_file_name = os.path.join(output_source.uri, input_file)
                data = np.loadtxt(input_file_name, delimiter=",", dtype=str)
                values = []

                for name_cluster in network_names:
                    values.append(
                        data[data[:, 2] == name_cluster, np.where(data[0, :] == variable)[0][0]].astype(np.float32)
                    )

                outputs_array.append(np.concatenate(values))

            try:
                outputs.append(np.stack(outputs_array))

            except Exception:
                for i in range(len(input_files)):
                    if len(outputs_array[i]) != len(outputs_array[0]):
                        print(
                            f"Error length does not match in simulation {i} it should be {len(outputs_array[0])}. "
                            f"However, the length is {len(outputs_array[i])}"
                        )

        output_networks.append(np.moveaxis(np.stack(outputs), 0, 1))

    save_processed_flowline_h5(output_source, output_networks)


def get_processed_network_json(base_output_source):
    network_file_name = os.path.join(base_output_source.uri, "network.json")
    with open(network_file_name, "r") as network_file:
        return json.load(network_file)


def download_raw_flowline_csvs(download_func, output_source, input_files):
    for input_file in input_files:
        download_func(input_file, output_source.uri)


def save_processed_flowline_h5(output_source, output_networks):
    output_file_name = os.path.join(output_source.uri, "flowline.h5")
    with h5py.File(output_file_name, "w") as output_file:
        for i in range(len(output_networks)):
            output_file.create_dataset(f"arr_{i}", data=output_networks[i])
