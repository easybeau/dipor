import markdown
from jinja2 import Environment, PackageLoader, Undefined
from os import listdir
import os
import pathlib

class SilentUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return ''


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


def get_subapps(appname):
    subapps = []
    app_path = 'content/'+appname
    for file in listdir(app_path):
        if os.path.isdir(app_path+"/"+file):
            subapps.append(file)

    return subapps


def load_template(tpl, appname):
    template_path = 'src/'+appname
    # templates = []
    env = Environment(loader=PackageLoader('src', appname), undefined=SilentUndefined)
    env.globals.update(zip=zip)
    template =  env.get_template(tpl)
    return template
    

def get_templates_for_app(appname):
    templates_app_path = 'src/'+appname
    app_templates = []
    for file in listdir(templates_app_path):
        if file.endswith(('.tpl', '.html')):
            app_templates.append(file)

    return app_templates

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
            print(final_context)

            for loaded_tpl in loaded_templates:
                pathlib.Path('public/'+subapp+"/").mkdir(parents=True, exist_ok=True) 
                loaded_tpl[0].stream(**final_context).dump('public/'+subapp+"/"+loaded_tpl[1])


if __name__ == "__main__":
    appname = 'blog_post'
    allowed_extensions = ['md', 'json']
    generate_static_site_for_app(appname, allowed_extensions)