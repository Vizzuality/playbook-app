import os
import fnmatch
from markdown_it import MarkdownIt

mdit = MarkdownIt()


def search_md_files(search_text, base_path, logged_in=False):
    matching_files = []

    excluded_files = ["public_index.md", "private_index.md"]

    for root, _, files in os.walk(base_path):
        for file in fnmatch.filter(files, '*.md'):
            if file in excluded_files:
                print(f"Excluded file: {file}")  # Debug print
                continue

            if not logged_in and file.startswith("private"):
                print(f"Excluded private file: {file}")  # Debug print
                continue

            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as md_file:
                content = md_file.read()
                if search_text.lower() in content.lower():
                    excerpt_start = content.lower().find(search_text.lower())
                    excerpt_end = excerpt_start + len(search_text) + 100
                    excerpt = content[excerpt_start:excerpt_end]
                    html_excerpt = mdit.render(excerpt)  # Convert the excerpt to HTML
                    matching_files.append({
                        'path': os.path.relpath(file_path, base_path),
                        'excerpt': html_excerpt
                    })

    return matching_files
