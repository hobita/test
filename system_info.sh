#!/bin/bash
echo "📡 Hostname: $(hostname)"
echo "🕒 Uptime:"
uptime
echo "🧠 Memory usage:"
free -h
echo "🗄️ Disk usage:"
df -h
echo "📅 Date: $(date)"
