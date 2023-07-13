# osu!searcher

**简体中文** | [English](README_en.md)

## 介绍

osu!searcher 是一个为 [osu!](https://osu.ppy.sh) 开发的本地谱面查找工具，无需启动 osu! 即可快速查找已下载的谱面。

## 功能

- [x] 查看本地谱面
- [x] 按关键字筛选谱面
- [x] 检查重复的谱面
- [ ] 对特定条件，如谱面编号、歌名、艺术家、谱师等，按关键字筛选谱面

## 依赖

- [Python 3.10](https://www.python.org/downloads) 或更高版本

## 开发

- 将本仓库复制到本地：
  ```bash
  git clone https://github.com/syzomnia-el/osu-searcher.git
  ```

## 使用

1. 运行 `main.py` 文件：
   ```bash
   python <your_dir>/main.py
   ```
2. 或者直接运行 `startup.cmd`（或 `startup.sh`）脚本。

> 首次使用时，需要先输入谱面所在文件夹的**绝对路径**。

## 命令

| 命令                   | 描述              |
|----------------------|-----------------|
| check                | 检查重复的谱面         |
| exit                 | 退出 osu!searcher |
| find &lt;keyword&gt; | 按关键词筛选谱面        |
| flush                | 刷新谱面信息缓存        |
| list                 | 列出所有本地谱面        |
| path                 | 修改谱面存储路径        |

## 许可证

osu!searcher 基于 [MIT License](https://opensource.org/licenses/MIT) 授予许可。详情请见[许可证](LICENSE)。