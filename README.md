# CorePriority Pro 🚀 (v2.2.4)

[TH] **CorePriority Pro** คือสุดยอดเครื่องมือปรับแต่ง CPU ที่เกิดมาเพื่อ "เกมเมอร์" และ "สตรีมเมอร์" โดยเฉพาะ! ออกแบบมาเพื่อจัดการกับ CPU สถาปัตยกรรม Hybrid (Intel Gen 12 ขึ้นไป) ให้ทำงานได้เต็มประสิทธิภาพสูงสุด โดยการคุมให้เกมรันบน P-Core ที่แรงที่สุด และโยนงานเบื้องหลังไปไว้ที่ E-Core เพื่อไม่ให้มาดึงเฟรมเรตของคุณ

[EN] **CorePriority Pro** is the ultimate CPU optimization utility built for gamers and streamers. Designed specifically for Intel Hybrid Architecture (12th Gen+), it ensures your games run exclusively on high-performance P-Cores while offloading background tasks to Efficiency Cores, eliminating micro-stutter and maximizing FPS.

---

## 🌟 จุดเด่นที่ทำให้เราแตกต่าง (Key Features)

### 🇹🇭 [TH] ภาษาไทย
- **🧹 Auto Junk Cleanup (ใหม่!):** ระบบล้างไฟล์ขยะอัตโนมัติทุก 24 ชั่วโมง ช่วยให้พื้นที่ Hard Drive ว่างและเครื่องลื่นขึ้นโดยไม่ต้องกดเอง
- **🎯 แยก Core แม่นยำ 100%:** ใช้ Windows API อ่านค่าจาก Hardware โดยตรง แยก P-Core และ E-Core ได้ถูกต้อง แม้คุณจะปิด Hyper-Threading ใน BIOS
- **⚡ ระบบคุม SMT อัจฉริยะ:** สั่งให้เกมรันเฉพาะ "Physical Cores" (Thread แรก) ได้เพียงแค่คลิกเดียว ช่วยลด Latency และความร้อน
- **🚀 โหมดจัดลำดับความสำคัญ:** ปรับแต่ง P-CORE Mode และ E-CORE Mode ได้ตามใจชอบ
- **📂 จัดการยกโฟลเดอร์:** รองรับการจัดการทุกเกมใน Steam, Epic, หรือโฟลเดอร์เกมอื่นๆ โดยอัตโนมัติ

### 🇺🇸 [EN] English
- **🧹 Auto Junk Cleanup (New):** Automatically cleans system temporary files every 24 hours to ensure your system stays lean and fast.
- **🎯 Robust Hybrid Detection:** Uses direct Windows API calls to identify `EfficiencyClass`, ensuring perfect core mapping regardless of BIOS settings.
- **⚡ Manual SMT Control:** Force games to use only Physical Cores with a single toggle. Reduces context-switching latency and improves 1% low FPS.
- **🚀 Advanced Affinity Modes:** High-performance locking for games and efficiency offloading for background apps (OBS, Browsers).
- **📂 Path-Based Optimization:** Add your entire game library (Steam/Epic/etc.) and let the software handle every game automatically.

---

## 🔍 ทำไมต้องใช้ CorePriority Pro? (Technical Deep Dive)

### 🇹🇭 [TH] ภาษาไทย
ปัญหาใหญ่ของ Windows คือบางครั้งมันเอา "เกม" ไปรันบน E-Core หรือสลับคอร์ไปมา ทำให้เกิดอาการ **Micro-stutter (กระตุกกึกๆ)** CorePriority Pro จะเข้ามา "ล็อค" ให้เกมอยู่กับที่บนคอร์ที่แรงที่สุด และด้วยระบบ **SMT Filtering** ในเวอร์ชันล่าสุด จะช่วยให้เข้าถึงพลังของ Physical Core ได้โดยตรง ไม่ต้องผ่าน Hyper-Threading ที่อาจทำให้เกิดความร้อนและ Latency สะสม

### 🇺🇸 [EN] English
Windows Scheduler doesn't always get it right. By forcing core affinity, CorePriority Pro eliminates the overhead of thread migration. Version 2.2.4 continues our commitment to performance by introducing background maintenance, allowing the raw power of physical cores to be utilized without system clutter slowing you down.

---

## 🛠 วิธีใช้งาน (How to Use)

1. **Run as Admin:** ต้องรันโปรแกรมด้วยสิทธิ์ผู้ดูแลระบบเสมอ
2. **Settings:**
    - เปิด **Auto Junk Cleanup** หากต้องการให้ระบบคลีนไฟล์ขยะอัตโนมัติ
    - เปิด **Disable SMT (Phys Only)** เพื่อความลื่นไหลสูงสุดในเกม
3. **Add Targets:** เพิ่มไฟล์ .exe ของเกม หรือเลือกโฟลเดอร์เกมในหน้า Settings
4. **Start:** กดปุ่ม **START OPTIMIZER** ในหน้า Dashboard แล้วไปลุยในเกมได้เลย!

---

## 📦 การติดตั้ง (Installation)
```bash
git clone https://github.com/TDitbam/CoreOptimizer.git
cd CoreOptimizer
pip install -r requirements.txt
python main.py
```

---
*Developed with ❤️ for the Gaming Community.*
*เวอร์ชัน 2.2.4 - คลีนกว่า แรงกว่า เสถียรกว่า*
