#!/usr/bin/env python3
"""archiver.py

Tiny Glade Daily Theme Archiver.

Usage:
  archiver.py [-O <outdir>] -s

Args:
  -s --single           Download the current live daily theme.
  -O --outdir=<outdir>  Directory to save to [default: .]
"""

import sys
import tgdaily

if __name__ == "__main__":
    from docopt import docopt
    args = docopt(__doc__)
    print(args)

    if "--single" in args and args["--single"]:
        tgdaily.get_latest_daily_theme(outdir=args["--outdir"])
        sys.exit(0)
