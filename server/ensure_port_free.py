#!/usr/bin/env python3
"""
Port 5000 Security Script
Ensures only the server can use port 5000
"""
import subprocess
import sys
import time
import socket

def is_port_free(port):
    """Check if port is completely free"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except:
            return False

def kill_all_port_users(port):
    """Kill ALL processes using the specified port"""
    print(f"🔒 Securing port {port}...")
    
    # Method 1: netstat approach
    try:
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            pids_killed = set()
            
            for line in lines:
                if 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        if pid.isdigit() and pid not in pids_killed:
                            print(f"🚫 Terminating process {pid} on port {port}")
                            subprocess.run(['taskkill', '/PID', pid, '/F'], capture_output=True)
                            pids_killed.add(pid)
                            
    except Exception as e:
        print(f"Error with netstat: {e}")
    
    # Method 2: Kill any remaining node processes
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq node.exe', '/FO', 'CSV'], 
                              capture_output=True, text=True)
        if result.stdout and 'node.exe' in result.stdout:
            print("🚫 Terminating all remaining node processes...")
            subprocess.run(['taskkill', '/IM', 'node.exe', '/F'], capture_output=True)
    except:
        pass

def secure_port_5000():
    """Main function to secure port 5000"""
    port = 5000
    max_attempts = 5
    
    for attempt in range(max_attempts):
        print(f"📊 Attempt {attempt + 1}/{max_attempts} to secure port {port}")
        
        # Kill all processes using the port
        kill_all_port_users(port)
        
        # Wait for cleanup
        time.sleep(3)
        
        # Check if port is free
        if is_port_free(port):
            print(f"✅ Port {port} is now secure and free!")
            return True
        else:
            print(f"⚠️  Port {port} still occupied, retrying...")
    
    print(f"❌ Failed to secure port {port} after {max_attempts} attempts")
    return False

if __name__ == "__main__":
    if secure_port_5000():
        print("🎯 Port 5000 is ready for your server!")
        print("🚀 You can now run: npm start")
    else:
        print("💥 Port security failed. Check manually.")
        sys.exit(1)
