import time

class SortingAlgorithms:
    
    @staticmethod
    def insertion_sort(books, key='publish_year'):
        """
        Insertion Sort - เหมาะสำหรับข้อมูลจำนวนน้อย
        Big O: O(n²) ใน worst case, O(n) ใน best case
        """
        n = len(books)
        for i in range(1, n):
            key_book = books[i]
            j = i - 1
            
            # เลื่อนข้อมูลที่มีค่าน้อยกว่าไปทางขวา
            while j >= 0 and getattr(books[j], key) > getattr(key_book, key):
                books[j + 1] = books[j]
                j -= 1
            books[j + 1] = key_book
        
        return books
    
    @staticmethod
    def merge_sort(books, key='publish_year'):
        """
        Merge Sort - เหมาะสำหรับข้อมูลจำนวนมาก
        Big O: O(n log n) ทุกกรณี
        """
        if len(books) <= 1:
            return books
        
        # แบ่งข้อมูลออกเป็นสองส่วน
        mid = len(books) // 2
        left = books[:mid]
        right = books[mid:]
        
        # เรียกใช้ recursive
        left = SortingAlgorithms.merge_sort(left, key)
        right = SortingAlgorithms.merge_sort(right, key)
        
        # รวมข้อมูลที่เรียงแล้ว
        return SortingAlgorithms._merge(left, right, key)
    
    @staticmethod
    def _merge(left, right, key):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if getattr(left[i], key) <= getattr(right[j], key):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # เพิ่มข้อมูลที่เหลือ
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    @staticmethod
    def measure_time(sort_func, books, key):
        """วัดเวลาในการเรียงข้อมูล"""
        start_time = time.time()
        sorted_books = sort_func(books.copy(), key)
        end_time = time.time()
        return sorted_books, end_time - start_time
