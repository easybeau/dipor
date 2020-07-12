import pathlib
import shutil
import os
import dipor

def main():
    # src_root = pathlib.Path(__file__).parent.absolute()
    dest_root = pathlib.Path().absolute()
    src_root = os.path.dirname(dipor.__file__)
    print(os.path.join(src_root, 'src'))
    print(dest_root)
    shutil.copytree(os.path.join(src_root, 'src'), dest_root)