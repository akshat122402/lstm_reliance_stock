import subprocess
import os
import time

def run_command(command):
    return subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, env=os.environ.copy())

if __name__ == "__main__":
    try:
        print("Starting Flask API server...")
        backend = run_command("python app.py")

        time.sleep(10)

        print("Starting Streamlit app...")
        frontend = run_command("streamlit run streamlit_app.py")

        backend.wait()
        frontend.wait()
    except Exception as e:
        print(f"An error occurred: {e}")