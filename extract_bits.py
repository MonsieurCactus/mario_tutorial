import zipfile
import numpy as np

def extract_bits(filename):
    if zipfile.is_zipfile(filename):
        zp = zipfile.ZipFile(filename)
        raw_buffer = zp.read(zp.filelist[0])
        bytes = np.frombuffer(raw_buffer, dtype=np.uint8)
    else:
        bytes = np.fromfile(filename, dtype=np.uint8)
    return np.unpackbits(bytes)

if __name__ == "__main__":
	print len(extract_bits( "smb.nes" ))
