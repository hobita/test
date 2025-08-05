#!/bin/bash
echo "Hello from $(hostname)"
echo "Date: $(date)"
echo "Done." | tee /dev/stderr
