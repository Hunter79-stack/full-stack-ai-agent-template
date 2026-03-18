"""RAG Config.

Variables and constants used in the RAG feature to run it."""

from enum import StrEnum

from pydantic import BaseModel, Field


class DocumentExtensions(StrEnum):
    """Extensions supported by the RAG ingestion pipeline."""

    PDF = ".pdf"
    DOCX = ".docx"
    MD = ".md"
    TXT = ".txt"


class EmbeddingsConfig(BaseModel):
    """Embeddings configuration for usage in RAG feature."""

    model: str = "all-MiniLM-L6-v2"
    dim: int = 384


class RerankerConfig(BaseModel):
    """Reranker configuration for usage in RAG features."""

    model: str = "cross_encoder"


class DocumentParser(BaseModel):
    """Document parsing settings for RAG features.

    Note: This now only applies to non-PDF files (txt, md, docx).
    PDF parsing is controlled separately via pdf_parser.
    """

    method: str = "python_native"  # Always python_native for non-PDF


class PdfParser(BaseModel):
    """PDF parsing settings for RAG features."""

    method: str = "pymupdf"


class RAGSettings(BaseModel):
    """Constants and variables used to setup the RAG features."""

    # Collection
    collection_name: str = "documents"

    # Documents
    allowed_extensions: list[DocumentExtensions] = Field(
        default_factory=lambda: list(DocumentExtensions)
    )

    # Chunking
    chunk_size: int = 512
    chunk_overlap: int = 50
    chunking_strategy: str = "recursive"  # recursive, markdown, or fixed
    enable_hybrid_search: bool = False  # BM25 + vector fusion
    enable_ocr: bool = False  # OCR fallback for scanned PDFs (requires tesseract)

    # Embeddings
    embeddings_config: EmbeddingsConfig = Field(default_factory=EmbeddingsConfig)

    # Reranker
    reranker_config: RerankerConfig = Field(default_factory=RerankerConfig)

    # Document parsing
    document_parser: DocumentParser = Field(default_factory=DocumentParser)

    # PDF parsing
    pdf_parser: PdfParser = Field(default_factory=PdfParser)
    # Ingestion
    gdrive_ingestion: bool = True
