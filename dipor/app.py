import markdown
from jinja2 import Environment, PackageLoader, Undefined, FileSystemLoader
from os import listdir
import os
import pathlib

RESERVED_PATHS = ['_components', '_assets', '_branches']

class SilentUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return ''


class RelEnvironment(Environment):
    """Override join_path() to enable relative template paths."""
    def join_path(self, template, parent):
        return os.path.join(os.path.dirname(parent), template)


def get_files_for_app(appname, extensions_list):
    extensions_tuple = tuple(extensions_list)
    app_path = 'content/'+appname
    allowed_files_for_app = []
    has_subapps = False
    for file in listdir(app_path):
        if os.path.isdir(app_path+"/"+file):
            has_subapps = True
        elif file.endswith(extensions_tuple):
            allowed_files_for_app.append(file)

    return allowed_files_for_app, has_subapps


def get_current_context(current_app_path):
    extensions_tuple = ('.md', '.json')
    md_files_for_app = []
    current_ctx = {}
    # current app path starts w/ src, make it content
    current_content_path = 'content' + current_app_path[3:]
    md = markdown.Markdown(extensions=['meta'])
    for file in listdir(current_content_path):
        if file.endswith(extensions_tuple):
            min_file_name = file.strip().lower().split(".")[0]
            current_ctx[min_file_name] = {}
            with open(os.path.join(current_content_path, file), "r", encoding="utf-8") as f:
                md_content = f.read()
            current_ctx[min_file_name]['content'] = md.convert(md_content)
            if not current_ctx[min_file_name]['content']:
                del current_ctx[min_file_name]['content']
            meta = {}
            meta = md.Meta
            for k, v in meta.items():
                if len(v) == 1:
                    meta[k] = v[0]
            current_ctx[min_file_name].update(meta)
    return current_ctx
            
def get_current_branch_context(dir_path):
    extensions_tuple = ('.md', '.json')
    md_files_for_app = []
    current_ctx = {}
    # current app path starts w/ src, make it content
    # current_content_path = 'content' + current_app_path[3:]
    md = markdown.Markdown(extensions=['meta'])
    for file in listdir(dir_path):
        if file.endswith(extensions_tuple):
            min_file_name = file.strip().lower().split(".")[0]
            current_ctx[min_file_name] = {}
            with open(os.path.join(dir_path, file), "r", encoding="utf-8") as f:
                md_content = f.read()
            current_ctx[min_file_name]['content'] = md.convert(md_content)
            if not current_ctx[min_file_name]['content']:
                del current_ctx[min_file_name]['content']
            meta = {}
            meta = md.Meta
            for k, v in meta.items():
                if len(v) == 1:
                    meta[k] = v[0]
            current_ctx[min_file_name].update(meta)
    return current_ctx
    


def get_common_context(appname, common_content_files):
    # only works for md files currently
    file_root = 'content/'+appname
    context = {}

    md = markdown.Markdown(extensions=['meta'])
    # meta = {}
    for file in common_content_files:
        min_file_name = file.strip().lower().split(".")[0]
        context[min_file_name] = {}
        with open(file_root+"/"+file, "r", encoding='utf-8') as f:
            md_content = f.read()
        context[min_file_name]['content'] = md.convert(md_content)
        meta = {}
        meta = md.Meta
        for k, v in meta.items():
            if len(v) == 1:
                meta[k] = v[0]
        context[min_file_name].update(meta)

    return context

def get_subapps(appname):
    subapps = []
    app_path = 'content/'+appname
    for file in listdir(app_path):
        if os.path.isdir(app_path+"/"+file):
            subapps.append(file)

    return subapps


# def load_template(tpl, appname):
#     template_path = 'src/'+appname
#     # templates = []
#     env = Environment(loader=PackageLoader('src', appname), undefined=SilentUndefined)
#     env.globals.update(zip=zip)
#     template =  env.get_template(tpl)
#     return template
    

def load_template(tpl_path):
    # template_path = 'src/'+appname
    # templates = []
    tpl_path = tpl_path[3:]
    env = RelEnvironment(loader=FileSystemLoader('src'), undefined=SilentUndefined)
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


