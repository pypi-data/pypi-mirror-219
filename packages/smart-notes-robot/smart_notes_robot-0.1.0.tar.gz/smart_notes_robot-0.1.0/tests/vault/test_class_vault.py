import pytest
import snr.vault
import textwrap

from pathlib import Path
from os import getcwd



def test__init__(vault_dir):
    # Act
    vault = snr.vault.Vault(root_dir=vault_dir)
    # Assert
    assert vault.root_dir == vault_dir

def test__init__create_not_exists_dir(tmp_path):
    # Arrange
    root_dir = tmp_path / "vault"
    # Act
    vault = snr.vault.Vault(root_dir, create_root_dir=True)
    # Assert
    assert vault.root_dir == root_dir
    assert root_dir.exists()

@pytest.mark.parametrize("root_dir, error", [
    (None, ValueError),
    ("dir_is_not_path", TypeError),
    (Path("dir_does_not_exist"), FileNotFoundError),
    (Path("./readme.md"), NotADirectoryError),
])
def test__init__raise_error(root_dir, error):
    # Act & Assert
    with pytest.raises(error):
        snr.vault.Vault(root_dir)

def test_open_note(vault, simple_note):
    # Arrange
    filename = simple_note["filename"]
    # Act
    result = vault.open_note(filename)
    # Assert
    assert result is not None
    assert type(result) == snr.vault.Note
    assert result.filename == filename
    assert result.content == simple_note['content']

def test_open_note_not_existing(vault):
    # Arrange
    filename = "not_exists.md"
    # Act
    result = vault.open_note(filename)
    # Assert
    assert result is not None
    assert type(result) == snr.vault.Note
    assert result.filename == filename
    assert result.content is None

def test_open_note_with_duplicite_name(vault):
    # Arrange
    filename = "simple_with_header"
    # Act
    result = vault.open_note(filename)
    # Assert
    assert result is not None
    assert type(result) == list
    assert len(result) == 2
    assert type(result[0]) == snr.vault.Note 
    assert type(result[1]) == snr.vault.Note 

def test_find_by_path(vault_dir, all_notes):
    # Arrange
    vault = snr.vault.Vault(vault_dir)
    # Act
    notes = vault.find_note_by_path("*")
    # Assert
    assert len(notes) == len(all_notes)
    assert all(map(lambda n: isinstance(n, snr.vault.Note), notes))
    assert notes[0].content is not None

def test_find_by_path_not_recursive(vault_dir, all_notes):
    # Arrange
    vault = snr.vault.Vault(vault_dir)
    # Act
    notes = vault.find_note_by_path("*", recursive=False)
    # Assert
    assert len(notes) == len([n for n in all_notes if "/" not in n['filename']]) 

def test_save_note(vault: snr.vault.Vault):
    # Arrange
    note = snr.vault.Note("test", textwrap.dedent("""
            ---
            title: Note title 
            tags: [tag1, tag2]
            ---
            # Title 

            Some content
            ---
            """).strip())
    # Act
    vault.save_note(note)
    # Assert
    stored_note = vault.open_note("test", deep_search=False)
    
    assert stored_note.content == note.content
