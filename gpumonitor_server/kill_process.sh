#!/bin/bash
ps -ef | grep "python3.7 main.py" | grep -v grep | awk '{print $2}' | xargs kill -9