import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_catalog


class BuildCatalogTests(unittest.TestCase):
    def test_pack_digest_uses_lf_canonical_bytes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            pack = Path(temporary_directory) / "PCSA00008.psv"
            pack.write_bytes(
                b"# Title: Example\r\n"
                b"# Region: US\r"
                b"# Version: 1.00\n"
                b"_V0 Test\r\n"
                b"$0200 81000000 00000001\r"
            )

            entry = build_catalog.build_entry(pack, "PCSA00008", "")

        expected = hashlib.sha256(
            b"# Title: Example\n"
            b"# Region: US\n"
            b"# Version: 1.00\n"
            b"_V0 Test\n"
            b"$0200 81000000 00000001\n"
        ).hexdigest()
        self.assertEqual(expected, entry["sha256"])

    def test_normalizer_handles_crlf_lf_and_cr(self):
        self.assertEqual(
            b"one\ntwo\nthree\n",
            build_catalog.canonical_pack_bytes(b"one\r\ntwo\nthree\r"),
        )

    def test_catalog_json_writer_keeps_lf_on_windows(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "catalog.json"
            build_catalog.write_json(output, {"entryCount": 1})

            self.assertEqual(b'{\n  "entryCount": 1\n}\n', output.read_bytes())

    def test_pack_count_includes_vita_parser_empty_name_declarations(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            pack = Path(temporary_directory) / "PCSA00008.psv"
            pack.write_bytes(b"_V0\n$0000 00000000 00000000\n_V1 Named\n")

            _, block_count = build_catalog.parse_pack(pack)

        self.assertEqual(2, block_count)


if __name__ == "__main__":
    unittest.main()
