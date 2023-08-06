import pytest
import textwrap
import snr

from pathlib import Path


@pytest.fixture(scope="session")
def simple_note():
    return {
        "filename": "simple.md",
        "content": textwrap.dedent("""
            # Simple note

            Contains only text, not other features like:
                - links
                - tags
                - footers
            """).strip()
    }


@pytest.fixture(scope="session")
def simple_note_with_header(simple_note):
    return {
        "filename": "simple_with_header.md",
        "content": textwrap.dedent("""
            ---
            #aliases: [3D tisk insert]
            tags: [Honza]
            created: 2022-07-12
            ---
            # simple_with_header

            """).strip() + simple_note["content"]
    }

@pytest.fixture(scope="session")
def simple_note_in_folder(simple_note):
    return {
        "filename": "topic/simple_with_header.md",
        "content": textwrap.dedent("""
            ---
            #aliases: [3D tisk insert]
            tags: [Honza]
            created: 2022-07-12
            ---
            # topic/simple_with_header
           
            """).strip() + simple_note["content"]
    }

@pytest.fixture(scope="session")
def all_notes(
    simple_note,
    simple_note_with_header,
    simple_note_in_folder,
):
    return [
        simple_note,
        simple_note_with_header,
        simple_note_in_folder,
    ]


@pytest.fixture(scope="session")
def vault_dir(tmp_path_factory: pytest.TempPathFactory,
              all_notes):
    root_dir = tmp_path_factory.mktemp("vault")

    for note_fixture in all_notes:
        path = Path(root_dir / note_fixture["filename"])
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, mode="w", encoding="utf-8") as file:
            file.write(note_fixture["content"])

    return root_dir


@pytest.fixture(scope="session")
def vault(vault_dir):
    return snr.open_vault(vault_dir)
