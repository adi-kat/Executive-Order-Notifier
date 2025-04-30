import re

def slugify(title):
    # Lowercase, remove non-word characters, replace spaces/hyphens with hyphens
    title = title.lower()
    title = re.sub(r'[^a-z0-9\s-]', '', title)
    title = re.sub(r'[\s-]+', '-', title).strip('-')
    return title
