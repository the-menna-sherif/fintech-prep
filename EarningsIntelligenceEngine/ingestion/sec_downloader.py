from sec_edgar_downloader import Downloader
import pathlib


# directing downloads into data/raw/ -- separate from processed data & code
RAW_DIR = pathlib.Path(__file__).parent.parent / "data" / "raw"

# define downloder function
def download_sec_filings(ticker: str, filing_type: str, count: int = 10):
    downloader = Downloader("menmen_fintech_prep", "mennaseducation@gmail.com")

    downloader.get(ticker, filing_type, count, output_dir=RAW_DIR)

    print(f"Downloaded {count} {filing_type} filings for {ticker} → {RAW_DIR}")


if __name__ == "__main__":
    # example usage
    download_sec_filings("AAPL", "10-K", count=5)