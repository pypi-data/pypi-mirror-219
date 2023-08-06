from datetime import datetime

from pydantic import AnyUrl, BaseModel, EmailStr, Field, HttpUrl, PositiveInt, root_validator
from rdflib import BNode
from rdflib.term import Identifier as RDFIdentifier

from hsmodels.namespaces import DCTERMS, HSTERMS, RDF, RDFS
from hsmodels.schemas.enums import CoverageType, DateType, MultidimensionalSpatialReferenceType, SpatialReferenceType
from hsmodels.schemas.fields import (
    AwardInfo,
    BandInformation,
    CellInformation,
    FieldInformation,
    GeometryInformation,
    ProcessingLevel,
    Publisher,
    Rights,
    TimeSeriesMethod,
    TimeSeriesResult,
    TimeSeriesSite,
    TimeSeriesVariable,
    Unit,
    UTCOffSet,
    Variable,
)
from hsmodels.schemas.rdf.root_validators import parse_relation_rdf, rdf_parse_utc_offset, split_user_identifiers


class RDFBaseModel(BaseModel):
    rdf_subject: RDFIdentifier = Field(default_factory=BNode)


class DCTypeInRDF(RDFBaseModel):
    is_defined_by: AnyUrl = Field(rdf_predicate=RDFS.isDefinedBy)
    label: str = Field(rdf_predicate=RDFS.label)


class RelationInRDF(RDFBaseModel):
    isExecutedBy: str = Field(rdf_predicate=HSTERMS.isExecutedBy, default=None)
    isCreatedBy: str = Field(rdf_predicate=HSTERMS.isCreatedBy, default=None)
    isDescribedBy: str = Field(rdf_predicate=HSTERMS.isDescribedBy, default=None)
    isSimilarTo: str = Field(rdf_predicate=HSTERMS.isSimilarTo, default=None)

    isPartOf: str = Field(rdf_predicate=DCTERMS.isPartOf, default=None)
    hasPart: str = Field(rdf_predicate=DCTERMS.hasPart, default=None)
    isVersionOf: str = Field(rdf_predicate=DCTERMS.isVersionOf, default=None)
    isReplacedBy: str = Field(rdf_predicate=DCTERMS.isReplacedBy, default=None)
    conformsTo: str = Field(rdf_predicate=DCTERMS.conformsTo, default=None)
    hasFormat: str = Field(rdf_predicate=DCTERMS.hasFormat, default=None)
    isFormatOf: str = Field(rdf_predicate=DCTERMS.isFormatOf, default=None)
    isRequiredBy: str = Field(rdf_predicate=DCTERMS.isRequiredBy, default=None)
    requires: str = Field(rdf_predicate=DCTERMS.requires, default=None)
    isReferencedBy: str = Field(rdf_predicate=DCTERMS.isReferencedBy, default=None)
    references: str = Field(rdf_predicate=DCTERMS.references, default=None)
    replaces: str = Field(rdf_predicate=DCTERMS.replaces, default=None)
    source: str = Field(rdf_predicate=DCTERMS.source, default=None)

    _parse_relation = root_validator(pre=True)(parse_relation_rdf)


class DescriptionInRDF(RDFBaseModel):
    abstract: str = Field(rdf_predicate=DCTERMS.abstract, default=None)


class IdentifierInRDF(RDFBaseModel):
    hydroshare_identifier: AnyUrl = Field(rdf_predicate=HSTERMS.hydroShareIdentifier)


class ExtendedMetadataInRDF(RDFBaseModel):
    value: str = Field(rdf_predicate=HSTERMS.value, default="")
    key: str = Field(rdf_predicate=HSTERMS.key)


class CellInformationInRDF(CellInformation, RDFBaseModel):
    class Config:
        fields = {
            'name': {"rdf_predicate": HSTERMS.name},
            'rows': {"rdf_predicate": HSTERMS.rows},
            'columns': {"rdf_predicate": HSTERMS.columns},
            'cell_size_x_value': {"rdf_predicate": HSTERMS.cellSizeXValue},
            'cell_data_type': {"rdf_predicate": HSTERMS.cellDataType},
            'cell_size_y_value': {"rdf_predicate": HSTERMS.cellSizeYValue},
        }


class DateInRDF(RDFBaseModel):
    type: DateType = Field(rdf_predicate=RDF.type)
    value: datetime = Field(rdf_predicate=RDF.value)


class RightsInRDF(Rights, RDFBaseModel):
    class Config:
        fields = {'statement': {"rdf_predicate": HSTERMS.rightsStatement}, 'url': {"rdf_predicate": HSTERMS.URL}}


