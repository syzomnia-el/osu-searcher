# osu!searcher

[简体中文](README.md) | **English**

## Introduction

osu!searcher is a local beatmap searcher for [osu!](https://osu.ppy.sh), quick for downloaded beatmap searching without
startup.

## Features

- [x] View local beatmaps
- [x] Filter beatmaps by keywords
- [x] Check the duplicate beatmaps
- [ ] Filter beatmaps by keywords for specific conditions such as sid, name, artist, mapper, etc.

## Requirements

- [Python 3.7](https://www.python.org/downloads) or later

## Download

- Clone the repository:
  ```bash
  git clone https://github.com/syzomnia-el/osu-searcher.git
  ```
- You can also download the source code as a ZIP file.

## Usage

1. Navigate to the directory of osu!searcher.
2. Run the`startup.cmd`(or`startup.sh`) script.
3. When using it for the first time, you need to enter the **absolute** path of the folder where your beatmaps are
   saved.

## Commands

| Command              | Description                         |
|----------------------|-------------------------------------|
| check                | Check the duplicate beatmaps        | 
| exit                 | Exit osu!searcher                   |
| find &lt;keyword&gt; | Filter beatmaps by keywords         |
| flush                | Flush the beatmap information cache |
| list                 | View all local beatmaps             |
| path                 | Reset the saved path of beatmaps    |

## License

osu!searcher is licensed under [MIT License](https://opensource.org/licenses/MIT). Please view [license file](LICENSE)
for more information.