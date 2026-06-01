# 🚀 บันทึกการอัปเดต (Release Notes) - CorePriority Pro v2.2.2

## 🌟 มีอะไรใหม่ (What's New)
- **Robust CPU Topology Logic**: ปรับปรุงระบบตรวจจับ Core ใหม่ทั้งหมด รองรับ Hybrid CPUs (Intel 12th Gen+) และระบบ SMT (Hyper-Threading) ได้อย่างแม่นยำ
- **Smart SMT Handling**: เมื่อเลือก 'Exclude Core 0' ระบบจะสั่งปิด Logical Core ทั้งหมดที่อยู่บน Physical Core เดียวกันโดยอัตโนมัติ เพื่อประสิทธิภาพสูงสุด
- **Affinity Mask Calculation**: เพิ่มการคำนวณ Bitmask สำหรับ CPU Affinity ทำให้การจัดการ Core ทำงานในระดับลึก (System Level) ได้เสถียรยิ่งขึ้น
- **Enhanced Error Handling**: เพิ่มระบบดักจับ Exception สำหรับสิทธิ์การเข้าถึง (Admin Rights) และกระบวนการที่ถูกป้องกันโดยระบบ
- **System Tray Integration**: สามารถย่อหน้าต่างลงใน System Tray เพื่อทำงานเบื้องหลังได้
- **Updated Dependencies**: อัปเดตไลบรารีเพื่อความเสถียรและการจัดการทรัพยากรที่ดีขึ้น

## 📦 ข้อมูลทางเทคนิค (Technical Details)
- **อินเตอร์เฟส**: CustomTkinter 5.2.2
- **การจัดการถาดระบบ**: pystray 0.19.5, Pillow 12.2.0

----
*สร้างขึ้นด้วยความใส่ใจ เพื่อให้ทุกเฟรมของคุณลื่นไหลที่สุด*
