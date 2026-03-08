# 📚 ระบบบริหารจัดการห้องสมุด (Library Management System) - Python

## โครงสร้างโปรเจค
```
LibraryManagement/
├── models/
│   └── book.py
├── algorithms/
│   ├── sorting.py
│   └── searching.py
├── main.py
└── README.md
```

## 📊 สรุป Big O ของแต่ละ Algorithm

### 1. **Insertion Sort** - O(n²)
- **Best Case**: O(n) - เมื่อข้อมูลเรียงอยู่แล้ว
- **Average Case**: O(n²)
- **Worst Case**: O(n²) - เมื่อข้อมูลเรียงย้อนกลับ
- **ใช้เมื่อ**: ข้อมูลจำนวนน้อย (≤ 50 รายการ)

### 2. **Merge Sort** - O(n log n)
- **ทุกกรณี**: O(n log n)
- **ใช้เมื่อ**: ข้อมูลจำนวนมาก (> 50 รายการ)
- **ข้อดี**: มีประสิทธิภาพคงที่ ไม่ขึ้นกับลักษณะข้อมูล

### 3. **Binary Search** - O(log n)
- **ต้องการ**: ข้อมูลต้องเรียงลำดับก่อนค้นหา
- **มีประสิทธิภาพสูง** เมื่อค้นหาด้วย ISBN

### 4. **Sequential Search** - O(n)
- **ไม่ต้องการ**: ข้อมูลเรียงลำดับ
- **ใช้เมื่อ**: ค้นหาจากชื่อหนังสือ (อาจมีหลายรายการ)

## 🚀 วิธีติดตั้งและรันโปรแกรม

1. **สร้างโฟลเดอร์โปรเจค:**
```bash
mkdir LibraryManagement
cd LibraryManagement
```

2. **สร้างโฟลเดอร์ย่อย:**
```bash
mkdir models algorithms
```

3. **สร้างไฟล์ตามโครงสร้างข้างต้น**

4. **รันโปรแกรม:**
```bash
python main.py
```

โปรแกรมนี้จะ:
- ✅ เก็บข้อมูลในไฟล์ JSON เพื่อให้ข้อมูลคงอยู่
- ✅ รองรับการเพิ่ม/แก้ไข/ลบ หนังสือ
- ✅ มีทั้ง Insertion Sort และ Merge Sort ให้เลือกตามขนาดข้อมูล
- ✅ ค้นหาได้ทั้งแบบ Binary Search (ISBN) และ Sequential Search (ชื่อ)
- ✅ แสดงเวลาในการทำงานของแต่ละ Algorithm
