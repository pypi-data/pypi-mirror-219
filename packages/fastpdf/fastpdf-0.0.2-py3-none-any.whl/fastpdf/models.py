"""
models.py

MIT Licence

FastPDF Service/Fast Track Technologies
"""

import datetime

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

   
class EngineEnum(str, Enum):
    jinja2 = "jinja2"
    flask = "flask"
    chrome = "chrome"
    webkit = "webkit"
    

@dataclass
class StyleFile:
    format: str
    description: Optional[str] = field(default="fastpdf-python StyleFile")
    stylesheet_file: Optional[bytes] = field(default=None)
    id: Optional[str] = field(default=None)
    number: Optional[int] = field(default=None)
    timestamp: Optional[datetime.datetime] = field(default=None)
    template_name: Optional[str] = field(default=None)
    template_id: Optional[str] = field(default=None)


@dataclass
class ImageFile:
    format: str
    uri: str
    description: Optional[str] = field(default="fastpdf-python ImageFile")
    image_file: Optional[bytes] = field(default=None)
    id: Optional[str] = field(default=None)
    number: Optional[int] = field(default=None)
    timestamp: Optional[datetime.datetime] = field(default=None)
    template_name: Optional[str] = field(default=None)
    template_id: Optional[str] = field(default=None)


@dataclass
class Template:
    name: str
    format: str
    description: Optional[str] = field(default="fastpdf-python Template")
    id: Optional[str] = field(default=None)
    #style_files: list[StyleFile]
    #image_files: list[ImageFile]
    #template_file: Optional[bytes]
    header_file: Optional[bytes] = field(default=None)
    footer_file: Optional[bytes] = field(default=None)
    
    landscape: Optional[bool] = field(default=None)
    paper_format: Optional[str] = field(default=None)
    background: Optional[bool] = field(default=None)
    page_range: Optional[str] = field(default=None)
    scale: Optional[float] = field(default=None)
    
    margin_top: Optional[float] = field(default=None)
    margin_right: Optional[float] = field(default=None)
    margin_bottom: Optional[float] = field(default=None)
    margin_left: Optional[float] = field(default=None)
    
    page_number_footer_enabled: Optional[bool] = field(default=None)
    title_header_enabled: Optional[bool] = field(default=None)
    date_header_enabled: Optional[bool] = field(default=None)


@dataclass
class RenderOptions:
    templating_engine: Optional[str] = field(default=None)
    rendering_engine: Optional[str] = field(default=None)
    display_header_footer: Optional[bool] = field(default=None)

    header_file: Optional[bytes] = field(default=None)
    footer_file: Optional[bytes] = field(default=None)
    
    landscape: Optional[bool] = field(default=None)
    paper_format: Optional[str] = field(default=None)
    background: Optional[bool] = field(default=None)
    page_range: Optional[str] = field(default=None)
    scale: Optional[float] = field(default=None)
    
    margin_top: Optional[float] = field(default=None)
    margin_right: Optional[float] = field(default=None)
    margin_bottom: Optional[float] = field(default=None)
    margin_left: Optional[float] = field(default=None)
    
    page_number_footer_enabled: Optional[bool] = field(default=None)
    title_header_enabled: Optional[bool] = field(default=None)
    date_header_enabled: Optional[bool] = field(default=None)
    
    # Barcode & Image
    x: Optional[float] = field(default=None)
    y: Optional[float] = field(default=None)
    w: Optional[float] = field(default=None)
    h: Optional[float] = field(default=None)
    width: Optional[float] = field(default=None)
    height: Optional[float] = field(default=None)
    keep_ratio: Optional[bool] = field(default=None)
    text_enabled: Optional[bool] = field(default=None)

    # Image
    image_mode: Optional[str] = field(default=None)
    compress: Optional[bool] = field(default=None)
    transparency_enabled: Optional[bool] = field(default=None)
    background_color: Optional[tuple] = field(default=None)

