#!/usr/bin/env python3

import subprocess
import os

def run_findomain(input_file):
    """
    Reads each domain from doms.txt and runs findomain with the -o flag.
    This creates one or more .txt files (one for each domain) containing subdomains.
    """
    with open(input_file, 'r') as f:
        for domain in f:
            domain = domain.strip()
            if not domain:
                continue

            print(f"[+] Running findomain for {domain}")
            # Run findomain for each domain
            subprocess.run(["findomain", "-t", domain, "-o"], check=True)


def run_nmap_on_subdomains_only_open_ports(open_ports_file):
    """
    Reads all .txt files created by findomain (in the current directory),
    runs nmap against each subdomain found in those files,
    and writes only the open-port lines to SubDom_openports.txt.
    """
    # Gather all .txt files created by findomain, excluding our output file
    txt_files = [
        f for f in os.listdir('.') 
        if f.endswith('.txt') and f != open_ports_file
    ]
    
    with open(open_ports_file, 'w') as out:
        for txt_file in txt_files:
            print(f"[+] Reading subdomains from {txt_file}")
            with open(txt_file, 'r') as f:
                subdomains = [line.strip() for line in f if line.strip()]

            # Run nmap on each subdomain
            for sub in subdomains:
                print(f"[+] Scanning subdomain {sub} with nmap")
                nmap_cmd = ["nmap", "-sV", "-oN", "-", sub]  # Adjust flags as needed

                # Capture output so we can filter only 'open' lines
                process = subprocess.run(nmap_cmd, capture_output=True, text=True)
                
                # Extract lines containing "open"
                open_port_lines = [
                    line for line in process.stdout.splitlines() 
                    if "open" in line
                ]

                # If there are open ports, write them to the output file with a header
                if open_port_lines:
                    out.write(f"\n===== Open ports for subdomain: {sub} =====\n")
                    for port_line in open_port_lines:
                        out.write(port_line + "\n")
                    out.write("============================================\n")


def main():
    """
    Main function orchestrating:
      1) Subdomain discovery (findomain)
      2) Port scanning (nmap), extracting only open ports
    """
    input_domains_file = "doms.txt"               # Input list of domains
    openports_results_file = "SubDom_openports.txt"  # Only open ports output

    print("[*] Starting subdomain enumeration with findomain...")
    run_findomain(input_domains_file)

    print("[*] Starting nmap scanning for open ports...")
    run_nmap_on_subdomains_only_open_ports(openports_results_file)

    print(f"[+] All open ports saved to '{openports_results_file}'.")


if __name__ == "__main__":
    main()
