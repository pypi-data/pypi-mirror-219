from pathlib import Path

import h5py
import numpy as np

from preprocessing.facilities.network import preprocess as preprocess_network

VARIABLES = [
    "VolumeFlowrateOilStockTank",
    "VolumeFlowrateLiquidStockTank",
    "Pressure",
    "Watercut",
    "VolumeFlowrateOilInSitu",
    "VolumeFlowrateLiquidInSitu",
]


def preprocess(download_func, output_source, input_files, **_):
    network_file_name = input_files[0]  # network.csv
    input_file_names = input_files[1:]  # (cases/{group}/SIMULATION_{case}/flowline.csv, ...)
    output_sub_directory = Path(input_file_names[0]).parents[1]  # cases/{group}  # noqa

    network = preprocess_network(download_func, output_source, network_file_name, save=False)

    download_raw_flowline_csvs(download_func, output_source, input_file_names)

    output_networks = []
    for n in range(len(network)):
        network_names = network[list(network.keys())[n]]["branches"]
        outputs = []

        for variable in VARIABLES:
            outputs_array = []

            for input_file in input_file_names:
                input_file_name = Path(output_source.uri) / input_file
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
                for i in range(len(input_file_names)):
                    if len(outputs_array[i]) != len(outputs_array[0]):
                        print(
                            f"Error length does not match in simulation {i} it should be {len(outputs_array[0])}. "
                            f"However, the length is {len(outputs_array[i])}"
                        )

        output_networks.append(np.moveaxis(np.stack(outputs), 0, 1))

    save_processed_flowline_h5(output_source, output_sub_directory, output_networks)

    return output_networks


def download_raw_flowline_csvs(download_func, output_source, input_files):
    for input_file in input_files:
        download_func(input_file, output_source.uri)


def save_processed_flowline_h5(output_source, output_directory, output_networks):
    output_file_name = Path(output_source.uri) / output_directory / "flowline.h5"
    with h5py.File(output_file_name, "w") as output_file:
        for i in range(len(output_networks)):
            output_file.create_dataset(f"network_{i}", data=output_networks[i])
