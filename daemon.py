import os
import signal
import sys
import time


def serve():
    with open("log", "w") as logfile:
        while True:
            logfile.write(f"working...\n")
            logfile.flush()
            time.sleep(1)


def start():
    if os.path.exists("pid"):
        sys.stderr.write("seems like the daemon is already running\n")
        sys.stderr.flush()
        sys.exit(1)

    # Someone does fork two times, but I found an article which explains when
    # it is necessary. As far as I understand, it is necessary only for cases
    # when the parent proccess is supposed to be long-running as well.
    # https://wikileaks.org/ciav7p1/cms/page_33128479.html
    pid = os.fork()

    if pid != 0:
        with open("pid", "w") as pidfile:
            pidfile.write(str(pid))

        sys.stdout.write(f"pid: {pid}\n")
        sys.stdout.flush()
        sys.exit(0)

    os.setsid()
    os.chdir("/")
    os.umask(0)
    stdin = os.open(os.devnull, os.O_RDONLY)
    stdout = os.open(os.devnull, os.O_APPEND)
    stderr = os.open(os.devnull, os.O_APPEND)
    os.dup2(stdin, sys.stdin.fileno())
    os.dup2(stdout, sys.stdout.fileno())
    os.dup2(stderr, sys.stderr.fileno())

    signal.signal(signal.SIGINT, handle_stopping)
    signal.signal(signal.SIGTERM, handle_stopping)

    serve()


def handle_stopping(signum, frame):
    os.remove("pid")
    sys.exit(0)


def stop():
    try:
        with open("pid") as pidfile:
            pid = int(pidfile.read())
    except FileNotFoundError:
        sys.stderr.write("seems like the daemon is not running\n")
        sys.stderr.flush()
        sys.exit(1)

    os.kill(pid, signal.SIGTERM)

    sys.stdout.write("stopped the daemon\n")


def main():
    try:
        command = sys.argv[1]
    except IndexError:
        sys.stderr.write(
            "you must provide a command:\n"
            "  start\n"
            "  stop\n"
        )
        sys.stderr.flush()
        sys.exit(1)

    match command:
        case "start":
            start()
        case "stop":
            stop()
        case _:
            sys.stderr.write(f"no such command: {command}\n")
            sys.stderr.flush()
            sys.exit(1)


if __name__ == "__main__":
    main()