def generate_static_site_for_app(appname, allowed_extensions):
    files_for_app, has_subapps = get_files_for_app(appname, allowed_extensions)
    templates_for_app = get_templates_for_app(appname)
    common_context = get_common_context(appname, files_for_app)
    loaded_templates = []
    for tpl in templates_for_app:
        loaded_templates.append((load_template(tpl, appname), tpl))

    if has_subapps:
        subapps = get_subapps(appname)
        for subapp in subapps:
            files_for_app, _ = get_files_for_app(appname+"/"+subapp, allowed_extensions)
            extra_context = get_common_context(appname+"/"+subapp, files_for_app)

            final_context = {}
            final_context.update(common_context)
            final_context.update(extra_context)

            for loaded_tpl in loaded_templates:
                pathlib.Path('public/'+subapp+"/").mkdir(parents=True, exist_ok=True) 
                loaded_tpl[0].stream(**final_context).dump('public/'+subapp+"/"+loaded_tpl[1])


def get_project_apps(root_path):
    app_list = []
    for file in listdir(root_path):
        if os.path.isdir(root_path+file) and not file.startswith('_'):
            app_list.append(file)
    
    return app_list

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



def main(current_app_path, current_app_name, initial_context={'common': {}}, is_branch=False):
    current_app_name = current_app_name.strip("/")
    print("current path.........", current_app_path)

    if is_branch:
        content_branch_dirs = get_content_branch_dirs(current_app_path)
        for dir_path in content_branch_dirs:
            current_branch_context = get_current_branch_context(dir_path)

            current_common_ctx = {'common': {}}
            if initial_context.get('common'):
                current_common_ctx['common'].update(initial_context['common'])
            if current_branch_context.get('common'):
                current_common_ctx['common'].update(current_branch_context['common'])
            total_ctx = {}
            total_ctx.update(initial_context)
            total_ctx.update(current_branch_context)
            total_ctx.update(current_common_ctx)
            # total_ctx = initial_context.update(current_ctx).update(current_common_ctx)

            main_template = os.path.join(current_app_path, 'index.html')
            if os.path.isfile(main_template):
                loaded_tpl = load_template(main_template)
                current_sub_path = current_app_path[3:].strip("/")
                res_dir = os.path.join('public', current_sub_path)
                pathlib.Path(res_dir).mkdir(parents=True, exist_ok=True) 
                file_name = os.path.basename(dir_path)
                loaded_tpl.stream(**total_ctx).dump(os.path.join(res_dir, f"{file_name}.html"))
                print(f"written to file CUSTOM......{res_dir}/{file_name}.html")

    else:
        current_ctx = get_current_context(current_app_path) #nitially src/

        current_common_ctx = {'common': {}}
        if initial_context.get('common'):
            current_common_ctx['common'].update(initial_context['common'])
        if current_ctx.get('common'):
            current_common_ctx['common'].update(current_ctx['common'])
        total_ctx = {}
        total_ctx.update(initial_context)
        total_ctx.update(current_ctx)
        total_ctx.update(current_common_ctx)
        # total_ctx = initial_context.update(current_ctx).update(current_common_ctx)

        main_template = os.path.join(current_app_path, 'index.html')
        if os.path.isfile(main_template):
            loaded_tpl = load_template(main_template)
            current_sub_path = current_app_path[3:].strip("/")
            res_dir = os.path.join('public', current_sub_path)
            pathlib.Path(res_dir).mkdir(parents=True, exist_ok=True) 
            print(total_ctx)
            loaded_tpl.stream(**total_ctx).dump(os.path.join(res_dir, 'index.html'))
            print(f"written to file......{res_dir}/index.html")

    
    if is_branch:
        return # do not look for further dirs
    # process branches & subapps
    print("trying branch...", os.path.join(current_app_path, '_branches'))
    if os.path.isdir(os.path.join(current_app_path, '_branches')):
        next_path = os.path.join(current_app_path, '_branches')
        next_context = {'common': total_ctx['common']}
        print("getting branch....", next_path)
        main(next_path, '_branches', initial_context=next_context, is_branch=True)

    subapps = get_subapps(current_app_path)
    if subapps:
        for subapp in subapps:
            print("entering subapp.......", subapp)
            next_path = os.path.join(current_app_path, subapp)
            next_context = {'common': total_ctx['common']}
            print(next_context)
            main(next_path, subapp, initial_context=next_context)

    return


if __name__ == "__main__":
    allowed_extensions = ['md', 'json']
    print("!!!!!!!!!!! START !!!!!!!!!!!")
    main('src/', '/')
    print("!!!!!!!!!!! END !!!!!!!!!!!!!")

    # todo: make subapps names availale to context
    # comon is unavailable to recursive apps check
    # include not giving error when nt present