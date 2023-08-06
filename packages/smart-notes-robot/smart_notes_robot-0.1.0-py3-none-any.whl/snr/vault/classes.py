from snr.vault.md import extract_header, extract_markdown

from pathlib import Path
from yaml import unsafe_load, dump
from glob import glob



class Note:

    def __init__(self, filename: str, content: str = None):
        """Initializes a new Note object.

        Args:
            filename (str): The name of the note, including the .md extension.
            content (str, optional): The content of the note. Defaults to None.

        Raises:
            ValueError: If the name does not end in .md.
            TypeError: If name is not a string.
        """
        try:
            if not filename.endswith(".md"):
                if __debug__:
                    print(f"Add suffix '.md' to name {filename}")
                filename += '.md'
            if not isinstance(filename, str):
                raise TypeError("Note filename must be a string")
            path = Path(filename)
            if not path.is_file:
                raise ValueError(f"filename {filename!r} is not valid file path")
            if path.is_absolute():
                raise ValueError(
                    f"filename {filename!r} is not relative to vault folder")
            self.__path = path

            if content:
                if not isinstance(content, str):
                    raise TypeError(f"content is not str but {type(content)}")
            self.__content = content
        except OSError as exc:
            raise ValueError(f"filename {filename!r} is not valid path") from exc

    @property
    def filename(self) -> str:
        """Returns the name of the note with the .md extension.

        Returns:
            str: The name of the note.
        """
        return str(self.__path)

    @property
    def content(self) -> str:
        """Returns the content of the note as a string.

        Returns:
            str: The content of the note.
        """
        return self.__content

    def __str__(self) -> str:
        return self.__content

    def __repr__(self) -> str:
        if not self.content:
            content = type(self.content)
        else:
            content = self.content if len(
                self.content) < 32 else f"{self.content[:32]} ... {len(self.content)} total size"
        return f"Note(filename={self.filename!r}, content='{content!r}')"

    @property
    def header(self):
        if not hasattr(self, "_Note__header"):
            extract = extract_header(self.content)
            self.__header = Note.Header(self, extract)
        return self.__header

    @property
    def markdown(self):
        if not hasattr(self, "_Note__markdown"):
            c = self.content
            extract = extract_markdown(c)
            self.__markdown = extract
        return self.__markdown

    class Header:

        COMMENT_LABEL = "#"
        KEY_TAGS = "tags"

        def __init__(self, note: "Note", header: str):
            if not note:
                raise ValueError("Parameter note is None.")
            if not isinstance(note, Note):
                raise TypeError(
                    f"Parameter note is not type 'Note' but {type(note)}.")
            self.__note = note

            if header:
                if not isinstance(header, str):
                    raise TypeError(
                        f"Parameter note is not type 'str' but {type(header)}.")
            self.__header = header

        def __str__(self) -> str:
            return self.__header or ""

        def __repr__(self) -> str:
            return f"Note.Header(note={self.__note!r}, len={len(self.__header or '')})"

        def __as_dict(self) -> dict:
            try:
                if not self.__header:
                    return dict()
                # Remove comment lines, the yaml library can't work with it
                data = '\n'.join(filter(
                    lambda line: not line.strip().startswith(self.COMMENT_LABEL),
                    self.__header.splitlines()
                ))
                return unsafe_load(data[4:-4])
            except Exception as exc:
                raise ValueError(
                    f"Can not parse header {self.__header!r}") from exc

        def tags(self) -> list[str]:
            """Return the list of tags for this note header."""
            try:
                data = self.__as_dict()
                return tuple(data.get(self.KEY_TAGS, tuple()))
            except Exception as exc:
                raise ValueError(
                    f"Can not parse header {self.__header!r}") from exc

        def remove_tag(self, tag: str) -> 'Note':
            """Remove a tag from the note metadata.  

            Removes the given ptag from the list of tags in the note metadata.
            If the tag does not exist, no changes are made.

            Args:
                tag (str): The tag to remove.

            Returns:
                Note: The Note object.

            Raises:
                ValueError: If the note metadata cannot be parsed.
            """
            try:
                data = self.__as_dict()
                if self.KEY_TAGS not in data:
                    return self.__note
                tags = list(data[self.KEY_TAGS])
                if tag not in tags:
                    return self.__note
                
                tags.remove(tag)
                data[self.KEY_TAGS] = tags
                comments = '\n'.join(
                    map(str.strip,
                        filter(lambda line: line.strip().startswith(self.COMMENT_LABEL),
                               self.__header.splitlines()
                               )
                        )
                )
                if comments:
                    comments += '\n'
                new_header = f"---\n{comments}{dump(data)}---\n"
                old_markdown = extract_markdown(str(self.__note))
                filename = self.__note.filename
                return Note(
                    filename,
                    content=new_header+old_markdown
                )
            except Exception as exc:
                raise ValueError(
                    f"Can remove tag {tag} from header {self.__header!r}") from exc

