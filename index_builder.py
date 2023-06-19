import os
import urllib
from utils import humanize
from config import content_folder_path
from urllib.parse import urljoin
from io import StringIO
import logging


class IndexBuilder:
    _instance = None
    public_index_string = ""
    private_index_string = ""

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.reload_data()
        return cls._instance

    def reload_data(self):
        logging.info("Reloading menu data...")
        public_menu, private_menu = self.__build_menus(content_folder_path)
        self.public_index_string = self.__save_menus_to_string(public_menu)
        self.private_index_string = self.__save_menus_to_string(private_menu)
        logging.info("Menu data reloaded!")

    def get_public_index(self):
        return self.public_index_string

    def get_private_index(self):
        return self.private_index_string

    @staticmethod
    def __build_menus(folder_path):
        public_menu = {}
        private_menu = {}

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if not file.endswith(".md"):
                    continue
                if file.lower() == "readme.md":
                    continue

                rel_path = os.path.relpath(os.path.join(root, file), folder_path)
                rel_dir = os.path.dirname(rel_path)

                is_private = file.startswith("private_")
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

    @staticmethod
    def __save_menus_to_string(menu):
        def write_nested_list_to_buffer(output_buffer, input_menu, level=0, is_sub_menu=False, padding_level=0):
            indent = "    " * level

            if is_sub_menu:
                output_buffer.write(f'{indent}<ul class="mt-1 px-2 collapsed-menu">\n')
            else:
                output_buffer.write(
                    f'{indent}<ul role="list" class="flex flex-1 flex-col gap-y-2">\n'
                )

            for item, value in input_menu.items():
                padding_value = f"{padding_level}rem" if padding_level > 0 else "0"
                text_color = "text-gray-200" if is_sub_menu else "text-white"
                hover_color = "hover:text-white"
                if isinstance(value, dict):
                    output_buffer.write(f'{indent}    <li style="padding-left: {padding_value};">\n')
                    output_buffer.write(
                        f'{indent}        <button type="button" class="{hover_color} {text_color} hover:bg-gray-900 flex items-center w-full text-left rounded-md p-2 gap-x-3 text-sm leading-6 font-semibold" aria-controls="sub-menu-{item.replace(" ", "-")}" aria-expanded="false">\n'
                    )
                    output_buffer.write(
                        f'{indent}            <svg class="transform transition-transform text-gray-200 h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">\n'
                    )
                    output_buffer.write(
                        f'{indent}                <path fill-rule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clip-rule="evenodd" />\n'
                    )
                    output_buffer.write(f"{indent}            </svg>\n")
                    output_buffer.write(f"{indent}            {humanize(item)}\n")
                    output_buffer.write(f"{indent}        </button>\n")
                    output_buffer.write(
                        f'{indent}        <div id="sub-menu-{item.replace(" ", "-")}"class="sub-menu">\n'
                    )  # Add the id attribute here
                    write_nested_list_to_buffer(
                        output_buffer,
                        value,
                        level + 1,
                        is_sub_menu=True,
                        padding_level=padding_level + 1,
                    )
                    output_buffer.write(f"{indent}        </div>\n")
                    output_buffer.write(f"{indent}    </li>\n")
                else:
                    url = urllib.parse.quote(
                        value[:-3]
                    )  # Remove .md extension here and quote the URL
                    output_buffer.write(f'{indent}    <li style="padding-left: {padding_value};">\n')
                    output_buffer.write(
                        f'{indent}        <a href="/view-md/{url}" class="{hover_color} {text_color} hover:bg-gray-900 block rounded-md py-1 pr-1 text-sm leading-6">{humanize(item[:-3])}</a>\n'
                    )
                    output_buffer.write(f"{indent}    </li>\n")

            output_buffer.write(f"{indent}</ul>\n")

        with StringIO("") as buffer:
            write_nested_list_to_buffer(buffer, menu)
            buffer.seek(0)
            return buffer.read()


