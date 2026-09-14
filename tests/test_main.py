import os
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

import yaml

from main import parse_dlc_plain, parse_gfwlist_text, release_quanx_file


class ParseDLCTests(unittest.TestCase):
    def test_collects_cn_from_all_lists_and_deduplicates_each_rule_type(self):
        apple = "full:init-p01st.push.apple.com:@cn"
        source = {
            "lists": [
                {"name": "geolocation-cn", "rules": ["domain:base.cn", apple]},
                {"name": "geolocation-!cn", "rules": ["domain:apple.com"]},
                {
                    "name": "apple",
                    "rules": [
                        apple,
                        "full:extra.example:@ads,@cn",
                        "domain:cdn.example:@cn,@other",
                        "keyword:china-service:@cn",
                        r"regexp:^cn[0-9]+\.example$:@cn",
                        "full:foreign.example:@!cn",
                        "full:similar.example:@cn2",
                        "full:untagged.example",
                    ],
                },
                {
                    "name": "duplicate",
                    "rules": [
                        apple,
                        "keyword:china-service:@cn",
                        r"regexp:^cn[0-9]+\.example$:@cn",
                    ],
                },
            ]
        }
        with patch(
            "main.urlopen", return_value=BytesIO(yaml.safe_dump(source).encode())
        ):
            rules = parse_dlc_plain("fixture", ("geolocation-cn", "geolocation-!cn"))
        self.assertEqual(
            rules["geolocation-cn"],
            (
                ["init-p01st.push.apple.com", "extra.example"],
                ["base.cn", "cdn.example"],
                ["china-service"],
                [r"^cn[0-9]+\.example$"],
            ),
        )
        self.assertEqual(rules["geolocation-!cn"], ([], ["apple.com"], [], []))

    def test_missing_cn_list_is_still_an_error(self):
        source = b'lists:\n- name: apple\n  rules: ["full:example.com:@cn"]\n'
        with (
            patch("main.urlopen", return_value=BytesIO(source)),
            self.assertRaisesRegex(ValueError, "Missing DLC tags: geolocation-cn"),
        ):
            parse_dlc_plain("fixture", ("geolocation-cn",))


class ParseGFWListTests(unittest.TestCase):
    def test_converts_current_autoproxy_rule_forms(self) -> None:
        source = r"""[AutoProxy 0.2.9]
! metadata
||example.com
||cdn*.assets.example/path
|https://exact.example/a/path
|http://*.wild.example/
plain.example
/^https?:\/\/[^\/]+blogspot\.(.*)/
@@||direct.example
@@/^https?:\/\/(?=.*?(2x3|ni5|j5o))[a-z0-9.-]+\.xn--ngstr-lra8j\.com$
"""

        rules = parse_gfwlist_text(source.encode())
        domain, domain_suffix, domain_keyword, domain_regex = rules["gfw"]

        self.assertEqual(domain, ["exact.example", "plain.example"])
        self.assertEqual(
            domain_suffix, ["example.com", "assets.example", "wild.example"]
        )
        self.assertEqual(domain_keyword, [])
        self.assertEqual(domain_regex, [r"[^\/]+blogspot\.(.*)"])
        self.assertEqual(rules["gfw-skip"][1], ["direct.example"])
        self.assertEqual(
            rules["gfw-skip"][3],
            [r"^[a-z0-9.-]*(?:2x3|ni5|j5o)[a-z0-9.-]*\.xn--ngstr-lra8j\.com$"],
        )

    def test_rejects_non_gfwlist_data(self) -> None:
        with self.assertRaisesRegex(ValueError, "header"):
            parse_gfwlist_text(b"not a gfwlist")

    def test_gfw_quanx_rules_use_proxy_policy(self) -> None:
        previous_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            os.chdir(directory)
            try:
                Path("dist").mkdir()
                release_quanx_file(
                    "gfw", ["exact.example"], ["suffix.example"], [], "proxy"
                )
                output = Path("dist/gfw.quanx").read_text()
            finally:
                os.chdir(previous_cwd)

        self.assertEqual(
            output,
            "host, exact.example, proxy\n"
            "host-suffix, suffix.example, proxy\n",
        )


if __name__ == "__main__":
    unittest.main()
