import streamlit as st
import pandas as pd
import os
import json
import time
from models.book import Book
from algorithms.sorting import SortingAlgorithms
from algorithms.searching import SearchAlgorithms

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="ระบบบริหารจัดการห้องสมุด",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# กำหนดไฟล์ข้อมูล
DATA_FILE = "library_data.json"

# ------------------------------------------------------------------
# ฟังก์ชันช่วยเหลือ (โหลด/บันทึกข้อมูล, แปลงเป็น DataFrame)
# ------------------------------------------------------------------
def load_data():
    """โหลดข้อมูลหนังสือจากไฟล์ JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Book(**book_data) for book_data in data]
        except Exception as e:
            st.warning(f"⚠️ ไม่สามารถโหลดข้อมูลได้: {e}")
            return []
    return []

def save_data(books):
    """บันทึกข้อมูลหนังสือลงไฟล์ JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        data = [book.to_dict() for book in books]
        json.dump(data, f, ensure_ascii=False, indent=2)

def books_to_df(books):
    """แปลงลิสต์หนังสือเป็น pandas DataFrame สำหรับแสดงผล"""
    if not books:
        return pd.DataFrame()
    data = [{
        "ISBN": book.isbn,
        "ชื่อหนังสือ": book.title,
        "ผู้แต่ง": book.author,
        "ปีที่พิมพ์": book.publish_year
    } for book in books]
    return pd.DataFrame(data)

# ------------------------------------------------------------------
# เริ่มต้น Session State
# ------------------------------------------------------------------
if 'books' not in st.session_state:
    st.session_state.books = load_data()

# ------------------------------------------------------------------
# Sidebar - เมนูหลัก
# ------------------------------------------------------------------
with st.sidebar:
    st.title("📚 ระบบห้องสมุด")
    st.metric("จำนวนหนังสือ", len(st.session_state.books))
    st.markdown("---")
    
    menu = st.radio(
        "เลือกเมนู",
        ["📖 ดูหนังสือทั้งหมด",
         "➕ เพิ่มหนังสือ",
         "✏️ แก้ไขหนังสือ",
         "🗑️ ลบหนังสือ",
         "🔀 เรียงลำดับหนังสือ",
         "🔍 ค้นหาหนังสือ"],
        index=0
    )
    st.markdown("---")
    st.caption("พัฒนาด้วย Streamlit • อัลกอริทึมการเรียงและค้นหา")

# ------------------------------------------------------------------
# ฟังก์ชันแสดงตารางหนังสือ (ใช้ซ้ำ)
# ------------------------------------------------------------------
def display_books(books, caption="รายการหนังสือ"):
    """แสดง DataFrame ของหนังสือในรูปแบบที่สวยงาม"""
    if not books:
        st.info("📭 ไม่มีหนังสือในระบบ")
        return
    df = books_to_df(books)
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "ISBN": st.column_config.TextColumn("ISBN", width="small"),
            "ชื่อหนังสือ": st.column_config.TextColumn("ชื่อหนังสือ", width="large"),
            "ผู้แต่ง": st.column_config.TextColumn("ผู้แต่ง", width="medium"),
            "ปีที่พิมพ์": st.column_config.NumberColumn("ปีที่พิมพ์", format="%d")
        },
        hide_index=True
    )
    st.caption(f"แสดง {len(books)} รายการ")

# ------------------------------------------------------------------
# ส่วนแสดงผลตามเมนูที่เลือก
# ------------------------------------------------------------------
st.title("📚 ระบบบริหารจัดการห้องสมุด")
st.markdown("---")

if menu == "📖 ดูหนังสือทั้งหมด":
    st.header("📖 หนังสือทั้งหมด")
    display_books(st.session_state.books)

