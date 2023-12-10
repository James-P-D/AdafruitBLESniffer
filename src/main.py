import time
from SnifferAPI import Sniffer, UART
import argparse
import pcapng.blocks as blocks # pip install  python-pcapng
from pcapng import FileWriter


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


def loop(follow_name, pcap_file):
    while True:
        time.sleep(0.1)
        packets = mySniffer.getPackets()
        process_packets(packets, follow_name, pcap_file)


def process_packets(packets, follow_name, pcap_file):
    for packet in packets:
        if packet.OK:
            if follow_name:
                if packet.blePacket.name == f'"{follow_name}"':
                    print(f"{bcolors.BLUE}", end="")
                else:
                    print(f"{bcolors.GREEN}", end="")
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

        if packet.OK and pcap_file:
            shb = blocks.SectionHeader(
                options={
                    "shb_hardware": "artificial",
                    "shb_os": "python",
                    "shb_userappl": "python-pcapng",
                }
            )
            idb = shb.new_member(
                blocks.InterfaceDescription,
                link_type=272,
                snaplen=65535,
                options={
                    "if_description": "Hand-rolled",
                    "if_os": "Python",
                },
            )

            writer = FileWriter(pcap_file, shb)
            spb = shb.new_member(blocks.SimplePacket)
            spb.packet_data = b"\x10" + bytes(data)
            writer.write_block(spb)

        print()


def main(com_port, list_mode, follow_name, pcap_file):
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

    dev = all_devices.find("" if follow_name is None else f'"{follow_name}"')

    if dev is not None:
        print(f"Found BLE device named {follow_name}")
        mySniffer.follow(dev)
    else:
        print(f"Could not find BLE device named {follow_name}")
        exit()

    if mySniffer is not None:
        loop(follow_name, pcap_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adafruit BLE Sniffer")
    parser.add_argument("-l",
                        action="store_true",
                        help="List known BLE devices")
    parser.add_argument("-c",
                        metavar="COM port",
                        type=str,
                        nargs="?",
                        required="true",
                        help="COM port for Adafruit Bluefruit device")
    parser.add_argument("-n",
                        metavar="Follow name",
                        type=str,

                        help="BLE device name to follow")
    parser.add_argument("-p",
                        metavar="PCAPNG output file",
                        type=argparse.FileType("wb"),
                        help="Path to PCAPNG file to dump packets")
    args = parser.parse_args()

    try:
        main(args.c, args.l, args.n, args.p)
    except KeyboardInterrupt:
        print(bcolors.RESET + "Aborting")

