from django.dispatch import Signal

import logging
logger = logging.getLogger(__name__)


pre_switch = Signal(providing_args=['namespace', 'search_path', 'cursor'])
post_switch = Signal(providing_args=['namespace', 'search_path', 'cursor'])

pre_create = Signal(providing_args=['namespace', 'cursor'])
post_create = Signal(providing_args=['namespace', 'cursor'])

pre_rename = Signal(providing_args=[])
post_rename = Signal(providing_args=[])

pre_drop = Signal(providing_args=['namespace'])
post_drop = Signal(providing_args=['namespace'])
