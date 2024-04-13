import os
import csv
import subprocess

# 恶意文件列表
malicious_files = ["virus.exe", "malware.dll", "trojan.py"]

# 检测恶意文件
def check_malicious_files(directory):
    detected_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file in malicious_files:
                detected_files.append(os.path.join(root, file))
    return detected_files

# 检测恶意进程
def check_malicious_processes():
    detected_processes = []
    output = subprocess.check_output(["ps", "-e"])
    processes = output.decode("utf-8").split("\n")
    for process in processes:
        if "malicious_process" in process:  # 替换为实际的恶意进程名
            detected_processes.append(process)
    return detected_processes

# 写入日志文件
def write_log(log_filename, message):
    with open(log_filename, "a") as logfile:
        logfile.write(message + "\n")

# 抛出异常并写入日志
def raise_exception_and_log(log_filename, message):
    write_log(log_filename, message)
    raise Exception(message)

# 主函数
def main():
    directory = "/path/to/scan"  # 替换为要扫描的目录
    log_filename = "scan_log.txt"

    try:
        # 检测恶意文件
        detected_files = check_malicious_files(directory)
        if detected_files:
            raise_exception_and_log(log_filename, "Detected malicious files: {}".format(detected_files))

        # 检测恶意进程
        detected_processes = check_malicious_processes()
        if detected_processes:
            raise_exception_and_log(log_filename, "Detected malicious processes: {}".format(detected_processes))

        # 写入CSV文件
        with open("scan_results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Detected Files", "Detected Processes"])
            writer.writerow([detected_files, detected_processes])

        print("Scan completed successfully. No malicious files or processes found.")

    except Exception as e:
        print("Error occurred during scan: ", e)

# 执行主函数
if __name__ == "__main__":
    main()
