"""Command-line entry point for the catalogue generator.

This module loads the curated catalogue, validates it, converts it into typed
models, renders the configured Markdown pages and writes the generated output
into the MkDocs source directory.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from .loader import (
    CatalogueLoadError,
    find_repository_root,
    load_catalogue,
)
from .models import PortalCatalogue, build_portal_catalogue
from .renderer import CatalogueRenderer, RenderedPage
from .validator import (
    CatalogueValidationError,
    ValidationResult,
    validate_catalogue,
)


EXIT_SUCCESS = 0
EXIT_LOAD_ERROR = 2
EXIT_VALIDATION_ERROR = 3
EXIT_GENERATION_ERROR = 4


def build_argument_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        prog="lupaxa-catalogue",
        description=(
            "Validate The Lupaxa Project catalogue and generate the "
            "curated MkDocs portal pages."
        ),
    )

    parser.add_argument(
        "--repository-root",
        type=Path,
        help=(
            "Path to the repository root. When omitted, the generator searches "
            "upwards from the current working directory."
        ),
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate the catalogue without generating any output files.",
    )

    parser.add_argument(
        "--include-unpublished",
        action="store_true",
        help=(
            "Include unpublished catalogue entries in generated output for "
            "local preview purposes."
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Render and validate all output without writing files."
        ),
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Check whether generated files are current without modifying them. "
            "The command fails when any generated file differs."
        ),
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress normal informational output.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show additional catalogue and output information.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the catalogue generator."""

    parser = build_argument_parser()
    arguments = parser.parse_args(argv)

    try:
        repository_root = resolve_repository_root(
            arguments.repository_root
        )

        paths, data = load_catalogue(repository_root)

        if arguments.include_unpublished:
            _enable_unpublished_entries(data.config)

        validation_result = validate_catalogue(data)

        _print_validation_result(
            validation_result,
            quiet=arguments.quiet,
        )

        if not validation_result.is_valid:
            raise CatalogueValidationError(validation_result)

        if arguments.validate_only:
            if not arguments.quiet:
                print("Catalogue validation completed successfully.")

            return EXIT_SUCCESS

        catalogue = build_portal_catalogue(data)
        renderer = CatalogueRenderer(catalogue)
        rendered_pages = renderer.render_all_pages()

        outputs = build_output_map(
            repository_root=repository_root,
            catalogue=catalogue,
            rendered_pages=rendered_pages,
        )

        if arguments.verbose and not arguments.quiet:
            _print_catalogue_summary(catalogue)
            _print_output_summary(outputs)

        if arguments.dry_run:
            if not arguments.quiet:
                print(
                    f"Dry run completed successfully. "
                    f"{len(outputs)} file(s) were rendered."
                )

            return EXIT_SUCCESS

        if arguments.check:
            return check_generated_files(
                outputs,
                quiet=arguments.quiet,
            )

        write_generated_files(
            outputs,
            quiet=arguments.quiet,
        )

        return EXIT_SUCCESS

    except CatalogueLoadError as exc:
        print(f"Catalogue load failed: {exc}", file=sys.stderr)
        return EXIT_LOAD_ERROR

    except CatalogueValidationError as exc:
        if not exc.result.issues:
            print(str(exc), file=sys.stderr)

        return EXIT_VALIDATION_ERROR

    except (OSError, TypeError, ValueError, KeyError) as exc:
        print(
            f"Catalogue generation failed: {exc}",
            file=sys.stderr,
        )

        return EXIT_GENERATION_ERROR


def resolve_repository_root(
    configured_root: Path | None,
) -> Path:
    """Resolve the repository root supplied to the generator."""

    if configured_root is None:
        return find_repository_root()

    root = configured_root.expanduser().resolve()

    if not root.exists():
        raise CatalogueLoadError(
            f"Repository root does not exist: {root}"
        )

    if not root.is_dir():
        raise CatalogueLoadError(
            f"Repository root is not a directory: {root}"
        )

    if not (root / "mkdocs.yml").is_file():
        raise CatalogueLoadError(
            f"Repository root does not contain mkdocs.yml: {root}"
        )

    if not (root / "catalogue").is_dir():
        raise CatalogueLoadError(
            f"Repository root does not contain a catalogue directory: {root}"
        )

    return root


