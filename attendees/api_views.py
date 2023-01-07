from django.http import JsonResponse
from .encoders import AttendeeListEncoder, AttendeeDetailEncoder
from .models import Attendee
from events.models import Conference
from django.views.decorators.http import require_http_methods
import json


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    if request.method == "GET":
        attendees = Attendee.objects.filter(id=conference_id)
        return JsonResponse(attendees, encoder=AttendeeListEncoder, safe=False)
    else:
        content = json.loads(request.body)

        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid confernece id"}, status=400
            )

        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee, encoder=AttendeeDetailEncoder, safe=False
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_attendee(request, id):
    if request.method == "GET":
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee, encoder=AttendeeDetailEncoder, safe=False
        )
    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        try:
            if "conference" in content:
                conference = Conference.objects.get(name=content["conference"])
                content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference name"}, status=400
            )

        Attendee.objects.filter(id=id).update(**content)

        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee, encoder=AttendeeDetailEncoder, safe=False
        )
