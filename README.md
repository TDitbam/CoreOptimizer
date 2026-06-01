# CorePriority Pro 🚀 (v2.2.3)

[TH] **CorePriority Pro** คือสุดยอดเครื่องมือปรับแต่ง CPU ที่เกิดมาเพื่อ "เกมเมอร์" และ "สตรีมเมอร์" โดยเฉพาะ! ออกแบบมาเพื่อจัดการกับ CPU สถาปัตยกรรม Hybrid (Intel Gen 12 ขึ้นไป) ให้ทำงานได้เต็มประสิทธิภาพสูงสุด โดยการคุมให้เกมรันบน P-Core ที่แรงที่สุด และโยนงานเบื้องหลังไปไว้ที่ E-Core เพื่อไม่ให้มาดึงเฟรมเรตของคุณ

[EN] **CorePriority Pro** is the ultimate CPU optimization utility built for gamers and streamers. Designed specifically for Intel Hybrid Architecture (12th Gen+), it ensures your games run exclusively on high-performance P-Cores while offloading background tasks to Efficiency Cores, eliminating micro-stutter and maximizing FPS.

---

## 🌟 จุดเด่นที่ทำให้เราแตกต่าง (Key Features)

### 🇹🇭 [TH] ภาษาไทย
- **🎯 แยก Core แม่นยำ 100% (ใหม่!):** เลิกสุ่ม! เราใช้ Windows API อ่านค่าจาก Hardware โดยตรง แยก P-Core และ E-Core ได้ถูกต้อง แม้คุณจะปิด Hyper-Threading ใน BIOS ก็ตาม
- **⚡ ระบบคุม SMT อัจฉริยะ (ใหม่!):** สั่งให้เกมรันเฉพาะ "Physical Cores" (Thread แรก) ได้เพียงแค่คลิกเดียว ช่วยลด Latency (อาการหน่วง) และความร้อนได้อย่างเห็นผล
- **🚀 โหมดจัดลำดับความสำคัญ:** 
    - **P-CORE Mode:** บังคับเกมรันบนคอร์ที่แรงที่สุดเท่านั้น
    - **E-CORE Mode:** ย้าย Discord, OBS, หรือ Browser ไปไว้ที่คอร์ประหยัดพลังงาน
- **📂 จัดการยกโฟลเดอร์:** ไม่ต้องแอดทีละเกม! แค่เลือกโฟลเดอร์ Steam หรือ Epic ของคุณ ระบบจะจัดการทุกเกมที่เปิดจากในนั้นทันที
- **🧹 คลีนเนอร์ในตัว:** ลบไฟล์ขยะและ Shader Cache ที่ค้างอยู่ในระบบ เพื่อให้เครื่องลื่นไหลที่สุด

### 🇺🇸 [EN] English
- **🎯 Robust Hybrid Detection (New):** No more guessing. We use direct Windows API calls to identify `EfficiencyClass`, ensuring perfect P/E core mapping regardless of BIOS settings.
- **⚡ Manual SMT Control (New):** Force games to use only Physical Cores with a single toggle. Reduces context-switching latency and improves 1% low FPS.
- **🚀 Advanced Affinity Modes:**
    - **P-CORE Mode:** Locks critical apps to high-performance execution units.
    - **E-CORE Mode:** Offloads background apps (OBS, Browsers) to efficiency cores.
- **📂 Path-Based Optimization:** Add your entire game library (Steam/Epic/etc.) and let the software handle every game automatically.
- **🧹 Integrated System Cleaner:** Free up space and reduce system overhead by cleaning temporary junk and cache files.

---

## 🔍 ทำไมต้องใช้ CorePriority Pro? (Technical Deep Dive)

### 🇹🇭 [TH] ภาษาไทย
ปัญหาใหญ่ของ Windows คือบางครั้งมันเอา "เกม" ไปรันบน E-Core หรือสลับคอร์ไปมา ทำให้เกิดอาการ **Micro-stutter (กระตุกกึกๆ)** CorePriority Pro จะเข้ามา "ล็อค" ให้เกมอยู่กับที่บนคอร์ที่แรงที่สุด และด้วยระบบ **SMT Filtering** ในเวอร์ชัน 2.2.3 จะช่วยให้เข้าถึงพลังของ Physical Core ได้โดยตรง ไม่ต้องผ่าน Hyper-Threading ที่อาจทำให้เกิดความร้อนและ Latency สะสม

### 🇺🇸 [EN] English
Windows Scheduler doesn't always get it right. By forcing core affinity, CorePriority Pro eliminates the overhead of thread migration. Version 2.2.3 introduces hardware-level masking, allowing apps to bypass logical threads (Hyper-Threading) and utilize the raw power of physical cores, resulting in smoother frame times and better thermal efficiency.

---

## 🛠 วิธีใช้งาน (How to Use)

1. **Run as Admin:** ต้องรันโปรแกรมด้วยสิทธิ์ผู้ดูแลระบบเสมอ
2. **Add Targets:** เพิ่มไฟล์ .exe ของเกม หรือเลือกโฟลเดอร์เกมของคุณในหน้า Settings
3. **Choose Mode:** เลือกโหมด P-CORE สำหรับเกม และ E-CORE สำหรับแอปเบื้องหลัง
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
*เวอร์ชัน 2.2.3 - แม่นยำกว่า แรงกว่า เสถียรกว่า*
