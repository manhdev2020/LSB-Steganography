import os
import shutil
from PIL import Image

class LSB():
    # Phần mã hóa:
    def encode_image(self,img, msg):
        # Mã hóa thông điệp vào ảnh sử dụng thuật toán LSB
        length = len(msg)  # Lấy độ dài của thông điệp
        encoded = img.copy()  # Tạo bản sao của ảnh gốc để mã hóa
        width, height = img.size  # Lấy kích thước của ảnh
        index = 0
        # Mã hóa độ dài của thông điệp vào 4 pixel đầu tiên của ảnh
        for i in range(4):
            row, col = divmod(i, width)  # Tính toán vị trí của pixel
            r, g, b = img.getpixel((col, row))  # Lấy giá trị màu của pixel
            # Dịch phải độ dài thông điệp 'length' i*8 bit và thực hiện phép AND với 0xFF để lấy 8 bit cuối cùng.
            # Điều này giúp chúng ta lấy từng byte của độ dài thông điệp một cách tuần tự từ byte thấp đến byte cao.
            asc = (length >> (i * 8)) & 0xFF
            encoded.putpixel((col, row), (r, g, asc))  # Ghi giá trị mới vào pixel
        index = 4  # Bắt đầu mã hóa thông điệp từ pixel thứ 5
        for row in range(height):
            for col in range(width):
                if index >= length + 4:  # Kiểm tra xem đã mã hóa xong thông điệp chưa
                    break
                if row == 0 and col < 4:  # Bỏ qua 4 pixel đầu tiên đã dùng để mã hóa độ dài thông điệp
                    continue
                if img.mode != 'RGB':  # Kiểm tra chế độ màu của ảnh
                    r, g, b, a = img.getpixel((col, row))
                elif img.mode == 'RGB':
                    r, g, b = img.getpixel((col, row))
                if index < length + 4:
                    c = msg[index - 4]  # Lấy ký tự tiếp theo trong thông điệp để mã hóa
                    asc = ord(c)  # Chuyển ký tự thành giá trị ASCII
                else:
                    asc = b
                encoded.putpixel((col, row), (r, g, asc))  # Ghi giá trị mới vào pixel
                index += 1
        return encoded  # Trả về ảnh đã mã hóa

    # Phần giải mã:
    def decode_image(self,img):
        # Giải mã thông điệp từ ảnh đã mã hóa sử dụng thuật toán LSB
        width, height = img.size  # Lấy kích thước của ảnh
        msg = ""  # Khởi tạo chuỗi để lưu thông điệp giải mã
        index = 0
        length = 0  # Biến để lưu độ dài thông điệp
        # Giải mã độ dài thông điệp từ 4 pixel đầu tiên
        for i in range(4):
            row, col = divmod(i, width)  # Tính toán vị trí của pixel
            r, g, b = img.getpixel((col, row))  # Lấy giá trị màu của pixel
            length |= b << (i * 8)  # Tính toán độ dài thông điệp
        index = 4  # Bắt đầu giải mã thông điệp từ pixel thứ 5
        for row in range(height):
            for col in range(width):
                if index >= length + 4:  # Kiểm tra xem đã giải mã xong thông điệp chưa
                    break
                if row == 0 and col < 4:  # Bỏ qua 4 pixel đầu tiên đã dùng để mã hóa độ dài thông điệp
                    continue
                if img.mode != 'RGB':  # Kiểm tra chế độ màu của ảnh
                    r, g, b, a = img.getpixel((col, row))
                elif img.mode == 'RGB':
                    r, g, b = img.getpixel((col, row))
                if index < length + 4:
                    msg += chr(b)  # Chuyển giá trị màu thành ký tự và thêm vào thông điệp
                index += 1
        return msg  # Trả về thông điệp đã giải mã


#driver part :
#deleting previous folders :
if os.path.exists("Encoded_image/"):
    shutil.rmtree("Encoded_image/")
if os.path.exists("Decoded_output/"):
    shutil.rmtree("Decoded_output/")

#creating new folders :
os.makedirs("Encoded_image/")
os.makedirs("Decoded_output/")
original_image_file = ""    # to make the file name global variable
lsb_encoded_image_file = ""
dwt_encoded_image_file = ""

while True:
    m = input("Nhấn '1' để encode, nhấn '2' để decode, nhấn '3' để thoát: ")

    if m == "1":
        os.chdir("Original_image/")
        original_image_file = input("Nhập tên file kèm đuôi mở rộng: ")
        lsb_img = Image.open(original_image_file)
        print("Mô tả: ",lsb_img,"\nChế độ: ", lsb_img.mode)
        secret_msg = input("Nhập thông điệp bạn muốn ẩn: ")
        print("Độ dài thông điệp là: ",len(secret_msg))
        os.chdir("..")
        os.chdir("Encoded_image/")
        lsb_img_encoded = LSB().encode_image(lsb_img, secret_msg)
        lsb_encoded_image_file = "lsb_" + original_image_file
        lsb_img_encoded.save(lsb_encoded_image_file)
        print("Hình ảnh đã mã hóa được lưu!")
        os.chdir("..")

    elif m == "2":
        os.chdir("Encoded_image/")
        lsb_img = Image.open(lsb_encoded_image_file)
        os.chdir("..") 
        os.chdir("Decoded_output/")
        lsb_hidden_text = LSB().decode_image(lsb_img)
        file = open("lsb_hidden_text.txt","w")
        file.write(lsb_hidden_text) 
        file.close()
        print("Văn bản ẩn đã được lưu dưới dạng file văn bản!")
        os.chdir("..")
    elif m == "3":
        print("Đã thoát!")
        break