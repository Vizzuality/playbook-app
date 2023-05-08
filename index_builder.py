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

                is_private = file.startswith("private")
                # Check if file is not public_index.md or private_index.md
                if file not in ("public_index.md", "private_index.md"):
                # Update private menu
                    current_level = private_menu
                    for folder in rel_dir.split(os.sep):
                        current_level = current_level.setdefault(folder, {})

                    current_level[file] = rel_path

                    # Update public menu if not private
                    if not is_private:
                        current_level = public_menu
                        for folder in rel_dir.split(os.sep):
                            current_level = current_level.setdefault(folder, {})

                        current_level[file] = rel_path

    return public_menu, private_menu


def save_menus_to_files(public_menu, private_menu, local_repo_path):
    public_index_file = os.path.join(local_repo_path, "public_index.md")
    private_index_file = os.path.join(local_repo_path, "private_index.md")

    def write_nested_list(file, menu, level=0, is_sub_menu=False, padding_level=0):
        indent = "    " * level

        if is_sub_menu:
            file.write(f'{indent}<ul class="mt-1 px-2 collapsed-menu">\n')
        else:
            file.write(f'{indent}<ul role="list" class="flex flex-1 flex-col gap-y-2">\n')

        for item, value in menu.items():
            padding_value = f"{padding_level}rem" if padding_level > 0 else "0"
            text_color = "text-gray-200" if is_sub_menu else "text-white"
            hover_color = "hover:text-white"
            if isinstance(value, dict):
                file.write(f'{indent}    <li style="padding-left: {padding_value};">\n')
                file.write(f'{indent}        <button type="button" class="{hover_color} {text_color} hover:bg-gray-900 flex items-center w-full text-left rounded-md p-2 gap-x-3 text-sm leading-6 font-semibold" aria-controls="sub-menu-{item.replace(" ", "-")}" aria-expanded="false">\n')
                file.write(f'{indent}            <svg class="transform transition-transform text-gray-200 h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">\n')
                file.write(f'{indent}                <path fill-rule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clip-rule="evenodd" />\n')
                file.write(f'{indent}            </svg>\n')
                file.write(f'{indent}            {humanize(item)}\n')
                file.write(f'{indent}        </button>\n')
                file.write(f'{indent}        <div id="sub-menu-{item.replace(" ", "-")}"class="sub-menu">\n')  # Add the id attribute here
                write_nested_list(file, value, level + 1, is_sub_menu=True, padding_level=padding_level + 1)
                file.write(f'{indent}        </div>\n')
                file.write(f'{indent}    </li>\n')
            else:
                url = urllib.parse.quote(value[:-3])  # Remove .md extension here and quote the URL
                file.write(f'{indent}    <li style="padding-left: {padding_value};">\n')
                file.write(f'{indent}        <a href="/view-md/{url}" class="{hover_color} {text_color} hover:bg-gray-900 block rounded-md py-1 pr-1 text-sm leading-6">{humanize(item[:-3])}</a>\n')
                file.write(f'{indent}    </li>\n')

        file.write(f'{indent}</ul>\n')




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

