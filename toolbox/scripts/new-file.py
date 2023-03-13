import os
import sys

path = sys.argv[1]

if not os.path.exists(path):
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)
    with open(path, 'w') as f:
        print(f'Created file: {path}')
    exit(0)
else:
    print(f'{path} already exists.')
    exit(1)