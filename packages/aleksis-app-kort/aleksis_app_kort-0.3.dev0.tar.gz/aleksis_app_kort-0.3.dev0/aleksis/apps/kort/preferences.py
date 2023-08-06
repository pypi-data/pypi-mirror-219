from binascii import hexlify

from django.utils.translation import gettext as _

from dynamic_preferences.preferences import Section
from dynamic_preferences.types import StringPreference

from aleksis.core.registries import site_preferences_registry

kort = Section("kort", verbose_name=_("Student ID Cards"))


@site_preferences_registry.register
class SdmFileReadKey(StringPreference):
    """SDM file read key for NFC."""

    section = kort
    name = "sdm_file_read_key"
    default = hexlify(bytes(16)).decode()
    verbose_name = _("SDM file read key")
    required = False


@site_preferences_registry.register
class SdmMetaReadKey(StringPreference):
    """SDM meta read key for NFC."""

    section = kort
    name = "sdm_meta_read_key"
    default = hexlify(bytes(16)).decode()
    verbose_name = _("SDM meta read key")
    required = False
