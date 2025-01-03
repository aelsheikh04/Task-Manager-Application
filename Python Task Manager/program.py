import sys
import psutil
import time
import platform
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QMainWindow, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import GPUtil  # GPU library

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cpu_usage_history = []
        self.memory_usage_history = []
        self.update_interval = 1
        self.history_limit = 60  # Limit for history arrays

        # Initialize layout and window
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #f0f0f5;")

        # Remove maximize button
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Sidebar layout
        self.sidebar_layout = QVBoxLayout()
        self.sidebar = QWidget(self)
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: #2b2b2b;")
        self.sidebar.setLayout(self.sidebar_layout)
        self.main_layout.addWidget(self.sidebar)

        # Main logo in sidebar
        self.sidebar_logo = QLabel(self)
        self.sidebar_logo.setPixmap(QPixmap("task_manager_logo.png").scaled(150, 150))
        self.sidebar_logo.setStyleSheet("margin: 10px;")
        self.sidebar_layout.addWidget(self.sidebar_logo)

        # Content area
        self.content_area = QStackedWidget(self)
        self.main_layout.addWidget(self.content_area)

        # Sidebar buttons
        self.sidebar_buttons = {
            "Home": self.show_home_page,
            "CPU": self.show_cpu_page,
            "Memory": self.show_memory_page,
            "GPU": self.show_gpu_page,
            "Battery": self.show_battery_page,
            "Network": self.show_network_page,
            "Disk": self.show_disk_page,
            "Processes": self.show_process_page
        }

        for label, callback in self.sidebar_buttons.items():
            button = QPushButton(label, self)
            button.setStyleSheet("background-color: #444444; color: white; font-size: 14px;")
            button.clicked.connect(callback)
            self.sidebar_layout.addWidget(button)

        # Pages
        self.pages = {
            "home_page": QWidget(self),
            "cpu_page": QWidget(self),
            "memory_page": QWidget(self),
            "gpu_page": QWidget(self),
            "battery_page": QWidget(self),
            "network_page": QWidget(self),
            "disk_page": QWidget(self),
            "process_page": QWidget(self)
        }

        for page in self.pages.values():
            self.content_area.addWidget(page)

        # Initialize pages
        self.init_home_page()
        self.init_cpu_page()
        self.init_memory_page()
        self.init_battery_page()
        self.init_network_page()
        self.init_disk_page()
        self.init_gpu_page()
        self.init_process_page()

        # Timer for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(1000)

        # Set default page
        self.show_home_page()

    def init_home_page(self):
        self.home_layout = QVBoxLayout(self.pages["home_page"])

        # Title and logo
        self.home_title = QLabel("Task Manager", self)
        self.home_title.setStyleSheet("font-size: 30px; font-weight: bold; text-align: center;")
        self.home_title.setAlignment(Qt.AlignCenter)
        self.home_layout.addWidget(self.home_title)

        self.home_logo = QLabel(self)
        self.home_logo.setPixmap(QPixmap("task_manager_logo.png").scaled(200, 200))
        self.home_logo.setAlignment(Qt.AlignCenter)
        self.home_layout.addWidget(self.home_logo)

        # Team information
        self.team_info = QLabel(
            "Welcome to my Task Manager\n\n"
            "Made by Abdelaziz El-Sheikh", self
        )
        self.team_info.setStyleSheet("font-size: 14px; text-align: center;")
        self.team_info.setAlignment(Qt.AlignCenter)
        self.home_layout.addWidget(self.team_info)

        # Buttons
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setStyleSheet("background-color: red; color: white; font-size: 14px;")
        self.exit_button.clicked.connect(self.close)
        self.home_layout.addWidget(self.exit_button)

        self.save_button = QPushButton("Save Metrics", self)
        self.save_button.setStyleSheet("background-color: green; color: white; font-size: 14px;")
        self.save_button.clicked.connect(self.save_metrics_to_file)
        self.home_layout.addWidget(self.save_button)

    def save_metrics_to_file(self):
        try:
            filename = "system_metrics.html"
            metrics_summary = self.get_metrics_summary()

            html_content = f"""
            <html>
            <head><title>System Metrics</title></head>
            <body>
                <h1>System Metrics</h1>
                <pre>{metrics_summary}</pre>
            </body>
            </html>
            """

            with open(filename, "w") as f:
                f.write(html_content)

            QMessageBox.information(self, "Saved", f"Metrics saved to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save metrics: {e}")

    def get_metrics_summary(self):
        summary = []
        summary.append(f"CPU Usage: {psutil.cpu_percent()}%\n")
        summary.append(f"Memory Usage: {psutil.virtual_memory().percent}%\n")
        summary.append(f"Disk Usage: {psutil.disk_usage('/').percent}%\n")

        battery = psutil.sensors_battery()
        if battery:
            summary.append(f"Battery: {battery.percent}%\n")
        else:
            summary.append("Battery: N/A\n")

        network_stats = psutil.net_io_counters()
        summary.append(f"Downloaded: {network_stats.bytes_recv / (1024 * 1024):.2f} MB\n")
        summary.append(f"Uploaded: {network_stats.bytes_sent / (1024 * 1024):.2f} MB\n")

        return "".join(summary)

    def init_cpu_page(self):
        self.cpu_layout = QVBoxLayout(self.pages["cpu_page"])

        self.cpu_logo = QLabel(self)
        self.cpu_logo.setPixmap(QPixmap("cpu_logo.png").scaled(100, 100))
        self.cpu_logo.setAlignment(Qt.AlignCenter)
        self.cpu_layout.addWidget(self.cpu_logo)

        self.cpu_label = QLabel("CPU Usage: ", self)
        self.cpu_label.setStyleSheet("font-size: 16px; text-align: center;")
        self.cpu_layout.addWidget(self.cpu_label)

        self.cpu_description = QLabel("This page shows real-time CPU usage, including core utilization and system uptime.", self)
        self.cpu_description.setStyleSheet("font-size: 14px; text-align: center;")
        self.cpu_description.setAlignment(Qt.AlignCenter)
        self.cpu_layout.addWidget(self.cpu_description)

        self.cpu_canvas, self.cpu_ax = plt.subplots()
        self.cpu_canvas_widget = FigureCanvas(self.cpu_canvas)
        self.cpu_layout.addWidget(self.cpu_canvas_widget)

    def init_memory_page(self):
        self.memory_layout = QVBoxLayout(self.pages["memory_page"])

        self.memory_logo = QLabel(self)
        self.memory_logo.setPixmap(QPixmap("memory_logo.png").scaled(100, 100))
        self.memory_logo.setAlignment(Qt.AlignCenter)
        self.memory_layout.addWidget(self.memory_logo)

        self.memory_label = QLabel("Memory Usage: ", self)
        self.memory_label.setStyleSheet("font-size: 16px; text-align: center;")
        self.memory_layout.addWidget(self.memory_label)

        self.memory_description = QLabel("Monitor the real-time memory usage, including total, used, and available memory.", self)
        self.memory_description.setStyleSheet("font-size: 14px; text-align: center;")
        self.memory_description.setAlignment(Qt.AlignCenter)
        self.memory_layout.addWidget(self.memory_description)

        self.memory_canvas, self.memory_ax = plt.subplots()
        self.memory_canvas_widget = FigureCanvas(self.memory_canvas)
        self.memory_layout.addWidget(self.memory_canvas_widget)

    def init_battery_page(self):
        self.battery_layout = QVBoxLayout(self.pages["battery_page"])

        self.battery_logo = QLabel(self)
        self.battery_logo.setPixmap(QPixmap("battery_logo.png").scaled(100, 100))
        self.battery_logo.setAlignment(Qt.AlignCenter)
        self.battery_layout.addWidget(self.battery_logo)

        self.battery_label = QLabel("Battery: ", self)
        self.battery_label.setStyleSheet("font-size: 16px; text-align: center;")
        self.battery_layout.addWidget(self.battery_label)

        self.battery_status_label = QLabel("Status: ", self)
        self.battery_status_label.setStyleSheet("font-size: 14px; text-align: center;")
        self.battery_layout.addWidget(self.battery_status_label)

        self.battery_description = QLabel("Displays the current battery percentage and charging status.", self)
        self.battery_description.setStyleSheet("font-size: 14px; text-align: center;")
        self.battery_description.setAlignment(Qt.AlignCenter)
        self.battery_layout.addWidget(self.battery_description)

    def init_network_page(self):
        self.network_layout = QVBoxLayout(self.pages["network_page"])

        self.network_logo = QLabel(self)
        self.network_logo.setPixmap(QPixmap("network_logo.png").scaled(100, 100))
        self.network_logo.setAlignment(Qt.AlignCenter)
        self.network_layout.addWidget(self.network_logo)

        self.network_label = QLabel("Network Information: ", self)
        self.network_label.setStyleSheet("font-size: 16px; text-align: center;")
        self.network_layout.addWidget(self.network_label)

        self.network_description = QLabel("Monitor real-time network activity, including download and upload speeds.", self)
        self.network_description.setStyleSheet("font-size: 14px; text-align: center;")
        self.network_description.setAlignment(Qt.AlignCenter)
        self.network_layout.addWidget(self.network_description)

        self.download_speed_label = QLabel("Download Speed: ", self)
        self.network_layout.addWidget(self.download_speed_label)
        self.upload_speed_label = QLabel("Upload Speed: ", self)
        self.network_layout.addWidget(self.upload_speed_label)

    def init_disk_page(self):
        self.disk_layout = QVBoxLayout(self.pages["disk_page"])

        self.disk_logo = QLabel(self)
        self.disk_logo.setPixmap(QPixmap("disk_logo.png").scaled(100, 100))
        self.disk_logo.setAlignment(Qt.AlignCenter)
        self.disk_layout.addWidget(self.disk_logo)

        self.disk_label = QLabel("Disk Usage: ", self)
        self.disk_label.setStyleSheet("font-size: 16px; text-align: center;")
        self.disk_layout.addWidget(self.disk_label)

        self.disk_free_label = QLabel("Free Disk Space: ", self)
        self.disk_layout.addWidget(self.disk_free_label)

        self.disk_description = QLabel("View disk usage statistics, including used and free disk space.", self)
        self.disk_description.setStyleSheet("font-size: 14px; text-align: center;")
        self.disk_description.setAlignment(Qt.AlignCenter)
        self.disk_layout.addWidget(self.disk_description)

    def init_gpu_page(self):
        self.gpu_layout = QVBoxLayout(self.pages["gpu_page"])

        self.gpu_logo = QLabel(self)
        self.gpu_logo.setPixmap(QPixmap("gpu_logo.png").scaled(100, 100))
        self.gpu_logo.setAlignment(Qt.AlignCenter)
        self.gpu_layout.addWidget(self.gpu_logo)

        self.gpu_label = QLabel("GPU Information: ", self)
        self.gpu_label.setStyleSheet("font-size: 16px; text-align: center;")
        self.gpu_layout.addWidget(self.gpu_label)

        self.gpu_description = QLabel("Displays real-time GPU usage, memory utilization, and temperature.", self)
        self.gpu_description.setStyleSheet("font-size: 14px; text-align: center;")
        self.gpu_description.setAlignment(Qt.AlignCenter)
        self.gpu_layout.addWidget(self.gpu_description)

    def init_process_page(self):
        self.process_layout = QVBoxLayout(self.pages["process_page"])

        self.process_logo = QLabel(self)
        self.process_logo.setPixmap(QPixmap("process_logo.png").scaled(100, 100))
        self.process_logo.setAlignment(Qt.AlignCenter)
        self.process_layout.addWidget(self.process_logo)

        self.process_label = QLabel("Processes: ", self)
        self.process_label.setStyleSheet("font-size: 16px; text-align: center;")
        self.process_layout.addWidget(self.process_label)

        self.process_description = QLabel("View the list of currently running processes and their resource usage.", self)
        self.process_description.setStyleSheet("font-size: 14px; text-align: center;")
        self.process_description.setAlignment(Qt.AlignCenter)
        self.process_layout.addWidget(self.process_description)

        self.process_table = QTableWidget(self)
        self.process_table.setColumnCount(5)
        self.process_table.setHorizontalHeaderLabels([
            "PID", "Name", "CPU (%)", "Memory (MB)", "Status"
        ])
        self.process_layout.addWidget(self.process_table)

    def show_home_page(self):
        self.content_area.setCurrentWidget(self.pages["home_page"])

    def show_cpu_page(self):
        self.content_area.setCurrentWidget(self.pages["cpu_page"])

    def show_memory_page(self):
        self.content_area.setCurrentWidget(self.pages["memory_page"])

    def show_gpu_page(self):
        self.content_area.setCurrentWidget(self.pages["gpu_page"])

    def show_battery_page(self):
        self.content_area.setCurrentWidget(self.pages["battery_page"])

    def show_network_page(self):
        self.content_area.setCurrentWidget(self.pages["network_page"])

    def show_disk_page(self):
        self.content_area.setCurrentWidget(self.pages["disk_page"])

    def show_process_page(self):
        self.content_area.setCurrentWidget(self.pages["process_page"])

    def update_metrics(self):
        self.update_cpu_page()
        self.update_memory_page()
        self.update_battery_page()
        self.update_network_page()
        self.update_disk_page()
        self.update_gpu_page()
        self.update_process_page()

    def update_cpu_page(self):
        cpu_usage = psutil.cpu_percent(interval=0)
        self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")

        self.cpu_usage_history.append(cpu_usage)
        if len(self.cpu_usage_history) > self.history_limit:
            self.cpu_usage_history.pop(0)

        self.cpu_ax.clear()
        self.cpu_ax.plot(self.cpu_usage_history, label="CPU Usage", color="blue")
        self.cpu_ax.set_ylim(0, 100)
        self.cpu_ax.set_title("CPU Usage Over Time")
        self.cpu_ax.set_xlabel("Time")
        self.cpu_ax.set_ylabel("Usage (%)")
        self.cpu_ax.legend()
        self.cpu_canvas_widget.draw()

    def update_memory_page(self):
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        self.memory_label.setText(f"Memory Usage: {memory_usage}%")

        self.memory_usage_history.append(memory_usage)
        if len(self.memory_usage_history) > self.history_limit:
            self.memory_usage_history.pop(0)

        self.memory_ax.clear()
        self.memory_ax.plot(self.memory_usage_history, label="Memory Usage", color="green")
        self.memory_ax.set_ylim(0, 100)
        self.memory_ax.set_title("Memory Usage Over Time")
        self.memory_ax.set_xlabel("Time")
        self.memory_ax.set_ylabel("Usage (%)")
        self.memory_ax.legend()
        self.memory_canvas_widget.draw()

    def update_battery_page(self):
        battery = psutil.sensors_battery()
        if battery:
            self.battery_label.setText(f"Battery: {battery.percent}%")
            status = "Charging" if battery.power_plugged else "Discharging"
            self.battery_status_label.setText(f"Status: {status}")
        else:
            self.battery_label.setText("Battery: N/A")
            self.battery_status_label.setText("Status: N/A")

    def update_network_page(self):
        net_io = psutil.net_io_counters()
        download_speed = net_io.bytes_recv / (1024 * 1024)  # Convert to MB
        upload_speed = net_io.bytes_sent / (1024 * 1024)  # Convert to MB

        self.download_speed_label.setText(f"Download Speed: {download_speed:.2f} MB")
        self.upload_speed_label.setText(f"Upload Speed: {upload_speed:.2f} MB")

    def update_disk_page(self):
        disk_usage = psutil.disk_usage('/')
        self.disk_label.setText(f"Disk Usage: {disk_usage.percent}%")
        free_space = disk_usage.free / (1024 * 1024 * 1024)  # Convert to GB
        self.disk_free_label.setText(f"Free Disk Space: {free_space:.2f} GB")

    def update_gpu_page(self):
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_info = "\n".join([
                    f"GPU {gpu.id}: {gpu.name}, Memory: {gpu.memoryUsed}/{gpu.memoryTotal} MB, Load: {gpu.load*100:.1f}%, Temp: {gpu.temperature} \u00b0C"
                    for gpu in gpus
                ])
                self.gpu_label.setText(gpu_info)
            else:
                self.gpu_label.setText("No GPU found")
        except Exception as e:
            self.gpu_label.setText(f"GPU Error: {e}")

    def update_process_page(self):
        self.process_table.setRowCount(0)
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status']):
            try:
                row = self.process_table.rowCount()
                self.process_table.insertRow(row)

                pid_item = QTableWidgetItem(str(proc.info['pid']))
                name_item = QTableWidgetItem(proc.info['name'])
                cpu_item = QTableWidgetItem(f"{proc.info['cpu_percent']}%")
                mem_item = QTableWidgetItem(f"{proc.info['memory_info'].rss / (1024 * 1024):.2f} MB")
                status_item = QTableWidgetItem(proc.info['status'])

                self.process_table.setItem(row, 0, pid_item)
                self.process_table.setItem(row, 1, name_item)
                self.process_table.setItem(row, 2, cpu_item)
                self.process_table.setItem(row, 3, mem_item)
                self.process_table.setItem(row, 4, status_item)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue


if __name__ == "__main__":
    app = QApplication(sys.argv)
    task_manager = TaskManager()
    task_manager.show()
    sys.exit(app.exec_())
