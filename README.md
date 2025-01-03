# Task Manager

## Project Overview

The Task Manager project is a cross-platform application designed to monitor and manage system resources and processes in real-time. It has been implemented in both Python and Bash, exploring the strengths and limitations of each approach.

### Key Features

- Real-time monitoring of:
  - CPU usage
  - Memory usage
  - Disk usage
  - Network activity
  - Battery status
  - GPU usage
- Display of running processes with detailed information.
- Export of system metrics to an HTML file for further analysis.
- Interactive GUI:
  - Python: Built using PyQt5 for a robust and feature-rich interface.
  - Bash: Utilized Zenity for dialogs and Feh for image display.

---

## Python Implementation

### Tools and Libraries

- **PyQt5**: For building the graphical user interface.
- **psutil**: To retrieve system resource metrics.
- **matplotlib**: For graph plotting.
- **GPUtil**: For GPU monitoring.

### Highlights

- **Object-Oriented Design**: Encapsulated functionalities within classes (e.g., `TaskManager`).
- **Real-Time Monitoring**: Updates occur every second using `QTimer`.
- **Dynamic Graphs**: Visual representation of CPU and memory usage over time.
- **Multi-Page GUI**: Separate pages for each system metric.

### Key Features

- **Home Page**: Includes project details and navigation options.
- **CPU Monitoring**: Real-time usage and historical graph.
- **Memory Monitoring**: Real-time usage and trends.
- **GPU Monitoring**: Utilization, memory, and temperature.
- **Processes Page**: Lists running processes with attributes like PID, CPU%, memory usage, and status.
- **Metrics Export**: Saves system metrics to an HTML file.

---

## Bash Implementation

### Tools and Utilities

- **Zenity**: For creating interactive GUI dialogs.
- **Feh**: For displaying images.
- **System Utilities**: Used `awk`, `grep`, and `/proc` to gather system metrics.

### Highlights

- **Menu-Driven Interface**: User-friendly menu using `case` statements.
- **Dynamic Data Retrieval**: Extracted live system metrics from `/proc` and other utilities.
- **HTML Export**: Automates system metrics export.

### Key Features

- **CPU Monitoring**: Uses `/proc/stat` for calculations.
- **Memory Monitoring**: Retrieves data from `/proc/meminfo`.
- **Disk Monitoring**: Displays usage stats with `df`.
- **Network Statistics**: Tracks upload and download data.
- **Battery Monitoring**: Checks status with `acpi`.
- **Processes Page**: Lists top processes sorted by CPU usage.
- **Metrics Export**: Saves metrics to an HTML file.

---

## Documentation

For detailed information on the design, features, and challenges, refer to the attached documentation file: **Task Manager Documentation.pdf**.

---

## Setup and Usage

### Prerequisites

- **Python Implementation**:

  - Python 3.x
  - Required libraries: `psutil`, `matplotlib`, `PyQt5`, `GPUtil`
  - Install dependencies using `pip install -r requirements.txt`

- **Bash Implementation**:

  - Linux environment with `zenity`, `feh`, `awk`, `grep`, and `acpi` (optional for battery stats).

### Running the Task Manager

1. **Python Version**:
   bash
   python program.py
   
2. **Bash Version**:
   bash
   bash program.sh
   

---

## Author

**Abdelaziz El-Sheikh**

This project represents an integration of technical skills, innovation, and problem-solving capabilities to create a robust system monitoring tool.

---

## License

This project is licensed under the CC BY-NC-ND 4.0 License - see the LICENSE file for details.