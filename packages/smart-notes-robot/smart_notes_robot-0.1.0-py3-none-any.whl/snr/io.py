from os import getcwd
from pathlib import Path

from snr.vault import Vault


def open_vault(dir: str = getcwd()) -> Vault:
    """Opens a Vault (collection of notes) from the given directory.

    >>> open_vault('./vault_dir')
    <Vault: './vault_dir'>

    Args:
        dir (str, optional): The path to the directory containing the Vault. 
            Defaults to the current working directory.

    Returns:
        Vault: An object representing the opened Vault.

    Raises:
        ValueError: If the Vault could not be opened from the given path.
    """
    try:
        path = Path(dir)
        return Vault(path)
    except Exception as exc:
        raise ValueError(f"Can not open vault from path: {path}") from exc

if __name__ == '__main__':
    import doctest
    doctest.testmod()