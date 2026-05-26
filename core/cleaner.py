import os
import shutil
import platform

def get_junk_paths():
    paths = []
    if platform.system() == "Windows":
        # User Temp
        user_temp = os.environ.get('TEMP')
        if user_temp:
            paths.append(user_temp)
        
        # System Temp
        sys_temp = "C:\\Windows\\Temp"
        if os.path.exists(sys_temp):
            paths.append(sys_temp)
            
        # Prefetch (requires admin usually, but we can try)
        prefetch = "C:\\Windows\\Prefetch"
        if os.path.exists(prefetch):
            paths.append(prefetch)
            
    return paths

def clean_junk(progress_callback=None):
    """
    Cleans junk files and directories.
    Returns: (files_deleted, bytes_saved)
    """
    files_deleted = 0
    bytes_saved = 0
    
    paths = get_junk_paths()
    
    for path in paths:
        if not os.path.exists(path):
            continue
            
        for root, dirs, files in os.walk(path):
            # Clean files
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    size = os.path.getsize(file_path)
                    os.remove(file_path)
                    files_deleted += 1
                    bytes_saved += size
                    if progress_callback:
                        progress_callback(f"Deleted: {name}")
                except Exception:
                    continue # Skip files in use
            
            # Clean empty directories
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    shutil.rmtree(dir_path)
                    if progress_callback:
                        progress_callback(f"Removed Dir: {name}")
                except Exception:
                    continue
                    
    return files_deleted, bytes_saved
