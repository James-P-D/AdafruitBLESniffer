import time
from SnifferAPI import Sniffer, UART
import argparse

class bcolors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[m"


mySniffer = None


def loop(follow_name):
    while True:
        time.sleep(0.1)
        packets = mySniffer.getPackets()
        process_packets(packets, follow_name)


def process_packets(packets, follow_name):
    for packet in packets:
        if packet.OK:
            if packet.blePacket.name == follow_name:
                print(f"{bcolors.BLUE}", end="")
            else:
                print(f"{bcolors.GREEN}", end="")

            addr = ":".join([f"{i:02x}" for i in packet.blePacket.advAddress])
            if len(packet.blePacket.name) > 2:
                print(f"name: {packet.blePacket.name}")
            print(f"addr: {addr}")
        else:
            print(bcolors.RED, end="")

        size = 16
        index = 0
        data = packet.packetList

        while index < len(data):
            data_slice = data[index:(size + index)]
            payload = format(" ".join(f"{i:02x}" for i in data_slice)).ljust(size * 3)
            payload += "| "
            payload += format("".join((chr(i) if chr(i).isprintable() else ".") for i in data_slice))
            print(payload)
            index += size

        print()


def main(com_port, list_mode, follow_name):
    global mySniffer

    mySniffer = Sniffer.Sniffer(com_port)

    mySniffer.start()
    mySniffer.scan()

    time.sleep(5)
    all_devices = mySniffer.getDevices()
    if list_mode:
        for some_dev in all_devices.asList():
            addr = ":".join([f"{i:02x}" for i in some_dev.address])
            if len(some_dev.name) > 2:
                print(f"{addr} {some_dev.name}")
            else:
                print(f"{addr}")
        exit()

    dev = all_devices.find("" if follow_name is None else f""{follow_name}"")

    if dev is not None:
        mySniffer.follow(dev)
    else:
        print("Could not find device")
        exit()

    if mySniffer is not None:
        loop(follow_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("-l",
                        action="store_true",
                        help="List known BLE devices")
    parser.add_argument("-c",
                        metavar="COM port",
                        type=str,
                        nargs=1,
                        required="true",
                        help="COM port for Adafruit Bluefruit device")
    parser.add_argument("-n",
                        metavar="follow name",
                        type=str,
                        nargs="?",
                        help="BLE device name to follow")
    args = parser.parse_args()

    try:
        main(args.c[0], args.l, args.n)
    except KeyboardInterrupt:
        print(bcolors.RESET + "Aborting")

