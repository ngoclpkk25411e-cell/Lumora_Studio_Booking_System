import os

from Lumora_Studio_Booking_System.guest_ui.guest_booking.models.booking import Booking
from Lumora_Studio_Booking_System.guest_ui.guest_booking.models.bookings import Bookings


base_dir = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

filename = os.path.join(base_dir, "datasets", "bookings.json")

lb = Bookings()

b1 = Booking(
    None,
    "Ngoc",
    "ngoc@gmail.com",
    "0981111424",
    "2026-02-25",
    "14:00",
    "Wedding",
    "Outdoor",
    "2",
    "Couple",
    "",
    "SALE10"
)

b2 = Booking(
    None,
    "An",
    "an@gmail.com",
    "0234567788",
    "2026-02-26",
    "10:00",
    "Portrait",
    "Indoor",
    "1",
    "Individual",
    "",
    ""
)

b3 = Booking(
    None,
    "Nguyên",
    "nguyen@gmail.com",
    "0987274537",
    "2026-02-26",
    "09:00",
    "Portrait",
    "Outdoor",
    "1",
    "Individual",
    "",
    ""
)

lb.add_booking(b1)
lb.add_booking(b2)
lb.add_booking(b3)

lb.export_json(filename)

print("Export bookings JSON thành công")