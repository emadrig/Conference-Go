import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Conference, Location, State
from .encoders import (
    ConferenceListEncoder,
    ConferenceDetailEncoder,
    LocationListEncoder,
    LocationDetailEncoder,
)


@require_http_methods(["GET", "POST"])
def api_list_conferences(request):
    if request.method == "GET":
        conferences = Conference.objects.all()
        return JsonResponse(
            {"conferences": conferences},
            encoder=ConferenceListEncoder,
            safe=False,
        )
    else:
        content = json.loads(request.body)

        try:
            location = Location.objects.get(id=content["location"])
            content["location"] = location
        except Location.DoesNotExist:
            return JsonResponse({"message": "Invalid location id"}, status=400)

        conference = Conference.objects.create(**content)
        return JsonResponse(
            conference, encoder=ConferenceDetailEncoder, safe=False
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_conference(request, id):
    conference = Conference.objects.get(id=id)
    return JsonResponse(
        conference, encoder=ConferenceDetailEncoder, safe=False
    )


@require_http_methods(["GET", "POST"])
def api_list_locations(request):
    if request.method == "GET":
        locations = Location.objects.all()
        return JsonResponse(
            {"locations": locations}, encoder=LocationListEncoder, safe=False
        )
    else:
        content = json.loads(request.body)
        try:
            state = State.objects.get(abbreviation=content["state"])
            content["state"] = state
            location = Location.objects.create(**content)
            return JsonResponse(
                location, encoder=LocationDetailEncoder, safe=False
            )
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_location(request, id):
    if request.method == "GET":
        location = Location.objects.get(id=id)
        return JsonResponse(
            location, encoder=LocationDetailEncoder, safe=False
        )
    elif request.method == "DELETE":
        count, _ = Location.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        try:
            if "state" in content:
                state = State.objects.get(abbreviation=content["state"])
                content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"}, status=400
            )
        Location.objects.filter(id=id).update(**content)

        location = Location.objects.get(id=id)
        return JsonResponse(
            location, encoder=LocationDetailEncoder, safe=False
        )
