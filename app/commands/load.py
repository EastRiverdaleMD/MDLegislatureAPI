
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir)))
from models import Legislator


def load(db):

    with open('../data/general_assembly_contacts.json', 'r') as f:
        data = json.loads(f.read())

    for legislator in data:
        email = legislator.get('Contact')
        name = legislator.get('name', {'first': None, 'last': None})
        if email:
            name = '{0} {1}'.format(
                name.get('first'), name.get('last')).strip()
            l = Legislator(email=email)
            l.name = name,
            l.county = legislator.get('county'),
            l.district = legislator.get('district')
            l.position = legislator.get('position')
            l.current_assignments = legislator.get('current_assignments')

            tenure = legislator.get('Tenure')
            if tenure and len(tenure) > 0:
                l.tenure = tenure[0]

            party = legislator.get('Party Affiliation')
            if party and len(party) > 0:
                l.party = party[0]

            address = legislator.get('Annapolis Address')
            if address:
                l.address_lines = address.get('address_lines')
                l.city = address.get('city')
                l.state = address.get('state')
                l.zip_code = address.get('zip')
                phone = address.get('phone_numbers')
                if phone and len(phone) > 0:
                    l.phone = phone[0]

            db.session.merge(l)
            db.session.commit()
