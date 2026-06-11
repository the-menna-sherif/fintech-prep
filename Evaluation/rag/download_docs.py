import requests
from pathlib import Path

# passing URLs for key docs from FATF, BIS, and FinCEN to download and save in corpus/ directory for ingestion later
# choosing to pass urls directly here for simplicity and reliability
# total docs: 3 (all pdf)

BIS_DOCS = [
    # Basel III framework
    "https://www.bis.org/publ/bcbs189.pdf",
    # Core principles for effective banking supervision
    "https://www.bis.org/publ/bcbs230.pdf",
    # Guidelines on AML/CFT
    "https://www.bis.org/publ/bcbs235.pdf",
]

def download_bis(output_dir="corpus/"):
    print("Downloading BIS docs...")
    Path(output_dir).mkdir(exist_ok=True)
    for url in BIS_DOCS:
        filename = url.split("/")[-1]
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            Path(f"{output_dir}/{filename}").write_bytes(r.content)
            print(f"Downloaded: {filename}")            


def download_all():
    download_bis()
    docs_downloaded = len(BIS_DOCS)
    print("num of docs: ", docs_downloaded)
    print("Done. Run ingest.py next.")

if __name__ == "__main__":
    download_all()