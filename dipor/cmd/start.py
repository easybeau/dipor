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
class EntryPointCommands:

    def __init__(self, args):
        self.ARGS_ACTIONS_MAP = {'quickstart': self.quickstart,
                        'bigbang': self.bigbang,
                        'use': self.use_theme,
                        'dev': self.soft_build,
                        'build': self.hard_build}

        self.src_root = self.get_src_root
        self.dst_root = self.get_dst_root

        self.action = args[1]
        self.ac_parameters = args[2:]

        self.call_action(self.action, self.ac_parameters)
        

    def call_action(self, action, ac_parameters):
        action_fn = self.ARGS_ACTIONS_MAP.get(action, self.default_action)
        action_fn(ac_parameters)


    @property
    def get_src_root(self):
        return os.path.dirname(dipor.__file__)

    @property
    def get_dst_root(self):
        return pathlib.Path().absolute()

    
    def copy_file(self, src, dst, file):
        '''
        is buggy!
        '''
        try:
            shutil.copy(os.path.join(src, file), os.path.join(dst, file))
        except FileExistsError:
            override = input("Hey, looks like a `settings` file already exists, do you want to override the src directory (Y/n): ")
            if override in ["Y", "y", "", "yes"]:
                if os.path.exists(os.path.join(dst, file)):
                    os.remove(os.path.join(dst, file))
                    copy_quickstart_settings(src, dst)
                    print("The `settings` file was overriden.")
            elif override in ["n", "N", "no"]:
                pass
            else:
                override = input("The available options are: [Y/y/yes]/[N/n/no]. Press Enter to default to Y: ")
                if override in ["Y", "y", "yes", ""]:
                    if os.path.exists(os.path.join(dst, file)) and os.path.isdir(os.path.join(dst, file)):
                        os.remove(os.path.join(dst, file))
                        copy_quickstart_settings(src, dst)
                        print("The `settings` file was overriden.")
                elif override in ["n", "N", "no"]:
                    pass

    def copy_tree(self, src, dst, dir):
        try:
            shutil.copytree(os.path.join(src, dir), os.path.join(dst, dir))
        except FileExistsError:
            override = input(f"Hey, looks like a `{dir}` directory already exists, do you want to override the src directory (Y/n): ")
            if override in ["Y", "y", "", "yes"]:
                if os.path.exists(os.path.join(dst, dir)) and os.path.isdir(os.path.join(dst, dir)):
                    shutil.rmtree(os.path.join(dst, dir))
                    copy_tree(src, dst)
                    print(f"The `{dir}` directory was overriden.")
            elif override in ["n", "N", "no"]:
                pass
            else:
                override = input("The available options are: [Y/y/yes]/[N/n/no]. Press Enter to default to Y: ")
                if override in ["Y", "y", "yes", ""]:
                    if os.path.exists(os.path.join(dst, dir)) and os.path.isdir(os.path.join(dst, dir)):
                        shutil.rmtree(os.path.join(dst, dir))
                        copy_tree(src, dst)
                        print(f"The `{dir}` directory was overriden.")
                elif override in ["n", "N", "no"]:
                    pass
 
    def quickstart(self, *args, **kwargs):
        print ("running quikcstart")
        print("Getting the /src directory...")
        self.copy_tree(self.src_root, self.dst_root, 'src')
        print("Getting the /content directory...")
        self.copy_tree(self.src_root, self.dst_root, 'content')
        print("Getting the settings file...")
        self.copy_file(self.src_root, self.dst_root, "settings.py")
        print("Building the /public repo")
        self.build_public(os.path.join(self.dst_root, 'src'), os.path.join(self.dst_root, 'content'))
        self.serve_public()

    def bigbang(self, *args, **kwargs):
        print("running bigbang")
        # create src
        # create content
        # create settings
        # create a hello dipor barren page
        # build to create single page


    def soft_build(self, *args, **kwargs):
        print("running dev")
        # get the content
        # get the src
        # convert to public

    def hard_build(self, *args, **kwargs):
        print("running build")
        # clean the public folder
        # get the directories
        # convert to public
        # do post-processing (prettify/compress/make static easily available)
        # do an accessibility check
        # serve

    def default_action(self, *args, **kwargs):
        print("running default action")

    def use_theme(self, *args, **kwargs):
        print("running use theme")

    def build_public(self, src_path, content_path):
        '''
        !! actually, call hard_build for this? !!
        -- oh yes, yet to figure out build process --
        Assumes that /src and /content already exist
        In the Destination Directory
        And Builds the Public Directory
        '''
        builder_main(src_path, content_path)

    def serve_public(self):
        runserver()

def main():
    '''
    Entry Point for all Commands
    '''
    args = sys.argv
    cmd_execution = EntryPointCommands(args)
