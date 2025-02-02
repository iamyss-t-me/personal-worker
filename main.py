import aria2p

def download_torrent(torrent_file_or_magnet_link, output_directory=None):
    """
    Downloads a torrent file or magnet link using aria2p.

    :param torrent_file_or_magnet_link: Path to the torrent file or magnet link.
    :param output_directory: Directory where the downloaded files will be saved.
    """
    try:
        # Initialize aria2p
        aria2 = aria2p.API(
            aria2p.Client(
                host="http://localhost",
                port=6800,
                secret=""
            )
        )

        # Add the torrent or magnet link
        download = aria2.add(torrent_file_or_magnet_link, options={"dir": output_directory} if output_directory else None)

        # Monitor the download progress
        while not download[0].is_complete:
            print(f"Downloading: {download[0].name} - {download[0].progress_string()}")
            download[0].update()

        print(f"Download completed: {download[0].name}")

    except Exception as e:
        # Handle errors
        print(f"Error occurred while downloading: {e}")

# Example usage
if __name__ == "__main__":
    # Replace with your torrent file path or magnet link
    magnet = input("Enter magnet link: ")

    # Optional: Specify the output directory
    output_directory = "/magnet"

    # Download the torrent
    download_torrent(magnet, output_directory)