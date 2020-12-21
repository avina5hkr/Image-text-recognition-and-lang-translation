import ocr


fileName="C:\\Users\\Avinash\\Desktop\\python_proj\\french4.png"

img, pdfpath= ocr.img_trans_threading(fileName, "French", "English") 

print(img)
print(pdfpath)


