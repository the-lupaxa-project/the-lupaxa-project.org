import pytest

from gallery_lib import collect_tags, load_photos_data, published_photos, validate_photos


SAMPLE = {
    "page": {"background": "#111111", "text_color": "#f5f5f5"},
    "photos": [
        {
            "photo": "assets/photos/a.jpg",
            "comment": "Visible",
            "tags": ["travel", "coast"],
        },
        {
            "photo": "assets/photos/draft.jpg",
            "comment": "Draft",
            "published": False,
            "tags": ["hidden-tag"],
        },
        {
            "photo": "https://example.com/b.jpg",
            "published": True,
            "tags": ["travel"],
        },
        {
            "photo": "assets/photos/c.jpg",
        },
    ],
}


def test_published_photos_defaults_true_and_respects_false():
    result = published_photos(SAMPLE)
    photos = [p["photo"] for p in result]
    assert photos == [
        "assets/photos/a.jpg",
        "https://example.com/b.jpg",
        "assets/photos/c.jpg",
    ]


def test_collect_tags_unique_sorted_from_given_list():
    photos = published_photos(SAMPLE)
    assert collect_tags(photos) == ["coast", "travel"]


def test_collect_tags_excludes_reserved_media_tags():
    photos = [
        {"photo": "a.jpg", "tags": ["travel", "photos"]},
        {"video": "b.mp4", "tags": ["videos", "animals"]},
    ]
    assert collect_tags(photos) == ["animals", "travel"]


def test_load_photos_data_reads_yaml(tmp_path):
    path = tmp_path / "photos.yml"
    path.write_text(
        "page:\n  background: '#1a1a1a'\n  text_color: '#f5f5f5'\n"
        "photos:\n  - photo: assets/photos/x.jpg\n    comment: Hi\n",
        encoding="utf-8",
    )
    data = load_photos_data(path)
    assert data["page"]["background"] == "#1a1a1a"
    assert data["photos"][0]["photo"] == "assets/photos/x.jpg"


def test_load_photos_data_rejects_non_mapping_yaml(tmp_path):
    path = tmp_path / "photos.yml"
    path.write_text("- photo: assets/photos/x.jpg\n", encoding="utf-8")
    with pytest.raises(ValueError, match="mapping at the top level"):
        load_photos_data(path)


def test_validate_photos_rejects_missing_photo():
    data = {"photos": [{"comment": "No photo field"}]}
    with pytest.raises(ValueError, match="photo or video"):
        validate_photos(data)


def test_validate_photos_accepts_video_without_photo():
    data = {"photos": [{"video": "https://example.com/clip.mp4", "tags": ["video"]}]}
    validate_photos(data)


def test_validate_photos_rejects_tags_as_string():
    data = {"photos": [{"photo": "assets/photos/x.jpg", "tags": "travel"}]}
    with pytest.raises(ValueError, match="tags"):
        validate_photos(data)


def test_validate_photos_rejects_non_mapping_photo_entry():
    data = {"photos": ["assets/photos/x.jpg"]}
    with pytest.raises(ValueError, match="mapping"):
        validate_photos(data)


def test_validate_photos_ignores_unpublished_photos():
    data = {"photos": [{"published": False, "comment": "Draft only"}]}
    validate_photos(data)
