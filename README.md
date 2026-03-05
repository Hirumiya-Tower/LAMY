# LAMY - Simple Multi-Log Monitor

A lightweight tool to monitor multiple log files in real-time.
It plays a sound and logs an alert when specific keywords are detected.

## Getting Started

1. Rename `targets.txt.example` to `targets.txt` and list the paths of the logs you want to monitor.
2. (Optional) Customize `keywords.txt` based on the example.
3. Run the script: `python LAMY.py`

## Features

* **Real-time Monitoring**: Tails multiple files simultaneously.
* **Log Rotation**: Automatically rotates alert logs once they exceed 1MB.
* **Cross-Platform Coding Support**: Supports both UTF-8 and CP932 (Windows).
* **Sound Alerts**: Beeps when a threat or error is found.
