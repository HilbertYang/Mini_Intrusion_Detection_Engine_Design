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
node_n0 = "$n0"
node_n1 = "$n1"
node_n2 = "$n2"
node_n3 = "$n3"
#node_n0 = "10.0.4.3"
#node_n1 = "10.0.5.3"
#node_n2 = "10.0.6.3"
#node_n3 = "10.0.7.3"
port = 5007

file = ''

P_MAP = {
    'tcp': 'iperf -s',
    'udp': 'iperf -s -u'
}
B_MAP = {
    'nic': '/home/netfpga/bitfiles/reference_nic.bit',
    'router': '/home/netfpga/bitfiles/reference_router.bit',
    'ids':  "bitfiles/nf2_top_par_ids.bit"
}

def logging(result):
    
    with open(file, 'a') as f:
        f.write(result + '\n')


def pattern_check(protocol):
    subprocess.run(['tmux', 'send-keys', '-t', 'nd0', './idsreg reset', 'C-m'])
    time.sleep(1)  # wait to initialize
    subprocess.run(['tmux', 'send-keys', '-t', 'nd0', './idsreg pattern ABCDEFG', 'C-m'])
    time.sleep(2)  # wait to initialize
    subprocess.run(['tmux', 'send-keys', '-t', 'nd0', './idsreg allregs', 'C-m'])
    time.sleep(5)
    for y in range(4):
         subprocess.run(['tmux', 'send-keys', '-t', f'nd{y+1}', 'echo -n "ABCDEFGH" > patternABCDEFG.txt' , 'C-m'])
         subprocess.run(['tmux', 'send-keys', '-t', f'nd{y+1}', 'echo -n "aqrwetwe" > pattern.txt', 'C-m'])
    time.sleep(1)  # wait to initialize
    print("Starting pattern check...")
    if protocol == 'udp':
        for m in range(1,5):   # nd1 -- node_0 -- nd0 in terminal        
            for k in range(4):
                node_n = globals()[f'node_n{k}']
                if m == k+1:
                    pass
                elif (m == k or m == k+4):
                    subprocess.run(['tmux', 'send-keys', '-t', f'nd{m}', f'iperf -c {node_n} -u -p {port} -t 30 -F patternABCDEFG.txt > /dev/null 2>&1', 'C-m'])
                else:
                    subprocess.run(['tmux', 'send-keys', '-t', f'nd{m}', f'iperf -c {node_n} -u -p {port} -t 30 -F pattern.txt > /dev/null 2>&1', 'C-m'])
                #time.sleep(5)
    else: #tcp
        for m in range(1,5):   # nd1 -- node_0 -- nd0 in terminal        
            for k in range(4):
                node_n = globals()[f'node_n{m-1}']
                if m == k+1:
                    pass
                elif (m == k or m == k+4):
                    subprocess.run(['tmux', 'send-keys', '-t', f'nd{k+1}', f'iperf -c {node_n} -p {port} -t 10 -F patternABCDEFG.txt > /dev/null 2>&1', 'C-m'])
                else:
                    subprocess.run(['tmux', 'send-keys', '-t', f'nd{k+1}', f'iperf -c {node_n} -p {port} -t 10 -F pattern.txt > /dev/null 2>&1', 'C-m'])
              #  time.sleep(10)
    time.sleep(10)

  




    

def iperf_test(protocol='tcp',bitfile='nic'):
    subprocess.run(['tmux', 'send-keys', '-t', 'nd0', f'nf_download {B_MAP[bitfile]}', 'C-m'])
    time.sleep(10)

    subprocess.run(['tmux', 'send-keys', '-t', 'nd0', 'rkd &', 'C-m'])
    if protocol == 'udp':
        time.sleep(1)
        print("Starting iperf server...")
        for i in range(4):
            subprocess.run(['tmux', 'send-keys', '-t', f'nd{i+1}', f'{P_MAP[protocol]} -p {port} & ', 'C-m'])
        time.sleep(5)

        if bitfile == 'ids':
            pattern_check('udp')
        else:

            for j in range(4):
                eth_n = globals()[f'eth_n{j}']
                node_n = globals()[f'node_n{j}']   #nd1 -- node_0 -- nd0 in terminal
                if j == 3:
                    subprocess.run(['tmux', 'send-keys', '-t', f'nd{1}', f'iperf -c {node_n} -u -p {port} -l 512 -t 30 -b 1000M > /dev/null 2>&1', 'C-m'])
                else:
                    subprocess.run(['tmux', 'send-keys', '-t', f'nd{j+2}', f'iperf -c {node_n} -u -p {port} -l 512 -t 30 -b 1000M > /dev/null 2>&1', 'C-m'])
                    
 

           
            # print(f"Node {j+1} testing against {eth_n}")

    else: #tcp
        print("Starting iperf server...")
        for i in range(4):
            subprocess.run(['tmux', 'send-keys', '-t', f'nd{i+1}', f'{P_MAP[protocol]} -p {port} & ', 'C-m'])
        time.sleep(5)

        if bitfile == 'ids':
            pattern_check('tcp')
        else:
            for j in range(4):
                eth_n = globals()[f'eth_n{j}']
                node_n = globals()[f'node_n{j}']
                if j == 3:
                    subprocess.run(['tmux', 'send-keys', '-t', f'nd{1}', f'iperf -c {node_n} -p {port} > /dev/null 2>&1', 'C-m'])
                else:
                    subprocess.run(['tmux', 'send-keys', '-t', f'nd{j+2}', f'iperf -c {node_n} -p {port} > /dev/null 2>&1', 'C-m'])

            
            # print(f"Node {j+1} testing against {eth_n}")
    
    if bitfile == 'ids':
        subprocess.run(['tmux', 'send-keys', '-t', 'nd0', './idsreg matches', 'C-m'])
        time.sleep(5)
        server_result = subprocess.check_output(['tmux', 'capture-pane', '-t', f'nd0', '-p','-S','-','-E','-']).decode('utf-8')
        logging(server_result)
    time.sleep(30)
   # subprocess.run(['tmux', 'send-keys', '-t', f'nd0', f'killall rkd ', 'C-m'])
    for i in range(4):
        server_result = subprocess.check_output(['tmux', 'capture-pane', '-t', f'nd{i+1}', '-p','-S','-','-E','-']).decode('utf-8')
        logging(server_result)
        time.sleep(1)


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

