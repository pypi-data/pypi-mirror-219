import pytest
import textwrap

from snr.vault import md


class Test_extract_header:

    def test_extract_header_no_header(self):
        # Arrange
        note = textwrap.dedent("""
            # Title

            Some content
            """).strip()
        # Act
        header = md.extract_header(note)
        # Assert
        assert header is None

    def test_extract_header_with_header(self):
        # Arrange
        note = textwrap.dedent("""
            ---
            title: Note title 
            tags: [tag1, tag2]
            ---
            # Title 

            Some content
            ---
            """).strip()
        # Act
        header = md.extract_header(note)
        # Assert
        assert header == note[:note.index("# Title")]

    def test_extract_header_invalid_note(self):
        # Arrange
        note = textwrap.dedent("""
            ---
            title: Note title 
            tags: [tag1, tag2]
            # Title 

            Some content
            """).strip()
        # Act
        header = md.extract_header(note)
        # Assert
        assert header is None

class Test_extract_markdown:

    def test_extract_header_no_header(self):
        # Arrange
        note = textwrap.dedent("""
            # Title

            Some content
            """).strip()
        # Act
        markdown = md.extract_markdown(note)
        # Assert
        assert markdown == note

    def test_extract_header_with_header(self):
        # Arrange
        note = textwrap.dedent("""
            ---
            title: Note title 
            tags: [tag1, tag2]
            ---
            # Title 

            Some content
            ---
            """).strip()
        # Act
        markdown = md.extract_markdown(note)
        # Assert
        assert markdown == note[46:]