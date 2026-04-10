"""Layer 3: read_gsb_file integration tests.

Tests GsbFile construction from inline XML. Does NOT re-assert individual
field values — Layer 2 already covers that. These tests focus on dispatch,
cardinality, and tolerant-parsing behaviour.
"""

from pathlib import Path

import pytest

from gsbparse.adapters.xml.reader import read_gsb_file
from gsbparse.domain.errors import InvalidGsbFileError, InvalidGsbFileRootError


def _write_gsb(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "test.gsb"
    path.write_text(content, encoding="utf-8")
    return path


class TestRootValidation:
    def test_raises_on_malformed_xml(self, tmp_path):
        path = _write_gsb(tmp_path, "not xml at all <<<")
        with pytest.raises(InvalidGsbFileError):
            read_gsb_file(path)

    def test_raises_on_wrong_root_tag(self, tmp_path):
        path = _write_gsb(tmp_path, '<?xml version="1.0"?><NotGrisbi />')
        with pytest.raises(InvalidGsbFileRootError):
            read_gsb_file(path)


class TestDispatch:
    def test_currencies_parsed_into_list(self, tmp_path):
        dummy_nb_1 = "1"
        dummy_nb_2 = "2"
        path = _write_gsb(
            tmp_path,
            f"""<?xml version="1.0"?>
            <Grisbi>
                <Currency Nb="{dummy_nb_1}" Na="Euro" Co="E" Ico="EUR" Fl="2" />
                <Currency Nb="{dummy_nb_2}" Na="Dollar" Co="$" Ico="USD" Fl="2" />
            </Grisbi>""",
        )

        gsb = read_gsb_file(path)

        assert gsb.currencies is not None
        assert len(gsb.currencies) == 2
        assert gsb.currencies[0].Nb == int(dummy_nb_1)
        assert gsb.currencies[1].Nb == int(dummy_nb_2)

    def test_absent_section_is_none(self, tmp_path):
        path = _write_gsb(tmp_path, '<?xml version="1.0"?><Grisbi />')

        gsb = read_gsb_file(path)

        assert gsb.currencies is None
        assert gsb.transactions is None
        assert gsb.general is None

    def test_unknown_tag_is_skipped(self, tmp_path, caplog):
        import logging

        path = _write_gsb(
            tmp_path,
            '<?xml version="1.0"?><Grisbi><UnknownTag Foo="bar" /></Grisbi>',
        )

        with caplog.at_level(logging.WARNING):
            gsb = read_gsb_file(path)

        assert gsb.currencies is None
        assert any("UnknownTag" in record.message for record in caplog.records)

    def test_empty_list_sections_become_none(self, tmp_path):
        path = _write_gsb(tmp_path, '<?xml version="1.0"?><Grisbi />')

        gsb = read_gsb_file(path)

        assert gsb.accounts is None
        assert gsb.parties is None

    def test_singleton_sections_dispatched(self, tmp_path):
        dummy_color = "(null)"
        path = _write_gsb(
            tmp_path,
            f"""<?xml version="1.0"?>
            <Grisbi>
                <RGBA
                    Background_color_0="{dummy_color}"
                    Background_color_1="{dummy_color}"
                    Couleur_jour="{dummy_color}"
                    Background_scheduled="{dummy_color}"
                    Background_archive="{dummy_color}"
                    Selection="{dummy_color}"
                    Background_split="{dummy_color}"
                    Text_color_0="{dummy_color}"
                    Text_color_1="{dummy_color}"
                    Couleur_bet_division="{dummy_color}"
                    Couleur_bet_future="{dummy_color}"
                    Couleur_bet_solde="{dummy_color}"
                    Couleur_bet_transfert="{dummy_color}"
                />
            </Grisbi>""",
        )

        gsb = read_gsb_file(path)

        assert gsb.rgba is not None
        assert gsb.rgba.Background_color_0 == dummy_color
