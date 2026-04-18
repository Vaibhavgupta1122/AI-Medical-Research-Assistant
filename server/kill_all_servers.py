#!/usr/bin/env python3
"""
Complete Server Process Killer
Permanently stops ALL processes on port 5000
"""
import subprocess
import time

def kill_all_node_processes():
    """Kill ALL Node.js processes"""
    print("🚫 Killing ALL Node.js processes...")
    subprocess.run(['taskkill', '/IM', 'node.exe', '/F'], capture_output=True)

def kill_port_5000():
    """Kill all processes using port 5000"""
    print("🔒 Killing all processes on port 5000...")
    try:
        result = subprocess.run(
            'netstat -ano | findstr :5000',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    if pid.isdigit():
                        print(f"💀 Killing process {pid} on port 5000")
                        subprocess.run(['taskkill', '/PID', pid, '/F'], capture_output=True)
    except Exception as e:
        print(f"Error: {e}")

def wait_for_port_free():
    """Wait and verify port 5000 is completely free"""
    import socket
    for i in range(10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', 5000))
                print("✅ Port 5000 is free!")
                return True
        except:
            print(f"⏳ Waiting for port 5000 to be free... ({i+1}/10)")
            time.sleep(2)
    
    print("❌ Port 5000 is still occupied")
    return False

def main():
    print("🎯 COMPLETE PORT 5000 CLEANUP")
    print("=" * 50)
    
    # Step 1: Kill all Node.js processes
    kill_all_node_processes()
    time.sleep(2)
    
    # Step 2: Kill port 5000 specifically
    kill_port_5000()
    time.sleep(3)
    
    # Step 3: Verify port is free
    if wait_for_port_free():
        print("\n🎉 SUCCESS! Port 5000 is completely free!")
        print("🚀 You can now run: npm start")
        return True
    else:
        print("\n💥 FAILED! Port 5000 cleanup incomplete")
        return False

if __name__ == "__main__":
    main()
