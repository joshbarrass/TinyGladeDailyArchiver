#!/usr/bin/env python3
"""archiver.py

Tiny Glade Daily Theme Archiver.

Usage:
  archiver.py --single [-f] [-O <outdir>] [-l <logfile>]
  archiver.py --continuous [-O <outdir>] [-l <logfile>]

Args:
  -s --single             Download the current live daily theme.
  -f --force              Redownload the theme if it has already been downloaded.
  -O --outdir=<outdir>    Directory to save to [default: .]
  -l --logfile=<logfile>  Log file to record timestamps for downloaded files.
                          Records are stored as the CID followed by the start
                          time for the event (in UNIX tiemstamp format).
                          If the log file already exists, the record for the
                          new daily theme is appended to the end.
  -c --continuous         Keep running and downloading daily themes as they are
                          released. The program will download the event and wait
                          until after the reported end time before downloading
                          the next event.
                          The program does not run as a daemon, so ensure you
                          have some way of keeping the program alive in the
                          background.
"""

import os
import sys
import time
import datetime
import tgdaily

def write_to_logfile(logfile, event):
    with open(logfile, "a") as f:
        f.write(f"{event.cid}\t{event.start}\n")

def get_download_path(args, event):
    if event.path is None:
        return os.path.join(args["--outdir"], event.cid)
    return event.path

if __name__ == "__main__":
    from docopt import docopt
    args = docopt(__doc__)
##    print(args)

    overwrite = ("--force" in args and args["--force"])

    if "--single" in args and args["--single"]:
        try:
            event = tgdaily.download_latest_daily_theme(outdir=args["--outdir"], overwrite=overwrite)
        except FileExistsError:
            print(f"Current daily theme already downloaded.")
            sys.exit(1)

        if "--logfile" in args and args["--logfile"]:
            write_to_logfile(args["--logfile"], event)
        sys.exit(0)

    if "--continuous" in args and args["--continuous"]:
        try:
            while True:
                event = tgdaily.get_daily_theme_info()
                if not os.path.exists(get_download_path(args, event)):
                    try:
                        event.download(outdir=args["--outdir"], overwrite=False)
                        if "--logfile" in args and args["--logfile"]:
                            write_to_logfile(args["--logfile"], event)
                    except FileExistsError:
                        print("Current daily theme already downloaded. Ignoring...")
                else:
                    print("Current daily theme already downloaded. Ignoring...")

                end_time = event.end
                # wait until an hour after the end time for good measure
                wait_to = end_time + 60*60
                wait_to_dt = datetime.datetime.fromtimestamp(wait_to)
                print(f"Waiting until {wait_to_dt:%Y-%m-%d %H:%M:%S}...")   
                time.sleep(int(wait_to - time.time()))
        except KeyboardInterrupt:
            print("Exiting gracefully...")

