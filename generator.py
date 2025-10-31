# importing Image class from PIL package
from PIL import Image
import qrcode
import cv2
#initialize qr object
qr = qrcode.QRCode(
    version =1,
    box_size =10,
    border=6)

#add data to qr code
qr.add_data('IntelliCare')
qr.make(fit=True)

#create an image of qr code
image = qr.make_image(fill_color="black", back_color= "white")

#save it locally 
image.save("intellicare.png")
print("QR code has been generated successfully!")
