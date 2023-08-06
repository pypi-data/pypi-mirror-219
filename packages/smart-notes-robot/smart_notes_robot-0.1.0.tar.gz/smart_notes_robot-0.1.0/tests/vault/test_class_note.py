import pytest
import snr.vault


def test__init__(simple_note_with_header):
    # Act
    note = snr.vault.Note(**simple_note_with_header)
    # Assert
    assert type(note) is snr.vault.Note
    assert note.filename == simple_note_with_header["filename"]
    assert note.content == simple_note_with_header["content"]

def test__init__file_not_exists():
    # Arrange
    filename = 'file_not_exists.md'
    # Act
    note = snr.vault.Note(filename)
    # Assert
    assert type(note) is snr.vault.Note
    assert note.filename == filename
    assert note.content is None

def test__repr__(simple_note_with_header):
    # Arrange
    note = snr.vault.Note(**simple_note_with_header)
    # Act
    result = repr(note)
    # Assert
    assert "Note" in result
    assert f"filename='{note.filename}'" in result
    assert f"content=" in result

def test__str__(simple_note_with_header):
    # Arrange
    note = snr.vault.Note(**simple_note_with_header)
    # Act
    content = str(note)
    # Assert
    assert content == simple_note_with_header["content"]

def test_property_header_None(simple_note):
    # Arrange
    note = snr.vault.Note(**simple_note)
    # Act
    header = note.header
    # Assert
    assert header is not None
    assert isinstance(header, snr.vault.Note.Header)
    assert str(header) == ""

def test_property_header_exists(simple_note_with_header):
    # Arrange
    note = snr.vault.Note(**simple_note_with_header)
    # Act
    header = note.header
    # Assert
    assert header is not None
    assert isinstance(header,snr.vault.Note.Header)
    assert str(header) == simple_note_with_header['content'][:69]

class TestHeader:

    def test_getting_tags_from_header(self, simple_note_with_header):
        # Arrange
        note = snr.vault.Note(**simple_note_with_header)
        header = note.header
        # Act
        tags = header.tags()
        # Assert
        assert tags == ("Honza",)

    def test_removing_tag_from_header(self, simple_note_with_header):
            # Arrange
            note = snr.vault.Note(**simple_note_with_header)
            header = note.header
            # Act
            result = header.remove_tag("Honza")
            # Assert
            assert isinstance(result, snr.vault.Note)
            assert "Honza" not in result.header.tags()

    def test_removing_not_contains_tag_from_header(self, simple_note_with_header):
        # Arrange
        note = snr.vault.Note(**simple_note_with_header)
        header = note.header
        # Act
        result = header.remove_tag("Not_contains")
        # Assert
        assert isinstance(result, snr.vault.Note)
        assert "Not_contains" not in result.header.tags()
