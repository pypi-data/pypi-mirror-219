from typing import Iterator

import mobilizon_reshare.config.notifiers
import mobilizon_reshare.config.publishers
from mobilizon_reshare.config.config import get_settings


def get_active_publishers() -> Iterator[str]:
    return mobilizon_reshare.config.publishers.get_active_publishers(get_settings())


def get_active_notifiers() -> Iterator[str]:
    return mobilizon_reshare.config.notifiers.get_active_notifiers(get_settings())
