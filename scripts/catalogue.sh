#!/usr/bin/env bash

###############################################################################
# The Lupaxa Project
#
# Catalogue Generator
###############################################################################

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "${ROOT_DIR}"

usage() {
    cat <<EOF
Usage:

  ./scripts/catalogue validate
      Validate catalogue only.

  ./scripts/catalogue generate
      Generate all catalogue pages.

  ./scripts/catalogue clean
      Remove generated files.

  ./scripts/catalogue rebuild
      Clean then generate.

  ./scripts/catalogue compile
      Compile Python files.

EOF
}

clean() {
    echo "Cleaning generated files..."

    rm -rf \
        catalogue/generators/__pycache__ \
        mkdocs/assets/data/catalogue.json \
        mkdocs/documentation \
        mkdocs/organisations \
        mkdocs/projects \
        mkdocs/toolboxes \
        mkdocs/documentation.md \
        mkdocs/organisations.md \
        mkdocs/projects.md \
        mkdocs/toolboxes.md

    find . -type d -name "__pycache__" -prune -exec rm -rf {} +
    find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete

    echo "Done."
}

case "${1:-}" in

    validate)
        python -m catalogue.generators.main --validate-only
        ;;

    generate)
        python -m catalogue.generators.main
        ;;

    clean)
        clean
        ;;

    rebuild)
        clean
        python -m catalogue.generators.main
        ;;

    compile)
        python -m compileall catalogue
        ;;

    *)
        usage
        exit 1
        ;;

esac
