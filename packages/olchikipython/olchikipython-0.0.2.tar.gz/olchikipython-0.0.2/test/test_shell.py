



#!/usr/bin/env python3
import time
#from subprocess import Popen, PIPE
import subprocess

proc = subprocess.Popen("python", stdin=subprocess.PIPE)
#while (proc.poll() is None):
proc.stdin.write("print('hello world!!')".encode('utf-8')) # etc
    #time.sleep(4)