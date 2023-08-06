import importlib
import logging
import os
from uuid import uuid4

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions
from rest_framework.request import Request

User = get_user_model()

LEARNGUAL_SERVICE_API_KEY = getattr(
    settings, "LEARNGUAL_SERVICE_API_KEY", None
) or os.getenv("LEARNGUAL_SERVICE_API_KEY", None)

"""
Configure authentication class
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        ...
        "iam_service.users.authentication.LearngualAuthentication",
        ...
    ),
    ...
}

LEARNGUAL_AUTH_RETRIEVE_URL=<auth server url to authenticate if user is login>
LEARNGUAL_AUTH_TEST_MODE=<True or False used for testing provide dummy data to authenticate user>
LEARNGUAL_AUTH_GET_USER=<dot path to the callable >

Data = {
    "account": {
        "id": "84bcaf2972",
        "cover_photo": None,
        "profile_photo": None,
        "type": "PERSONNAL",
        "metadata": {},
        "created_at": "2023-01-13T16:33:52.084540Z",
        "updated_at": "2023-01-13T16:33:52.084576Z"
    },
    "email": "Bulah53@gmail.com",
    "first_name": "Caitlyn",
    "id": "40e0e7013f",
    "last_name": "Marquardt",
    "registration_step": "REGISTRATION_COMPLETED",
    "username": "Eloisa.Senger42"
}

def get_user(data:Data):

    print("data in get user")
    return get_user_model().objects.get_or_create()

"""


user_test_data = {
    "account": {
        "id": "84bcaf2972",
        "cover_photo": None,
        "profile_photo": None,
        "type": "PERSONNAL",
        "metadata": {},
        "created_at": "2023-01-13T16:33:52.084540Z",
        "updated_at": "2023-01-13T16:33:52.084576Z",
    },
    "email": "Bulah53@gmail.com",
    "first_name": "Caitlyn",
    "id": "40e0e7013f",
    "last_name": "Marquardt",
    "registration_step": "REGISTRATION_COMPLETED",
    "username": "Eloisa.Senger42",
}


def load_callable(path: str):
    paths = path.split(".")
    modules = importlib.import_module(".".join(paths[:-1]))
    return getattr(modules, paths[-1])


LEARNGUAL_AUTH_RETRIEVE_URL = getattr(settings, "LEARNGUAL_AUTH_RETRIEVE_URL", None)
LEARNGUAL_AUTH_TEST_MODE = getattr(settings, "LEARNGUAL_AUTH_TEST_MODE", None)
LEARNGUAL_AUTH_GET_USER = getattr(settings, "LEARNGUAL_AUTH_GET_USER", None)


assert (
    LEARNGUAL_AUTH_RETRIEVE_URL
), "LEARNGUAL_AUTH_RETRIEVE_URL must be provided in the settings."
assert (
    LEARNGUAL_AUTH_GET_USER
), "LEARNGUAL_AUTH_GET_USER must be provided in the settings."
assert not (
    LEARNGUAL_AUTH_TEST_MODE and not settings.DEBUG
), "You cannot activate LEARNGUAL_AUTH_TEST_MODE when debug is False confirm you are not running test\
    mode in production."


get_user: callable = load_callable(LEARNGUAL_AUTH_GET_USER)


class LearngualAuthentication(authentication.BaseAuthentication):
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a request header.
    """

    www_authenticate_realm = "api"
    media_type = "application/json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    @classmethod
    def get_http_headers(cls, request: Request):

        headers = dict()
        if request:
            for key, value in request.META.items():
                if key.lower().startswith("http_"):
                    headers[key.lower().lstrip("http_")] = value
        return headers

    @classmethod
    def get_query_str(cls, request: Request):
        return "?{query}".format(query=request.META.get("QUERY_STRING", ""))

    def authenticate(self, request):
        # logging.info(
        #     "am here ooo %s" % dict(LEARNGUAL_AUTH_TEST_MODE=LEARNGUAL_AUTH_TEST_MODE)
        # )
        # this is for test mode

        service_key = str(
            request.META.get("HTTP_SERVICE_KEY", "")
            or request.GET.get("service-key", "")
            or request.GET.get("_service-key", "")
        )
        if service_key:
            if service_key == LEARNGUAL_SERVICE_API_KEY:
                service_user = User(id="service", username="service")
                service_user.is_service = True
                return service_user, service_key

            msg = _("Invalid service key")
            raise exceptions.AuthenticationFailed(msg)

        if LEARNGUAL_AUTH_TEST_MODE:
            logging.info("%s is in test mode" % self.__class__.__name__)
            return get_user(user_test_data), uuid4().hex

        header = self.get_header(request)

        if not header.get("authorization"):
            return None
        headers = self.get_http_headers(request)

        res = requests.get(
            LEARNGUAL_AUTH_RETRIEVE_URL + self.get_query_str(request), headers=headers
        )
        if not res.ok:
            return None

        return (
            get_user(res.json()),
            header.get("api_key") or header.get("authorization").split(" ")[-1],
        )

    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        account_id = str(request.META.get("HTTP_ACCOUNT", ""))
        api_key = str(request.META.get("HTTP_API_KEY", ""))
        service_key = str(
            request.META.get("HTTP_SERVICE_KEY", "")
            or request.GET.get("service-key", "")
            and request.GET.get("_service-key", "")
        )
        authorization = str(request.META.get("HTTP_AUTHORIZATION", ""))

        return dict(
            account_id=account_id,
            api_key=api_key,
            authorization=authorization,
            service_key=service_key,
        )


def default_user_authentication_rule(user):
    # Prior to Django 1.10, inactive users could be authenticated with the
    # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
    # prevents inactive users from authenticating.  App designers can still
    # allow inactive users to authenticate by opting for the new
    # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
    # users from authenticating to enforce a reasonable policy and provide
    # sensible backwards compatibility with older Django versions.
    return user is not None and user.is_active
