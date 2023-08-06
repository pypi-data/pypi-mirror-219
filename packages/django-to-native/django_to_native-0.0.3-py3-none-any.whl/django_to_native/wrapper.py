import subprocess
import sys

def wrap_desktop():
    # Get the command-line arguments
    args = sys.argv[2:]  # Exclude the first two arguments (e.g., 'wrap' and 'desktop')
    app_name = None
    url = None
    
    # Extract app name and URL from arguments
    for i in range(len(args)):
        if args[i] == "--url":
            app_name = " ".join(args[:i])
            url = args[i+1]
            break
    
    if app_name and url:
        # Run create-electron-app
        subprocess.run(['npx', 'create-electron-app', app_name], shell=True)
    else:
        print("Invalid command. Please provide the app name followed by '--url' and a URL.")