def build_output_map(
    *,
    repository_root: Path,
    catalogue: PortalCatalogue,
    rendered_pages: dict[str, RenderedPage],
) -> dict[Path, str]:
    """Create the complete generated-file mapping."""

    output = catalogue.configuration.output

    page_paths = {
        "projects": output.projects,
        "organisations": output.organisations,
        "toolboxes": output.toolboxes,
        "documentation": output.documentation,
    }

    generated: dict[Path, str] = {}

    for page_name, relative_path in page_paths.items():
        page = rendered_pages.get(page_name)

        if page is None:
            raise ValueError(
                f"Renderer did not produce the required '{page_name}' page."
            )

        generated[
            _resolve_output_path(
                repository_root,
                relative_path,
            )
        ] = page.content

    catalogue_data_path = _resolve_output_path(
        repository_root,
        output.catalogue_data,
    )

    generated[catalogue_data_path] = render_catalogue_json(catalogue)

    return generated


def render_catalogue_json(
    catalogue: PortalCatalogue,
) -> str:
    """Render the published catalogue as formatted JSON."""

    payload = {
        "portal": {
            "name": catalogue.configuration.portal.name,
            "description": catalogue.configuration.portal.description,
            "base_url": catalogue.configuration.portal.base_url,
            "github_url": catalogue.configuration.portal.github_url,
            "default_language": (
                catalogue.configuration.portal.default_language
            ),
        },
        "projects": [
            _serialise_model(project)
            for project in catalogue.published_projects
        ],
        "organisations": [
            _serialise_model(organisation)
            for organisation in catalogue.published_organisations
        ],
        "documentation": [
            _serialise_model(entry)
            for entry in catalogue.published_documentation
        ],
        "categories": [
            _serialise_model(category)
            for category in catalogue.published_categories
        ],
    }

    return (
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
            sort_keys=False,
        )
        + "\n"
    )


def write_generated_files(
    outputs: dict[Path, str],
    *,
    quiet: bool = False,
) -> None:
    """Write all generated files using atomic replacement."""

    changed_count = 0
    unchanged_count = 0

    for path, content in outputs.items():
        existing_content = _read_existing_file(path)

        if existing_content == content:
            unchanged_count += 1

            if not quiet:
                print(f"[UNCHANGED] {path}")

            continue

        _write_text_atomically(path, content)
        changed_count += 1

        if not quiet:
            print(f"[GENERATED] {path}")

    if not quiet:
        print(
            f"Generation completed: {changed_count} changed, "
            f"{unchanged_count} unchanged."
        )


def check_generated_files(
    outputs: dict[Path, str],
    *,
    quiet: bool = False,
) -> int:
    """Check whether generated files match the expected output."""

    missing: list[Path] = []
    outdated: list[Path] = []

    for path, expected_content in outputs.items():
        if not path.exists():
            missing.append(path)
            continue

        if not path.is_file():
            outdated.append(path)
            continue

        existing_content = _read_existing_file(path)

        if existing_content != expected_content:
            outdated.append(path)

    if not missing and not outdated:
        if not quiet:
            print(
                f"Generated catalogue is current. "
                f"{len(outputs)} file(s) checked."
            )

        return EXIT_SUCCESS

    for path in missing:
        print(
            f"[MISSING] {path}",
            file=sys.stderr,
        )

    for path in outdated:
        print(
            f"[OUTDATED] {path}",
            file=sys.stderr,
        )

    print(
        "Generated catalogue files are not current. "
        "Run the generator without --check to update them.",
        file=sys.stderr,
    )

    return EXIT_GENERATION_ERROR


