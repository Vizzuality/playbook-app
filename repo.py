import os
import subprocess
from datetime import datetime
from index_builder import build_menus, save_menus_to_files

def create_log_directory(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

def log_to_file(log_dir, cmd, output, error):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(os.path.join(log_dir, 'git_commands.log'), 'a') as log_file:
        log_file.write(f"Timestamp: {timestamp}\n")
        log_file.write(f"Command: {cmd}\n")
        log_file.write(f"Output: {output}\n")
        log_file.write(f"Error: {error}\n")
        log_file.write(f"{'-' * 80}\n")

def run_command(cmd, cwd, log_dir):
    process = subprocess.run(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    log_to_file(log_dir, cmd, process.stdout, process.stderr)
    return process

def pull_changes(local_repo_path):
    git_ssh_command = 'GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no"'
    log_dir = 'logs'
    
    create_log_directory(log_dir)
    
    run_command(f"{git_ssh_command} git fetch origin", local_repo_path, log_dir)
    run_command(f"{git_ssh_command} git reset --hard origin/new_playbook", local_repo_path, log_dir)  # Replace 'main' with your default branch
    run_command(f"{git_ssh_command} git clean -fd", local_repo_path, log_dir)
    run_command(f"{git_ssh_command} git status", local_repo_path, log_dir)
    run_command(f"{git_ssh_command} git remote show origin", local_repo_path, log_dir)

    public_menu, private_menu = build_menus(local_repo_path)
    save_menus_to_files(public_menu, private_menu, local_repo_path)
