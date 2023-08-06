from datetime import datetime
from typing import Dict, List, Union

from pydantic import AnyUrl, Field, root_validator, validator

from hsmodels.schemas.base_models import BaseMetadata
from hsmodels.schemas.fields import (
    AwardInfo,
    BoxCoverage,
    Contributor,
    Creator,
    PeriodCoverage,
    PointCoverage,
    Publisher,
    Relation,
    Rights,
)
from hsmodels.schemas.rdf.validators import language_constraint, subjects_constraint
from hsmodels.schemas.root_validators import (
    normalize_additional_metadata,
    parse_abstract,
    parse_additional_metadata,
    parse_url,
    split_coverages,
    split_dates,
)
from hsmodels.schemas.validators import list_not_empty, parse_identifier, parse_spatial_coverage


class ResourceMetadataIn(BaseMetadata):
    """
    A class used to represent the metadata for a resource
    """

    class Config:
        title = 'Resource Metadata'

        schema_config = {
            'read_only': ['type', 'identifier', 'created', 'modified', 'review_started', 'published', 'url'],
            'dictionary_field': ['additional_metadata'],
        }

    title: str = Field(
        max_length=300, default=None, title="Title", description="A string containing the name given to a resource"
    )
    abstract: str = Field(default=None, title="Abstract", description="A string containing a summary of a resource")
    language: str = Field(
        default="eng",
        title="Language",
        description="A 3-character string for the language in which the metadata and content of a resource are expressed",
    )
    subjects: List[str] = Field(
        default=[], title="Subject keywords", description="A list of keyword strings expressing the topic of a resource"
    )
    creators: List[Creator] = Field(
        default=[],
        title="Creators",
        description="A list of Creator objects indicating the entities responsible for creating a resource",
    )
    contributors: List[Contributor] = Field(
        default=[],
        title="Contributors",
        description="A list of Contributor objects indicating the entities that contributed to a resource",
    )
    relations: List[Relation] = Field(
        default=[],
        title="Related resources",
        description="A list of Relation objects representing resources related to a described resource",
    )
    additional_metadata: Dict[str, str] = Field(
        default={},
        title="Additional metadata",
        description="A dictionary containing key-value pair metadata associated with a resource",
    )
    rights: Rights = Field(
        default_factory=Rights.Creative_Commons_Attribution_CC_BY,
        title="Rights",
        description="An object containing information about rights held in an over a resource",
    )
    awards: List[AwardInfo] = Field(
        default=[],
        title="Funding agency information",
        description="A list of objects containing information about the funding agencies and awards associated with a resource",
    )
    spatial_coverage: Union[PointCoverage, BoxCoverage] = Field(
        default=None,
        title="Spatial coverage",
        description="An object containing information about the spatial topic of a resource, the spatial applicability of a resource, or jurisdiction under with a resource is relevant",
    )
    period_coverage: PeriodCoverage = Field(
        default=None,
        title="Temporal coverage",
        description="An object containing information about the temporal topic or applicability of a resource",
    )
    publisher: Publisher = Field(
        default=None,
        title="Publisher",
        description="An object containing information about the publisher of a resource",
    )
    citation: str = Field(
        default=None, title="Citation", description="A string containing the biblilographic citation for a resource"
    )

    _parse_coverages = root_validator(pre=True, allow_reuse=True)(split_coverages)
    _parse_additional_metadata = root_validator(pre=True, allow_reuse=True)(parse_additional_metadata)
    _parse_abstract = root_validator(pre=True)(parse_abstract)

    _parse_spatial_coverage = validator("spatial_coverage", allow_reuse=True, pre=True)(parse_spatial_coverage)

    _normalize_additional_metadata = root_validator(allow_reuse=True, pre=True)(normalize_additional_metadata)

    _subjects_constraint = validator('subjects', allow_reuse=True)(subjects_constraint)
    _language_constraint = validator('language', allow_reuse=True)(language_constraint)
    _creators_constraint = validator('creators')(list_not_empty)


class BaseResourceMetadata(ResourceMetadataIn):
    url: AnyUrl = Field(title="URL", description="An object containing the URL for a resource", allow_mutation=False)

    identifier: AnyUrl = Field(
        title="Identifier",
        description="An object containing the URL-encoded unique identifier for a resource",
        allow_mutation=False,
    )
    created: datetime = Field(
        default_factory=datetime.now,
        title="Creation date",
        description="A datetime object containing the instant associated with when a resource was created",
        allow_mutation=False,
    )
    modified: datetime = Field(
        default_factory=datetime.now,
        title="Modified date",
        description="A datetime object containing the instant associated with when a resource was last modified",
        allow_mutation=False,
    )
    review_started: datetime = Field(
        default=None,
        title="Review started date",
        description="A datetime object containing the instant associated with when metadata review started on a resource",
        allow_mutation=False,
    )
    published: datetime = Field(
        default=None,
        title="Published date",
        description="A datetime object containing the instant associated with when a resource was published",
        allow_mutation=False,
    )

    _parse_dates = root_validator(pre=True, allow_reuse=True)(split_dates)
    _parse_url = root_validator(pre=True, allow_reuse=True)(parse_url)

    _parse_identifier = validator("identifier", pre=True)(parse_identifier)


class ResourceMetadata(BaseResourceMetadata):
    type: str = Field(
        const=True,
        default="CompositeResource",
        title="Resource Type",
        description="An object containing a URL that points to the HydroShare resource type selected from the hsterms namespace",
        allow_mutation=False,
    )


class CollectionMetadata(BaseResourceMetadata):
    type: str = Field(
        const=True,
        default="CollectionResource",
        title="Resource Type",
        description="An object containing a URL that points to the HydroShare resource type selected from the hsterms namespace",
        allow_mutation=False,
    )
