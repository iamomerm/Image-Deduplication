import os
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

SUFFIXES = ['.JPEG','.JPG','.PNG','.BMP']
directory = input('Enter Directory: ').strip()

if os.path.isdir(directory):
    #Time Stamp Start (Process Duration)
    pStart = datetime.now().timestamp()
	
    img_files = [x for x in os.listdir(directory) if Path(x).suffix.upper() in SUFFIXES]
    print(f'Found {len(img_files)} Images')

    globals()['hashes'] = SingleSet()
    globals()['removed'] = set()

    def deduplicate(r_file):
        r_path = os.path.join(directory, r_file)
        _hash = hash(frozenset(Image.open(r_path).getdata()))
        try:
            globals()['hashes'].add(_hash)
        except DuplicateKeyError:
            globals()['removed'].add(r_file)
            os.remove(r_path)
            
    with TPE(max_workers=1024) as executor:
        executor.map(deduplicate, img_files)

    #Time Stamp End (Process Duration)
    pEnd = datetime.now().timestamp()

    print('Removed:')
    [print(f'{idx}. x{x}') for idx, x in enumerate(globals()['removed'])]
    print(f'Duration: {pEnd - pStart} Seconds')
    print('Finished...')
else:
    print(f'Invalid Directory: {directory}')
