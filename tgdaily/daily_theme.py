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

    def download(self, outdir=None, overwrite=False):
        cid = self.cid
        download_path = download_file(BLOB_URL.format(cid=cid),
                                      filename=f"{cid}",
                                      outdir=outdir,
                                      overwrite=overwrite)
        if not verify_checksum(download_path):
            raise ChecksumError("bad checksum on downloaded save")
        self.path = download_path

def get_daily_theme_info():
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

    return DailyTheme(None, event["cid"], event["start"], event["end"])

def download_latest_daily_theme(outdir=None, overwrite=False):
    event = get_daily_theme_info()
    event.download(outdir=outdir, overwrite=overwrite)
    return event
