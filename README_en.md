# osu!searcher

[简体中文](README.md) | **English**

## Introduction

osu!searcher is a local beatmap searcher for [osu!](https://osu.ppy.sh), quick for downloaded beatmap searching without
startup.

## Feature

- [x] View local beatmaps
- [x] Filter beatmaps by keywords
- [x] Check the duplicate beatmaps
- [ ] Filter beatmaps by keywords for specific conditions such as sid, name, artist, mapper, etc.

## Dependency

- [Python 3.10](https://www.python.org/downloads) or later

## Development

- Clone the repository:
  ```bash
  git clone https://github.com/syzomnia-el/osu-searcher.git
  ```

## Usage

1. Run the `main.py` file:
   ```bash
   python <your_dir>/main.py
   ```
2. Run the`startup.cmd`(or`startup.sh`) script.

> When using it for the first time, you need to input the **absolute** path of the folder where your beatmaps are
> saved.

## Command

| Command              | Description                       |
|----------------------|-----------------------------------|
| check                | Check the duplicate beatmaps      | 
| exit                 | Exit osu!searcher                 |
| find &lt;keyword&gt; | Filter beatmaps by a keyword      |
| flush                | Flush the beatmap data cache      |
| list                 | List all local beatmaps           |
| path                 | Modify the saved path of beatmaps |

## License

osu!searcher is licensed under [MIT License](https://opensource.org/licenses/MIT). Please view [license file](LICENSE)
for more information.