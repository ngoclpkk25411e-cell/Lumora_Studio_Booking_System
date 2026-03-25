import json
import os

from guest_ui.review.models.review import Review


class Reviews:

    def __init__(self):
        self.list = []

    def add_review(self, item):
        self.list.append(item)

    def print_items(self):
        for r in self.list:
            print(r)

    # =========================
    # IMPORT JSON
    # =========================

    def import_json(self, filename):

        self.filename = filename
        self.list.clear()

        if not os.path.exists(filename):

            data = {"reviews": []}

            with open(filename, "w", encoding="utf8") as f:
                json.dump(data, f, indent=4)

        with open(filename, encoding="utf8") as f:

            data = json.load(f)

            for r in data["reviews"]:

                review = Review(
                    r.get("name"),
                    r.get("email"),
                    r.get("rating"),
                    r.get("review"),
                    r.get("created_at")
                )

                self.add_review(review)

    # =========================
    # EXPORT JSON
    # =========================

    def export_json(self, filename):

        data = {"reviews": []}

        if os.path.exists(filename):

            with open(filename, encoding="utf8") as f:
                data = json.load(f)

        for r in self.list:

            data["reviews"].append({

                "name": r.name,
                "email": r.email,
                "rating": r.rating,
                "review": r.review,
                "created_at": r.created_at

            })

        with open(filename, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)