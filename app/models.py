from md_leg_api import db
from sqlalchemy.dialects.postgresql import JSON


class Legislator(db.Model):
    __tablename__ = 'legislators'

    email = db.Column(db.Unicode(), primary_key=True)
    name = db.Column(db.String())
    county = db.Column(db.String())
    district = db.Column(db.String())
    position = db.Column(db.String())
    tenure = db.Column(db.String())
    address_lines = db.Column(JSON)
    city = db.Column(db.String())
    state = db.Column(db.String())
    zip_code = db.Column(db.String())
    phone = db.Column(db.String())
    current_assignments = db.Column(JSON)
    party = db.Column(db.String())

    def __init__(self, email, ):
        self.email = email

    def __repr__(self):
        return '<id {}>'.format(self.email)

    def display(self):
        return {
            'name': self.name,
            'county': self.county,
            'email': self.email,
            'phone': self.phone,
            'district': self.district,
            'position': self.position,
            'party': self.party
        }

    def display_details(self):
        return {
            'name': self.name,
            'county': self.county,
            'email': self.email,
            'phone': self.phone,
            'district': self.district,
            'position': self.position,
            'party': self.party,
            'tenure': self.tenure,
            'current_assignments': self.current_assignments,
            'address': {
                'street': self.address_lines,
                'city': self.city,
                'state': self.state,
                'zip': self.zip_code
            }
        }

    # Resources
    @classmethod
    def list(cls):
        data = cls.query.order_by(cls.county, cls.position.desc()).all()
        return [p.display() for p in data]

    @classmethod
    def search(cls, **kwargs):
        return [p.display() for p in cls.query.filter_by(**kwargs)]

    @classmethod
    def details(cls, email):
        person = Legislator.query.filter_by(email=email).all()
        if len(person) > 0:
            return person[0].display_details()
