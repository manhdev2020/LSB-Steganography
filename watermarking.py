import os
import shutil
from PIL import Image
import xlwt
import cv2
import math
import numpy as np
import random
from matplotlib import pyplot as plt

# Dictionary mapping characters to Morse code
morse_code = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
              'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
              'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
              'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
              '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'}

# Function to encode text to Morse code
def encode_to_morse(text):
    morse = ''
    for char in text:
        if char.upper() in morse_code:
            morse += morse_code[char.upper()] + ' '
        elif char == ' ':
            morse += '/'  # If character not found in Morse code dictionary, keep it unchanged
    return morse

# Function to decode Morse code
def decode_morse(morse):
    decoded_text = ''
    morse_code_inv = {v: k for k, v in morse_code.items()}
    for code in morse.split():
        if code in morse_code_inv:
            decoded_text += morse_code_inv[code]
        else:
            if code[0] == '/':
                decoded_text += ' ' + morse_code_inv[code[1:]]
    return decoded_text


# Function to generate random Caesar key
def generate_caesar_key():
    return random.randint(0, 35)

# Function to generate random Vigenere key
def generate_vigenere_key(length):
    key = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(length))
    return key

# Caesar encrypt
def caesar_cipher(text, key):
    caesar_space = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    encrypted_text = ''
    for char in text.upper():
        if char.isalnum():
            index = (caesar_space.find(char) + key) % len(caesar_space)
            encrypted_text += caesar_space[index]
        else:
            encrypted_text += char    
    return encrypted_text.lower()


# Hàm mã hoá Vigenere
def vigenere_cipher(text, key):
    text = text.upper()
    key = key.upper()
    ciphertext = ''
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index]) - ord('A')
            encrypted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            ciphertext += encrypted_char
            key_index = (key_index + 1) % len(key)
        else:
            ciphertext += char
    return ciphertext.lower()

# Hàm giải mã vigenere
def vigenere_decode(text, key):
    text = text.upper()
    key = key.upper()
    plaintext = ''
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index]) - ord('A')
            decrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            plaintext += decrypted_char
            key_index = (key_index + 1) % len(key)
        else:
            plaintext += char
    return plaintext


# Generate random keys
caesar_key = generate_caesar_key()
vigenere_key = generate_vigenere_key(3)
    
