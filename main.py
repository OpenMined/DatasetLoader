import os
import json
import time
from syftbox.lib import Client, SyftPermission
from pathlib import Path


def gather_file_information(directory_path):
    """
    Gathers information about files in a given directory.

    Parameters:
        directory_path (str): The path of the directory to inspect.

    Returns:
        dict: A dictionary where each key is a filename and each value is
              a dictionary containing the file's size and creation time.
    """
    files_info = {}

    files = [str(file) for file in Path(directory_path).rglob('*') if file.is_file()]
    
    # Iterate over all items in the given directory
    for item_path in files:
        # Check if the item is a file
        if os.path.isfile(item_path) and "syftperm" not in item_path:
            # Gather file information
            file_size = os.path.getsize(item_path)
            creation_time = os.path.getctime(item_path)

            # Convert timestamp to a human-readable format
            # If you prefer the raw timestamp, you can skip this step.
            creation_date_str = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(creation_time)
            )

            file_size = round(file_size / 1024, 2)
            item_name = item_path.split("/")[-1]
            # Add the file info to the dictionary
            files_info[item_name] = {"size": file_size, "created": creation_date_str}
    
    print(files_info)
    return files_info


def save_to_json(data, output_path):
    """
    Saves the given data as a JSON file to the specified path.

    Parameters:
        data (dict): The data to be saved as JSON.
        output_path (str): The path where the JSON file will be saved.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_app_private_data(client: Client) -> Path:
    """
    Returns the private data directory of the app
    """
    return client.workspace.data_dir / "private" 


def main():
    client = Client.load()

    # Create the data loader private folder
    dataset_private_folder = get_app_private_data(client)
    os.makedirs(dataset_private_folder, exist_ok=True)

    data_loader = client.api_data("data_loader")

    # Set permissions for the api_data/data_loader to be visible to everyone
    permissions = SyftPermission.datasite_default(email=client.email)
    permissions.read.append("GLOBAL")
    permissions.save(data_loader)

    output_path = data_loader / "datasets.json"

    file_data = gather_file_information(dataset_private_folder)
    final_data = {"datasets": file_data, "owner": client.email}
    save_to_json(final_data, output_path)
    print(f"File information has been saved to {output_path}")


if __name__ == "__main__":
    main()