class Vault:
    """Represents a collection of smart notes stored in a folder.

    A Vault is responsible for opening notes, storing new notes, and searching existing notes.

    ## Example of usage
    - Creating a Vault from a './vault_dir' path.
    - Checking the length of the Vault is 3 notes.
    - Accessing the first note.
    - Checking the name of the first note is 'note1'.

    >>> vault = Vault(Path('./vault_dir'))
    >>> len(vault)
    3
    >>> note = vault[0]
    >>> note.name
    'note1'

    Attributes:
        root_dir (Path): The path to the folder containing the Vault.
    """

    def __init__(self, root_dir: Path, *, create_root_dir: bool = False) -> None:
        """Initialize a new Vault.

        Args:
            root_dir (Path): The path to the directory containing the Vault.
            create_not_exists_dir (bool, optional): Whether to create the directory if it does not exist, but not parents!!!. Defaults to False.

        Raises:
            ValueError: If root_dir is None.
            TypeError: If root_dir is not a Path.
            FileNotFoundError: If root_dir does not exist and create_root_dir is False.
            NotADirectoryError: If root_dir is not a directory.
        """

        if not root_dir:
            raise ValueError("root_dir cannot be None")
        if not isinstance(root_dir, Path):
            raise TypeError(f"root_dir must be a Path, got {type(root_dir)}")
        if not root_dir.exists():
            if create_root_dir:
                if __debug__:
                    print(f"root_dir {root_dir} is created.")
                root_dir.mkdir()
            else:
                raise FileNotFoundError(f"root_dir {root_dir} does not exist")
        if not root_dir.is_dir():
            raise NotADirectoryError(f"root_dir {root_dir} is not a directory")
        self.__root_dir = root_dir

    def __repr__(self):
        return f"Vault(root_dir={self.__root_dir!r})"

    def __str__(self):
        return f"Vault at {self.__root_dir}"

    @property
    def root_dir(self) -> Path:
        return self.__root_dir

    def open_note(self, filename: str, *, deep_search=True) -> Note | list[Note]:
        """Create instance of a note or notes from the vault.  

        Searches for notes matching the given filename. By default, performs a deep, recursive search 
        through subdirectories. If multiple notes share the same name, returns a list of notes. 
        Otherwise, returns a single Note object.

        Args: 
            filename (str): The name of the note(s) to open.
            deep_search (bool, optional): Whether to search recursively through subdirectories. Defaults to True.
        Returns: 
            Note or list[Note]: Either a single Note object or a list of Note objects.
        Raises:
            ValueError: If the note could not be opened.
        """
        try:
            if not filename.endswith(".md"):
                filename += '.md'
            search = f"**/{filename}" if deep_search else filename
            if found := glob(search, root_dir=self.root_dir, recursive=deep_search):
                if __debug__:
                    print(f"For name {filename} found: {found} files.")
                notes = []
                for file in found:
                    full_path = self.root_dir / file
                    assert full_path.is_relative_to(
                        self.root_dir), f"File {full_path} is outside vault root directory."

                    with open(full_path, mode="r", encoding="utf-8") as f:
                        note = Note(file, f.read())
                        notes.append(note)
                return notes[0] if len(notes) == 1 else notes
            else:
                return Note(filename, None)
        except Exception as exc:
            raise ValueError(f"Open note {filename} failed.") from exc

    def find_note_by_path(self, path_expression: str, recursive=True) -> list[Note]:
        """
        Retrieve a list of 'Note' objects based on a given 'path_expression' that can be a pattern
        representing the location of the desired notes. By default, the search is performed recursively
        through subdirectories unless 'recursive' is set to False.

        Args: 
            path_expression: A string representing the pattern used to locate the desired notes.
            recursive: A boolean indicating whether the search should be performed recursively through
                        subdirectories. Defaults to True.
        Returns: 
            A list of 'Note' objects matching the given 'filename'.

        Raises: 
            ValueError: If the provided 'path_expression' is not valid.
        """
        try:
            if not path_expression.endswith(".md"):
                path_expression += '.md'
            if recursive and not path_expression.startswith("**/"):
                path_expression = "**/" + path_expression

            files = glob(path_expression, root_dir=self.root_dir,
                         recursive=recursive)
            return [self.open_note(file, deep_search=False) for file in files]

        except Exception as exc:
            raise ValueError(
                f"Paremeter {path_expression} is nor valid.") from exc

    def save_note(self, note: "Note"):
        """Persist a note to the vault.  

        Stores the note content to a file named after the note's filename attribute.
        If the filename does not end in .md, .md is appended. 

        Args:
            note (Note): The note to be stored.

        Raises:
            ValueError: If the note could not be saved.
        """
        try:
            filename = note.filename
            if not filename.endswith(".md"):
                filename += '.md'
            filename = self.root_dir / filename

            with open(filename, mode="w", encoding="utf-8") as f:
                f.write(str(note))
        except Exception as exc:
            raise ValueError(
                f"Note save failed.") from exc