from typing import Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.light_source import LightSource
from ome_types._autogenerated.ome_2016_06.map import Map

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class GenericExcitationSource(LightSource):
    """The GenericExcitationSource element is used to represent a source as a
    collection of key/value pairs, stored in a Map.

    The other lightsource objects should always be used in preference to
    this if possible.
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    map: Optional[Map] = Field(
        default=None,
        metadata={
            "name": "Map",
            "type": "Element",
        },
    )
