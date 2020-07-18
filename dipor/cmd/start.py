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

def quickstart(*args, **kwargs):
    print ("running quikcstart")
    src_root = get_src_root()
    dst_root = get_dst_root()
    copy_quickstart_src()
    copy_quickstart_content()
    try:
        build_public()
    except:
        print("fine ok")
    serve_public()

def bigbang(*args, **kwargs):
    print("running bigbang")
    # create src
    # create content
    # create settings
    # create a hello dipor barren page
    # build to create single page

def use(*args, **kwargs):
    print("running use")
    # download the repo to current directory
    # build it serve it

def soft_build(*args, **kwargs):
    print("running dev")
    # get the content
    # get the src
    # convert to public

def hard_build(*args, **kwargs):
    print("running build")
    # clean the public folder
    # get the directories
    # convert to public
    # do post-processing (prettify/compress/make static easily available)
    # do an accessibility check
    # serve

def default_action(*args, **kwargs):
    print("running default action")

def use_theme(*args, **kwargs):
    print("running use theme")

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
    action = args[0]    # when only dipor is given, what should we do?
    action_fn = ARGS_ACTIONS_MAP.get(action, default_action)
    action_fn(args[1:])


def main():
    args = sys.argv
    call_action(args[1:])