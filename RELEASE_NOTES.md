# 🚀 บันทึกการอัปเดต (Release Notes) - CorePriority Pro v2.2.4

## 🌟 มีอะไรใหม่ (What's New)
- **Auto Junk Cleanup**: ระบบล้างไฟล์ขยะอัตโนมัติ! เมื่อเปิดใช้งาน โปรแกรมจะช่วยคลีนไฟล์ Temp และ Cache ที่ไม่จำเป็นให้ทุกๆ 24 ชั่วโมง เพื่อให้เครื่องลื่นไหลอยู่เสมอ
- **Background Processing**: ระบบคลีนทำงานเบื้องหลัง ไม่รบกวนการเล่นเกมหรือการใช้งาน GUI
- **Improved Settings UI**: จัดวางหน้า Settings ใหม่ให้รองรับตัวเลือกที่มากขึ้น (Exclude Core 0, Disable SMT, Auto Cleanup)
- **Elevation Fix (v2.2.3.1)**: แก้ไขปัญหา Error 740 ในตัวติดตั้ง โดยการใช้ระบบ ShellExecute เพื่อรองรับสิทธิ์ Admin อย่างถูกต้อง

## 📦 ข้อมูลทางเทคนิค (Technical Details)
- **Cleanup Cycle**: 24 Hours (Every 86,400 seconds)
- **Safety**: ใช้ระบบ Whitelist ป้องกันการลบไฟล์สำคัญของ Steam, Epic, Unity และแอปยอดนิยมอื่นๆ
- **API**: Windows API + Background Threading

----
*สร้างขึ้นด้วยความใส่ใจ เพื่อให้ทุกเฟรมของคุณลื่นไหลที่สุด*
