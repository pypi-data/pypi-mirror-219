# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from ncbi.datasets.openapi.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from ncbi.datasets.openapi.model.protobuf_any import ProtobufAny
from ncbi.datasets.openapi.model.rpc_status import RpcStatus
from ncbi.datasets.openapi.model.v1_accessions import V1Accessions
from ncbi.datasets.openapi.model.v1_accessions import V1Accessions as V1alpha1Accessions
from ncbi.datasets.openapi.model.v1_annotated_assemblies import V1AnnotatedAssemblies
from ncbi.datasets.openapi.model.v1_annotated_assemblies import V1AnnotatedAssemblies as V1alpha1AnnotatedAssemblies
from ncbi.datasets.openapi.model.v1_annotation import V1Annotation
from ncbi.datasets.openapi.model.v1_annotation import V1Annotation as V1alpha1Annotation
from ncbi.datasets.openapi.model.v1_annotation_for_assembly import V1AnnotationForAssembly
from ncbi.datasets.openapi.model.v1_annotation_for_assembly import V1AnnotationForAssembly as V1alpha1AnnotationForAssembly
from ncbi.datasets.openapi.model.v1_annotation_for_assembly_file import V1AnnotationForAssemblyFile
from ncbi.datasets.openapi.model.v1_annotation_for_assembly_file import V1AnnotationForAssemblyFile as V1alpha1AnnotationForAssemblyFile
from ncbi.datasets.openapi.model.v1_annotation_for_assembly_type import V1AnnotationForAssemblyType
from ncbi.datasets.openapi.model.v1_annotation_for_assembly_type import V1AnnotationForAssemblyType as V1alpha1AnnotationForAssemblyType
from ncbi.datasets.openapi.model.v1_annotation_for_virus_type import V1AnnotationForVirusType
from ncbi.datasets.openapi.model.v1_annotation_for_virus_type import V1AnnotationForVirusType as V1alpha1AnnotationForVirusType
from ncbi.datasets.openapi.model.v1_assembly_dataset_availability import V1AssemblyDatasetAvailability
from ncbi.datasets.openapi.model.v1_assembly_dataset_availability import V1AssemblyDatasetAvailability as V1alpha1AssemblyDatasetAvailability
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptor import V1AssemblyDatasetDescriptor
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptor import V1AssemblyDatasetDescriptor as V1alpha1AssemblyDatasetDescriptor
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptor_chromosome import V1AssemblyDatasetDescriptorChromosome
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptor_chromosome import V1AssemblyDatasetDescriptorChromosome as V1alpha1AssemblyDatasetDescriptorChromosome
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors import V1AssemblyDatasetDescriptors
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors import V1AssemblyDatasetDescriptors as V1alpha1AssemblyDatasetDescriptors
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors_filter import V1AssemblyDatasetDescriptorsFilter
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors_filter import V1AssemblyDatasetDescriptorsFilter as V1alpha1AssemblyDatasetDescriptorsFilter
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors_filter_assembly_level import V1AssemblyDatasetDescriptorsFilterAssemblyLevel
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors_filter_assembly_level import V1AssemblyDatasetDescriptorsFilterAssemblyLevel as V1alpha1AssemblyDatasetDescriptorsFilterAssemblyLevel
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors_filter_assembly_source import V1AssemblyDatasetDescriptorsFilterAssemblySource
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors_filter_assembly_source import V1AssemblyDatasetDescriptorsFilterAssemblySource as V1alpha1AssemblyDatasetDescriptorsFilterAssemblySource
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors_filter_assembly_version import V1AssemblyDatasetDescriptorsFilterAssemblyVersion
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors_filter_assembly_version import V1AssemblyDatasetDescriptorsFilterAssemblyVersion as V1alpha1AssemblyDatasetDescriptorsFilterAssemblyVersion
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors_request import V1AssemblyDatasetDescriptorsRequest
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors_request import V1AssemblyDatasetDescriptorsRequest as V1alpha1AssemblyDatasetDescriptorsRequest
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors_request_content_type import V1AssemblyDatasetDescriptorsRequestContentType
from ncbi.datasets.openapi.model.v1_assembly_dataset_descriptors_request_content_type import V1AssemblyDatasetDescriptorsRequestContentType as V1alpha1AssemblyDatasetDescriptorsRequestContentType
from ncbi.datasets.openapi.model.v1_assembly_dataset_request import V1AssemblyDatasetRequest
from ncbi.datasets.openapi.model.v1_assembly_dataset_request import V1AssemblyDatasetRequest as V1alpha1AssemblyDatasetRequest
from ncbi.datasets.openapi.model.v1_assembly_dataset_request_resolution import V1AssemblyDatasetRequestResolution
from ncbi.datasets.openapi.model.v1_assembly_dataset_request_resolution import V1AssemblyDatasetRequestResolution as V1alpha1AssemblyDatasetRequestResolution
from ncbi.datasets.openapi.model.v1_assembly_match import V1AssemblyMatch
from ncbi.datasets.openapi.model.v1_assembly_match import V1AssemblyMatch as V1alpha1AssemblyMatch
from ncbi.datasets.openapi.model.v1_assembly_metadata import V1AssemblyMetadata
from ncbi.datasets.openapi.model.v1_assembly_metadata import V1AssemblyMetadata as V1alpha1AssemblyMetadata
from ncbi.datasets.openapi.model.v1_assembly_metadata_request import V1AssemblyMetadataRequest
from ncbi.datasets.openapi.model.v1_assembly_metadata_request import V1AssemblyMetadataRequest as V1alpha1AssemblyMetadataRequest
from ncbi.datasets.openapi.model.v1_assembly_metadata_request_bioprojects import V1AssemblyMetadataRequestBioprojects
from ncbi.datasets.openapi.model.v1_assembly_metadata_request_bioprojects import V1AssemblyMetadataRequestBioprojects as V1alpha1AssemblyMetadataRequestBioprojects
from ncbi.datasets.openapi.model.v1_assembly_metadata_request_content_type import V1AssemblyMetadataRequestContentType
from ncbi.datasets.openapi.model.v1_assembly_metadata_request_content_type import V1AssemblyMetadataRequestContentType as V1alpha1AssemblyMetadataRequestContentType
from ncbi.datasets.openapi.model.v1_bio_project import V1BioProject
from ncbi.datasets.openapi.model.v1_bio_project import V1BioProject as V1alpha1BioProject
from ncbi.datasets.openapi.model.v1_bio_project_lineage import V1BioProjectLineage
from ncbi.datasets.openapi.model.v1_bio_project_lineage import V1BioProjectLineage as V1alpha1BioProjectLineage
from ncbi.datasets.openapi.model.v1_busco_stat import V1BuscoStat
from ncbi.datasets.openapi.model.v1_busco_stat import V1BuscoStat as V1alpha1BuscoStat
from ncbi.datasets.openapi.model.v1_count_type import V1CountType
from ncbi.datasets.openapi.model.v1_count_type import V1CountType as V1alpha1CountType
from ncbi.datasets.openapi.model.v1_dataset_request import V1DatasetRequest
from ncbi.datasets.openapi.model.v1_dataset_request import V1DatasetRequest as V1alpha1DatasetRequest
from ncbi.datasets.openapi.model.v1_download_summary import V1DownloadSummary
from ncbi.datasets.openapi.model.v1_download_summary import V1DownloadSummary as V1alpha1DownloadSummary
from ncbi.datasets.openapi.model.v1_download_summary_available_files import V1DownloadSummaryAvailableFiles
from ncbi.datasets.openapi.model.v1_download_summary_available_files import V1DownloadSummaryAvailableFiles as V1alpha1DownloadSummaryAvailableFiles
from ncbi.datasets.openapi.model.v1_download_summary_dehydrated import V1DownloadSummaryDehydrated
from ncbi.datasets.openapi.model.v1_download_summary_dehydrated import V1DownloadSummaryDehydrated as V1alpha1DownloadSummaryDehydrated
from ncbi.datasets.openapi.model.v1_download_summary_file_summary import V1DownloadSummaryFileSummary
from ncbi.datasets.openapi.model.v1_download_summary_file_summary import V1DownloadSummaryFileSummary as V1alpha1DownloadSummaryFileSummary
from ncbi.datasets.openapi.model.v1_download_summary_hydrated import V1DownloadSummaryHydrated
from ncbi.datasets.openapi.model.v1_download_summary_hydrated import V1DownloadSummaryHydrated as V1alpha1DownloadSummaryHydrated
from ncbi.datasets.openapi.model.v1_element_flank_config import V1ElementFlankConfig
from ncbi.datasets.openapi.model.v1_element_flank_config import V1ElementFlankConfig as V1alpha1ElementFlankConfig
from ncbi.datasets.openapi.model.v1_error import V1Error
from ncbi.datasets.openapi.model.v1_error import V1Error as V1alpha1Error
from ncbi.datasets.openapi.model.v1_error_assembly_error_code import V1ErrorAssemblyErrorCode
from ncbi.datasets.openapi.model.v1_error_assembly_error_code import V1ErrorAssemblyErrorCode as V1alpha1ErrorAssemblyErrorCode
from ncbi.datasets.openapi.model.v1_error_gene_error_code import V1ErrorGeneErrorCode
from ncbi.datasets.openapi.model.v1_error_gene_error_code import V1ErrorGeneErrorCode as V1alpha1ErrorGeneErrorCode
from ncbi.datasets.openapi.model.v1_error_virus_error_code import V1ErrorVirusErrorCode
from ncbi.datasets.openapi.model.v1_error_virus_error_code import V1ErrorVirusErrorCode as V1alpha1ErrorVirusErrorCode
from ncbi.datasets.openapi.model.v1_fasta import V1Fasta
from ncbi.datasets.openapi.model.v1_fasta import V1Fasta as V1alpha1Fasta
from ncbi.datasets.openapi.model.v1_feature_counts import V1FeatureCounts
from ncbi.datasets.openapi.model.v1_feature_counts import V1FeatureCounts as V1alpha1FeatureCounts
from ncbi.datasets.openapi.model.v1_gene_counts import V1GeneCounts
from ncbi.datasets.openapi.model.v1_gene_counts import V1GeneCounts as V1alpha1GeneCounts
from ncbi.datasets.openapi.model.v1_gene_dataset_request import V1GeneDatasetRequest
from ncbi.datasets.openapi.model.v1_gene_dataset_request import V1GeneDatasetRequest as V1alpha1GeneDatasetRequest
from ncbi.datasets.openapi.model.v1_gene_dataset_request_content_type import V1GeneDatasetRequestContentType
from ncbi.datasets.openapi.model.v1_gene_dataset_request_content_type import V1GeneDatasetRequestContentType as V1alpha1GeneDatasetRequestContentType
from ncbi.datasets.openapi.model.v1_gene_dataset_request_sort import V1GeneDatasetRequestSort
from ncbi.datasets.openapi.model.v1_gene_dataset_request_sort import V1GeneDatasetRequestSort as V1alpha1GeneDatasetRequestSort
from ncbi.datasets.openapi.model.v1_gene_dataset_request_sort_field import V1GeneDatasetRequestSortField
from ncbi.datasets.openapi.model.v1_gene_dataset_request_sort_field import V1GeneDatasetRequestSortField as V1alpha1GeneDatasetRequestSortField
from ncbi.datasets.openapi.model.v1_gene_dataset_request_symbols_for_taxon import V1GeneDatasetRequestSymbolsForTaxon
from ncbi.datasets.openapi.model.v1_gene_dataset_request_symbols_for_taxon import V1GeneDatasetRequestSymbolsForTaxon as V1alpha1GeneDatasetRequestSymbolsForTaxon
from ncbi.datasets.openapi.model.v1_gene_descriptor import V1GeneDescriptor
from ncbi.datasets.openapi.model.v1_gene_descriptor import V1GeneDescriptor as V1alpha1GeneDescriptor
from ncbi.datasets.openapi.model.v1_gene_descriptor_gene_type import V1GeneDescriptorGeneType
from ncbi.datasets.openapi.model.v1_gene_descriptor_gene_type import V1GeneDescriptorGeneType as V1alpha1GeneDescriptorGeneType
from ncbi.datasets.openapi.model.v1_gene_descriptor_rna_type import V1GeneDescriptorRnaType
from ncbi.datasets.openapi.model.v1_gene_descriptor_rna_type import V1GeneDescriptorRnaType as V1alpha1GeneDescriptorRnaType
from ncbi.datasets.openapi.model.v1_gene_descriptors import V1GeneDescriptors
from ncbi.datasets.openapi.model.v1_gene_descriptors import V1GeneDescriptors as V1alpha1GeneDescriptors
from ncbi.datasets.openapi.model.v1_gene_group import V1GeneGroup
from ncbi.datasets.openapi.model.v1_gene_group import V1GeneGroup as V1alpha1GeneGroup
from ncbi.datasets.openapi.model.v1_gene_match import V1GeneMatch
from ncbi.datasets.openapi.model.v1_gene_match import V1GeneMatch as V1alpha1GeneMatch
from ncbi.datasets.openapi.model.v1_gene_metadata import V1GeneMetadata
from ncbi.datasets.openapi.model.v1_gene_metadata import V1GeneMetadata as V1alpha1GeneMetadata
from ncbi.datasets.openapi.model.v1_genomic_location import V1GenomicLocation
from ncbi.datasets.openapi.model.v1_genomic_location import V1GenomicLocation as V1alpha1GenomicLocation
from ncbi.datasets.openapi.model.v1_genomic_region import V1GenomicRegion
from ncbi.datasets.openapi.model.v1_genomic_region import V1GenomicRegion as V1alpha1GenomicRegion
from ncbi.datasets.openapi.model.v1_genomic_region_genomic_region_type import V1GenomicRegionGenomicRegionType
from ncbi.datasets.openapi.model.v1_genomic_region_genomic_region_type import V1GenomicRegionGenomicRegionType as V1alpha1GenomicRegionGenomicRegionType
from ncbi.datasets.openapi.model.v1_mature_peptide import V1MaturePeptide
from ncbi.datasets.openapi.model.v1_mature_peptide import V1MaturePeptide as V1alpha1MaturePeptide
from ncbi.datasets.openapi.model.v1_message import V1Message
from ncbi.datasets.openapi.model.v1_message import V1Message as V1alpha1Message
from ncbi.datasets.openapi.model.v1_method_payload_request import V1MethodPayloadRequest
from ncbi.datasets.openapi.model.v1_method_payload_request import V1MethodPayloadRequest as V1alpha1MethodPayloadRequest
from ncbi.datasets.openapi.model.v1_micro_bigge_dataset_request import V1MicroBiggeDatasetRequest
from ncbi.datasets.openapi.model.v1_micro_bigge_dataset_request import V1MicroBiggeDatasetRequest as V1alpha1MicroBiggeDatasetRequest
from ncbi.datasets.openapi.model.v1_micro_bigge_dataset_request_file_type import V1MicroBiggeDatasetRequestFileType
from ncbi.datasets.openapi.model.v1_micro_bigge_dataset_request_file_type import V1MicroBiggeDatasetRequestFileType as V1alpha1MicroBiggeDatasetRequestFileType
from ncbi.datasets.openapi.model.v1_nomenclature_authority import V1NomenclatureAuthority
from ncbi.datasets.openapi.model.v1_nomenclature_authority import V1NomenclatureAuthority as V1alpha1NomenclatureAuthority
from ncbi.datasets.openapi.model.v1_organism import V1Organism
from ncbi.datasets.openapi.model.v1_organism import V1Organism as V1alpha1Organism
from ncbi.datasets.openapi.model.v1_organism_count_by_type import V1OrganismCountByType
from ncbi.datasets.openapi.model.v1_organism_count_by_type import V1OrganismCountByType as V1alpha1OrganismCountByType
from ncbi.datasets.openapi.model.v1_organism_counts import V1OrganismCounts
from ncbi.datasets.openapi.model.v1_organism_counts import V1OrganismCounts as V1alpha1OrganismCounts
from ncbi.datasets.openapi.model.v1_organism_query_request import V1OrganismQueryRequest
from ncbi.datasets.openapi.model.v1_organism_query_request import V1OrganismQueryRequest as V1alpha1OrganismQueryRequest
from ncbi.datasets.openapi.model.v1_organism_query_request_tax_rank_filter import V1OrganismQueryRequestTaxRankFilter
from ncbi.datasets.openapi.model.v1_organism_query_request_tax_rank_filter import V1OrganismQueryRequestTaxRankFilter as V1alpha1OrganismQueryRequestTaxRankFilter
from ncbi.datasets.openapi.model.v1_organism_rank_type import V1OrganismRankType
from ncbi.datasets.openapi.model.v1_organism_rank_type import V1OrganismRankType as V1alpha1OrganismRankType
from ncbi.datasets.openapi.model.v1_orientation import V1Orientation
from ncbi.datasets.openapi.model.v1_orientation import V1Orientation as V1alpha1Orientation
from ncbi.datasets.openapi.model.v1_ortholog_request import V1OrthologRequest
from ncbi.datasets.openapi.model.v1_ortholog_request import V1OrthologRequest as V1alpha1OrthologRequest
from ncbi.datasets.openapi.model.v1_ortholog_request_content_type import V1OrthologRequestContentType
from ncbi.datasets.openapi.model.v1_ortholog_request_content_type import V1OrthologRequestContentType as V1alpha1OrthologRequestContentType
from ncbi.datasets.openapi.model.v1_ortholog_set import V1OrthologSet
from ncbi.datasets.openapi.model.v1_ortholog_set import V1OrthologSet as V1alpha1OrthologSet
from ncbi.datasets.openapi.model.v1_prokaryote_gene_request import V1ProkaryoteGeneRequest
from ncbi.datasets.openapi.model.v1_prokaryote_gene_request import V1ProkaryoteGeneRequest as V1alpha1ProkaryoteGeneRequest
from ncbi.datasets.openapi.model.v1_prokaryote_gene_request_gene_flank_config import V1ProkaryoteGeneRequestGeneFlankConfig
from ncbi.datasets.openapi.model.v1_prokaryote_gene_request_gene_flank_config import V1ProkaryoteGeneRequestGeneFlankConfig as V1alpha1ProkaryoteGeneRequestGeneFlankConfig
from ncbi.datasets.openapi.model.v1_protein import V1Protein
from ncbi.datasets.openapi.model.v1_protein import V1Protein as V1alpha1Protein
from ncbi.datasets.openapi.model.v1_range import V1Range
from ncbi.datasets.openapi.model.v1_range import V1Range as V1alpha1Range
from ncbi.datasets.openapi.model.v1_ref_gene_catalog_dataset_request import V1RefGeneCatalogDatasetRequest
from ncbi.datasets.openapi.model.v1_ref_gene_catalog_dataset_request import V1RefGeneCatalogDatasetRequest as V1alpha1RefGeneCatalogDatasetRequest
from ncbi.datasets.openapi.model.v1_ref_gene_catalog_dataset_request_file_type import V1RefGeneCatalogDatasetRequestFileType
from ncbi.datasets.openapi.model.v1_ref_gene_catalog_dataset_request_file_type import V1RefGeneCatalogDatasetRequestFileType as V1alpha1RefGeneCatalogDatasetRequestFileType
from ncbi.datasets.openapi.model.v1_sars2_protein_dataset_request import V1Sars2ProteinDatasetRequest
from ncbi.datasets.openapi.model.v1_sars2_protein_dataset_request import V1Sars2ProteinDatasetRequest as V1alpha1Sars2ProteinDatasetRequest
from ncbi.datasets.openapi.model.v1_sci_name_and_ids import V1SciNameAndIds
from ncbi.datasets.openapi.model.v1_sci_name_and_ids import V1SciNameAndIds as V1alpha1SciNameAndIds
from ncbi.datasets.openapi.model.v1_sci_name_and_ids_sci_name_and_id import V1SciNameAndIdsSciNameAndId
from ncbi.datasets.openapi.model.v1_sci_name_and_ids_sci_name_and_id import V1SciNameAndIdsSciNameAndId as V1alpha1SciNameAndIdsSciNameAndId
from ncbi.datasets.openapi.model.v1_seq_range_set import V1SeqRangeSet
from ncbi.datasets.openapi.model.v1_seq_range_set import V1SeqRangeSet as V1alpha1SeqRangeSet
from ncbi.datasets.openapi.model.v1_sleep_reply import V1SleepReply
from ncbi.datasets.openapi.model.v1_sleep_reply import V1SleepReply as V1alpha1SleepReply
from ncbi.datasets.openapi.model.v1_sleep_request import V1SleepRequest
from ncbi.datasets.openapi.model.v1_sleep_request import V1SleepRequest as V1alpha1SleepRequest
from ncbi.datasets.openapi.model.v1_sort_direction import V1SortDirection
from ncbi.datasets.openapi.model.v1_sort_direction import V1SortDirection as V1alpha1SortDirection
from ncbi.datasets.openapi.model.v1_table_format import V1TableFormat
from ncbi.datasets.openapi.model.v1_table_format import V1TableFormat as V1alpha1TableFormat
from ncbi.datasets.openapi.model.v1_tabular_output import V1TabularOutput
from ncbi.datasets.openapi.model.v1_tabular_output import V1TabularOutput as V1alpha1TabularOutput
from ncbi.datasets.openapi.model.v1_tax_tree_request import V1TaxTreeRequest
from ncbi.datasets.openapi.model.v1_tax_tree_request import V1TaxTreeRequest as V1alpha1TaxTreeRequest
from ncbi.datasets.openapi.model.v1_taxonomy_filtered_subtree_request import V1TaxonomyFilteredSubtreeRequest
from ncbi.datasets.openapi.model.v1_taxonomy_filtered_subtree_request import V1TaxonomyFilteredSubtreeRequest as V1alpha1TaxonomyFilteredSubtreeRequest
from ncbi.datasets.openapi.model.v1_taxonomy_filtered_subtree_response import V1TaxonomyFilteredSubtreeResponse
from ncbi.datasets.openapi.model.v1_taxonomy_filtered_subtree_response import V1TaxonomyFilteredSubtreeResponse as V1alpha1TaxonomyFilteredSubtreeResponse
from ncbi.datasets.openapi.model.v1_taxonomy_filtered_subtree_response_edge import V1TaxonomyFilteredSubtreeResponseEdge
from ncbi.datasets.openapi.model.v1_taxonomy_filtered_subtree_response_edge import V1TaxonomyFilteredSubtreeResponseEdge as V1alpha1TaxonomyFilteredSubtreeResponseEdge
from ncbi.datasets.openapi.model.v1_taxonomy_filtered_subtree_response_edge_child_status import V1TaxonomyFilteredSubtreeResponseEdgeChildStatus
from ncbi.datasets.openapi.model.v1_taxonomy_filtered_subtree_response_edge_child_status import V1TaxonomyFilteredSubtreeResponseEdgeChildStatus as V1alpha1TaxonomyFilteredSubtreeResponseEdgeChildStatus
from ncbi.datasets.openapi.model.v1_taxonomy_filtered_subtree_response_edges_entry import V1TaxonomyFilteredSubtreeResponseEdgesEntry
from ncbi.datasets.openapi.model.v1_taxonomy_filtered_subtree_response_edges_entry import V1TaxonomyFilteredSubtreeResponseEdgesEntry as V1alpha1TaxonomyFilteredSubtreeResponseEdgesEntry
from ncbi.datasets.openapi.model.v1_taxonomy_match import V1TaxonomyMatch
from ncbi.datasets.openapi.model.v1_taxonomy_match import V1TaxonomyMatch as V1alpha1TaxonomyMatch
from ncbi.datasets.openapi.model.v1_taxonomy_metadata_request import V1TaxonomyMetadataRequest
from ncbi.datasets.openapi.model.v1_taxonomy_metadata_request import V1TaxonomyMetadataRequest as V1alpha1TaxonomyMetadataRequest
from ncbi.datasets.openapi.model.v1_taxonomy_metadata_request_content_type import V1TaxonomyMetadataRequestContentType
from ncbi.datasets.openapi.model.v1_taxonomy_metadata_request_content_type import V1TaxonomyMetadataRequestContentType as V1alpha1TaxonomyMetadataRequestContentType
from ncbi.datasets.openapi.model.v1_taxonomy_metadata_response import V1TaxonomyMetadataResponse
from ncbi.datasets.openapi.model.v1_taxonomy_metadata_response import V1TaxonomyMetadataResponse as V1alpha1TaxonomyMetadataResponse
from ncbi.datasets.openapi.model.v1_taxonomy_node import V1TaxonomyNode
from ncbi.datasets.openapi.model.v1_taxonomy_node import V1TaxonomyNode as V1alpha1TaxonomyNode
from ncbi.datasets.openapi.model.v1_taxonomy_node_count_by_type import V1TaxonomyNodeCountByType
from ncbi.datasets.openapi.model.v1_taxonomy_node_count_by_type import V1TaxonomyNodeCountByType as V1alpha1TaxonomyNodeCountByType
from ncbi.datasets.openapi.model.v1_transcript import V1Transcript
from ncbi.datasets.openapi.model.v1_transcript import V1Transcript as V1alpha1Transcript
from ncbi.datasets.openapi.model.v1_transcript_transcript_type import V1TranscriptTranscriptType
from ncbi.datasets.openapi.model.v1_transcript_transcript_type import V1TranscriptTranscriptType as V1alpha1TranscriptTranscriptType
from ncbi.datasets.openapi.model.v1_version_reply import V1VersionReply
from ncbi.datasets.openapi.model.v1_version_reply import V1VersionReply as V1alpha1VersionReply
from ncbi.datasets.openapi.model.v1_virus_availability import V1VirusAvailability
from ncbi.datasets.openapi.model.v1_virus_availability import V1VirusAvailability as V1alpha1VirusAvailability
from ncbi.datasets.openapi.model.v1_virus_availability_request import V1VirusAvailabilityRequest
from ncbi.datasets.openapi.model.v1_virus_availability_request import V1VirusAvailabilityRequest as V1alpha1VirusAvailabilityRequest
from ncbi.datasets.openapi.model.v1_virus_data_report_request import V1VirusDataReportRequest
from ncbi.datasets.openapi.model.v1_virus_data_report_request import V1VirusDataReportRequest as V1alpha1VirusDataReportRequest
from ncbi.datasets.openapi.model.v1_virus_data_report_request_content_type import V1VirusDataReportRequestContentType
from ncbi.datasets.openapi.model.v1_virus_data_report_request_content_type import V1VirusDataReportRequestContentType as V1alpha1VirusDataReportRequestContentType
from ncbi.datasets.openapi.model.v1_virus_dataset_filter import V1VirusDatasetFilter
from ncbi.datasets.openapi.model.v1_virus_dataset_filter import V1VirusDatasetFilter as V1alpha1VirusDatasetFilter
from ncbi.datasets.openapi.model.v1_virus_dataset_request import V1VirusDatasetRequest
from ncbi.datasets.openapi.model.v1_virus_dataset_request import V1VirusDatasetRequest as V1alpha1VirusDatasetRequest
from ncbi.datasets.openapi.model.v1_virus_table_field import V1VirusTableField
from ncbi.datasets.openapi.model.v1_virus_table_field import V1VirusTableField as V1alpha1VirusTableField
from ncbi.datasets.openapi.model.v1_warning import V1Warning
from ncbi.datasets.openapi.model.v1_warning import V1Warning as V1alpha1Warning
from ncbi.datasets.openapi.model.v1_warning_gene_warning_code import V1WarningGeneWarningCode
from ncbi.datasets.openapi.model.v1_warning_gene_warning_code import V1WarningGeneWarningCode as V1alpha1WarningGeneWarningCode
from ncbi.datasets.openapi.model.v1_warning_replaced_id import V1WarningReplacedId
from ncbi.datasets.openapi.model.v1_warning_replaced_id import V1WarningReplacedId as V1alpha1WarningReplacedId
from ncbi.datasets.openapi.model.v1reports_assembly_status import V1reportsAssemblyStatus
from ncbi.datasets.openapi.model.v1reports_assembly_status import V1reportsAssemblyStatus as V1alpha1reportsAssemblyStatus
from ncbi.datasets.openapi.model.v1reports_bio_project import V1reportsBioProject
from ncbi.datasets.openapi.model.v1reports_bio_project import V1reportsBioProject as V1alpha1reportsBioProject
from ncbi.datasets.openapi.model.v1reports_bio_sample_attribute import V1reportsBioSampleAttribute
from ncbi.datasets.openapi.model.v1reports_bio_sample_attribute import V1reportsBioSampleAttribute as V1alpha1reportsBioSampleAttribute
from ncbi.datasets.openapi.model.v1reports_bio_sample_contact import V1reportsBioSampleContact
from ncbi.datasets.openapi.model.v1reports_bio_sample_contact import V1reportsBioSampleContact as V1alpha1reportsBioSampleContact
from ncbi.datasets.openapi.model.v1reports_bio_sample_description import V1reportsBioSampleDescription
from ncbi.datasets.openapi.model.v1reports_bio_sample_description import V1reportsBioSampleDescription as V1alpha1reportsBioSampleDescription
from ncbi.datasets.openapi.model.v1reports_bio_sample_descriptor import V1reportsBioSampleDescriptor
from ncbi.datasets.openapi.model.v1reports_bio_sample_descriptor import V1reportsBioSampleDescriptor as V1alpha1reportsBioSampleDescriptor
from ncbi.datasets.openapi.model.v1reports_bio_sample_id import V1reportsBioSampleId
from ncbi.datasets.openapi.model.v1reports_bio_sample_id import V1reportsBioSampleId as V1alpha1reportsBioSampleId
from ncbi.datasets.openapi.model.v1reports_bio_sample_owner import V1reportsBioSampleOwner
from ncbi.datasets.openapi.model.v1reports_bio_sample_owner import V1reportsBioSampleOwner as V1alpha1reportsBioSampleOwner
from ncbi.datasets.openapi.model.v1reports_bio_sample_status import V1reportsBioSampleStatus
from ncbi.datasets.openapi.model.v1reports_bio_sample_status import V1reportsBioSampleStatus as V1alpha1reportsBioSampleStatus
from ncbi.datasets.openapi.model.v1reports_conserved_domain import V1reportsConservedDomain
from ncbi.datasets.openapi.model.v1reports_conserved_domain import V1reportsConservedDomain as V1alpha1reportsConservedDomain
from ncbi.datasets.openapi.model.v1reports_gene_descriptor_gene_type import V1reportsGeneDescriptorGeneType
from ncbi.datasets.openapi.model.v1reports_gene_descriptor_gene_type import V1reportsGeneDescriptorGeneType as V1alpha1reportsGeneDescriptorGeneType
from ncbi.datasets.openapi.model.v1reports_gene_descriptor_rna_type import V1reportsGeneDescriptorRnaType
from ncbi.datasets.openapi.model.v1reports_gene_descriptor_rna_type import V1reportsGeneDescriptorRnaType as V1alpha1reportsGeneDescriptorRnaType
from ncbi.datasets.openapi.model.v1reports_genomic_region_genomic_region_type import V1reportsGenomicRegionGenomicRegionType
from ncbi.datasets.openapi.model.v1reports_genomic_region_genomic_region_type import V1reportsGenomicRegionGenomicRegionType as V1alpha1reportsGenomicRegionGenomicRegionType
from ncbi.datasets.openapi.model.v1reports_lineage_organism import V1reportsLineageOrganism
from ncbi.datasets.openapi.model.v1reports_lineage_organism import V1reportsLineageOrganism as V1alpha1reportsLineageOrganism
from ncbi.datasets.openapi.model.v1reports_linked_assembly_linked_assembly_type import V1reportsLinkedAssemblyLinkedAssemblyType
from ncbi.datasets.openapi.model.v1reports_linked_assembly_linked_assembly_type import V1reportsLinkedAssemblyLinkedAssemblyType as V1alpha1reportsLinkedAssemblyLinkedAssemblyType
from ncbi.datasets.openapi.model.v1reports_organism import V1reportsOrganism
from ncbi.datasets.openapi.model.v1reports_organism import V1reportsOrganism as V1alpha1reportsOrganism
from ncbi.datasets.openapi.model.v1reports_orientation import V1reportsOrientation
from ncbi.datasets.openapi.model.v1reports_orientation import V1reportsOrientation as V1alpha1reportsOrientation
from ncbi.datasets.openapi.model.v1reports_prokaryote_gene_location_completeness import V1reportsProkaryoteGeneLocationCompleteness
from ncbi.datasets.openapi.model.v1reports_prokaryote_gene_location_completeness import V1reportsProkaryoteGeneLocationCompleteness as V1alpha1reportsProkaryoteGeneLocationCompleteness
from ncbi.datasets.openapi.model.v1reports_purpose_of_sampling import V1reportsPurposeOfSampling
from ncbi.datasets.openapi.model.v1reports_purpose_of_sampling import V1reportsPurposeOfSampling as V1alpha1reportsPurposeOfSampling
from ncbi.datasets.openapi.model.v1reports_range import V1reportsRange
from ncbi.datasets.openapi.model.v1reports_range import V1reportsRange as V1alpha1reportsRange
from ncbi.datasets.openapi.model.v1reports_seq_range_set_fasta import V1reportsSeqRangeSetFasta
from ncbi.datasets.openapi.model.v1reports_seq_range_set_fasta import V1reportsSeqRangeSetFasta as V1alpha1reportsSeqRangeSetFasta
from ncbi.datasets.openapi.model.v1reports_transcript_transcript_type import V1reportsTranscriptTranscriptType
from ncbi.datasets.openapi.model.v1reports_transcript_transcript_type import V1reportsTranscriptTranscriptType as V1alpha1reportsTranscriptTranscriptType
from ncbi.datasets.openapi.model.v1reports_virus_annotation import V1reportsVirusAnnotation
from ncbi.datasets.openapi.model.v1reports_virus_annotation import V1reportsVirusAnnotation as V1alpha1reportsVirusAnnotation
from ncbi.datasets.openapi.model.v1reports_virus_assembly import V1reportsVirusAssembly
from ncbi.datasets.openapi.model.v1reports_virus_assembly import V1reportsVirusAssembly as V1alpha1reportsVirusAssembly
from ncbi.datasets.openapi.model.v1reports_virus_assembly_collection_location import V1reportsVirusAssemblyCollectionLocation
from ncbi.datasets.openapi.model.v1reports_virus_assembly_collection_location import V1reportsVirusAssemblyCollectionLocation as V1alpha1reportsVirusAssemblyCollectionLocation
from ncbi.datasets.openapi.model.v1reports_virus_assembly_completeness import V1reportsVirusAssemblyCompleteness
from ncbi.datasets.openapi.model.v1reports_virus_assembly_completeness import V1reportsVirusAssemblyCompleteness as V1alpha1reportsVirusAssemblyCompleteness
from ncbi.datasets.openapi.model.v1reports_virus_assembly_isolate import V1reportsVirusAssemblyIsolate
from ncbi.datasets.openapi.model.v1reports_virus_assembly_isolate import V1reportsVirusAssemblyIsolate as V1alpha1reportsVirusAssemblyIsolate
from ncbi.datasets.openapi.model.v1reports_virus_data_report_page import V1reportsVirusDataReportPage
from ncbi.datasets.openapi.model.v1reports_virus_data_report_page import V1reportsVirusDataReportPage as V1alpha1reportsVirusDataReportPage
from ncbi.datasets.openapi.model.v1reports_virus_gene import V1reportsVirusGene
from ncbi.datasets.openapi.model.v1reports_virus_gene import V1reportsVirusGene as V1alpha1reportsVirusGene
from ncbi.datasets.openapi.model.v1reports_virus_peptide import V1reportsVirusPeptide
from ncbi.datasets.openapi.model.v1reports_virus_peptide import V1reportsVirusPeptide as V1alpha1reportsVirusPeptide
from ncbi.datasets.openapi.model.v1reports_virus_peptide_uni_prot_id import V1reportsVirusPeptideUniProtId
from ncbi.datasets.openapi.model.v1reports_virus_peptide_uni_prot_id import V1reportsVirusPeptideUniProtId as V1alpha1reportsVirusPeptideUniProtId
