import argparse
from .models import download

def main():
    parser = argparse.ArgumentParser(description="Command line tool")
    subparsers = parser.add_subparsers(dest="command")

    # Create a subparser for the "download" command
    download_parser = subparsers.add_parser("download", help="Download command")
    download_parser.add_argument("--model", help="Specify model to download")
    download_parser.add_argument('--overwrite', action='store_true', default=False, help="Will overwrite if model already exists")


    args = parser.parse_args()

    # Call the appropriate function based on the provided command
    if args.command == "download":
        download(args.model, overwrite=args.overwrite)

if __name__ == "__main__":
    main()