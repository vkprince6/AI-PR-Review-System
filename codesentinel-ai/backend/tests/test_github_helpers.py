"""Unit tests for diff formatting and truncation utilities."""

from app.utils.github_helpers import build_diff_text, truncate_patch


def test_truncate_patch_leaves_short_patch_unchanged():
    patch = "short diff content"
    assert truncate_patch(patch, max_chars=100) == patch


def test_truncate_patch_truncates_and_marks_long_patch():
    patch = "x" * 500
    result = truncate_patch(patch, max_chars=50)
    assert len(result) < len(patch)
    assert "truncated" in result


def test_build_diff_text_respects_max_files_limit():
    files = [
        {"filename": f"file{i}.py", "status": "modified", "patch": "diff content"}
        for i in range(5)
    ]
    result = build_diff_text(files, max_chars_per_file=200, max_files=2)
    assert "file0.py" in result
    assert "file1.py" in result
    assert "file2.py" not in result
    assert "3 additional file" in result
