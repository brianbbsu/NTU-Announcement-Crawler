# NTU Announcement Crawler

This is a tool which crawls announcements from courses on NTU Ceiba, NTU Cool, and other websites which can be easily added by writing plugins.

Currently it supports sending Telegram messages when new announcements are found. Also there's an api endpoint which returns all announcements in json format.

## How to use

These instructions will get you a copy of the tool up and running.

### Prerequisites

- Python 3.6 or up
- git

### Installing

1. Clone the repository.

```
git clone https://github.com/brianbbsu/NTU-Announcement-Crawler.git
cd NTU-Announcement-Crawler
```

2. Install Python dependencies

```
pip3 install -r requirements.txt
```

or

```
python3 -m pip install -r requirements.txt
```

3. Edit Config

```
cp example.config.yaml config.yaml
# Setup your username, passwords and telegram info in config.yaml
```

### Running

```
python3 main.py
```
