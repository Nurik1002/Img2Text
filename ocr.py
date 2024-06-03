import easyocr
import cv2

reader = easyocr.Reader(["ru","rs_cyrillic","be","bg","uk","mn","en"], detector='DB', recognizer = 'Transformer')

def image2text(img):
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = reader.readtext(img)
    text = ""
    for i in result:
        text += i[1] + " "

    text = text.strip()
    return text