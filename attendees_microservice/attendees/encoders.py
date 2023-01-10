from common.json import ModelEncoder
from .models import Attendee, ConferenceVO


class ConferenceVODetailEncoder(ModelEncoder):
    model = ConferenceVO
    properties = ["name", "import_href"]


class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = ["name"]


class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = ["name", "email", "company_name", "created", "conference"]

    encoders = {
        "conference": ConferenceVODetailEncoder(),
    }
