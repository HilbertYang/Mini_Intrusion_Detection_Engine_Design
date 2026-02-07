#!/usr/bin/env python3

import sys
import subprocess

n = 5
eth_n0 = "10.0.4.2"
eth_n1 = "10.0.5.2"
eth_n2 = "10.0.6.2"
eth_n3 = "10.0.7.2"

def openterm(argv, n):
    if len(argv) <3:
        print("Usage: openterm <title> <command>")
        sys.exit(1)
        return
    
    no = int(argv[1])
    password = argv[2]
        
        
    
    for i in range(n):
        name = 'nd'+str(i)
        subprocess.run(['tmux', 'kill-session', '-t', name], stderr=subprocess.DEVNULL)
        host = f'node{no}@nf{(no+i)%5}.usc.edu' if i > 0 else f'netfpga@nf{(no+i)%5}.usc.edu'
        cmd = f"sshpass -p '{password}' ssh -t -o StrictHostKeyChecking=no {host} 'bash'"
        # ssh_cmd = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {host} 'bash'"
        subprocess.run(['tmux', 'new-session', '-d', '-s', name, cmd])
        subprocess.Popen(['gnome-terminal', '--', 'tmux', 'attach-session', '-t', name])
        print(f'{host} is {name}')


def main():
    openterm(sys.argv, n)

if __name__ == "__main__":
    main()

