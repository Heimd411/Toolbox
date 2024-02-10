import argparse
import queue
import threading
import time
import socket
from queue import Queue

num_threads = 50
p_lock = threading.Lock()
queue = Queue()
open_ports = []
socket.setdefaulttimeout(0.15)

def portscan(port):
    """
    Tries to connect to ports, if successfull adds port to list.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        with p_lock:
            print('port open', port)
            open_ports.append(port)
        s.close()
    except(socket.timeout, ConnectionRefusedError):
        pass

def scan_thread():
    """
    Handle workers
    """
    global queue
    while True:
        worker = queue.get()
        portscan(worker)
        queue.task_done()

def main(host, ports):
    """
    Main function
    """
    global queue
    startTime = time.time()
    for t in range(num_threads):
        t = threading.Thread(target = scan_thread)
        t.daemon = True
        t.start()

    for worker in ports:
        queue.put(worker)

    queue.join()
    run_time = float("%0.2f" % (time.time() - startTime))
    print("Runtime: ", run_time, "seconds.")
    print("Open ports:\n", host, open_ports)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Portscanner")
        parser.add_argument("--target", "-t", dest="host", help="Target host.")
        parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="Specify portrange to scan. Default 1-65535")
        args = parser.parse_args()
        host, port_range = args.host, args.port_range

        start_port, end_port = port_range.split("-")
        start_port, end_port = int(start_port), int(end_port)

        ports = [p for p in range(start_port, end_port)]

        main(host, ports)
    except KeyboardInterrupt:
        print("Aborting, stopping scan...")