# ------------------------------------------------------------------
# เพิ่มหนังสือ
# ------------------------------------------------------------------
elif menu == "➕ เพิ่มหนังสือ":
    st.header("➕ เพิ่มหนังสือใหม่")
    
    with st.form("form_add_book", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            isbn = st.text_input("ISBN *", placeholder="เช่น 978-616-123-456-7")
            title = st.text_input("ชื่อหนังสือ *", placeholder="เช่น ปัญญาประดิษฐ์เบื้องต้น")
        with col2:
            author = st.text_input("ผู้แต่ง *", placeholder="เช่น สมชาย ใจดี")
            publish_year = st.number_input("ปีที่พิมพ์", min_value=1000, max_value=2100, value=2024, step=1)
        
        submitted = st.form_submit_button("📥 เพิ่มหนังสือ", use_container_width=True)
        
        if submitted:
            if not isbn or not title or not author:
                st.error("❌ กรุณากรอกข้อมูลให้ครบ (ISBN, ชื่อหนังสือ, ผู้แต่ง)")
            else:
                # ตรวจสอบ ISBN ซ้ำ
                if any(book.isbn == isbn for book in st.session_state.books):
                    st.error("❌ ISBN นี้มีอยู่ในระบบแล้ว")
                else:
                    new_book = Book(isbn, title.strip(), author.strip(), publish_year)
                    st.session_state.books.append(new_book)
                    save_data(st.session_state.books)
                    st.success(f"✅ เพิ่มหนังสือ '{title}' สำเร็จ")
                    time.sleep(0.5)
                    st.rerun()

# ------------------------------------------------------------------
# แก้ไขหนังสือ
# ------------------------------------------------------------------
elif menu == "✏️ แก้ไขหนังสือ":
    st.header("✏️ แก้ไขข้อมูลหนังสือ")
    
    if not st.session_state.books:
        st.warning("⚠️ ไม่มีหนังสือในระบบ")
    else:
        # สร้างตัวเลือกหนังสือ
        book_options = {f"{book.isbn} — {book.title}": book for book in st.session_state.books}
        selected_label = st.selectbox("เลือกหนังสือที่ต้องการแก้ไข", list(book_options.keys()))
        selected_book = book_options[selected_label]
        
        st.divider()
        col_info, col_form = st.columns([1, 1])
        
        with col_info:
            st.subheader("📄 ข้อมูลปัจจุบัน")
            st.write(f"**ISBN:** {selected_book.isbn}")
            st.write(f"**ชื่อหนังสือ:** {selected_book.title}")
            st.write(f"**ผู้แต่ง:** {selected_book.author}")
            st.write(f"**ปีที่พิมพ์:** {selected_book.publish_year}")
        
        with col_form:
            with st.form("form_edit_book"):
                st.subheader("✏️ กรอกข้อมูลใหม่")
                new_title = st.text_input("ชื่อหนังสือ", value=selected_book.title)
                new_author = st.text_input("ผู้แต่ง", value=selected_book.author)
                new_year = st.number_input("ปีที่พิมพ์", min_value=1000, max_value=2100, value=selected_book.publish_year, step=1)
                
                submitted = st.form_submit_button("💾 บันทึกการแก้ไข", use_container_width=True)
                if submitted:
                    # อัปเดตหนังสือ (ใช้ ISBN เป็นตัวระบุ)
                    for book in st.session_state.books:
                        if book.isbn == selected_book.isbn:
                            book.title = new_title.strip()
                            book.author = new_author.strip()
                            book.publish_year = new_year
                            break
                    save_data(st.session_state.books)
                    st.success("✅ แก้ไขข้อมูลสำเร็จ")
                    time.sleep(0.5)
                    st.rerun()

# ------------------------------------------------------------------
# ลบหนังสือ
# ------------------------------------------------------------------
elif menu == "🗑️ ลบหนังสือ":
    st.header("🗑️ ลบหนังสือ")
    
    if not st.session_state.books:
        st.warning("⚠️ ไม่มีหนังสือในระบบ")
    else:
        book_options = {f"{book.isbn} — {book.title}": book for book in st.session_state.books}
        selected_label = st.selectbox("เลือกหนังสือที่ต้องการลบ", list(book_options.keys()))
        selected_book = book_options[selected_label]
        
        st.divider()
        col_info, col_delete = st.columns([1, 1])
        
        with col_info:
            st.subheader("📄 ข้อมูลหนังสือที่จะลบ")
            st.write(f"**ISBN:** {selected_book.isbn}")
            st.write(f"**ชื่อหนังสือ:** {selected_book.title}")
            st.write(f"**ผู้แต่ง:** {selected_book.author}")
            st.write(f"**ปีที่พิมพ์:** {selected_book.publish_year}")
        
        with col_delete:
            st.subheader("⚠️ ยืนยันการลบ")
            confirm = st.checkbox("ฉันต้องการลบหนังสือเล่มนี้")
            if st.button("🗑️ ลบหนังสือ", disabled=not confirm, type="primary", use_container_width=True):
                st.session_state.books = [b for b in st.session_state.books if b.isbn != selected_book.isbn]
                save_data(st.session_state.books)
                st.success(f"✅ ลบหนังสือ '{selected_book.title}' สำเร็จ")
                time.sleep(0.5)
                st.rerun()

# ------------------------------------------------------------------
# เรียงลำดับหนังสือ
# ------------------------------------------------------------------
elif menu == "🔀 เรียงลำดับหนังสือ":
    st.header("🔀 เรียงลำดับหนังสือ")
    
    if not st.session_state.books:
        st.warning("⚠️ ไม่มีหนังสือในระบบ")
    else:
        sort_by = st.radio(
            "เลือกเกณฑ์การเรียงลำดับ",
            ["📅 ปีที่พิมพ์", "✍️ ชื่อผู้แต่ง"],
            horizontal=True
        )
        
        if st.button("🔀 เรียงลำดับ", type="primary", use_container_width=True):
            key = 'publish_year' if sort_by == "📅 ปีที่พิมพ์" else 'author'
            key_name = "ปีที่พิมพ์" if sort_by == "📅 ปีที่พิมพ์" else "ชื่อผู้แต่ง"
            
            books = st.session_state.books
            if len(books) <= 50:
                sorted_books, time_taken = SortingAlgorithms.measure_time(
                    SortingAlgorithms.insertion_sort, books, key
                )
                algo = "Insertion Sort"
            else:
                sorted_books, time_taken = SortingAlgorithms.measure_time(
                    SortingAlgorithms.merge_sort, books, key
                )
                algo = "Merge Sort"
            
            st.info(f"📊 **{algo}** ใช้เวลา: {time_taken:.6f} วินาที")
            display_books(sorted_books, f"เรียงลำดับตาม{key_name}")

# ------------------------------------------------------------------
# ค้นหาหนังสือ
# ------------------------------------------------------------------
elif menu == "🔍 ค้นหาหนังสือ":
    st.header("🔍 ค้นหาหนังสือ")
    
    if not st.session_state.books:
        st.warning("⚠️ ไม่มีหนังสือในระบบ")
    else:
        search_type = st.radio(
            "เลือกวิธีการค้นหา",
            ["🏷️ ค้นหาจาก ISBN (Binary Search)", "📖 ค้นหาจากชื่อหนังสือ (Sequential Search)"],
            horizontal=True
        )
        
        if search_type == "🏷️ ค้นหาจาก ISBN (Binary Search)":
            isbn = st.text_input("กรุณากรอก ISBN ที่ต้องการค้นหา")
            if st.button("🔍 ค้นหา", type="primary", use_container_width=True):
                # เรียงหนังสือตาม ISBN ก่อน (binary search ต้องการข้อมูลที่เรียงแล้ว)
                sorted_books = SortingAlgorithms.merge_sort(st.session_state.books, 'isbn')
                index, found_book = SearchAlgorithms.binary_search(sorted_books, isbn)
                
                if found_book:
                    st.success(f"✅ พบหนังสือ: {found_book}")
                    display_books([found_book], "ผลการค้นหา")
                else:
                    st.error(f"❌ ไม่พบหนังสือที่มี ISBN: {isbn}")
        
        else:  # ค้นหาจากชื่อ
            keyword = st.text_input("กรุณากรอกคำค้นหาจากชื่อหนังสือ")
            if st.button("🔍 ค้นหา", type="primary", use_container_width=True):
                found_books, comparisons = SearchAlgorithms.sequential_search(st.session_state.books, keyword)
                st.info(f"📊 จำนวนการเปรียบเทียบ: {comparisons} ครั้ง")
                
                if found_books:
                    st.success(f"✅ พบ {len(found_books)} รายการ")
                    display_books(found_books, "ผลการค้นหา")
                else:
                    st.error(f"❌ ไม่พบหนังสือที่มีคำค้นหา: {keyword}")

# ------------------------------------------------------------------
# ส่วนท้าย
# ------------------------------------------------------------------
st.markdown("---")
st.caption("📌 ระบบบันทึกข้อมูลอัตโนมัติทุกครั้งที่มีการเปลี่ยนแปลง")