class CreatorInRDF(RDFBaseModel):
    creator_order: PositiveInt
    name: str = Field(default=None)
    phone: str = Field(default=None)
    address: str = Field(default=None)
    organization: str = Field(default=None)
    email: EmailStr = Field(default=None)
    homepage: HttpUrl = Field(default=None)
    hydroshare_user_id: int = Field(default=None)
    ORCID: AnyUrl = Field(default=None)
    google_scholar_id: AnyUrl = Field(default=None)
    research_gate_id: AnyUrl = Field(default=None)

    _group_identifiers = root_validator(pre=True, allow_reuse=True)(split_user_identifiers)

    class Config:
        fields = {
            'name': {"rdf_predicate": HSTERMS.name},
            'creator_order': {"rdf_predicate": HSTERMS.creatorOrder},
            'google_scholar_id': {"rdf_predicate": HSTERMS.GoogleScholarID},
            'research_gate_id': {"rdf_predicate": HSTERMS.ResearchGateID},
            'phone': {"rdf_predicate": HSTERMS.phone},
            'ORCID': {"rdf_predicate": HSTERMS.ORCID},
            'address': {"rdf_predicate": HSTERMS.address},
            'organization': {"rdf_predicate": HSTERMS.organization},
            'email': {"rdf_predicate": HSTERMS.email},
            'homepage': {"rdf_predicate": HSTERMS.homepage},
            'hydroshare_user_id': {"rdf_predicate": HSTERMS.hydroshare_user_id},
        }


class ContributorInRDF(RDFBaseModel):
    name: str = Field(default=None)
    phone: str = Field(default=None)
    address: str = Field(default=None)
    organization: str = Field(default=None)
    email: EmailStr = Field(default=None)
    homepage: HttpUrl = Field(default=None)
    hydroshare_user_id: int = Field(default=None)
    ORCID: AnyUrl = Field(default=None)
    google_scholar_id: AnyUrl = Field(default=None)
    research_gate_id: AnyUrl = Field(default=None)

    _group_identifiers = root_validator(pre=True, allow_reuse=True)(split_user_identifiers)

    class Config:
        fields = {
            'name': {"rdf_predicate": HSTERMS.name},
            'phone': {"rdf_predicate": HSTERMS.phone},
            'address': {"rdf_predicate": HSTERMS.address},
            'organization': {"rdf_predicate": HSTERMS.organization},
            'email': {"rdf_predicate": HSTERMS.email},
            'homepage': {"rdf_predicate": HSTERMS.homepage},
            'ORCID': {"rdf_predicate": HSTERMS.ORCID},
            'google_scholar_id': {"rdf_predicate": HSTERMS.GoogleScholarID},
            'research_gate_id': {"rdf_predicate": HSTERMS.ResearchGateID},
            'hydroshare_user_id': {"rdf_predicate": HSTERMS.hydroshare_user_id},
        }


class AwardInfoInRDF(AwardInfo, RDFBaseModel):
    class Config:
        fields = {
            'funding_agency_name': {"rdf_predicate": HSTERMS.fundingAgencyName},
            'title': {"rdf_predicate": HSTERMS.awardTitle},
            'number': {"rdf_predicate": HSTERMS.awardNumber},
            'funding_agency_url': {"rdf_predicate": HSTERMS.fundingAgencyURL},
        }


class BandInformationInRDF(BandInformation, RDFBaseModel):
    class Config:
        fields = {
            'name': {"rdf_predicate": HSTERMS.name},
            'variable_name': {"rdf_predicate": HSTERMS.variableName},
            'variable_unit': {"rdf_predicate": HSTERMS.variableUnit},
            'no_data_value': {"rdf_predicate": HSTERMS.noDataValue},
            'maximum_value': {"rdf_predicate": HSTERMS.maximumValue},
            'comment': {"rdf_predicate": HSTERMS.comment},
            'method': {"rdf_predicate": HSTERMS.method},
            'minimum_value': {"rdf_predicate": HSTERMS.minimumValue},
        }


class CoverageInRDF(RDFBaseModel):
    type: CoverageType = Field(rdf_predicate=RDF.type)
    value: str = Field(rdf_predicate=RDF.value)


class SpatialReferenceInRDF(RDFBaseModel):
    type: SpatialReferenceType = Field(rdf_predicate=RDF.type)
    value: str = Field(rdf_predicate=RDF.value)


class MultidimensionalSpatialReferenceInRDF(RDFBaseModel):
    type: MultidimensionalSpatialReferenceType = Field(rdf_predicate=RDF.type)
    value: str = Field(rdf_predicate=RDF.value)


class FieldInformationInRDF(FieldInformation, RDFBaseModel):
    class Config:
        fields = {
            'field_name': {"rdf_predicate": HSTERMS.fieldName},
            'field_type': {"rdf_predicate": HSTERMS.fieldType},
            'field_type_code': {"rdf_predicate": HSTERMS.fieldTypeCode},
            'field_width': {"rdf_predicate": HSTERMS.fieldWidth},
            'field_precision': {"rdf_predicate": HSTERMS.fieldPrecision},
        }


