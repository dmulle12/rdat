# rdat

自动生成并发布适用于 Clash、Surge、Quantumult X、sing-box 和 V2Ray GeoSite 的域名规则。

## 规则

规则数据来自
[`v2fly/domain-list-community`](https://github.com/v2fly/domain-list-community)
发布的 `dlc.dat_plain.yml`，以及官方
[`gfwlist/gfwlist`](https://github.com/gfwlist/gfwlist) 明文规则，生成以下五个标签：

- `reject`：广告及补充拦截域名
- `gfw`：官方 GFWList 中的代理域名
- `gfw-skip`：GFWList 白名单，以及补充直连域名
- `loc-!cn`：非中国大陆域名
- `loc-cn`：面向中国大陆网络的直连规则，合并 `geolocation-cn`、所有列表中带 `@cn` 属性的规则，以及手工直连补充

`domain-list-community` 上游文件已经完成规则展开、属性过滤和去重。

GFWList 的 URL 及通配符规则会转换为域名规则，白名单例外单独写入 `gfw-skip`。

本项目负责提取、补充并转换为各客户端格式。

`@cn` 按完整属性名匹配，不包含 `@!cn`。合并后去重；`@cn` 不保证服务器位于境内。使用 `loc-cn` 和 `loc-!cn` 时，应将 `loc-cn` 的直连规则放在 `loc-!cn` 的代理规则之前，处理可能存在的域名覆盖重叠。

## 发布

GitHub Actions 每天构建一次，并在 `main` 更新时自动构建。产物发布到 `rel` 分支；该分支每次发布都会重建，只保留最新结果。

| 路径              | 格式                                              |
| ----------------- | ------------------------------------------------- |
| `<tag>.yaml`      | Clash Rule Provider                               |
| `<tag>.list`      | Surge Domain Set                                  |
| `<tag>.quanx`     | Quantumult X Filter                               |
| `<tag>.srs`       | sing-box Binary Rule Set                          |
| `geosite.dat`     | V2Ray GeoSite，包含 `reject`、`loc-!cn`、`loc-cn` |
| `geosite-cn.dat`  | V2Ray GeoSite，包含 `loc-cn`                      |
| `geosite-gfw.dat` | V2Ray GeoSite，包含 `gfw`、`gfw-skip`             |
| `ext/*.quanx`     | Quantumult X 重写规则                             |
| `ext/*.sgmodule`  | Surge 模块                                        |

下载地址格式：

```text
https://github.com/lauyv/rdat/raw/rel/<文件路径>
```

例如：

```text
https://github.com/lauyv/rdat/raw/rel/loc-cn.srs
https://github.com/lauyv/rdat/raw/rel/ext/bili.quanx
https://github.com/lauyv/rdat/raw/rel/ext/bili.sgmodule
```

## 项目结构

```text
.
├── main.py                    # 规则生成器
├── source/                    # 手工维护的重写规则和模块
├── js/                        # JS 脚本
├── example/                   # 客户端配置示例
├── tests/                     # 规则解析测试
├── .github/workflows/build.yml
├── pyproject.toml
└── uv.lock
```

## 本地构建

需要 Python 3.12、[uv](https://docs.astral.sh/uv/) 和
[sing-box](https://sing-box.sagernet.org/)。

```bash
uv sync
uv run python main.py
```

构建产物位于 `dist/`。
