# 🚀 บันทึกการอัปเดต (Release Notes) - CorePriority Pro v2.2.3

## 🌟 มีอะไรใหม่ (What's New)
- **Windows API Robust Detection**: เปลี่ยนมาใช้ `EfficiencyClass` จาก Windows API โดยตรง ทำให้แยกแยะ P-Core และ E-Core ได้ถูกต้อง 100% แม้จะปิด Hyper-Threading (SMT) ใน BIOS
- **Manual SMT Control (Phys Only)**: เพิ่มฟีเจอร์ "Disable SMT (Phys Only)" ในหน้า Settings เพื่อบังคับให้โปรแกรมใช้เฉพาะ Physical Cores (Thread แรกของแต่ละ Core) เพื่อลด Latency
- **Multi-Group CPU Support**: รองรับ CPU ที่มีมากกว่า 64 Logical Processors (เช่น Threadripper, Xeon)
- **Improved UI Dashboard**: แสดงจำนวน Core แยกประเภทแบบ Real-time ตามโหมดการทำงานที่เลือก
- **Bug Fixes**: แก้ไขปัญหา IndentationError ใน main loop และปรับปรุงความเสถียรของการบันทึก Config

## 📦 ข้อมูลทางเทคนิค (Technical Details)
- **API**: Windows GetLogicalProcessorInformationEx
- **ความต้องการ**: Windows 10/11 (สำหรับ Hybrid Detection)
- **สิทธิ์การใช้งาน**: ต้องรันด้วย Administrator

----
*สร้างขึ้นด้วยความใส่ใจ เพื่อให้ทุกเฟรมของคุณลื่นไหลที่สุด*
