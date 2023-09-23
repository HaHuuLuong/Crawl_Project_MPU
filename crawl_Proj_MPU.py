import csv
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import re
import time


def crawl_Proj_MPU(file_tu_dien, thang, nam):
    # Tạo danh sách từ điển từ tệp tin
    with open(file_tu_dien, 'r', encoding='utf-8') as f:
        tu_dien = [line.strip() for line in f]

    # Tạo danh sách kết quả
    ket_qua = []

    for keywords in tu_dien:
        # Tạo từ khóa tìm kiếm bằng cách gộp từng từ trong danh sách từ khóa
        keyword = ' '.join(keywords.split())

        # Tìm kiếm trên Google với từ khóa và giới hạn theo thời gian
        query = f"{keyword} site:.vn after:{nam}-{thang:02d}-01 before:{nam}-{thang+1:02d}-01"
        results = search(query, num_results=10, lang="vi")

        for result in results:
            try:
                # Phân tích kết quả tìm kiếm
                response = requests.get(result, timeout=10)
                response.raise_for_status()  # Kiểm tra lỗi HTTP
                soup = BeautifulSoup(response.text, 'html.parser')
                title_element = soup.title
                if title_element:
                    title = title_element.string
                else:
                    title = "Không có tiêu đề"
                link = result

                # Thêm thông tin vào danh sách kết quả
                ket_qua.append([title, link, keywords])
                time.sleep(2)

            except requests.exceptions.RequestException as e:
                print(f"Lỗi khi truy cập trang web: {e}")

    # Lưu danh sách kết quả vào file CSV
    with open('ket_qua_v8.8csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tiêu đề', 'Link', 'Từ điển'])
        writer.writerows(ket_qua)

    print('Tìm kiếm và lưu kết quả thành công')

# Tệp tin chứa danh sách từ điển
file_tu_dien = 'tu_dien.txt'

# Nhập tháng và năm từ người dùng
thang = int(input("Nhập tháng (1-12): "))
nam = int(input("Nhập năm: "))

# Gọi hàm
crawl_Proj_MPU(file_tu_dien, thang, nam)
