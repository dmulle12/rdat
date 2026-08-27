# rdat

自动生成并发布适用于 Clash、Surge、Quantumult X、sing-box 和 V2Ray GeoSite 的域名规则。

## 规则

规则数据来自
[`v2fly/domain-list-community`](https://github.com/v2fly/domain-list-community)
发布的 `dlc.dat_plain.yml`，生成以下三个标签：

- `reject`：广告及补充拦截域名
- `loc-!cn`：非中国大陆域名
- `loc-cn`：中国大陆及补充直连域名

上游文件已经完成规则展开、属性过滤和去重，本项目负责提取、补充并转换为各客户端格式。

## 发布

GitHub Actions 每天构建一次，并在 `main` 更新时自动构建。产物发布到 `rel` 分支；该分支每次发布都会重建，只保留最新结果。

| 路径                 | 格式                           |
| -------------------- | ------------------------------ |
| `<tag>.yaml`         | Clash Rule Provider            |
| `<tag>.list`         | Surge Domain Set               |
| `<tag>.quanx`        | Quantumult X Filter            |
| `<tag>.srs`          | sing-box Binary Rule Set       |
| `geosite.dat`        | V2Ray GeoSite，包含全部标签    |
| `geosite-cn.dat`     | V2Ray GeoSite，仅包含 `loc-cn` |
| `rewrite/*.quanx`    | Quantumult X 重写规则          |
| `rewrite/*.sgmodule` | Surge 模块                     |

下载地址格式：

```text
https://github.com/lauyv/rdat/raw/rel/<文件路径>
```

例如：

```text
https://github.com/lauyv/rdat/raw/rel/loc-cn.srs
https://github.com/lauyv/rdat/raw/rel/rewrite/bili.quanx
https://github.com/lauyv/rdat/raw/rel/rewrite/bili.sgmodule
```

## 项目结构

```text
.
├── main.py                    # 规则生成器
├── source/                    # 手工维护的重写规则和模块
├── js/                        # JS 脚本
├── example/                   # 客户端配置示例
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
