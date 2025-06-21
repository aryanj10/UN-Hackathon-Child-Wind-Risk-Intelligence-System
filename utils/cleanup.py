import os

def cleanup_files(files):
    for f in files:
        if os.path.exists(f):
            os.remove(f)
