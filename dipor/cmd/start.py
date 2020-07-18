import pathlib
import shutil
import os
import sys
import dipor
from dipor.main import builder_main
from dipor.server import runserver

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
    '''
    Get the Root Directory for the Source
    '''
    return os.path.dirname(dipor.__file__)

def get_dst_root():
    '''
    Get the Root Directory for the Destination
    '''
    return pathlib.Path().absolute()

def copy_quickstart_settings(src_root, dst_root):
    '''
    Copy the Quickstart Settings to Destination Root
    !! does not give option when a file already exists !!
    '''
    try:
        shutil.copy(os.path.join(src_root, 'settings.py'), os.path.join(dst_root, 'settings.py'))
    except FileExistsError:
        override = input("Hey, looks like a `settings` file already exists, do you want to override the src directory (Y/n): ")
        if override in ["Y", "y", "", "yes"]:
            if os.path.exists(os.path.join(dst_root, 'settings.py')):
                os.remove(os.path.join(dst_root, 'settings.py'))
                copy_quickstart_settings(src_root, dst_root)
                print("The `settings` file was overriden.")
        elif override in ["n", "N", "no"]:
            pass
        else:
            override = input("The available options are: [Y/y/yes]/[N/n/no]. Press Enter to default to Y: ")
            if override in ["Y", "y", "yes", ""]:
                if os.path.exists(os.path.join(dst_root, 'settings.py')) and os.path.isdir(os.path.join(dst_root, 'settings.py')):
                    os.remove(os.path.join(dst_root, 'settings.py'))
                    copy_quickstart_settings(src_root, dst_root)
                    print("The `settings` file was overriden.")
            elif override in ["n", "N", "no"]:
                pass


def copy_quickstart_src(src_root, dst_root):
    '''
    Copy the Quickstart Source Directory to Destination Root
    '''
    try:
        shutil.copytree(os.path.join(src_root, 'src'), os.path.join(dst_root, 'src'))
    except FileExistsError:
        override = input("Hey, looks like a `src` directory already exists, do you want to override the src directory (Y/n): ")
        if override in ["Y", "y", "", "yes"]:
            if os.path.exists(os.path.join(dst_root, 'src')) and os.path.isdir(os.path.join(dst_root, 'src')):
                shutil.rmtree(os.path.join(dst_root, 'src'))
                copy_quickstart_src(src_root, dst_root)
                print("The `src` directory was overriden.")
        elif override in ["n", "N", "no"]:
            pass
        else:
            override = input("The available options are: [Y/y/yes]/[N/n/no]. Press Enter to default to Y: ")
            if override in ["Y", "y", "yes", ""]:
                if os.path.exists(os.path.join(dst_root, 'src')) and os.path.isdir(os.path.join(dst_root, 'src')):
                    shutil.rmtree(os.path.join(dst_root, 'src'))
                    copy_quickstart_src(src_root, dst_root)
                    print("The `src` directory was overriden.")
            elif override in ["n", "N", "no"]:
                pass

def copy_quickstart_content(src_root, dst_root):
    '''
    Copy the Quickstart Content Directory to Destination Root
    '''
    try:
        shutil.copytree(os.path.join(src_root, 'content'), os.path.join(dst_root, 'content'))
    except FileExistsError:
        override = input("Hey, looks like a `content` directory already exists, do you want to override the src directory (Y/n): ")
        if override in ["Y", "y", "yes", ""]:
            if os.path.exists(os.path.join(dst_root, 'content')) and os.path.isdir(os.path.join(dst_root, 'content')):
                shutil.rmtree(os.path.join(dst_root, 'content'))
                copy_quickstart_content(src_root, dst_root)
                print("The `content` directory was overriden.")
        elif override in ["n", "N", "no"]:
            pass
        else:
            override = input("The available options are: [Y/y/yes]/[N/n/no]. Press Enter to default to Y: ")
            if override in ["Y", "y", "yes", ""]:
                if os.path.exists(os.path.join(dst_root, 'content')) and os.path.isdir(os.path.join(dst_root, 'content')):
                    shutil.rmtree(os.path.join(dst_root, 'content'))
                    copy_quickstart_content(src_root, dst_root)
                    print("The `content` directory was overriden.")
            elif override in ["n", "N", "no"]:
                pass

def build_public(src_path, content_path):
    '''
    Assumes that /src and /content already exist
    In the Destination Directory
    And Builds the Public Directory
    '''
    builder_main(src_path, content_path)

def serve_public(public_path):
    runserver(public_path)

def quickstart(*args, **kwargs):
    print ("running quikcstart")
    src_root = get_src_root()
    dst_root = get_dst_root()
    print("Getting the /src directory...")
    copy_quickstart_src(src_root, dst_root)
    print("Getting the /content directory...")
    copy_quickstart_content(src_root, dst_root)
    print("Getting the settings file...")
    copy_quickstart_settings(src_root, dst_root)
    print("Building the /public repo")
    build_public(os.path.join(dst_root, 'src'), os.path.join(dst_root, 'content'))
    serve_public(os.path.join(dst_root, 'public'))

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