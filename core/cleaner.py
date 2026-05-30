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
            
    return paths

def clean_junk(progress_callback=None):
    """
    Cleans junk files and directories safely without breaking games or apps.
    Returns: (files_deleted, bytes_saved)
    """
    files_deleted = 0
    bytes_saved = 0
    
    # 🌟 1. กำหนด Whitelist (คำที่ถ้าเจอใน Path ห้ามลบเด็ดขาด)
    whitelist = [
        "steam", "epic", "unity", "unreal", "riot games", "localbackups", 
        "discord", "spotify", "roblox", "minecraft", "hoyoverse"
    ]
    
    paths = get_junk_paths()
    
    for path in paths:
        if not os.path.exists(path):
            continue
            
        # ใช้ topdown=False เพื่อให้จัดการจากไฟล์ข้างในสุดออกข้างนอก เพื่อความปลอดภัย
        for root, dirs, files in os.walk(path, topdown=False):
            
            # ตรวจสอบว่า root path ปัจจุบันติด Whitelist หรือไม่
            is_whitelisted = any(w_word in root.lower() for w_word in whitelist)
            if is_whitelisted:
                continue # Skip ทั้งโฟลเดอร์นี้ไปเลย
                
            # Clean files
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    # ตรวจสอบขนาดไฟล์ก่อนลบ
                    size = os.path.getsize(file_path)
                    os.remove(file_path)
                    files_deleted += 1
                    bytes_saved += size
                    if progress_callback:
                        progress_callback(f"Deleted: {name}")
                except Exception:
                    continue # ไฟล์ไหนเปิดอยู่ หรือลบไม่ได้ ระบบจะข้ามทันที
            
            # Clean empty directories (ปรับปรุงใหม่ให้ปลอดภัย)
            for name in dirs:
                dir_path = os.path.join(root, name)
                
                # เช็กซ้ำอีกทีเพื่อความชัวร์ว่าไม่ยุ่งกับ Whitelist
                if any(w_word in dir_path.lower() for w_word in whitelist):
                    continue
                    
                try:
                    # 🌟 เปลี่ยนจาก shutil.rmtree เป็น os.rmdir
                    # os.rmdir จะยอมลบก็ต่อเมื่อโฟลเดอร์นั้น "ว่างเปล่าจริงๆ" เท่านั้น
                    os.rmdir(dir_path)
                    if progress_callback:
                        progress_callback(f"Removed Empty Dir: {name}")
                except Exception:
                    continue
                    
    return files_deleted, bytes_saved
