from pydantic import Field

from ome_types._autogenerated.ome_2016_06.text_annotation import TextAnnotation

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class TagAnnotation(TextAnnotation):
    """A tag annotation (represents a tag or a tagset)."""

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    value: str = Field(
        metadata={
            "name": "Value",
            "type": "Element",
            "required": True,
        }
    )
