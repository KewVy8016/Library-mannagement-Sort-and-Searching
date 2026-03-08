class SearchAlgorithms:
    
    @staticmethod
    def binary_search(books, target_isbn):
        """
        Binary Search - ค้นหาจาก ISBN (ข้อมูลต้องเรียงลำดับก่อน)
        Big O: O(log n)
        """
        left, right = 0, len(books) - 1
        
        while left <= right:
            mid = (left + right) // 2
            current_isbn = books[mid].isbn
            
            if current_isbn == target_isbn:
                return mid, books[mid]  # พบหนังสือ
            elif current_isbn < target_isbn:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1, None  # ไม่พบหนังสือ
    
    @staticmethod
    def sequential_search(books, title_keyword):
        """
        Sequential Search - ค้นหาจากชื่อหนังสือ
        Big O: O(n)
        """
        found_books = []
        comparisons = 0
        
        for book in books:
            comparisons += 1
            if title_keyword.lower() in book.title.lower():
                found_books.append(book)
        
        return found_books, comparisons
