#!/usr/bin/env python3
from daemon import start_daemon
import api

if __name__ == "__main__":
    start_daemon(600)
    api.run()
