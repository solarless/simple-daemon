# Simple Daemon =)

Playing around concept of UNIX daemon (background process).

In this simple script I'm trying to implement proper daemonization mechanism,
according to [this page](https://en.wikipedia.org/wiki/Daemon_(computing)),
only for Unix-like systems.

## How to run

  - `python3 daemon.py start` — starts the daemon.
    Daemon itself produces stub messages into `log` file so you can see it's
    working
  - `python3 daemon.py stop` — stops the daemon.
