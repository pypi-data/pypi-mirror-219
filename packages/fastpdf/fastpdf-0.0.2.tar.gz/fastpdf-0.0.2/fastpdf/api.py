"""
api.py

MIT Licence

FastPDF Service/Fast Track Technologies
"""

import requests
import json
import mimetypes
import magic
import os

from typing import Union
from io import BytesIO


from dataclasses import asdict

from .exceptions import PDFException
from .models import RenderOptions, Template, StyleFile, ImageFile


def _raise_for_status(response):
    if not response.ok:
        raise PDFException(response)
        
        
def _read_file(file: Union[str, BytesIO, bytes]) -> tuple:
    filename=""
    # If the input is a string, it's treated as a file path
    if isinstance(file, str):
        file_path = file
        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            file_content = f.read()
        content_type = magic.from_buffer(file_content, mime=True)

    # If the input is a BytesIO, get the value
    elif isinstance(file, BytesIO):
        #file.seek(0)
        file_content = file.read()
        content_type = magic.from_buffer(file_content, mime=True)
        
    # If the input is bytes, just use it directly
    elif isinstance(file, bytes):
        file_content = file
        content_type = magic.from_buffer(file_content, mime=True)

    else:
        raise ValueError(f"Expected str, BytesIO, or bytes. Unsupported file type: {type(file)}")

    return (filename, file_content, content_type)


def _asdict_skip_none(data):
    return {k: v for k, v in asdict(data).items() if v is not None}


def _parse_dataclass(_obj, _obj_type):
     _dict_obj = {}
     if _obj is not None:
        if isinstance(_obj, _obj_type):
           _dict_obj = _asdict_skip_none(_obj)
        else:
           _dict_obj = _obj   
     return _dict_obj
     
     
def _parse_render_data_obj(_obj):
    if isinstance(_obj, dict):
       return _obj
    if isinstance(_obj, str):
       with open(_obj, 'rb') as f:
            file_content = f.read()
       return json.loads(file_content)
    raise ValueError(f'Expected dict or str (file path). Unsupported render data type: {type(file)}')
    
def _parse_render_data_list(_obj):
    if isinstance(_obj, list):
       return _obj
    if isinstance(_obj, str):
       with open(_obj, 'rb') as f:
            file_content = f.read()
       return json.loads(file_content)
    raise ValueError(f'Expected list or str (file path). Unsupported render data type: {type(file)}')
     
     
