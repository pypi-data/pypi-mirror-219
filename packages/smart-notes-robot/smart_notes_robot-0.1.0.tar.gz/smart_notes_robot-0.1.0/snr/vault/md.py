def extract_header(note: str, *, header_separator='---\n') -> None | str :
    """Retrieve metadata from a note string.

    The metadata, containing specific information about the note, is enclosed by a designated string,
    which is set as '---\n' by default. If the metadata is not found, the function returns None.

    Args:
        note (str): The string content of the note.
        header_separator (str, optional): The string used to mark the metadata section.
            Defaults to '---\n'.

    Returns:
        str or None: The extracted metadata string or None if metadata is not found.

    Raises:
        ValueError: If the note string cannot be processed.
    """
    try:
        if not note.startswith(header_separator):
            return None
        lhs = len(header_separator)
        header_end = note.index(header_separator, lhs)
        if not header_end:
            return  None
        header = note[:header_end + lhs]
        return header
    except ValueError:
        if __debug__: print(f"Note start with header symbol, but do not finish it, {note}.")
        return None
    except Exception as exc:
        raise ValueError(f"Note is not procesible.") from exc
    
def extract_markdown(note: str, *, header_separator='---\n') -> str:
    """Get the markdown part of note as a string.

    Removes the metadata header and header separator from the note string and returns the remaining 
    Markdown content.

    Args:
        note (str): The string content of the note.
        header_separator (str, optional): The string used to mark the metadata section. 
            Defaults to '---\n'.

    Returns:
        str: The Markdown content of the note.

    Raises:
        ValueError: If the note string cannot be processed.
    """
    try:
        if note.count(header_separator) >= 2:
            lhs = len(header_separator)
            content_start = note.index(header_separator, lhs)
            return note[content_start+lhs:]
        return note
    except Exception as exc:
        raise ValueError(f"Note is not procesible.") from exc