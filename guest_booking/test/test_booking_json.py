import sys
import os

from guest_ui.guest_booking.models.booking import Booking
from guest_ui.guest_booking.models.bookings import Bookings

# thêm đường dẫn để import models
sys.path.append(os.path.abspath("../../.."))



# đường dẫn file json
filename = "../../../datasets/bookings.json"

lb = Bookings()

# tạo các booking object (ví dụ)
b1 = Booking(
        "Ngoc",
        "ngoc@gmail.com",
        "0981111424",
        "2026-02-25",
        "14:00",
        "Wedding",
        "Outdoor",
        "2",
        "None",
        "SALE10"
    )
b2 = Booking(
        "An",
        "an@gmail.com",
        "0234567788",
        "2026-02-26",
        "10:00",
        "Portrait",
        "Indoor",
        "1",
        "",
        ""
    )
b3 =Booking(
        "Nguyên",
        "nguyen@gmail.com",
        "0987274537",
        "2026-02-26",
        "9:00",
        "Portrait",
        "Outdoor",
        "1",
        "",
        ""
    )

# thêm vào danh sách
lb.add_booking(b1)
lb.add_booking(b2)
lb.add_booking(b3)

# export json
lb.export_json(filename)

print("Export bookings JSON thành công")