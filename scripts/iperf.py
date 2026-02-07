#!/usr/bin/env python3

import sys
import os
import subprocess
import time
from base_opterm import openterm

#default: 0 == fpga, 1-4 == node0-4



n = 5
eth_n0 = "10.0.4.2"
eth_n1 = "10.0.5.2"
eth_n2 = "10.0.6.2"
eth_n3 = "10.0.7.2"


file = 'iperf_tcp_test.log'

def logging(result):
    
    with open(file, 'a') as f:
        f.write(result + '\n')




def iperf_test():
    subprocess.run(['tmux', 'send-keys', '-t', 'nd0', 'nf_download /home/netfpga/bitfiles/reference_nic.bit', 'C-m'])
    time.sleep(10)
    print("Starting iperf server...")
    subprocess.run(['tmux', 'send-keys', '-t', 'nd0', 'iperf -s -p 5003 ', 'C-m'])
    for i in range(4):
        for j in range(4):
            eth_n = globals()[f'eth_n{j}']
            subprocess.run(['tmux', 'send-keys', '-t', f'nd{i+1}', f'iperf -c {eth_n} -p 5003', 'C-m'])
            # print(f"Node {i+1} testing against {eth_n}")
            time.sleep(15)

    server_result = subprocess.check_output(['tmux', 'capture-pane', '-t', 'nd0', '-p','-S','-','-E','-']).decode('utf-8')
    logging(server_result)


def main():
    if os.path.exists(file):
        os.remove(file)
        print(f"{file} removed.")
    openterm(sys.argv, n)
    iperf_test()
    print('finish test')

if __name__ == "__main__":
    main()

