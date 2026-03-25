from datetime import datetime


class Booking:

    def __init__(self,
                 booking_id=None,
                 name=None,
                 email=None,
                 phone=None,
                 date=None,
                 time=None,
                 concept=None,
                 location=None,
                 number_people=None,
                 package=None,
                 notes=None,
                 promo=None,
                 created_at=None):

        # =========================
        # BOOKING ID
        # =========================
        self.booking_id = booking_id

        # =========================
        # CUSTOMER INFO
        # =========================
        self.name = name
        self.email = email
        self.phone = phone

        # =========================
        # BOOKING INFO
        # =========================
        self.date = date
        self.time = time
        self.concept = concept
        self.location = location
        self.number_people = number_people
        self.package = package

        # =========================
        # OPTIONAL
        # =========================
        self.notes = notes if notes else ""
        self.promo = promo if promo else ""

        # =========================
        # CREATED TIME
        # =========================
        if created_at:
            self.created_at = created_at
        else:
            self.created_at = datetime.now().strftime("%Y-%m-%d\t%H:%M:%S")


    # =========================
    # STRING
    # =========================
    def __str__(self):

        return (
            f"{self.booking_id}\t"
            f"{self.name}\t"
            f"{self.email}\t"
            f"{self.phone}\t"
            f"{self.date}\t"
            f"{self.time}\t"
            f"{self.concept}\t"
            f"{self.location}\t"
            f"{self.number_people}\t"
            f"{self.package}\t"
            f"{self.notes}\t"
            f"{self.promo}\t"
            f"{self.created_at}"
        )