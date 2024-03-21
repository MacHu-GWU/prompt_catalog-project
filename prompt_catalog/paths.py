# -*- coding: utf-8 -*-

from pathlib import Path

dir_here = Path(__file__).absolute().parent
PACKAGE_NAME = dir_here.name

dir_project_root = dir_here.parent

# ------------------------------------------------------------------------------
# Virtual Environment Related
# ------------------------------------------------------------------------------
dir_venv = dir_project_root / ".venv"
dir_venv_bin = dir_venv / "bin"

# virtualenv executable paths
bin_pytest = dir_venv_bin / "pytest"

# test related
dir_htmlcov = dir_project_root / "htmlcov"
path_cov_index_html = dir_htmlcov / "index.html"
dir_unit_test = dir_project_root / "tests"

# ------------------------------------------------------------------------------
# Prompt data related
# ------------------------------------------------------------------------------
dir_project_home = Path.home().joinpath(".prompt_catalog")
dir_project_home.mkdir(exist_ok=True)

dir_cache = dir_project_home.joinpath(".cache")
dir_index = dir_project_home.joinpath(".index")
path_airtable_pac = dir_project_home.joinpath("airtable_pac.txt")
path_airtable_data = dir_project_home / "airtable_data.json"
path_documents_data = dir_project_home / "documents_data.json"
