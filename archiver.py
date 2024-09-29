#!/usr/bin/env python3
"""archiver.py

Tiny Glade Daily Theme Archiver.

Usage:
  archiver.py -s [-f] [-O <outdir>] [-l <logfile>]

Args:
  -s --single             Download the current live daily theme.
  -f --force              Redownload the theme if it has already been downloaded.
  -O --outdir=<outdir>    Directory to save to [default: .]
  -l --logfile=<logfile>  Log file to record timestamps for downloaded files.
                          Records are stored as the CID followed by the start
                          time for the event (in UNIX tiemstamp format).
                          If the log file already exists, the record for the
                          new daily theme is appended to the end.
                          
"""

import sys
import tgdaily

def write_to_logfile(logfile, event):
    with open(logfile, "a") as f:
        f.write(f"{event.cid}\t{event.start}\n")

if __name__ == "__main__":
    from docopt import docopt
    args = docopt(__doc__)
    print(args)

    overwrite = ("--force" in args and args["--force"])

    if "--single" in args and args["--single"]:
        try:
            event = tgdaily.get_latest_daily_theme(outdir=args["--outdir"], overwrite=overwrite)
        except FileExistsError:
            print(f"Current daily theme already downloaded.")
            sys.exit(1)

        if "--logfile" in args and args["--logfile"]:
            write_to_logfile(args["--logfile"], event)
        sys.exit(0)
