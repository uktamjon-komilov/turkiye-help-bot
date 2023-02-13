from .models import FAQ, Info

from dataclasses import dataclass

def get_faq_details() -> str:
    output: str = ""

    faqs = list(FAQ.objects.all())
    for index, faq in enumerate(faqs):
        output += f"""Savol-{index+1}: <b>{faq.question}</b>\n"""
        output += f"""Javob: <i>-{faq.answer}</i>\n\n"""
    
    if len(output) == 0:
        output = "..."

    return output


def get_call_center_details() -> str:
    try:
        info = Info.objects.get(slug="call_center")
    except Info.DoesNotExist:
        info = Info(
            slug="call_center",
            name="Aloqa markazi",
            text="Aloqa markazi ma'lumotlari"
        )
        info.save()
    return info.text


@dataclass
class Location:
    longitude: float | None
    latitude: float | None

    def is_valid(self) -> bool:
        return bool(self.latitude) and bool(self.latitude)


def get_location_details() -> Location:
    try:
        info = Info.objects.get(slug="location")
    except Info.DoesNotExist:
        info = Info(
            slug="location",
            name="Qabul lokatsiyasi",
            text="Qabul qilish joyi (xaritada)"
        )
        info.save()
    return Location(longitude=info.longitude, latitude=info.latitude)


def get_required_items_details() -> str:
    try:
        info = Info.objects.get(slug="required_items")
    except Info.DoesNotExist:
        info = Info(
            slug="required_items",
            name="Kerakli buyumlar",
            text="Kerakli buyumlar"
        )
        info.save()
    return info.text


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip