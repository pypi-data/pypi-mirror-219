# Timer App

DEVELOPMENT IN PROGRESS

Dissatisfied with the selection of timer applications available in linux, I built my own.  It maintains a simple local db in /tmp

The application is fairly simple:
* user can specify a list of different timers.
* timers can be renamed.
* timers can be started / stopped concurrently.
* on startup the timers will resume the count from the last start.
* timers should not cross over days. automatic stop times at 23:59:59 for forgotten timers.
* daily statistics view



## Installation
```bash
pip install jtimer  # not timer
```

## Usage
```bash
jtimer
```

## Planned Future developments

* timer linked triggers
* timer event view