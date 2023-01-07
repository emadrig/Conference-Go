from common.json import ModelEncoder
from events.api_views import ConferenceListEncoder
from .models import Presentation


class PresentaionDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
        "conference",
    ]
    encoders = {"conference": ConferenceListEncoder()}

    def get_extra_data(self, o):
        return {"status": o.status.name}


class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = ["title"]