class PDFClient:
    def __init__(self, api_key: str, base_url: str ="https://data.fastpdfservice.com",
                 api_version: str = "v1"):
        self.api_version = api_version
        self.base_url = "{}/{}".format(base_url, api_version)
        self.api_key = api_key
        self.headers = {'Authorization': self.api_key}
        self.supported_image_formats = [
            'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'svg', 'ico', 'pdf', 
            'psd', 'ai', 'eps', 'cr2', 'nef', 'sr2', 'orf', 'rw2', 'dng', 
            'arw', 'heic'
        ]

    def validate_token(self) -> bool:
      response = requests.get(
             url=f"{self.base_url}/token",
             headers=self.headers
        )
      _raise_for_status(response)
      return response.status_code == 200


    def split(self, file: Union[str, BytesIO, bytes], splits: list[int]) -> bytes:
        files = {'file':_read_file(file)}
        data = {'splits': json.dumps(splits)}
        response = requests.post(
             url=f"{self.base_url}/pdf/split",
             headers=self.headers,
             files=files,
             data=data
        )
        _raise_for_status(response)
        return response.content


    def split_zip(self, file: Union[str, BytesIO, bytes], splits: list[list[int]]) -> bytes:
        files = {'file':_read_file(file)}
        data = {'splits': json.dumps(splits)}
        response = requests.post(
             url=f"{self.base_url}/pdf/split-zip",
             headers=self.headers,
             files=files,
             data=data
        )
        _raise_for_status(response)
        return response.content


    def save(self, content, file_path: str):
        with open(file_path, 'wb') as fd:
            fd.write(content)
        
        
    def edit_metadata(self, file: Union[str, BytesIO, bytes], metadata: dict[str, str]) -> bytes:
        files = {'file':_read_file(file)}
        data = {'metadata': json.dumps(metadata)}
        response = requests.post(
             url=f"{self.base_url}/pdf/metadata",
             headers=self.headers,
             files=files,
             data=data
        )
        _raise_for_status(response)
        return response.content
        
        
    def merge(self, file_paths: list[str]) -> bytes:
        if len(file_paths) < 2:
            raise ValueError('You need at least 2 files in order to merge.')
        if len(file_paths) > 10:
            raise ValueError('You can merge a maximum of 100 files at once.')

        files = {}
        for i, f in enumerate(file_paths):
            files['file'+str(i)] = _read_file(f)
        
        response = requests.post(
            url=f"{self.base_url}/pdf/merge",
            headers=self.headers,
            files=files,
        )
        
        _raise_for_status(response)
        return response.content
        
        
    def to_image(self, file: Union[str, BytesIO, bytes], output_format: str) -> bytes:
        output_format = output_format.lower()
        if output_format.lower() not in self.supported_image_formats:
            raise ValueError(f'Unsupported output format. Must be one of: {self.supported_image_formats}')

        files = {'file':_read_file(file)}
        response = requests.post(
             url=f"{self.base_url}/pdf/image/{output_format}",
             headers=self.headers,
             files=files,
        )
        
        _raise_for_status(response)
        return response.content
        

    def compress(self, file: Union[str, BytesIO, bytes], options:dict=None) -> bytes:
        files = {'file':_read_file(file)}
        data = {'options': json.dumps(options) if options else None} 
        response = requests.post(
             url=f"{self.base_url}/pdf/compress",
             headers=self.headers,
             files=files,
             data=data
        )
        _raise_for_status(response)
        return response.content
        
        
    def url_to_pdf(self, url: str) -> bytes:
        data = {'url':url}
        response = requests.post(
            url=f"{self.base_url}/pdf/url",
            headers=self.headers,
            data=data
        )
        _raise_for_status(response)
        return response.content
        
        
    def render_barcodes(self, data: str, barcode_format: str = 'code128', 
                        render_options: RenderOptions=None) -> bytes:
        barcode_format = barcode_format.lower()
        _available_formats = [
            'codabar', 'code128', 'code39', 'ean', 'ean13', 'ean13-guard',
            'ean14', 'ean8', 'ean8-guard', 'gs1', 'gs1_128', 'gtin', 'isbn',
            'isbn10', 'isbn13', 'issn', 'itf', 'jan', 'nw-7', 'pzn', 'upc',
            'upca'
        ]
        if barcode_format not in _available_formats:
           raise ValueError(f'Invalid barcode type: {barcode_format}')
        
        _render_options_obj = _parse_dataclass(render_options, RenderOptions)
        _data_obj = {'data':data, 'barcode_format': barcode_format}
        
        request_data = {
           "data" : _data_obj, 
           "render_options": _render_options_obj
        }

        response = requests.post(
            url=f"{self.base_url}/render/barcode",
            headers=self.headers,
            json=request_data,
        )
        _raise_for_status(response)
        return response.content
        
        
    def render_image(self, image: Union[str, BytesIO, bytes], render_options: RenderOptions=None) -> bytes:
        _data_obj = {
            "render_options": json.dumps(_parse_dataclass(render_options, RenderOptions))
        }
        _files = {  
            'image': _read_file(image)
        }
        
        response = requests.post(
            url=f"{self.base_url}/render/img",
            headers=self.headers,
            data=_data_obj,
            files=_files
        )
        _raise_for_status(response)
        return response.content
        
        
    def get_all_templates(self) -> list:
        response = requests.get(
            url=f"{self.base_url}/template",
            headers=self.headers,
        )
        _raise_for_status(response)
        return response.json()
        
        
    def add_template(self, file_data: Union[str, BytesIO, bytes], template_data: Template, 
                     header_data: Union[str, BytesIO, bytes] = None,
                     footer_data: Union[str, BytesIO, bytes] = None) -> dict:
        files = {
         'file_data': _read_file(file_data), 
         'header_data': _read_file(header_data) if header_data is not None else None,
         'footer_data': _read_file(footer_data) if footer_data is not None else None
        }
        _data_obj = {
         'template_data': json.dumps(_parse_dataclass(template_data, Template)),
        }
        response = requests.post(
            url=f"{self.base_url}/template",
            headers=self.headers,
            data=_data_obj,
            files=files
        )
        _raise_for_status(response)
        return response.json()
      
      
    def render(self, file_data: Union[str, BytesIO, bytes], template_data: Template = None,
               render_data: Union[dict, str] = {},
               header_data: Union[str, BytesIO, bytes] = None,
               footer_data: Union[str, BytesIO, bytes] = None,
               format_type: str="pdf",
               render_options: RenderOptions=None) -> bytes:
        if template_data is None:
            template_data = Template(name="fastpdf-document", format="html", title_header_enabled=False)
        format_type = format_type.lower()
        _files = {
         'file_data': _read_file(file_data), 
         'header_data': _read_file(header_data) if header_data is not None else None,
         'footer_data': _read_file(footer_data) if footer_data is not None else None
        }
        _data_obj = {
         'template_data': json.dumps(_parse_dataclass(template_data, Template)),
         'render_data': json.dumps(_parse_render_data_obj(render_data)),
         'render_options': json.dumps(_parse_dataclass(render_options, RenderOptions))
        }
        response = requests.post(
            url=f"{self.base_url}/render/{format_type}",
            headers=self.headers,
            data=_data_obj,
            files=_files
        )
        _raise_for_status(response)
        return response.content
        
        
    def render_many(self, file_data: Union[str, BytesIO, bytes], template_data: Template = None,
               render_data: Union[list, str] = [{}],
               header_data: Union[str, BytesIO, bytes] = None,
               footer_data: Union[str, BytesIO, bytes] = None,
               format_type: str="pdf",
               render_options: RenderOptions=None) -> bytes:
        if template_data is None:
            template_data = Template(name="fastpdf-document", format="html", title_header_enabled=False)
        format_type = format_type.lower()
        _files = {
         'file_data': _read_file(file_data), 
         'header_data': _read_file(header_data) if header_data is not None else None,
         'footer_data': _read_file(footer_data) if footer_data is not None else None
        }
        _data_obj = {
         'template_data': json.dumps(_parse_dataclass(template_data, Template)),
         'render_data': json.dumps(_parse_render_data_list(render_data)),
         'render_options': json.dumps(_parse_dataclass(render_options, RenderOptions))
        }
        response = requests.post(
            url=f"{self.base_url}/render/{format_type}/batch",
            headers=self.headers,
            data=_data_obj,
            files=_files
        )
        _raise_for_status(response)
        return response.content
      
        
    def add_stylesheet_to_template(self, template_id: str, 
                                   file_data: Union[str, BytesIO, bytes], 
                                   template_data: StyleFile) -> dict:
        _files = {
            'file_data': _read_file(file_data), 
        }
        _data_obj = {
            'template_data': json.dumps(_parse_dataclass(template_data, StyleFile)),
        }
        response = requests.post(
            url=f"{self.base_url}/template/css/{template_id}",
            headers=self.headers,
            data=_data_obj,
            files=_files
        )
        _raise_for_status(response)
        return response.json()
        
    def add_image_to_template(self, template_id: str, 
                              file_data:  Union[str, BytesIO, bytes], 
                              template_data: ImageFile) -> dict:
        _files = {
            'file_data': _read_file(file_data), 
        }
        _data_obj = {
            'template_data': json.dumps(_parse_dataclass(template_data, ImageFile)),
        }
        response = requests.post(
            url=f"{self.base_url}/template/img/{template_id}",
            headers=self.headers,
            data=_data_obj,
            files=_files
        )
        _raise_for_status(response)
        return response.json()


    def delete_template(self, template_id: str) -> bool:
        response = requests.delete(
            url=f"{self.base_url}/template/{template_id}",
            headers=self.headers,
        )
        _raise_for_status(response)
        return response.status_code == 204
        
        
    def render_template(self, template_id: str, 
                        render_data: Union[dict, str],
                        render_options: RenderOptions=None,
                        format_type: str="pdf") -> bytes:
        format_type = format_type.lower()
        data = {
         'render_data': json.dumps(_parse_render_data_obj(render_data)),
         'render_options':  json.dumps(_parse_dataclass(render_options, RenderOptions))
        }
        response = requests.post(
            url=f"{self.base_url}/render/{format_type}/{template_id}",
            headers=self.headers,
            data=data,
        )
        _raise_for_status(response)
        return response.content
    
    def render_template_many(self, template_id: str, 
                             render_data: Union[list, str],
                             render_options: RenderOptions=None,
                             format_type: str="pdf") -> bytes:
        format_type = format_type.lower()
        data = {
          'render_data': json.dumps(_parse_render_data_list(render_data)),
          'render_options':  json.dumps(_parse_dataclass(render_options, RenderOptions))
        }
        response = requests.post(
            url=f"{self.base_url}/render/{format_type}/batch/{template_id}",
            headers=self.headers,
            data=data,
        )
        _raise_for_status(response)
        return response.content
              
        
    def delete_stylesheet(self, stylesheet_id: str) -> bool:
        response = requests.delete(
            url=f"{self.base_url}/template/css/{stylesheet_id}",
            headers=self.headers
        )
        _raise_for_status(response)
        return response.status_code == 204


    def get_stylesheet(self, stylesheet_id: str) -> bytes:
        response = requests.get(
            url=f"{self.base_url}/css/file/{stylesheet_id}",
            headers=self.headers
        )
        _raise_for_status(response)
        return response.content
        
        
    def delete_image(self, image_id: str) -> bool:
        response = requests.delete(
            url=f"{self.base_url}/template/img/{image_id}",
            headers=self.headers
        )
        _raise_for_status(response)
        return response.status_code == 204


    def get_image(self, image_id: str) -> bytes:
        response = requests.get(
            url=f"{self.base_url}/img/file/{image_id}",
            headers=self.headers
        )
        _raise_for_status(response)
        return response.content
        
        
    # Convenience functions for each format
    def render_template_to_pdf(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, 'pdf')

    def render_template_to_docx(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, 'docx')

    def render_template_to_odp(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, 'odp')

    def render_template_to_ods(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, 'ods')

    def render_template_to_odt(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, 'odt')

    def render_template_to_pptx(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, 'pptx')

    def render_template_to_xlx(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, 'xlx')

    def render_template_to_xls(self, template_id: str, render_data: Union[dict, str]) -> bytes:
        return self.render_template(template_id, render_data, 'xls')
        
        
        
