# CorePriority Pro 🚀 (v2.2.3)

CorePriority Pro คือเครื่องมือจัดการ CPU สำหรับเกมเมอร์และสตรีมเมอร์  
ออกแบบมาสำหรับ Intel Hybrid Architecture (12th Gen ขึ้นไป) เพื่อเพิ่มประสิทธิภาพการเล่นเกม ลดอาการกระตุก (micro-stutter) และควบคุมการใช้งาน P-Core / E-Core อย่างแม่นยำ

---

## ✨ Key Features

### 🎯 Hybrid Core Detection (แม่นยำระดับ OS)
- ใช้ Windows API: `GetLogicalProcessorInformationEx`
- อ่านค่า `EfficiencyClass` โดยตรงจากระบบ
- แยก P-Core / E-Core ได้ถูกต้อง แม้ปิด Hyper-Threading ใน BIOS

---

### ⚡ SMT Control Mode (Physical Core Only)
- บังคับให้เกมใช้เฉพาะ Physical Core (logical thread แรก)
- ลด context switching และ latency ระหว่าง thread
- เปิด/ปิดได้แบบ real-time ผ่าน UI

---

### 🚀 Affinity Management System
- P-Core Mode: ล็อกเกมไว้บนคอร์ประสิทธิภาพสูง
- E-Core Mode: ย้ายแอปเบื้องหลัง (Discord / OBS / Browser)
- ลดการแย่งทรัพยากรระหว่างเกมและ background processes

---

### 📂 Game Library Support
- เพิ่มโฟลเดอร์เกม (Steam / Epic / Launcher) ได้ครั้งเดียว
- ระบบจัดการทุกเกมในโฟลเดอร์อัตโนมัติ

---

### 🧹 Built-in Cleaner
- ลบ temporary files และ shader cache
- ลด system overhead ก่อนเข้าเกม

---

## 🧠 Why CorePriority Pro?

Windows Scheduler อาจสลับ thread ไปยังคอร์ที่ไม่เหมาะสม เช่น E-Core  
ส่งผลให้เกิดอาการกระตุกเป็นช่วง (micro-stutter)

CorePriority Pro แก้ปัญหานี้โดย:
- ล็อก workload เกมไปยัง P-Core
- ลดการย้าย thread ข้าม core
- ลด overhead จาก Hyper-Threading ใน workload เกม

ผลลัพธ์ที่ได้:
- frame time นิ่งขึ้น
- latency ลดลง
- 1% low FPS ดีขึ้น

---
<img width="952" height="732" alt="Screenshot 2026-06-01 231545" src="https://github.com/user-attachments/assets/7ff2f2d1-adb8-4cfb-ab91-5aea08fedb4c" />
<img width="952" height="732" alt="Screenshot 2026-06-01 231557" src="https://github.com/user-attachments/assets/b56ddf72-2305-4425-b2cb-77574a30539a" />
<img width="952" height="732" alt="Screenshot 2026-06-01 231704" src="https://github.com/user-attachments/assets/d148402b-4239-49c3-a198-b541c3ca7c1d" />

---

## 🛠 How to Use

1. Run as Administrator
2. เพิ่มเกม (.exe) หรือเลือกโฟลเดอร์เกม
3. เลือกโหมด:
   - P-Core Mode (สำหรับเกม)
   - E-Core Mode (สำหรับแอปเบื้องหลัง)
4. กด Start Optimizer แล้วเริ่มเล่นได้ทันที

---

## 📦 Installation

```bash
git clone https://github.com/TDitbam/CoreOptimizer.git
cd CoreOptimizer
pip install -r requirements.txt
python main.py
