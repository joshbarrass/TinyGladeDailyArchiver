import os
import requests

# source: https://stackoverflow.com/a/16696317
# CC BY-SA 4.0 Roman Podlinov
def download_file(url, filename=None, outdir=None):
    if filename is None:
        filename = url.split('/')[-1]
    if outdir is not None:
        if filename != os.path.basename(filename):
            raise ValueError("filename contains a directory")
        filename = os.path.join(outdir, filename)

    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)

    return filename
