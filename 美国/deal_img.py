import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image

# 列出支持的语言
# print(pytesseract.get_languages())
# print(pytesseract.image_to_string(Image.open('验证码.jpg'), lang='eng'))
def deal(path):
    try:
        string=pytesseract.image_to_string(Image.open(path))
        string=string.split(' ')[0].strip()
        return string
    except BaseException:
        return '验证码错误'

print(deal('toutiao.jpg'))  
# import pytesseract as ts
# version = ts.get_tesseract_version()
# print('version:',version)
# print(deal("验证码.jpg"))