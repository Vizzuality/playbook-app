import re

def humanize(s):
    return re.sub(r'[-_]', ' ', s).title()
