import pathlib
import shutil
import os
import sys
import dipor
from dipor.main import mainap

'''
MAIN FUNCTIONS -
    - quickstart (the default template)
    - bigbang (nothing is set just the src/content directories/settings)
    - use <github-src> (to use themes from github)
    - dipor dev [-PORT]
    - dipor build [-NOSERVE]
    - help (?)
'''

def get_src_root():
    return os.path.dirname(dipor.__file__)

def get_dst_root():
    return pathlib.Path().absolute()

def copy_quickstart_src():
    shutil.copytree(os.path.join(src_root, 'src'), os.path.join(dest_root, 'src'))

def copy_quickstart_content():
    shutil.copytree(os.path.join(src_root, 'content'), os.path.join(dest_root, 'content'))

def build_public():
    pass

def serve_public():
    pass

def quickstart():
    src_root = get_src_root()
    dst_root = get_dst_root()
    try:
        copy_quickstart_src()
    except:
        print("exception man")
    try:
        copy_quickstart_content()
    except:
        print("exception again man")
    try:
        build_public()
    except:
        print("fine ok")
    serve_public()

def bigbang():
    # create src
    # create content
    # create settings
    # create a hello dipor barren page
    # build to create single page
    pass

def use():
    # download the repo to current directory
    # build it serve it
    pass

def dev():
    # get the content
    # get the src
    # convert to public
    pass

def build():
    # clean the public folder
    # get the directories
    # convert to public
    # do post-processing (prettify/compress/make static easily available)
    # do an accessibility check
    # serve
    pass

def default_action():
    pass


# def main():
#     # src_root = pathlib.Path(__file__).parent.absolute()
#     dest_root = pathlib.Path().absolute()
#     src_root = os.path.dirname(dipor.__file__)
#     shutil.copytree(os.path.join(src_root, 'content'), os.path.join(dest_root, 'content'))
#     shutil.copytree(os.path.join(src_root, 'src'), os.path.join(dest_root, 'src'))
#     mainap()
def call_action(args):
    ARGS_ACTIONS_MAP = {'quickstart': quickstart,
                        'bigbang': bigbang,
                        'use': use_theme,
                        'dev': soft_build,
                        'build': hard_build}
    action = args[1]    # when only dipor is given, what should we do?
    action_fn = ARGS_ACTIONS_MAP.get(action, default_action)
    action_fn()


def main():
    args = sys.argv
    call_action(args[1:])