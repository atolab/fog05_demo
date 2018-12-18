import psutil
import scipy.io
import time
import signal
import sys

cpus = []
ram = []


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    data = {
        'cpu': cpus,
        'mem': ram
    }
    scipy.io.savemat('htop.mat', data)
    sys.exit(0)


def main():
    while True:
        cpus.append(psutil.cpu_percent())
        ram.append(psutil.virtual_memory()._asdict().get('used')/1024)
        time.sleep(0.25)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
