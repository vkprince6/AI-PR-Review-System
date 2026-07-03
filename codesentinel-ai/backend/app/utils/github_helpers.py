"""
GitHub helper utilities.

Pure functions for preparing GitHub diff data to be safely and
efficiently passed into the Groq AI prompt context window.
"""

from typing import Any, Dict, List


def truncate_patch(patch: str, max_chars: int) -> str:
    """
    Truncate an individual file's diff patch to a maximum character count.

    Args:
        patch: The raw unified diff patch text.
        max_chars: Maximum number of characters to retain.

    Returns:
        str: The (possibly truncated) patch text, with a marker if cut.
    """
    if len(patch) <= max_chars:
        return patch
    return patch[:max_chars] + "\n... [diff truncated for length] ..."


def build_diff_text(
    changed_files: List[Dict[str, Any]],
    max_chars_per_file: int,
    max_files: int,
) -> str:
    """
    Build a single formatted diff document from multiple changed files.

    Args:
        changed_files: List of changed-file dicts with filename/status/patch.
        max_chars_per_file: Per-file character cap to bound prompt size.
        max_files: Maximum number of files to include in the diff text.

    Returns:
        str: A formatted, readable diff block for LLM consumption.
    """
    sections: list[str] = []
    for file_data in changed_files[:max_files]:
        filename = file_data.get("filename", "unknown_file")
        status = file_data.get("status", "modified")
        patch = file_data.get("patch") or "[No textual diff available - binary or too large]"
        truncated_patch = truncate_patch(patch, max_chars_per_file)
        sections.append(f"### File: {filename} ({status})\n```diff\n{truncated_patch}\n```")

    if len(changed_files) > max_files:
        sections.append(
            f"\n... and {len(changed_files) - max_files} additional file(s) not shown ..."
        )

    return "\n\n".join(sections)