# coding: utf-8

# flake8: noqa
"""
    Speech Services API v3.1

    Speech Services API v3.1.  # noqa: E501

    OpenAPI spec version: v3.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

# import models into model package
from swagger_client.models.base_model import BaseModel
from swagger_client.models.base_model_deprecation_dates import BaseModelDeprecationDates
from swagger_client.models.base_model_features import BaseModelFeatures
from swagger_client.models.base_model_links import BaseModelLinks
from swagger_client.models.base_model_properties import BaseModelProperties
from swagger_client.models.block_kind import BlockKind
from swagger_client.models.commit_blocks_entry import CommitBlocksEntry
from swagger_client.models.component import Component
from swagger_client.models.custom_model import CustomModel
from swagger_client.models.custom_model_deprecation_dates import CustomModelDeprecationDates
from swagger_client.models.custom_model_features import CustomModelFeatures
from swagger_client.models.custom_model_links import CustomModelLinks
from swagger_client.models.custom_model_properties import CustomModelProperties
from swagger_client.models.dataset import Dataset
from swagger_client.models.dataset_kind import DatasetKind
from swagger_client.models.dataset_links import DatasetLinks
from swagger_client.models.dataset_locales import DatasetLocales
from swagger_client.models.dataset_properties import DatasetProperties
from swagger_client.models.dataset_update import DatasetUpdate
from swagger_client.models.detailed_error_code import DetailedErrorCode
from swagger_client.models.diarization_properties import DiarizationProperties
from swagger_client.models.diarization_speakers_properties import DiarizationSpeakersProperties
from swagger_client.models.endpoint import Endpoint
from swagger_client.models.endpoint_links import EndpointLinks
from swagger_client.models.endpoint_properties import EndpointProperties
from swagger_client.models.endpoint_properties_update import EndpointPropertiesUpdate
from swagger_client.models.endpoint_update import EndpointUpdate
from swagger_client.models.entity_error import EntityError
from swagger_client.models.entity_reference import EntityReference
from swagger_client.models.error import Error
from swagger_client.models.error_code import ErrorCode
from swagger_client.models.evaluation import Evaluation
from swagger_client.models.evaluation_links import EvaluationLinks
from swagger_client.models.evaluation_properties import EvaluationProperties
from swagger_client.models.evaluation_update import EvaluationUpdate
from swagger_client.models.file import File
from swagger_client.models.file_kind import FileKind
from swagger_client.models.file_links import FileLinks
from swagger_client.models.file_properties import FileProperties
from swagger_client.models.health_status import HealthStatus
from swagger_client.models.inner_error import InnerError
from swagger_client.models.language_identification_properties import LanguageIdentificationProperties
from swagger_client.models.model_copy import ModelCopy
from swagger_client.models.model_file import ModelFile
from swagger_client.models.model_manifest import ModelManifest
from swagger_client.models.model_update import ModelUpdate
from swagger_client.models.paginated_base_models import PaginatedBaseModels
from swagger_client.models.paginated_custom_models import PaginatedCustomModels
from swagger_client.models.paginated_datasets import PaginatedDatasets
from swagger_client.models.paginated_endpoints import PaginatedEndpoints
from swagger_client.models.paginated_evaluations import PaginatedEvaluations
from swagger_client.models.paginated_files import PaginatedFiles
from swagger_client.models.paginated_projects import PaginatedProjects
from swagger_client.models.paginated_transcriptions import PaginatedTranscriptions
from swagger_client.models.paginated_web_hooks import PaginatedWebHooks
from swagger_client.models.profanity_filter_mode import ProfanityFilterMode
from swagger_client.models.project import Project
from swagger_client.models.project_links import ProjectLinks
from swagger_client.models.project_properties import ProjectProperties
from swagger_client.models.project_update import ProjectUpdate
from swagger_client.models.punctuation_mode import PunctuationMode
from swagger_client.models.response_block import ResponseBlock
from swagger_client.models.service_health import ServiceHealth
from swagger_client.models.shared_model import SharedModel
from swagger_client.models.shared_model_features import SharedModelFeatures
from swagger_client.models.status import Status
from swagger_client.models.transcription import Transcription
from swagger_client.models.transcription_links import TranscriptionLinks
from swagger_client.models.transcription_properties import TranscriptionProperties
from swagger_client.models.transcription_update import TranscriptionUpdate
from swagger_client.models.uploaded_blocks import UploadedBlocks
from swagger_client.models.web_hook import WebHook
from swagger_client.models.web_hook_events import WebHookEvents
from swagger_client.models.web_hook_links import WebHookLinks
from swagger_client.models.web_hook_properties import WebHookProperties
from swagger_client.models.web_hook_properties_update import WebHookPropertiesUpdate
from swagger_client.models.web_hook_update import WebHookUpdate
