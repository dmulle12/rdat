# rdat

Automatically generates and publishes domain rule sets for Clash, Surge, Quantumult X, sing-box, and V2Ray GeoSite.

## Rules

Rule data comes from `dlc.dat_plain.yml` published by
[`v2fly/domain-list-community`](https://github.com/v2fly/domain-list-community),
plus the plain-text rules from the official
[`gfwlist/gfwlist`](https://github.com/gfwlist/gfwlist), and is grouped into these five tags:

- `reject`: merged from `category-ads-all`, all rules with the `@ads` attribute, plus manual ad-block additions
- `gfw`: proxy domains from the official GFWList
- `gfw-skip`: GFWList whitelist plus additional direct-connect domains
- `loc-!cn`: domains outside mainland China
- `loc-cn`: direct-connect rules for mainland China networks, merged from `geolocation-cn`, all rules with the `@cn` attribute, plus manual direct-connect additions

The upstream `domain-list-community` file already performs rule expansion, attribute filtering, and deduplication.

URL and wildcard rules in GFWList are converted into domain rules, while whitelist exceptions are written separately into `gfw-skip`.

This project extracts, supplements, and converts those rules into client-specific formats.

`@cn` and `@ads` are matched by full attribute name only, excluding other attributes such as `@!cn` and `@!ads`, and results are deduplicated after merging. `@cn` does not guarantee that the server is physically located in mainland China. Rules that contain both `@cn` and `@ads` are included in both sets. Clients should match in this order: `reject` → `loc-cn` → `loc-!cn`, so ad blocking takes priority over direct connection and any domain overlap is handled correctly.

## Release

GitHub Actions builds once per day and also builds automatically when `main` is updated. Artifacts are published to the `rel` branch, which is rebuilt on each release and only keeps the latest output.

| Path              | Format                                       |
| ----------------- | -------------------------------------------- |
| `<tag>.yaml`      | Clash Rule Provider                          |
| `<tag>.list`      | Surge Domain Set                             |
| `<tag>.quanx`     | Quantumult X Filter                          |
| `<tag>.srs`       | sing-box Binary Rule Set                     |
| `geosite.dat`     | V2Ray GeoSite, includes `reject`, `loc-!cn`, `loc-cn` |
| `geosite-cn.dat`  | V2Ray GeoSite, includes `loc-cn`             |
| `geosite-gfw.dat` | V2Ray GeoSite, includes `gfw`, `gfw-skip`    |
| `ext/*.quanx`     | Quantumult X rewrite rules                   |
| `ext/*.sgmodule`  | Surge modules                                |

Download URL format:

```text
https://github.com/lauyv/rdat/raw/rel/<file-path>
```

For example:

```text
https://github.com/lauyv/rdat/raw/rel/loc-cn.srs
https://github.com/lauyv/rdat/raw/rel/ext/bili.quanx
https://github.com/lauyv/rdat/raw/rel/ext/bili.sgmodule
```

## Project structure

```text
.
├── main.py                    # Rule generator
├── source/                    # Manually maintained rewrite rules and modules
├── js/                        # JavaScript scripts
├── example/                   # Client configuration examples
├── tests/                     # Rule parsing tests
├── .github/workflows/build.yml
├── pyproject.toml
└── uv.lock
```

## Build locally

Requires Python 3.12, [uv](https://docs.astral.sh/uv/), and
[sing-box](https://sing-box.sagernet.org/).

```bash
uv sync
uv run python main.py
```

Build artifacts are output to `dist/`.
