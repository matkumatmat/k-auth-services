# IGNORE_PATTERN=$(grep -v '^#' .gitignore | grep -v '^$' | sed 's/\/$//' | tr '\n' '|')

# tree -J -I "${IGNORE_PATTERN}" --dirsfirst -o about/structure.json
# tree -I "${IGNORE_PATTERN}" --dirsfirst >> about/structure.md

tree -J -I '__pycache__|*.py[cod]|*$py.class|.venv|venv|env|.env*|app/env|.mypy_cache|.ruff_cache|.pytest_cache|.coverage|htmlcov|dist|build|*.egg-info|.claude|.vscode|.idea|.DS_Store|Thumbs.db|md|CLAUDE.md|project_structure*.txt|history' --dirsfirst -o about/structure.json
tree -I '__pycache__|*.py[cod]|*$py.class|.venv|venv|env|.env*|app/env|.mypy_cache|.ruff_cache|.pytest_cache|.coverage|htmlcov|dist|build|*.egg-info|.claude|.vscode|.idea|.DS_Store|Thumbs.db|md|CLAUDE.md|project_structure*.txt|history' --dirsfirst -o about/structure.md