from django.dispatch import Signal

import logging
logger = logging.getLogger(__name__)


pre_switch = Signal(providing_args=[])
post_switch = Signal(providing_args=[])

pre_create = Signal(providing_args=['namespace'])
post_create = Signal(providing_args=['namespace'])

pre_rename = Signal(providing_args=[])
post_rename = Signal(providing_args=[])

pre_drop = Signal(providing_args=[])
post_drop = Signal(providing_args=[])
