import os
from utils import humanize
from flask import url_for

def breadcrumbs(md_path):
    parts = md_path.split(os.sep)
    breadcrumbs_list = [{'name': 'Home', 'url': url_for('routes.index') }]
    url_parts = []

    for part in parts:
        name = humanize(part)
        is_md_file = part.endswith('.md')
        if is_md_file:
            name = name[:-3]  # Remove the .md extension from the name

        url_parts.append(part)

        if is_md_file:
            url = url_parts[-2]  # Get the parent folder's name
        else:
            url = part

        breadcrumbs_list.append({'name': name, 'url': url})

    return breadcrumbs_list





