from PIL import Image
import pytesseract
 
# 打开图像文件
img = Image.open(r'4.png')

# 指定语言为中文简体
lang = 'chi_sim+eng'

# 使用指定语言识别图像中的文本
text = pytesseract.image_to_string(img, lang=lang)
print (text)