def multi_encode(text):
    # Divide text to two part
    
    text_caesar = text[:(len(text) // 2)]
    text_vigenere = text[(len(text) // 2):]
    
    # print(f'Text for caesar: {text_caesar}')
    # print(f'Text for vigenere: {text_vigenere}')

    # Encode text using Caesar and Vigenere ciphers
    caesar_encoded = caesar_cipher(text_caesar, caesar_key)
    vigenere_encoded = vigenere_cipher(text_vigenere, vigenere_key)
    print(f'Caesar encrypt: {caesar_encoded}')
    print(f'Vigenere encrypt: {vigenere_encoded}')

    # Combine encoded strings
    combined_encoded = caesar_encoded + vigenere_encoded

    print(f'Combined encrypt: {combined_encoded}')

    # Encode combined string to Morse code
    morse_encoded = encode_to_morse(combined_encoded)
    print('')
    print("Chuỗi sau khi mã hóa Morse:", morse_encoded)
    return morse_encoded

def multi_decode(morse_encoded):
    # Decoding Morse code
    decoded_combined = decode_morse(morse_encoded)
    print('')
    print("Chuỗi đã giải mã từ Morse:", decoded_combined)

    # Decode combined text
    decoded_caesar = caesar_cipher(decoded_combined[:(len(decoded_combined) // 2)], -caesar_key)
    decoded_vigenere = vigenere_decode(decoded_combined[(len(decoded_combined) // 2):], vigenere_key)
    decoded_text = (decoded_caesar + decoded_vigenere).upper()

    print("Chuỗi đã giải mã từ combined_encoded:", decoded_text)
    return decoded_text

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


class Compare():
    
    # Hàm tính sai số bình phương trung bình giữa hai ảnh
    def meanSquareError(self, img1, img2):
        # err = np.mean(np.square(np.subtract(img1,img2)))
        err = np.mean((img1 - img2) ** 2)
        return err
    
    # Hàm tính PSNR (Peak Signal-to-Noise Ratio) giữa hai ảnh
    def psnr(self, img1, img2):
        mse = self.meanSquareError(img1,img2)
        if mse == 0:
            return 100
        PIXEL_MAX = 255.0
        return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    
    def plot_histogram(self, image, title, save_path=None):
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        plt.plot(hist, color='b')
        plt.xlim([0, 256])
        plt.title(title)
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Frequency')
        plt.grid(True)
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

    def compare_histograms(self, image1, image2):
        hist1 = cv2.calcHist([image1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0, 256])

        plt.plot(hist1, color='b', label='Original Image')
        plt.plot(hist2, color='r', label='Stego Image')
        plt.xlim([0, 256])
        plt.title('Histogram Comparison')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)
        plt.show()


#driver part :
#deleting previous folders :
if os.path.exists("Encoded_image/"):
    shutil.rmtree("Encoded_image/")
if os.path.exists("Decoded_output/"):
    shutil.rmtree("Decoded_output/")
if os.path.exists("Comparison_result/"):
    shutil.rmtree("Comparison_result/")
if os.path.exists("Key_Gen/"):
    shutil.rmtree("Key_Gen/")

#creating new folders :
os.makedirs("Encoded_image/")
os.makedirs("Decoded_output/")
os.makedirs("Comparison_result/")
os.makedirs("Key_Gen/")

with open('Key_Gen/caesar_key.txt', 'w') as file:
    file.write(f"Caesar Key: {caesar_key}")
    
with open('Key_Gen/vigenere_key.txt', 'w') as file:
    file.write(f"Vigenere Key: {vigenere_key}")
    

original_image_file = ""    # to make the file name global variable
lsb_encoded_image_file = ""
# dwt_encoded_image_file = ""

while True:
    m = input("Nhấn '1' để encode, nhấn '2' để decode, nhấn '3' để compare, nhấn 4 để thoát: ")

    if m == "1":
        os.chdir("Original_image/")
        original_image_file = input("Nhập tên file kèm đuôi mở rộng: ")
        lsb_img = Image.open(original_image_file)
        print("Mô tả: ",lsb_img,"\nChế độ: ", lsb_img.mode)
        secret_msg = input("Nhập thông điệp bạn muốn ẩn: ")
        print("Độ dài thông điệp là: ",len(secret_msg))
        print("")
        print("Key đã được gen trong thư mục Key_Gen!")
        os.chdir("..")
        os.chdir("Encoded_image/")
        encrypt_msg = multi_encode(secret_msg)
        lsb_img_encoded = LSB().encode_image(lsb_img, encrypt_msg)
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
        plain_text = multi_decode(lsb_hidden_text)
        file = open("plaintext.txt", "w")
        file.write(plain_text)
        file.close()
        print("Văn bản ẩn đã được lưu dưới dạng file văn bản!")
        os.chdir("..")
    elif m == "3":
        print('')
        os.chdir("Original_image/")
        original = np.uint8(cv2.imread(original_image_file, cv2.IMREAD_COLOR))
        os.chdir("..")
        os.chdir("Encoded_image/")
        lsb_encoded_img = np.uint8(cv2.imread(lsb_encoded_image_file, cv2.IMREAD_COLOR))

        # original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        # lsb_encoded_img = cv2.cvtColor(lsbEncoded, cv2.COLOR_BGR2RGB)
        # original = cv2.imread(original, cv2.IMREAD_COLOR)  # Load in RGB
        # lsb_encoded_img = cv2.imread(lsb_encoded_img, cv2.IMREAD_COLOR)  # Load in RGB

        os.chdir("..")
        os.chdir("Comparison_result/")

        book = xlwt.Workbook()
        sheet1=book.add_sheet("Sheet 1")
        style_string = "font: bold on , color red; borders: bottom dashed"
        style = xlwt.easyxf(style_string)
        sheet1.write(0, 0, "Image", style=style)
        sheet1.write(0, 1, "MSE", style=style)
        sheet1.write(0, 2, "PSNR", style=style)
        sheet1.write(1, 0, str(original_image_file))
        sheet1.write(1, 1, Compare().meanSquareError(original, lsb_encoded_img))
        sheet1.write(1, 2, Compare().psnr(original, lsb_encoded_img))

        print('Thông số đánh giá:')
        print(f'MSE = {Compare().meanSquareError(original, lsb_encoded_img)}')
        print(f'PSNR = {Compare().psnr(original, lsb_encoded_img)}')

        
        # Plot individual histograms
        Compare().plot_histogram(original, 'Histogram for Original Image')
        Compare().plot_histogram(lsb_encoded_img, 'Histogram for Stego Image')

        # Compare histograms
        Compare().compare_histograms(original, lsb_encoded_img)

        book.save("Comparison.xls")
        print("Kết quả so sánh đã được lưu dưới dạng file xls!")
        os.chdir("..")
    elif m == "4":
        print("Đã thoát!")
        break