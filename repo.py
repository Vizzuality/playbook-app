import os
import subprocess
import logging
from datetime import datetime
from index_builder import IndexBuilder


def create_log_directory(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


def log_to_file(log_dir, cmd, output, error):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_dir_fullpath = os.path.join(os.getcwd(), log_dir, 'git_commands.log')
    logging.info(f"Logging content repo update to {log_dir_fullpath}")
    with open(log_dir_fullpath, 'a') as log_file:
        log_file.write(f"Timestamp: {timestamp}\n")
        log_file.write(f"Command: {cmd}\n")
        log_file.write(f"Output: {output}\n")
        log_file.write(f"Error: {error}\n")
        log_file.write(f"{'-' * 80}\n")


def run_command(cmd, cwd, log_dir):
    process = subprocess.run(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    log_to_file(log_dir, cmd, process.stdout, process.stderr)
    return process


def pull_changes(local_repo_path, branch):
    logging.info("Pulling latest content from Github")
    log_dir = 'logs'

    create_log_directory(log_dir)

    run_command(f"git fetch origin", local_repo_path, log_dir)
    run_command(f"git reset --hard origin/{branch}", local_repo_path,
                log_dir)  # Replace 'main' with your default branch
    run_command(f"git clean -fd", local_repo_path, log_dir)
    run_command(f"git status", local_repo_path, log_dir)
    run_command(f"git remote show origin", local_repo_path, log_dir)

    IndexBuilder().reload_data()
