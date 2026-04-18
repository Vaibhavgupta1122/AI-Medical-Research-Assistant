#!/usr/bin/env python3
"""
AI Service Startup Script
Handles port conflicts and provides clean startup
"""
import subprocess
import sys
import time
import socket

def kill_processes_on_port(port):
    """Kill processes using the specified port using netstat"""
    try:
        # Find processes using the port
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            pids = set()
            
            for line in lines:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    if pid.isdigit():
                        pids.add(pid)
            
            # Kill each process
            for pid in pids:
                print(f"Terminating process {pid} using port {port}")
                subprocess.run(['taskkill', '/PID', pid, '/F'], capture_output=True)
                
    except Exception as e:
        print(f"Error killing processes: {e}")

def check_port_available(port):
    """Check if port is available"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except:
            return False

def main():
    port = 8000
    
    print(f"Starting AI Medical Research Service on port {port}...")
    
    # Kill existing processes on port
    print("Checking for existing processes on port 8000...")
    kill_processes_on_port(port)
    
    # Wait a moment for processes to terminate
    time.sleep(2)
    
    # Check if port is now available
    if not check_port_available(port):
        print(f"Port {port} is still in use. Please check manually.")
        sys.exit(1)
    
    # Start the service
    print("Starting AI service...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "simple_main:app", 
            "--host", "127.0.0.1",
            "--port", str(port),
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\nService stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start service: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
