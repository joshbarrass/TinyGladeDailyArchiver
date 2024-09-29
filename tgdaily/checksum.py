import os

try:
    from blake3 import blake3
    BLAKE3_AVAILABLE = True
except:
    import warnings
    warnings.warn("blake3 is not available. Verifying checksums will not be possible.", RuntimeWarning)
    BLAKE3_AVAILABLE = False

def verify_checksum(file, hash=None, chunksize=8192):
    if not BLAKE3_AVAILABLE:
        return True
    
    if hash is None:
        hash = os.path.splitext(os.path.basename(file))[0]

    if len(hash) != 64:
        raise ValueError("hash should be 256-bit hex digest (64 chars)")

    hasher = blake3()
    with open(file, "rb") as f:
        data = f.read(chunksize)
        while len(data) > 0:
            hasher.update(data)
            data = f.read(chunksize)

    calculated_hash = hasher.hexdigest()

    return hash == calculated_hash
