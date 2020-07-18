import markdown
from jinja2 import PackageLoader, FileSystemLoader
from os import listdir
import os
import pathlib
from dipor import settings
from pathlib import Path

from dipor.readers.markdown import MarkdownReader
from dipor.utils.context import get_structural_context
from dipor.jinja_changes import RelEnvironment, SilentUndefined
from dipor.jinja.extensions import RoutesExtension

RESERVED_PATHS = ['_components', '_assets', '_branches']


STRUCTURAL_CTX = get_structural_context(settings.CONTENT_ROOT)

def get_current_context(dir_path):
    extensions_tuple = ('.md', '.json')
    md_files_for_app = []
    current_ctx = {}
    for file in listdir(dir_path):
        if file.endswith(extensions_tuple):
            min_file_name = file.strip().lower().split(".")[0]
            current_ctx[min_file_name] = {}
            md_obj = MarkdownReader(os.path.join(dir_path, file))
            current_ctx[min_file_name] = md_obj.get_context()
    return current_ctx   
    

def load_template(tpl_path):
    print(Path(os.path.dirname(tpl_path)).parent))
    env = RelEnvironment(loader=FileSystemLoader(searchpath=Path(os.path.dirname(tpl_path)).parent), undefined=SilentUndefined, extensions=[RoutesExtension])
    env.globals.update(zip=zip)
    template =  env.get_template(tpl_path)
    return template

def get_templates_for_app(appname):
    templates_app_path = 'src/'+appname
    app_templates = []
    for file in listdir(templates_app_path):
        if file.endswith(('.tpl', '.html')):
            app_templates.append(file)

    return app_templates


def get_subapps(current_path):
    subapps = []
    for file in os.listdir(current_path):
        if os.path.isdir(os.path.join(current_path, file)) and not file.startswith("_"):
            subapps.append(file)

    return subapps


def get_content_branch_dirs(current_app_path):
    branch_dirs = []
    current_content_path = 'content' + current_app_path[3:]
    for file in os.listdir(current_content_path):
        if os.path.isdir(os.path.join(current_content_path, file)):
            branch_dirs.append(os.path.join(current_content_path, file))
        
    return branch_dirs


def get_total_context(initial_context, current_context):
    global STRUCTURAL_CTX
    current_common_ctx = {'common': {}}
    if initial_context.get('common'):
        current_common_ctx['common'].update(initial_context['common'])
    if current_context.get('common'):
        current_common_ctx['common'].update(current_context['common'])
    total_ctx = {}
    total_ctx.update(initial_context)
    total_ctx.update(current_context)
    total_ctx.update(current_common_ctx)
    total_ctx['_routes'] = STRUCTURAL_CTX   

    return total_ctx


def builder(current_app_path, current_content_path, initial_context={'common': {}}, is_branch=False):
    if is_branch:
        content_branch_dirs = get_content_branch_dirs(current_app_path)
        for dir_path in content_branch_dirs:
            current_context = get_current_context(dir_path)
            total_ctx = get_total_context(initial_context, current_context)

            main_template = os.path.join(current_app_path, 'index.html')
            if os.path.isfile(main_template):
                loaded_tpl = load_template(main_template)
                current_sub_path = current_app_path[3:].strip("/")
                current_sub_path = current_sub_path.replace("_branches", "").strip("/")
                res_dir = os.path.join('public', current_sub_path)
                pathlib.Path(res_dir).mkdir(parents=True, exist_ok=True) 
                file_name = os.path.basename(dir_path)
                loaded_tpl.stream(**total_ctx).dump(os.path.join(res_dir, f"{file_name}.html"))
                print(f"rendered file..................{res_dir}/{file_name}.html")

    else:
        current_context = get_current_context(current_content_path)
        total_ctx = get_total_context(initial_context, current_context)

        main_template = os.path.join(current_app_path, 'index.html')
        if os.path.isfile(main_template):
            loaded_tpl = load_template(main_template)
            current_sub_path = current_app_path[3:].strip("/")
            res_dir = os.path.join('public', current_sub_path)
            pathlib.Path(res_dir).mkdir(parents=True, exist_ok=True) 
            loaded_tpl.stream(**total_ctx).dump(os.path.join(res_dir, 'index.html'))
            print(f"rendered file..................{res_dir}/index.html")

    
    if is_branch:
        return # do not look for further dirs
    # process branches & subapps
    if os.path.isdir(os.path.join(current_app_path, '_branches')):
        next_src_path = os.path.join(current_app_path, '_branches')
        next_context = {'common': total_ctx['common']}
        next_content_path = os.path.join(current_content_path, '_branches')
        main(next_src_path, '_branches', next_content_path, initial_context=next_context, is_branch=True)

    subapps = get_subapps(current_app_path)
    if subapps:
        for subapp in subapps:
            next_src_path = os.path.join(current_app_path, subapp)
            next_context = {'common': total_ctx['common']}
            next_content_path = os.path.join(current_content_path, subapp)
            main(next_src_path, subapp, next_content_path, initial_context=next_context)

    return
