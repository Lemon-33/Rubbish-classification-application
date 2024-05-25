import pytesseract
import cv2
from PIL import Image
from urllib import request
import time
import os
import difflib


def getFileName(file_dir):
    for root, dirs, fileNames in os.walk(file_dir):
        return (fileNames)


def adjustFileName(fileName):
    fileName = fileName.replace(" ", "")
    fileName = fileName.replace(".PNG", "")
    fileName = fileName.replace(".png", "")
    fileName = fileName.replace(".JPG", "")
    fileName = fileName.replace(".jpg", "")
    fileName = fileName.replace("（", "(")
    fileName = fileName.replace("）", ")")
    fileName = fileName.replace("：", ":")
    return fileName


def adjustOCRResult(result):
    result = result.replace("\n", "")
    result = result.replace(" ", "")
    result = result.replace("", "")
    return result


def getStringSimilar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


#  文件夹名称
folderName = "4"

#  处理文件夹内文件
fileNames = getFileName(folderName)
fileNum = len(fileNames)

#  准备输出结果
output = "文件夹:" + folderName + "\n识别结果:\n"

#  变量
correctRatingList = []
resultLenth = 0
correctResultLength = 0

for i in range(fileNum):
    #  调用识别程序
    #  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\tesseract\bin\tesseract.exe'

    #  读取图片文件
    image = Image.open(folderName + "/" + fileNames[i])

    #  优化文件名
    fileNames[i] = adjustFileName(fileNames[i])

    #  计算正确结果总长度
    resultLenth = resultLenth + len(fileNames[i])

    #  OCR获取识别结果
    text = pytesseract.image_to_string(image, lang='chi_sim+eng')

    #  优化识别结果
    text = adjustOCRResult(text)

    #  计算并存储识别精确度
    correctRating = getStringSimilar(fileNames[i], str(text))
    correctRatingList.append(correctRating)
    correctResultLength = correctResultLength + len(fileNames[i]) * correctRating

    #  保存至识别结果
    output = output + "[" + fileNames[i] + "]-[" + text + "]-[" + str(correctRating * 100) + "%]\n"

#计算识别精度
averageCorrectRating = 0.00000000000
averageCorrectRating_ = 0.00000000000
for i in range(len(correctRatingList)):
    averageCorrectRating = averageCorrectRating + correctRatingList[i]
averageCorrectRating = averageCorrectRating / len(correctRatingList)
averageCorrectRating_ = correctResultLength / resultLenth
output = output + "平均识别精度:" + str(averageCorrectRating * 100) + "%\n"
output = output + "加权平均识别精度:" + str(averageCorrectRating_ * 100) + "%"

#输出识别结果
with open("result.txt", "w") as f:
    f.write(output.encode("GBK", "ignore").decode("GBK", "ignore"))
