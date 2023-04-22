import os
import re
import urllib
from utils import humanize
from config import local_repo_path
from urllib.parse import urljoin

def build_menus(local_repo_path):
    public_menu = {}
    private_menu = {}

    for root, dirs, files in os.walk(local_repo_path):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(
                    os.path.join(root, file), local_repo_path)
                rel_dir = os.path.dirname(rel_path)

                menu_to_update = private_menu if file.startswith(
                    "private") else public_menu
                current_level = menu_to_update
                for folder in rel_dir.split(os.sep):
                    current_level = current_level.setdefault(folder, {})

                current_level[file] = rel_path

    return public_menu, private_menu


def save_menus_to_files(public_menu, private_menu, local_repo_path):
    public_index_file = os.path.join(local_repo_path, "public_index.md")
    private_index_file = os.path.join(local_repo_path, "private_index.md")

    def write_nested_list(file, menu, level=0):
        indent = "    " * level
        file.write(f'{indent}<ul class="collapsible" data-collapsible="expandable">\n')
        for item, value in menu.items():
            if isinstance(value, dict):
                file.write(f'{indent}    <li>\n')
                file.write(f'{indent}        <div class="collapsible-header"><i class="tiny material-icons">chevron_right</i>{" " + humanize(item)}</div>\n') 
                file.write(f'{indent}        <div class="collapsible-body">\n')
                write_nested_list(file, value, level + 1)
                file.write(f'{indent}        </div>\n')
                file.write(f'{indent}    </li>\n')
            else:
                url = urllib.parse.quote(value)  # Quote the URL here
                file.write(f'{indent}    <li>\n')
                file.write(f'{indent}        <a href="/view-md/{url}" onclick="event.stopPropagation();" class="collapsible-header">{humanize(item[:-3])}</a>\n')
                file.write(f'{indent}    </li>\n')
        file.write(f'{indent}</ul>\n')

        if level == 0:
            file.write('<script>\n')
            file.write('    document.addEventListener("DOMContentLoaded", function() {\n')
            file.write('        var elems = document.querySelectorAll(".collapsible");\n')
            file.write('        var instances = M.Collapsible.init(elems, {accordion: false});\n')
            file.write('    });\n')
            file.write('</script>\n')

    with open(public_index_file, "w") as public_file:
        write_nested_list(public_file, public_menu)

    with open(private_index_file, "w") as private_file:
        write_nested_list(private_file, private_menu)

def fetch_markdown_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Get the real folder path
    real_folder_path = get_real_folder_path(file_path)
    # Find image paths and prepend the /images/ route and the real folder path to the path
    content = re.sub(r'\!\[(.*?)\]\((.*?)\)',
                     fr'![\1](/images/{real_folder_path}/\2)', content)

    # Prepend /view-md/ to all links pointing to .md files but not starting with #
    content = re.sub(r'\[(.*?)\]\((?!#)(.*?\.md)\)',
                     lambda m: f'[{m.group(1)}]({urljoin("/view-md/", m.group(2))})', content)

    return content

def get_real_folder_path(file_path):
    return os.path.relpath(os.path.dirname(file_path), local_repo_path)

