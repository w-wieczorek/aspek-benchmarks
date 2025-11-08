import sys
import time
import psutil
import subprocess
import argparse
import requests
import os
import platform
from datetime import datetime
import re

start_time = time.time()

hostname = platform.node()
machine_info = f"Machine Info: {hostname}\n"

def send_notification(title, message, color=0x00ff00):
    try:
        elapsed_time = time.time() - start_time if start_time else None
        time_info = f"\n\nTotal execution time (including monitoring overhead): {elapsed_time:.2f} seconds" if elapsed_time is not None else ""
        optimum_lines = []
        for idx, line in enumerate(message.splitlines()):
            if re.search(r'\b(optimum|optimal)\b', line, re.IGNORECASE):
                optimum_lines.append((idx, line))
        message = re.sub(r"[^\x00-\x7F]+", "", re.sub(r"\s+", " ", message.replace("\n", "--")))[-1024:]
        data = {
            "embeds": [{
                "title": title,
                "description": (machine_info + message + time_info + "\n\nOptimum lines:\n" + "\n".join([f"{idx}: {line}" for idx, line in optimum_lines])),
                "color": color,
                "timestamp": datetime.now().astimezone().isoformat()
            }]
        }
        print(message)
        discord_webhook = os.getenv('MONITOR_DISCORD_WEBHOOK_URL')
        response = requests.post(discord_webhook, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send a notification to Discord: {str(e)}")

def send_error_notification(title, message):
    send_notification(title, message, color=0xCF4444)

def send_warning_notification(title, message):
    send_notification(title, message, color=0xEBBB54)

def send_success_notification(title, message):
    send_notification(title, message, color=0x94BA65)

def monitor_process(pid, cmds, time_limit=None, subprocess_obj=None):
    try:
        process = psutil.Process(pid)
        process_name = process.name()
        start_time = time.time()
        
        output_lines = []
        
        if subprocess_obj:
            import threading
            def read_output(pipe, is_stderr=False):
                try:
                    for line in pipe:
                        if line:
                            output_lines.append(line.strip())
                except Exception as e:
                    output_lines.append(f"Error reading {'stderr' if is_stderr else 'stdout'}: {str(e)}")
            
            stdout_thread = threading.Thread(target=read_output, args=(subprocess_obj.stdout, False))
            stderr_thread = threading.Thread(target=read_output, args=(subprocess_obj.stderr, True))
            stdout_thread.daemon = True
            stderr_thread.daemon = True
            stdout_thread.start()
            stderr_thread.start()
        
        try:
            subprocess_obj.wait(timeout=time_limit if time_limit else None)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                process.kill()
            send_warning_notification(
                "Process Terminated",
                f"Command: {cmds}\nProcess {process_name} (PID: {pid}) was terminated after {time_limit} seconds."
            )
            return
        
        if subprocess_obj:
            stdout_thread.join(timeout=1)
            stderr_thread.join(timeout=1)
        
        output_str = "\n".join(output_lines) if output_lines else "No output"
        send_success_notification("Process Ended", f"Command: {cmds}\nProcess {process_name} (PID: {pid}) has ended.\n\nOutput:\n{output_str}")
    except psutil.NoSuchProcess:
        send_error_notification("Process Not Found", f"Command: {cmds}\nProcess with PID {pid} does not exist.")
    except Exception as e:
        send_error_notification("Error", f"Command: {cmds}\nAn error occurred while monitoring the process: {str(e)}")

def run_commands(commands, time_limit=None):
    try:
        processes = []
        for cmd in commands:
            use_shell = isinstance(cmd, str) and ' ' in cmd
            
            if processes:
                process = subprocess.Popen(
                    cmd,
                    stdin=processes[-1].stdout,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    shell=use_shell
                )
                processes[-1].stdout.close()
            else:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    shell=use_shell
                )
            processes.append(process)
        monitor_process(processes[-1].pid, ' | '.join(commands), time_limit, processes[-1])
        for process in processes:
            process.wait()
    except Exception as e:
        send_error_notification(
            "Error",
            f"Command: {' | '.join(commands)}\n\nError:\n{str(e)}"
        )

parser = argparse.ArgumentParser(description='Monitor a process pipeline and send notification when it ends.')
parser.add_argument('command', nargs='+', help='Commands to run in pipeline (separated by |)')
parser.add_argument('-t', '--time-limit', type=float, help='Maximum execution time in seconds')
args = parser.parse_args()
if args.command:
    commands = []
    for cmd in args.command:
        if '|' in cmd:
            commands.extend(cmd.split('|'))
        else:
            commands.append(cmd)
    commands = [cmd.strip() for cmd in commands]
    run_commands(commands, args.time_limit)
else:
    parser.print_help()
    sys.exit(1)