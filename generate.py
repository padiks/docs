import os
import yaml

docs_dir = "docs"

def format_title(name):
    # Replace dashes/underscores with spaces and title-case
    return name.replace("-", " ").replace("_", " ").title()

def build_nav(path, base=""):
    nav_items = []
    for item in sorted(os.listdir(path)):
        full_path = os.path.join(path, item)
        rel_path = os.path.join(base, item) if base else item
        if os.path.isdir(full_path):
            children = build_nav(full_path, rel_path)
            if children:  # only add folder if it has md files inside
                nav_items.append({format_title(item): children})
        elif item.endswith(".md"):
            nav_items.append({format_title(os.path.splitext(item)[0]): rel_path})
    return nav_items

mkdocs_config = {
    "site_name": "MkDocs Library",
    "theme": {"name": "dracula"},
    "extra_css": ["css/custom.css"],
    "nav": build_nav(docs_dir)
}

with open("mkdocs.yml", "w") as f:
    yaml.dump(mkdocs_config, f, sort_keys=False)
