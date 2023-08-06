import pytest
import os
import snr
import snr.vault

from pathlib import Path

class Test_open_vault:

    def test_open_vault_with_current_dir(self):
        # Act
        vault = snr.open_vault()
        # Assert
        assert isinstance(vault, snr.vault.Vault)
        assert vault.root_dir == Path(os.getcwd())


    def test_opening_existing_vault(self, vault_dir):
        # Act
        vault = snr.open_vault(vault_dir)
        # Assert
        assert isinstance(vault, snr.vault.Vault)
        assert vault.root_dir == vault_dir

    @pytest.mark.parametrize("dir", [
        "abc",
        "tests/test_io.py"
    ])
    def test_open_vault_with_notexisting_dir(self, dir):
        # Act
        with pytest.raises(Exception) as exc:
            snr.open_vault(dir)