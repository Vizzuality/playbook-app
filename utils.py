import re

def humanize(item):
    item = re.sub(r'^private\s*', '', item)  # Remove "private" and any trailing spaces
    item = re.sub(r'^[^a-zA-Z0-9\s]+', '', item)  # Remove any non-alphanumeric characters (except spaces) at the start of the string
    item = re.sub(r'[-_]', ' ', item)  # Replace underscores and hyphens with spaces
    return item.title()
