from typing import Optional

from django.core.exceptions import BadRequest
from django.http import HttpRequest

from pylibsdm.backend.validate import ParamValidator

from aleksis.core.mixins import ExtensibleModel, ObjectAuthenticator
from aleksis.core.util.core_helpers import get_site_preferences

from .cards import Card


class NfcSdmAuthenticator(ObjectAuthenticator):
    """Object authenticator using NFC SDM."""

    name = "nfc_sdm"

    def authenticate(self, request: HttpRequest, obj: Optional[ExtensibleModel]) -> ExtensibleModel:
        """SUN decrypting authenticator"""
        file_read_key = get_site_preferences()["kort__sdm_file_read_key"]
        meta_read_key = get_site_preferences()["kort__sdm_meta_read_key"]

        validator = ParamValidator(file_read_key, meta_read_key, param_picc_data="picc_data", param_cmac="cmac", param_cmac_input="picc_data")
        validator.parse_uri(request.build_absolute_uri())

        if validator.uid is None or validator.read_ctr is None or not validator.cmac_valid:
            raise BadRequest("Invalid SUN message or signature")

        try:
            card = Card.objects.get(chip_number__iexact=validator.uid.hex())
        except Card.DoesNotExist:
            return False

        if obj is None:
            obj = card.person

        if card.person != obj:
            raise BadRequest("Card is not linked to identified object")

        if card.last_read_counter >= validator.read_ctr:
            raise BadRequest("Read counter went backwards, possible replay attack")
        card.last_read_counter = validator.read_ctr
        card.save()

        return obj
