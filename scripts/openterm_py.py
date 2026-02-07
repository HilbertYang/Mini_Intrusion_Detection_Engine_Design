#!/usr/bin/env python3

import sys
import subprocess

n = 5

def openterm(argv, n):
    if len(argv) <3:
        print("Usage: openterm <title> <command>")
        sys.exit(1)
        return
    
    no = int(argv[1])
    password = argv[2]

    for i in range(n):
        if i == 0:
            host = f'netfpga@nf{(no+i)%5}.usc.edu'
        else:
            host = f'node{no}@nf{(no+i)%5}.usc.edu'

        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c',f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {host}"])



def main():
    openterm(sys.argv, n)

if __name__ == "__main__":
    main()

