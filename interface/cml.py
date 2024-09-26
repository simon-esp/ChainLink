elif cmd.startswith('paste'):
    if clipboard:
        print(f"Clipboard contains: '{clipboard}'")  # Debugging print
        destination = os.path.join(wp, os.path.basename(clipboard))
        print(f"Destination path: '{destination}'")  # Debugging print
        
        try:
            if os.path.isfile(clipboard):
                shutil.copy(clipboard, destination)  # Use shutil.copy for files
                print(f"File pasted to '{destination}'")
            elif os.path.isdir(clipboard):
                shutil.copytree(clipboard, destination)  # Use shutil.copytree for directories
                print(f"Directory pasted to '{destination}'")
            
            # If cut, remove original
            if 'cut' in cmd:  
                if os.path.isfile(clipboard):
                    os.remove(clipboard)
                    print(f"File '{clipboard}' removed after cut-paste.")
                elif os.path.isdir(clipboard):
                    shutil.rmtree(clipboard)
                    print(f"Directory '{clipboard}' removed after cut-paste.")
            
            clipboard = None  # Clear clipboard after paste
        except Exception as e:
            print(f"An error occurred during paste: {e}")
    else:
        print("Clipboard is empty, copy or cut something first.")