class GeometryInformationInRDF(GeometryInformation, RDFBaseModel):
    class Config:
        fields = {
            'feature_count': {"rdf_predicate": HSTERMS.featureCount},
            'geometry_type': {"rdf_predicate": HSTERMS.geometryType},
        }


class VariableInRDF(Variable, RDFBaseModel):
    class Config:
        fields = {
            'name': {"rdf_predicate": HSTERMS.name},
            'unit': {"rdf_predicate": HSTERMS.unit},
            'type': {"rdf_predicate": HSTERMS.type},
            'shape': {"rdf_predicate": HSTERMS.shape},
            'descriptive_name': {"rdf_predicate": HSTERMS.descriptive_name},
            'method': {"rdf_predicate": HSTERMS.method},
            'missing_value': {"rdf_predicate": HSTERMS.missing_value},
        }


class PublisherInRDF(Publisher, RDFBaseModel):
    class Config:
        fields = {'name': {"rdf_predicate": HSTERMS.publisherName}, 'url': {"rdf_predicate": HSTERMS.publisherURL}}


class TimeSeriesVariableInRDF(TimeSeriesVariable, RDFBaseModel):
    class Config:
        fields = {
            'variable_code': {"rdf_predicate": HSTERMS.VariableCode},
            'variable_name': {"rdf_predicate": HSTERMS.VariableName},
            'variable_type': {"rdf_predicate": HSTERMS.VariableType},
            'no_data_value': {"rdf_predicate": HSTERMS.NoDataValue},
            'variable_definition': {"rdf_predicate": HSTERMS.VariableDefinition},
            'speciation': {"rdf_predicate": HSTERMS.Speciation},
        }


class TimeSeriesSiteInRDF(TimeSeriesSite, RDFBaseModel):
    class Config:
        fields = {
            'site_code': {"rdf_predicate": HSTERMS.SiteCode},
            'site_name': {"rdf_predicate": HSTERMS.SiteName},
            'elevation_m': {"rdf_predicate": HSTERMS.Elevation_m},
            'elevation_datum': {"rdf_predicate": HSTERMS.ElevationDatum},
            'site_type': {"rdf_predicate": HSTERMS.SiteType},
            'latitude': {"rdf_predicate": HSTERMS.Latitude},
            'longitude': {"rdf_predicate": HSTERMS.Longitude},
        }


class TimeSeriesMethodInRDF(TimeSeriesMethod, RDFBaseModel):
    class Config:
        fields = {
            'method_code': {"rdf_predicate": HSTERMS.MethodCode},
            'method_name': {"rdf_predicate": HSTERMS.MethodName},
            'method_type': {"rdf_predicate": HSTERMS.MethodType},
            'method_description': {"rdf_predicate": HSTERMS.MethodDescription},
            'method_link': {"rdf_predicate": HSTERMS.MethodLink},
        }


class ProcessingLevelInRDF(ProcessingLevel, RDFBaseModel):
    class Config:
        fields = {
            'processing_level_code': {"rdf_predicate": HSTERMS.ProcessingLevelCode},
            'definition': {"rdf_predicate": HSTERMS.Definition},
            'explanation': {"rdf_predicate": HSTERMS.Explanation},
        }


class UnitInRDF(Unit, RDFBaseModel):
    class Config:
        fields = {
            'type': {"rdf_predicate": HSTERMS.UnitsType},
            'name': {"rdf_predicate": HSTERMS.UnitsName},
            'abbreviation': {"rdf_predicate": HSTERMS.UnitsAbbreviation},
        }


class UTCOffSetInRDF(UTCOffSet, RDFBaseModel):
    class Config:
        fields = {'value': {"rdf_predicate": HSTERMS.value}}


class TimeSeriesResultInRDF(TimeSeriesResult, RDFBaseModel):
    unit: UnitInRDF = Field(rdf_predicate=HSTERMS.unit, default=None)
    site: TimeSeriesSiteInRDF = Field(rdf_predicate=HSTERMS.site)
    variable: TimeSeriesVariableInRDF = Field(rdf_predicate=HSTERMS.variable)
    method: TimeSeriesMethodInRDF = Field(rdf_predicate=HSTERMS.method)
    processing_level: ProcessingLevelInRDF = Field(rdf_predicate=HSTERMS.processingLevel)
    utc_offset: UTCOffSetInRDF = Field(rdf_predicate=HSTERMS.UTCOffSet, default=None)

    class Config:
        fields = {
            'series_id': {"rdf_predicate": HSTERMS.timeSeriesResultUUID},
            'status': {"rdf_predicate": HSTERMS.Status},
            'sample_medium': {"rdf_predicate": HSTERMS.SampleMedium},
            'value_count': {"rdf_predicate": HSTERMS.ValueCount},
            'aggregation_statistic': {"rdf_predicate": HSTERMS.AggregationStatistic},
            'series_label': {"rdf_predicate": HSTERMS.SeriesLabel},
        }

    _parse_utc_offset = root_validator(pre=True)(rdf_parse_utc_offset)
