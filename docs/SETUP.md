# phdsx 的 GitHub 主页仓库

直接打开根目录的 `preview.html` 可预览整个主页，并切换浅色与深色。所有插画、图表和贡献动画均已生成成本地 SVG，预览不需要安装依赖或启动服务。真实的 GitHub README 排版以 GitHub 渲染为准。

## 本地更新

需要 Python 3.10 或以上版本，不需要第三方包。在仓库目录执行：

```powershell
python scripts/build_illustrations.py
python scripts/update_profile.py
python scripts/build_preview.py
```

`update_profile.py` 会读取 phdsx 的 GitHub 公开资料、公开仓库、仓库语言字节数和贡献日历。未登录的 GitHub API 存在请求频率限制；需要更高额度时，可以在当前终端配置 `GITHUB_TOKEN`，脚本只会把它发送到 `api.github.com`，不会保存到文件。

完全离线时可从已有快照重新生成：

```powershell
python scripts/update_profile.py --offline
python scripts/build_preview.py
```

## 修改内容与配色

- 修改文字、模块顺序和链接：编辑 `README.template.md`，然后重新运行生成脚本。
- 修改图表：编辑 `scripts/update_profile.py` 的配色或相应绘图函数。
- 修改插画：编辑 `scripts/build_illustrations.py`，或直接修改 `assets/illustrations/` 中的 SVG。SVG 可使用浏览器或矢量编辑器打开。
- 封面与页脚：`assets/header.svg` 与 `assets/footer.svg`。
- README 由模板生成；直接修改 `README.md` 会在下次更新时被覆盖。

## 数据与统计口径

原始公开快照位于 `data/github-public.json`，含 UTC 获取时间和来源。仓库列表来自账号下的公开仓库，这不意味着所有仓库均为账号所有者原创；项目本身的来源与许可应以各仓库内容为准。

| 模块 | 计算方式 |
| --- | --- |
| 公开仓库 | GitHub REST API 返回的仓库数量 |
| 仓库 Stars / Forks | 这些公开仓库的星标数 / 被 fork 数之和，不是个人收藏数 |
| 年度贡献 | GitHub 公开贡献日历所显示的日期范围与总数；不是所有历史提交数 |
| 连续活跃 | 在该日历范围内，连续有贡献的天数；今天尚无贡献时保留截至昨天的连续记录 |
| 活跃趋势 | 日历中最近 90 个自然日的每日贡献数 |
| 语言占比 | 非 fork 公开仓库的语言字节数汇总，**不等于**个人熟练程度、工作时长或原创代码占比 |
| 贡献蛇 | 网格使用真实贡献等级，移动的蛇是装饰动画，不改变贡献数 |
| 3D 贡献图 | 网格颜色来自真实贡献等级；柱高为 `2 + log₂(贡献数 + 1) × 10` |
| 近期更新 | 公开仓库的最近推送时间，排除主页仓库，按时间降序 |
| 社区卡片 | GitHub 加入年份、关注者数、关注数与公开仓库被 fork 数 |

GitHub 的贡献日历日期口径与个人本地时区可能不同。脚本保留 GitHub 的日期，不额外改写时区。语言统计、贡献数据和仓库信息只能覆盖公开可见范围。

## 以后放到 GitHub

本次只在本地生成，没有推送线上。未来如果要启用 GitHub 主页，把这些文件保留目录结构放入公开的 `phdsx/phdsx` 仓库，默认分支为 `main` 即可。

附带 `.github/workflows/profile.yml`：上传后支持手动运行与每天北京时间 08:23 自动更新，无需额外第三方服务或自建服务器。工作流只使用 GitHub 内置 `GITHUB_TOKEN`。如果仓库禁用了 Actions 或写入权限，需要在仓库设置中启用；分支保护规则也可能限制机器人提交。本地 SVG 仍可直接显示。

## 可按本人资料补充的模块

参考风格来自 [sun0225SUN 的主页](https://github.com/sun0225SUN/sun0225SUN)。这里只借鉴居中布局、分区卡片、插画与贡献可视化的组织方式；装饰 SVG 为本地新绘制，没有搬用其个人资料、账户数据或插画文件。

以下模块需要 phdsx 本人的资料，目前未放入可见主页：

- 博客更新：提供自己的博客地址或 RSS 后，可添加文章列表。
- 社交入口：提供本人 B 站、微信、YouTube 等账号后再加入。
- WakaTime：需要本人公开用户名或 API 数据；不会填入他人的时长、工具或工作习惯。
- 赞助、收款、Repobeats：需要本人对应账号、链接或服务配置。
- 个人经历、职业、爱好与技术熟练程度：需要本人明确给出的内容。

目录中的 `preview.html` 仅用于本地预览，不会自动开启 GitHub Pages，也不会发布独立网站。