def _enable_unpublished_entries(
    config: dict[str, Any],
) -> None:
    """Enable unpublished entries for the current generator run."""

    publication = config.setdefault(
        "publication",
        {},
    )

    if not isinstance(publication, dict):
        raise ValueError(
            "The publication configuration section must be a mapping."
        )

    publication["include_unpublished"] = True


def _resolve_output_path(
    repository_root: Path,
    configured_path: str,
) -> Path:
    """Resolve and constrain a configured output path."""

    if not isinstance(configured_path, str) or not configured_path.strip():
        raise ValueError(
            "Configured output paths must be non-empty strings."
        )

    configured = Path(configured_path)

    if configured.is_absolute():
        raise ValueError(
            f"Output path must be relative to the repository root: "
            f"{configured_path}"
        )

    resolved = (repository_root / configured).resolve()

    try:
        resolved.relative_to(repository_root)
    except ValueError as exc:
        raise ValueError(
            f"Output path escapes the repository root: {configured_path}"
        ) from exc

    return resolved


def _write_text_atomically(
    path: Path,
    content: str,
) -> None:
    """Write UTF-8 text using a temporary file and atomic replacement."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = path.with_name(
        f".{path.name}.tmp"
    )

    try:
        temporary_path.write_text(
            content,
            encoding="utf-8",
            newline="\n",
        )

        temporary_path.replace(path)

    except OSError:
        try:
            temporary_path.unlink(
                missing_ok=True,
            )
        except OSError:
            pass

        raise


def _read_existing_file(path: Path) -> str | None:
    """Read an existing UTF-8 file, returning ``None`` when absent."""

    if not path.is_file():
        return None

    return path.read_text(
        encoding="utf-8",
    )


def _serialise_model(value: Any) -> Any:
    """Convert a catalogue model into JSON-compatible values."""

    if is_dataclass(value) and not isinstance(value, type):
        dataclass_instance: Any = value

        return {
            key: _serialise_model(item)
            for key, item in asdict(dataclass_instance).items()
        }

    if isinstance(value, tuple):
        return [
            _serialise_model(item)
            for item in value
        ]

    if isinstance(value, list):
        return [
            _serialise_model(item)
            for item in value
        ]

    if isinstance(value, dict):
        return {
            str(key): _serialise_model(item)
            for key, item in value.items()
        }

    return value


def _print_validation_result(
    result: ValidationResult,
    *,
    quiet: bool,
) -> None:
    """Print validation issues and summary information."""

    for issue in result.issues:
        stream = (
            sys.stderr
            if issue.severity.value == "error"
            else sys.stdout
        )

        print(
            issue.format(),
            file=stream,
        )

    if quiet:
        return

    print(
        f"Validation completed: "
        f"{len(result.errors)} error(s), "
        f"{len(result.warnings)} warning(s)."
    )


def _print_catalogue_summary(
    catalogue: PortalCatalogue,
) -> None:
    """Print catalogue entry counts."""

    print("Catalogue summary:")
    print(
        f"  Projects:       "
        f"{len(catalogue.published_projects)} published / "
        f"{len(catalogue.projects)} total"
    )
    print(
        f"  Organisations:  "
        f"{len(catalogue.published_organisations)} published / "
        f"{len(catalogue.organisations)} total"
    )
    print(
        f"  Documentation:  "
        f"{len(catalogue.published_documentation)} published / "
        f"{len(catalogue.documentation)} total"
    )
    print(
        f"  Categories:     "
        f"{len(catalogue.published_categories)} published / "
        f"{len(catalogue.categories)} total"
    )


def _print_output_summary(
    outputs: dict[Path, str],
) -> None:
    """Print generated output paths."""

    print("Generated outputs:")

    for path in outputs:
        print(f"  {path}")


if __name__ == "__main__":
    raise SystemExit(main())
