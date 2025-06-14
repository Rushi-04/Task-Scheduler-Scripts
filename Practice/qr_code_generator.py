import qrcode

data = input("Enter the text or url: ")

filename = input("Enter filename you want to save qr_code as: ")

qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(data)

image = qr.make_image(fill_color='black', back_color='white')
image.save(filename)
print(f"QR Code Generated and Saved as {filename}")