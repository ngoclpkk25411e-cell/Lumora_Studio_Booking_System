from datetime import datetime


class Review:

    def __init__(self,
                 name=None,
                 email=None,
                 rating=None,
                 review=None,
                 created_at=None):

        self.name = name
        self.email = email
        self.rating = rating
        self.review = review

        if created_at:
            self.created_at = created_at
        else:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):

        return f"{self.name}\t{self.email}\t{self.rating}\t{self.review}\t{self.created_at}"