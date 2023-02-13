from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .services import BotService, TelegramService
from .serializers import JustSerializer
from .utils import (
    get_faq_details,
    get_required_items_details,
    get_call_center_details,
    get_location_details,
    get_client_ip,
    Location
)
from . import locales
from . import keyboards



class BotViewSet(
        mixins.CreateModelMixin,
        GenericViewSet
    ):
    authentication_classes = []
    permission_classes = []
    serializer_class = JustSerializer

    @method_decorator(csrf_exempt)
    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            data_service = TelegramService(data)
            bot_service = BotService(data)

            try:
                data_service.get_or_create_profile()
            except Exception:
                pass

            if (data_service.text not in locales.MENU_BUTTONS or
                data_service.text == locales.START):

                if data_service.text == locales.START:
                    bot_service.send_message(locales.WELCOME)

                bot_service.send_message(
                    locales.INSTRUCTIONS,
                    menu=keyboards.MAIN_MENU_KEYBOARD
                )

            elif data_service.text == locales.REQUIRED_ITEMS:
                result: str = get_required_items_details()
                bot_service.send_message(
                    result,
                    menu=keyboards.MAIN_MENU_KEYBOARD
                )

            elif data_service.text == locales.FAQ:
                result: str = get_faq_details()
                bot_service.send_message(
                    result,
                    menu=keyboards.MAIN_MENU_KEYBOARD
                )

            elif data_service.text == locales.CALL_CENTER:
                result: str = get_call_center_details()
                bot_service.send_message(
                    result,
                    menu=keyboards.MAIN_MENU_KEYBOARD
                )

            elif data_service.text == locales.LOCATIONS:
                location: Location = get_location_details()
                if location.is_valid():
                    bot_service.send_location(
                        longitude=location.longitude,
                        latitude=location.latitude
                    )

        except Exception as e:
            print(e)

        return Response(status=status.HTTP_200_OK)
