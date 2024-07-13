import os
import shutil
import logging
import schedule
import time
import argparse

class BackupAndCleanupTask:
    def __init__(self, source_dir, backup_dir, log_file):
        self.source_dir = source_dir
        self.backup_dir = backup_dir
        self.log_file = log_file
        self.logger = logging.getLogger('backup_cleanup_task')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def backup_files(self):
        try:
            shutil.copytree(self.source_dir, self.backup_dir)
            self.logger.info(f"Backup completed successfully from {self.source_dir} to {self.backup_dir}.")
        except Exception as e:
            self.logger.error(f"Error during backup process: {str(e)}")
            raise

    def cleanup_files(self):
        try:
            for filename in os.listdir(self.source_dir):
                file_path = os.path.join(self.source_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            self.logger.info(f"Cleanup completed successfully in {self.source_dir}.")
        except Exception as e:
            self.logger.error(f"Error during cleanup process: {str(e)}")
            raise

def perform_backup_and_cleanup(backup_cleanup_task):
    backup_cleanup_task.backup_files()
    backup_cleanup_task.cleanup_files()

# Парсинг аргументов командной строки
parser = argparse.ArgumentParser(description="Backup and Cleanup Task with time specification.")
parser.add_argument("--source_dir", type=str, help="Source directory for backup")
parser.add_argument("--backup_dir", type=str, help="Backup directory to store files")
parser.add_argument("--log_file", type=str, help="Path to log file")
parser.add_argument("--time", type=str, help="Time to run the task")

args = parser.parse_args()

source_dir = args.source_dir
backup_dir = args.backup_dir
log_file = args.log_file
task_time = args.time

# Инициализация объекта задачи резервного копирования и очистки с переданными аргументами
backup_cleanup = BackupAndCleanupTask(source_dir, backup_dir, log_file)

# Расписание выполнения задачи в указанное время
schedule.every().day.at(task_time).do(perform_backup_and_cleanup, backup_cleanup)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
