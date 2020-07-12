import pathlib
import shutil
import os
import dipor

def main():
    # src_root = pathlib.Path(__file__).parent.absolute()
    dest_root = pathlib.Path().absolute()
    src_root = os.path.dirname(dipor.__file__)
    shutil.copytree(os.path.join(src_root, 'content'), os.path.join(dest_root, 'content'))
    shutil.copytree(os.path.join(src_root, 'content'), os.path.join(dest_root, 'content'))
    dipor.main.mainap()