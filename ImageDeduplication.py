from os import listdir, path, remove
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor as TPE
from PIL import Image

class DuplicateKeyError(Exception): pass

class SingleSet(set):
    def add(self, value):
        if value in self:
            raise DuplicateKeyError()
        super().add(value)

SUFFIXES = ['.JPEG', '.JPG', '.PNG', '.BMP']
directory = input('Enter Directory: ').strip()

if path.isdir(directory):
    # Time Stamp Start (Process Duration)
    pStart = datetime.now().timestamp()

    globals()['hashes'] = SingleSet()
	
    img_files = [x for x in listdir(directory) if Path(x).suffix.upper() in SUFFIXES]
    print(f'Found {len(img_files)} Images')

    def deduplicate(r_file):
        r_path = path.join(directory, r_file)
        _hash = hash(frozenset(Image.open(r_path).getdata()))
        try:
            globals()['hashes'].add(_hash)
        except DuplicateKeyError:
            print(f'{r_path} Removed')
            remove(r_path)
            
    with TPE(max_workers=1024) as executor:
        executor.map(deduplicate, img_files)

    # Time Stamp End (Process Duration)
    pEnd = datetime.now().timestamp()

    print(f'Finished, Duration: {pEnd - pStart} Seconds')
else:
    print(f'Invalid Directory: {directory}')
