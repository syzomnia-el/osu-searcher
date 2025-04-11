# osu!searcher

[简体中文](README.md) | **English**

## Introduction

osu!searcher is a local beatmap searcher for [osu!](https://osu.ppy.sh), quick for downloaded beatmap searching without
the startup.

## Feature

- [x] View local beatmaps
- [x] Check the duplicate beatmaps
- [x] Filter beatmaps by keywords
- [x] Filter beatmaps by keywords for specific conditions including sid, name or artist.
- [ ] More condition filtering support

## Dependency

- [Python 3.12](https://www.python.org/downloads) or newer

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

> When using it for the first time,
> you need to input the **absolute** path of the folder where your beatmaps are saved.

## Command

| Command                          | Description                       |
|----------------------------------|-----------------------------------|
| check                            | Check the duplicate beatmaps      |
| exit                             | Exit osu!searcher                 |
| find [condition=]&lt;keyword&gt; | Filter beatmaps by a keyword      |
| flush                            | Flush the beatmap data cache      |
| list                             | List all local beatmaps           |
| path                             | Modify the saved path of beatmaps |

## License

osu!searcher is licensed under [MIT License](https://opensource.org/licenses/MIT).
View [license file](LICENSE) for more information.
