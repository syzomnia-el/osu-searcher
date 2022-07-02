# osu!searcher

[osu!](https://osu.ppy.sh/) 的本地谱面查找器，无需启动 osu! 即可快速查找已下载的谱面。

# 功能

- [x] 查看本地谱面。
- [x] 按关键字筛选谱面。
- [x] 检查重复的谱面。
- [ ] 对特定条件，如号码、姓名、曲师、谱师等，按关键字筛选谱面。

# 使用

1. 安装 [Python 3](https://www.python.org/downloads/) 。
2. 使用以下命令来运行： `py <PATH>/main.py`。
3. 首次使用时，需要先输入谱面所在文件夹的绝对路径。

# 命令

| 命令    | 描述                   |
|-------|----------------------|
| exit  | 退出 osu!searcher      |
| path  | 重设谱面路径               |
| flush | 刷新谱面信息缓存             |
| find  | 筛选谱面（当关键字为空时，显示所有谱面） |
| check | 检查重复的谱面              | 