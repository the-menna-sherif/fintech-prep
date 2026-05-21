from sec_edgar_downloader import Downloader
import pathlib
import os
from dotenv import load_dotenv

# This looks for a .env file in the current directory and loads it
load_dotenv()

# directing downloads into data/raw/ -- separate from processed data & code
RAW_DIR = pathlib.Path(__file__).parent.parent / "data" / "raw"

# define downloder function
def download_sec_filings(ticker: str, filing_type: str, count: int = 2):
    # initialize the downloader with credentials from environment variables
    # credentials are required by the SEC to track usage and prevent abuse of their API (my creds just identify me as a researcher)
    downloader = Downloader(os.getenv("COMPANY_NAME"), os.getenv("USER_EMAIL"))

    downloader.get(ticker, filing_type, count, output_dir=RAW_DIR)

    print(f"Downloaded {count} {filing_type} filings for {ticker} → {RAW_DIR}")


if __name__ == "__main__":
    # example usage
    download_sec_filings("AAPL", "10-K", count=2)