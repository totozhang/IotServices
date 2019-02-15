from queue import Queue
from iot_reception import *
from iot_processor import *


def main():
    # Global Configurations
    config = ConfigParser()
    config.read("server.config")
    threads_list = []

    # Message Queue
    msg_queue = Queue()

    # Message Reception Thread
    thread = IOTMsgReception("ThreadIDReception",
                             "ThreadReception",
                             msg_queue,
                             config.get("server", "ipaddress"),
                             config.getint("server", "udpport"),
                             config.getint("server", "buffersize"))
    threads_list.append(thread)
    thread.start()

    # Message Processing Threads
    for index in range(0, config.getint("concurrent", "process_thread_number")):
        thread = IOTMsgProcessor("ThreadIDProcessor" + str(index),
                                 "ThreadProcessor" + str(index),
                                 msg_queue)
        threads_list.append(thread)
        thread.start()

    # Join all the threads
    for index in range(0, len(threads_list)):
        threads_list[index].join()


if __name__ == "__main__":
    main()
