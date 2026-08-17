from catalogue_release_sync import (
    apply_catalogue_release,
    format_released_date,
    normalise_github_repo,
    version_from_tag,
)

SAMPLE = """\
- id: other
  published: true
  name: Other
  repository: https://github.com/example/other
  banner: in-review

- id: action-lint
  published: true
  name: Action Lint
  repository: https://github.com/lupaxa-cicd-toolbox/action-lint
  banner: in-review
"""


def test_normalise_github_repo_accepts_url_and_slug():
    assert normalise_github_repo(
        "https://github.com/Lupaxa-CICD-Toolbox/action-lint.git/"
    ) == "lupaxa-cicd-toolbox/action-lint"
    assert normalise_github_repo("lupaxa-cicd-toolbox/action-lint") == (
        "lupaxa-cicd-toolbox/action-lint"
    )


def test_version_from_tag_stable_only():
    assert version_from_tag("v1.2.0") == "1.2.0"
    assert version_from_tag("v1.2.0-rc1") is None
    assert version_from_tag("v1.2.0-draft1") is None
    assert version_from_tag("v1.2.0-dev1") is None


def test_format_released_date_strips_tz():
    assert format_released_date("2026-08-17T14:00:00Z") == "2026-08-17T14:00:00"
    assert format_released_date("2026-08-17T14:00:00+00:00") == "2026-08-17T14:00:00"


def test_apply_updates_only_matching_card():
    result = apply_catalogue_release(
        SAMPLE,
        repository="lupaxa-cicd-toolbox/action-lint",
        version="1.2.0",
        released_date="2026-08-17T14:00:00",
    )
    assert result.status == "updated"
    assert result.card_id == "action-lint"
    assert result.card_name == "Action Lint"
    assert 'id: other\n  published: true\n  name: Other' in result.yaml_text
    assert "banner: in-review" in result.yaml_text
    action = result.yaml_text.split("- id: action-lint", 1)[1]
    assert 'banner: released' in action
    assert 'version: "1.2.0"' in action
    assert 'released_date: "2026-08-17T14:00:00"' in action
    assert "banner: in-review" not in action


def test_apply_skips_when_already_matching():
    updated = apply_catalogue_release(
        SAMPLE,
        repository="lupaxa-cicd-toolbox/action-lint",
        version="1.2.0",
        released_date="2026-08-17T14:00:00",
    ).yaml_text
    again = apply_catalogue_release(
        updated,
        repository="lupaxa-cicd-toolbox/action-lint",
        version="1.2.0",
        released_date="2026-08-17T14:00:00",
    )
    assert again.status == "unchanged"
    assert again.yaml_text == updated


def test_apply_later_version_on_already_released_card():
    released = apply_catalogue_release(
        SAMPLE,
        repository="lupaxa-cicd-toolbox/action-lint",
        version="1.2.0",
        released_date="2026-08-17T14:00:00",
    ).yaml_text
    later = apply_catalogue_release(
        released,
        repository="lupaxa-cicd-toolbox/action-lint",
        version="1.3.0",
        released_date="2026-09-01T09:00:00",
    )
    assert later.status == "updated"
    action = later.yaml_text.split("- id: action-lint", 1)[1]
    assert 'version: "1.3.0"' in action
    assert 'released_date: "2026-09-01T09:00:00"' in action


def test_apply_not_found():
    result = apply_catalogue_release(
        SAMPLE,
        repository="example/unknown",
        version="1.0.0",
        released_date="2026-08-17T14:00:00",
    )
    assert result.status == "not_found"
    assert result.yaml_text == SAMPLE


def test_apply_unpublished():
    yaml_text = SAMPLE.replace(
        "name: Action Lint\n  repository:",
        "name: Action Lint\n  published: false\n  repository:",
    )
    result = apply_catalogue_release(
        yaml_text,
        repository="lupaxa-cicd-toolbox/action-lint",
        version="1.2.0",
        released_date="2026-08-17T14:00:00",
    )
    assert result.status == "unpublished"


def test_apply_ambiguous_duplicate_repository():
    yaml_text = SAMPLE + (
        "\n- id: action-lint-copy\n  published: true\n  name: Copy\n"
        "  repository: https://github.com/lupaxa-cicd-toolbox/action-lint\n"
    )
    result = apply_catalogue_release(
        yaml_text,
        repository="lupaxa-cicd-toolbox/action-lint",
        version="1.2.0",
        released_date="2026-08-17T14:00:00",
    )
    assert result.status == "ambiguous"
    assert result.yaml_text == yaml_text
