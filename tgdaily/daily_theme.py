import requests
from .checksum import verify_checksum
from .download import download_file

EVENTS_URL = "https://ryeland.pouncelight.games/v1/events"
BLOB_URL = "https://ryeland.pouncelight.games/v1/blob/{cid}"

class ChecksumError(Exception):
    pass

class DailyTheme:
    def __init__(self, path, cid, start, end):
        self.path = path
        self.cid = cid
        self.start = start
        self.end = end

def get_latest_daily_theme(outdir=None):
    r = requests.get(EVENTS_URL)
    r.raise_for_status()
    j = r.json()

    latest_start = 0
    latest_event = None
    for event in j["events"]:
        start = event["start"]
        if start > latest_start:
            latest_start = start
            latest_event = event

    cid = event["cid"]

    download_path = download_file(BLOB_URL.format(cid=cid),
                                  filename=f"{cid}.zip",
                                  outdir=outdir)

    if not verify_checksum(download_path):
        raise ChecksumError("bad checksum on downloaded save")

    return DailyTheme(download_path, cid, event["start"], event["end"])
