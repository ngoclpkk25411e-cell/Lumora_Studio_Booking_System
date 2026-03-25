import json
import os

from .booking import Booking


class Bookings:
    def __init__(self):
        self.list = []

    # =========================
    # ADD BOOKING
    # =========================
    def add_booking(self, item):
        self.list.append(item)

    # =========================
    # PRINT BOOKING
    # =========================
    def print_items(self):
        for it in self.list:
            print(it)

    # =========================
    # IMPORT JSON
    # =========================
    def import_json(self, filename):
        self.filename = filename
        self.list.clear()

        if not os.path.exists(filename):
            data = {"bookings": []}
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        with open(filename, encoding="utf8") as json_file:
            data = json.load(json_file)

            for p in data.get("bookings", []):
                it = Booking(
                    p.get("booking_id"),
                    p.get("name"),
                    p.get("email"),
                    p.get("phone"),
                    p.get("date"),
                    p.get("time"),
                    p.get("concept"),
                    p.get("location"),
                    p.get("number_people"),
                    p.get("package"),
                    p.get("notes"),
                    p.get("promo"),
                    p.get("created_at", "")
                )

                self.list.append(it)

    # =========================
    # GENERATE BOOKING ID
    # =========================
    def generate_booking_id(self, bookings):
        if not bookings:
            return "B001"

        numbers = []

        for b in bookings:
            try:
                numbers.append(int(b["booking_id"][1:]))
            except Exception:
                pass

        if not numbers:
            return "B001"

        new_number = max(numbers) + 1
        return f"B{new_number:03d}"

    # =========================
    # EXPORT JSON
    # =========================
    def export_json(self, filename):
        if os.path.exists(filename):
            with open(filename, encoding="utf8") as f:
                data = json.load(f)
        else:
            data = {"bookings": []}

        bookings = data.get("bookings", [])

        for it in self.list:
            if not getattr(it, "booking_id", None):
                it.booking_id = self.generate_booking_id(bookings)

            if any(b.get("booking_id") == it.booking_id for b in bookings):
                continue

            new_booking = {
                "booking_id": it.booking_id,
                "name": it.name,
                "email": it.email,
                "phone": it.phone,
                "date": it.date,
                "time": it.time,
                "concept": it.concept,
                "location": it.location,
                "number_people": it.number_people,
                "package": it.package,
                "notes": it.notes,
                "promo": it.promo,
                "created_at": it.created_at,
                "status": "Pending"
            }

            bookings.append(new_booking)

        data["bookings"] = bookings

        with open(filename, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

        self.list.clear()