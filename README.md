# 🚀 CorePriority Pro v3.1.0

CorePriority Pro เป็นเครื่องมือจัดการทรัพยากร CPU และทำความสะอาดระบบที่ออกแบบมาเพื่อเพิ่มประสิทธิภาพการเล่นเกมและการทำงานหนักบน Windows โดยเฉพาะระบบที่มีสถาปัตยกรรม Hybrid (P-Core & E-Core)

---

## ✨ คุณสมบัติหลัก (Key Features)

### 1. 🧠 Intelligent Process Optimizer (v3 Engine)
*   **Hybrid Architecture Support**: แยกการทำงานระหว่าง P-Cores (Performance) และ E-Cores (Efficiency) ได้อย่างแม่นยำ
*   **Auto-Affinity Control**: บังคับให้เกมหรือโปรแกรมที่เลือกใช้เฉพาะ P-Cores เพื่อลด Latency และป้องกันการสลับ Core ไปมา
*   **Priority Management**: ปรับระดับความสำคัญของ Process (Nice Level) อัตโนมัติ
*   **Exclusion Logic**: ระบบป้องกันการรบกวน Core 0 เพื่อให้ OS ทำงานได้ราบรื่น

### 2. 🧹 Advanced Junk & GPU Cleaner
*   **System Cleanup**: ล้างไฟล์ขยะใน Windows Temp และ User Temp
*   **GPU Shader Cache**: ล้างไฟล์ Cache ของ NVIDIA (DX/GL), AMD และ Intel เพื่อลดอาการ Stutter ในเกม
*   **Safety Whitelist**: ระบบป้องกันไฟล์สำคัญ (Steam, Epic, Discord ฯลฯ) ไม่ให้ถูกลบโดยไม่ตั้งใจ
*   **Auto-Cleanup Mode**: ตั้งเวลาทำความสะอาดอัตโนมัติ (หน่วยเป็นนาที)

### 3. 🖥️ Modern GUI
*   **Dark Mode**: อินเตอร์เฟสสวยงาม ใช้งานง่าย
*   **Real-time Dashboard**: แสดงสถานะการทำงานและจำนวน Core ที่ระบบตรวจพบ
*   **Managed Directories**: เลือกโฟลเดอร์ที่ต้องการให้ระบบจัดการ Priority ของโปรแกรมข้างในทั้งหมดได้อัตโนมัติ

---

## 🛠️ การติดตั้ง (Installation)

### สำหรับผู้ใช้ทั่วไป
1. ดาวน์โหลดไฟล์ `CoreOptimizer_Setup_v3.1.0.exe` จากโฟลเดอร์ `build_dist`
2. รันตัวติดตั้งและทำตามขั้นตอน
3. **สำคัญ**: โปรแกรมจำเป็นต้องได้รับสิทธิ์ **Administrator** เพื่อจัดการ Affinity ของ CPU และล้างไฟล์ขยะระบบ

### สำหรับนักพัฒนา (Build from Source)
```bash
# ติดตั้ง Library ที่จำเป็น
pip install -r requirements.txt

# รันโปรแกรม (GUI Mode)
python main.py

# รันโปรแกรม (CLI Mode)
python main.py --cli
```

---

## ⚙️ วิธีการใช้งาน (How to use)

1. **Dashboard**: กดปุ่ม `START OPTIMIZER` เพื่อเริ่มระบบจัดการ CPU อัตโนมัติ
2. **Settings**:
   - เพิ่มชื่อไฟล์ `.exe` ของเกมที่ต้องการในแท็บ `Games`
   - เลือกโหมด `P-CORE` สำหรับเกมที่ต้องการประสิทธิภาพสูงสุด
   - ตั้งค่า `Auto Junk Cleanup` และระบุเวลาที่ต้องการ (เช่น 1440 นาที สำหรับ 1 วัน)
3. **Cleanup**: กดปุ่ม `SCAN & CLEAN JUNK` เพื่อล้างไฟล์ขยะระบบและ Shader Cache ของการ์ดจอทันที

---

## 📦 โครงสร้างโปรเจค (Project Structure)
*   `core/`: เอนจิ้นหลัก (Optimizer & Cleaner)
*   `gui/`: ส่วนติดต่อผู้ใช้ (CustomTkinter)
*   `engine/`: ระบบจัดการ State และ Registry ของ Process
*   `policy/`: ตรรกะการตัดสินใจและโมเดลข้อมูล
*   `build_dist/`: ไฟล์สำหรับติดตั้งและไฟล์ .exe

---

## 📄 License
โปรเจคนี้จัดทำภายใต้ MIT License - ดูรายละเอียดในไฟล์ [LICENSE](LICENSE)

**พัฒนาโดย**: TDitbam
**GitHub**: [https://github.com/TDitbam/CoreOptimizer](https://github.com/TDitbam/CoreOptimizer)
