import os
import sys
import sphinx_godot_theme as sgt
from zupa import __version__

sys.path.insert(0, os.path.abspath(".."))
html_favicon = "static/images/docs_logo.svg"

project = "Owly"
supported_languages = {
    "en": f"{project} (%s)",
}
extensions = [
    # "notfound.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
    "sphinx_search.extension",
    "sphinx_tabs.tabs",
    "sphinxext.opengraph",
    "sphinxcontrib.drawio",
    "myst_parser",
    "sphinx_xournal",
]
# autosectionlabel_prefix_document = True
sphinx_tabs_nowarn = True
templates_path = sgt.templates_path
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}
source_encoding = sgt.source_encoding
master_doc = "index"

# https://pypi.org/project/sphinxcontrib-drawio/
drawio_binary_path = "/usr/bin/drawio"
drawio_headless  = True
drawio_no_sandbox = True

author = "Arkadiusz Michał Ryś"
copyright = f"2022, {author}"
version = __version__
release = version
ogp_site_name = project

env_tags = os.getenv("SPHINX_TAGS")
if env_tags is not None:
    for tag in env_tags.split(","):
        print("Adding Sphinx tag: %s" % tag.strip())
        tags.add(tag.strip())  # noqa: F821
language = os.getenv("READTHEDOCS_LANGUAGE", "en")
if language not in supported_languages.keys():
    print("Unknown language: " + language)
    print("Supported languages: " + ", ".join(supported_languages.keys()))
    print("The configured language is wrong. Falling back to 'en'.")
    language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
todo_include_todos = False
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "logo_only": True,
    "collapse_navigation": False,
}
html_logo = "static/images/docs_logo.svg"
html_static_path = ["static"] + sgt.html_static_path
htmlhelp_basename = project
html_extra_path = sgt.html_extra_path
html_css_files = ["css/custom.css"]
html_js_files = ["js/custom.js"]
on_rtd = os.environ.get("READTHEDOCS", None) == "True"
html_title = supported_languages[language] % version
html_context = {"conf_py_path": "/"}
latex_engine = "pdflatex"
latex_elements = {
    "papersize": "letterpaper",
    "pointsize": "10pt",
    "figure_align": "htbp",

    "preamble": r"""
    \DeclareUnicodeCharacter{2610}{[   ]}
    \DeclareUnicodeCharacter{2611}{[X]}
    \DeclareUnicodeCharacter{251C}{|}
    \DeclareUnicodeCharacter{2500}{-}
    \DeclareUnicodeCharacter{2514}{|}
    """,
}
latex_documents = [(master_doc, f"{project.lower().replace(' ', '_')}.tex", project, author, "manual"),]
man_pages = [(master_doc, project, project, [author], 1)]
texinfo_documents = [(master_doc, project, project, author, project, project, "Miscellaneous")]
notfound_context = sgt.notfound_context
