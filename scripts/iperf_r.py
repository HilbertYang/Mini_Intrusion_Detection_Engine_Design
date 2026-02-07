#!/usr/bin/env python3

import sys
import os
import subprocess
import time
from base_opterm import openterm

#default: 0 == fpga, 1-4 == node0-4
# command : .py <no> <ps> <protocol> <bitfile>

global file
n = 5
eth_n0 = "10.0.4.2"
eth_n1 = "10.0.5.2"
eth_n2 = "10.0.6.2"
eth_n3 = "10.0.7.2"
node_n0 = "10.0.4.3"
node_n1 = "10.0.5.3"
node_n2 = "10.0.6.3"
node_n3 = "10.0.7.3"

file = ''

P_MAP = {
    'tcp': 'iperf -s',
    'udp': 'iperf -s -u'
}
B_MAP = {
    'nic': 'reference_nic.bit',
    'router': 'reference_router.bit',
    'ids':  "?"
}

def logging(result):
    
    with open(file, 'a') as f:
        f.write(result + '\n')




def iperf_test(protocol='tcp',bitfile='nic'):
    subprocess.run(['tmux', 'send-keys', '-t', 'nd0', f'nf_download /home/netfpga/bitfiles/{B_MAP[bitfile]}', 'C-m'])
    time.sleep(10)

    if protocol == 'udp':
        subprocess.run(['tmux', 'send-keys', '-t', 'nd0', 'rkd &', 'C-m'])
        time.sleep(1)
        print("Starting iperf server...")
        for i in range(4):
            subprocess.run(['tmux', 'send-keys', '-t', f'nd{i+1}', f'{P_MAP[protocol]} -p 5002 & ', 'C-m'])
        time.sleep(5)

        for j in range(4):
            eth_n = globals()[f'eth_n{j}']
            node_n = globals()[f'node_n{j}']   #nd1 -- node_0 -- nd0 in terminal
            if j == 3:
                subprocess.run(['tmux', 'send-keys', '-t', f'nd{1}', f'iperf -c {node_n} -u -p 5002 -l 512 -t 30 -b 1000M > /dev/null 2>&1', 'C-m'])
            else:
                subprocess.run(['tmux', 'send-keys', '-t', f'nd{j+2}', f'iperf -c {node_n} -u -p 5002 -l 512 -t 30 -b 1000M > /dev/null 2>&1', 'C-m'])

           
            # print(f"Node {j+1} testing against {eth_n}")

    else: #tcp
        print("Starting iperf server...")
        for i in range(4):
            subprocess.run(['tmux', 'send-keys', '-t', f'nd{i+1}', f'{P_MAP[protocol]} -p 5002 & ', 'C-m'])
        time.sleep(5)
        for j in range(4):
            eth_n = globals()[f'eth_n{j}']
            node_n = globals()[f'node_n{j}']
            if j == 3:
                subprocess.run(['tmux', 'send-keys', '-t', f'nd{1}', f'iperf -c {node_n} -p 5002 > /dev/null 2>&1', 'C-m'])
            else:
                subprocess.run(['tmux', 'send-keys', '-t', f'nd{j+2}', f'iperf -c {node_n} -p 5002 > /dev/null 2>&1', 'C-m'])

            
            # print(f"Node {j+1} testing against {eth_n}")
    
    time.sleep(60)
    for i in range(4):
        server_result = subprocess.check_output(['tmux', 'capture-pane', '-t', f'nd{i+1}', '-p','-S','-','-E','-']).decode('utf-8')
        logging(server_result)


def main():
    protocol = sys.argv[3] if len(sys.argv) > 3 else "tcp"
    bitf = sys.argv[4] if len(sys.argv) > 4 else "nic"
    global file
    file = f'iperf_{protocol}_{bitf}_test.log'
    if os.path.exists(file):
        os.remove(file)
        print(f"{file} removed.")

    openterm(sys.argv, n)
    iperf_test(protocol=protocol,bitfile=bitf)
    print('finish test')

if __name__ == "__main__":
    main()

