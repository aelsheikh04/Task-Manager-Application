#!/bin/bash

# Function to display CPU usage
cpu_usage() {
  local usage=$(grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}')
  feh --title "CPU Usage" ./cpu_logo.png &
  zenity --info --title="CPU Usage" --width=400 --height=200 --text="Current CPU Usage: $usage"
  pkill -f feh
}

# Function to display memory usage
memory_usage() {
  local total=$(grep MemTotal /proc/meminfo | awk '{print $2}')
  local free=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
  local used=$((total - free))
  local usage=$((used * 100 / total))
  feh --title "Memory Usage" ./memory_logo.png &
  zenity --info --title="Memory Usage" --width=400 --height=200 --text="Memory Usage: $usage%\nUsed: $((used / 1024)) MB\nFree: $((free / 1024)) MB\nTotal: $((total / 1024)) MB"
  pkill -f feh
}

# Function to display disk usage
disk_usage() {
  local usage=$(df -h / | tail -1 | awk '{print $5}')
  local free=$(df -h / | tail -1 | awk '{print $4}')
  local total=$(df -h / | tail -1 | awk '{print $2}')
  feh --title "Disk Usage" ./disk_logo.png &
  zenity --info --title="Disk Usage" --width=400 --height=200 --text="Disk Usage: $usage\nFree: $free\nTotal: $total"
  pkill -f feh
}

# Function to display network statistics
network_stats() {
  local rx=$(cat /sys/class/net/$(ip route show default | awk '/default/ {print $5}')/statistics/rx_bytes)
  local tx=$(cat /sys/class/net/$(ip route show default | awk '/default/ {print $5}')/statistics/tx_bytes)
  feh --title "Network Statistics" ./network_logo.png &
  zenity --info --title="Network Statistics" --width=400 --height=200 --text="Network Statistics:\nDownloaded: $((rx / 1024 / 1024)) MB\nUploaded: $((tx / 1024 / 1024)) MB"
  pkill -f feh
}

# Function to display battery status
battery_status() {
  if command -v acpi >/dev/null 2>&1; then
    local battery=$(acpi -b | awk -F ', ' '{print $2, $3}' | tr -d '\n')
    if [ -z "$battery" ]; then
      battery="No battery data available"
    fi
    feh --title "Battery Status" ./battery_logo.png &
    zenity --info --title="Battery Status" --width=400 --height=200 --text="Battery Status: $battery"
    pkill -f feh
  else
    zenity --error --title="Battery Status" --width=400 --height=200 --text="Battery information not available. Install 'acpi' package."
  fi
}

# Function to list running processes
list_processes() {
  local processes=$(ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n 20 | awk '{printf "%s\t%s\t%s%%\t%s%%\n", $1, $2, $3, $4}')
  feh --title "Processes" ./process_logo.png &
  echo -e "PID\tCommand\tCPU Usage\tMemory Usage\n$processes" | zenity --text-info --title="Top Processes" --width=600 --height=400
  pkill -f feh
}

# Function to display GPU usage
gpu_usage() {
  if command -v nvidia-smi >/dev/null 2>&1; then
    local gpu=$(nvidia-smi --query-gpu=name,utilization.gpu,utilization.memory --format=csv,noheader | awk -F ',' '{printf "GPU: %s\nUsage: %s\nMemory: %s", $1, $2, $3}')
    feh --title "GPU Usage" ./gpu_logo.png &
    zenity --info --title="GPU Usage" --width=400 --height=200 --text="$gpu"
    pkill -f feh
  else
    zenity --error --title="GPU Usage" --width=400 --height=200 --text="GPU information not available. Install NVIDIA drivers or ensure nvidia-smi is installed."
  fi
}

# Function to save metrics to an HTML file
save_metrics() {
  local filename="metrics_$(date +%Y%m%d%H%M%S).html"
  {
    echo "<html><head><title>System Metrics</title></head><body>"
    echo "<h1>System Metrics</h1>"
    echo "<p>CPU Usage: $(grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}') </p>"
    local total=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    local free=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
    local used=$((total - free))
    echo "<p>Memory Usage: $((used * 100 / total))% (Used: $((used / 1024)) MB, Free: $((free / 1024)) MB, Total: $((total / 1024)) MB)</p>"
    local usage=$(df -h / | tail -1 | awk '{print $5}')
    local free=$(df -h / | tail -1 | awk '{print $4}')
    local total=$(df -h / | tail -1 | awk '{print $2}')
    echo "<p>Disk Usage: $usage (Free: $free, Total: $total)</p>"
    if command -v acpi >/dev/null 2>&1; then
      local battery=$(acpi -b | awk -F ', ' '{print $2, $3}' | tr -d '\n')
      echo "<p>Battery Status: $battery</p>"
    fi
    if command -v nvidia-smi >/dev/null 2>&1; then
      local gpu=$(nvidia-smi --query-gpu=name,utilization.gpu,utilization.memory --format=csv,noheader | awk -F ',' '{printf "GPU: %s, Usage: %s, Memory: %s", $1, $2, $3}')
      echo "<p>$gpu</p>"
    fi
    echo "</body></html>"
  } > "$filename"
  zenity --info --title="Save Metrics" --width=400 --height=200 --text="Metrics saved to $filename"
}

# Function to display the Home Page
home_page() {
  feh --title "Task Manager Home" ./task_manager_logo.png &
  zenity --info --title="Task Manager Home" --width=400 --height=200 --text="<b>Welcome to my Task Manager</b>\n\nMade by Abdelaziz El-Sheikh\n\nClick OK to proceed to the menu."
  pkill -f feh
}

# Main menu
while true; do
  home_page
  choice=$(zenity --list --title="Task Manager" --width=400 --height=400 \
    --column="Task" --column="Description" \
    "CPU" "Monitor CPU Usage" \
    "Memory" "Monitor Memory Usage" \
    "Disk" "Monitor Disk Usage" \
    "Network" "Monitor Network Statistics" \
    "Battery" "Monitor Battery Status" \
    "GPU" "Monitor GPU Usage" \
    "Processes" "List Running Processes" \
    "Save Metrics" "Save Metrics to HTML File" \
    "Exit" "Exit the Task Manager")

  case $choice in
    "CPU")
      cpu_usage
      ;;
    "Memory")
      memory_usage
      ;;
    "Disk")
      disk_usage
      ;;
    "Network")
      network_stats
      ;;
    "Battery")
      battery_status
      ;;
    "GPU")
      gpu_usage
      ;;
    "Processes")
      list_processes
      ;;
    "Save Metrics")
      save_metrics
      ;;
    "Exit")
      break
      ;;
    *)
      zenity --error --width=400 --height=200 --text="Invalid option. Please try again."
      ;;
  esac
done


