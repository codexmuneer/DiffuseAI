# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: text2img.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'text2img.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0etext2img.proto\x12\x08text2img\"A\n\x11GenerationRequest\x12\x0e\n\x06prompt\x18\x01 \x01(\t\x12\x12\n\x05style\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x08\n\x06_style\"z\n\x12GenerationResponse\x12\x14\n\nchunk_data\x18\x01 \x01(\x0cH\x00\x12 \n\x05\x65rror\x18\x02 \x01(\x0b\x32\x0f.text2img.ErrorH\x00\x12\x10\n\x08progress\x18\x03 \x01(\x05\x12\x10\n\x08is_final\x18\x04 \x01(\x08\x42\x08\n\x06result\"F\n\x18PromptEnhancementRequest\x12\x0e\n\x06prompt\x18\x01 \x01(\t\x12\x1a\n\x12use_ai_enhancement\x18\x02 \x01(\x08\"4\n\x19PromptEnhancementResponse\x12\x17\n\x0f\x65nhanced_prompt\x18\x01 \x01(\t\"=\n\x12ImageFilterRequest\x12\x12\n\nimage_data\x18\x01 \x01(\x0c\x12\x13\n\x0b\x66ilter_name\x18\x02 \x01(\t\"-\n\x13ImageFilterResponse\x12\x16\n\x0e\x66iltered_image\x18\x01 \x01(\x0c\".\n\x18\x43\x61ptionGenerationRequest\x12\x12\n\nimage_data\x18\x01 \x01(\x0c\",\n\x19\x43\x61ptionGenerationResponse\x12\x0f\n\x07\x63\x61ption\x18\x01 \x01(\t\"&\n\x05\x45rror\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\x32\xe0\x02\n\x0bTextToImage\x12I\n\x08Generate\x12\x1b.text2img.GenerationRequest\x1a\x1c.text2img.GenerationResponse\"\x00\x30\x01\x12Z\n\rEnhancePrompt\x12\".text2img.PromptEnhancementRequest\x1a#.text2img.PromptEnhancementResponse\"\x00\x12L\n\x0b\x41pplyFilter\x12\x1c.text2img.ImageFilterRequest\x1a\x1d.text2img.ImageFilterResponse\"\x00\x12\\\n\x0fGenerateCaption\x12\".text2img.CaptionGenerationRequest\x1a#.text2img.CaptionGenerationResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'text2img_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_GENERATIONREQUEST']._serialized_start=28
  _globals['_GENERATIONREQUEST']._serialized_end=93
  _globals['_GENERATIONRESPONSE']._serialized_start=95
  _globals['_GENERATIONRESPONSE']._serialized_end=217
  _globals['_PROMPTENHANCEMENTREQUEST']._serialized_start=219
  _globals['_PROMPTENHANCEMENTREQUEST']._serialized_end=289
  _globals['_PROMPTENHANCEMENTRESPONSE']._serialized_start=291
  _globals['_PROMPTENHANCEMENTRESPONSE']._serialized_end=343
  _globals['_IMAGEFILTERREQUEST']._serialized_start=345
  _globals['_IMAGEFILTERREQUEST']._serialized_end=406
  _globals['_IMAGEFILTERRESPONSE']._serialized_start=408
  _globals['_IMAGEFILTERRESPONSE']._serialized_end=453
  _globals['_CAPTIONGENERATIONREQUEST']._serialized_start=455
  _globals['_CAPTIONGENERATIONREQUEST']._serialized_end=501
  _globals['_CAPTIONGENERATIONRESPONSE']._serialized_start=503
  _globals['_CAPTIONGENERATIONRESPONSE']._serialized_end=547
  _globals['_ERROR']._serialized_start=549
  _globals['_ERROR']._serialized_end=587
  _globals['_TEXTTOIMAGE']._serialized_start=590
  _globals['_TEXTTOIMAGE']._serialized_end=942
# @@protoc_insertion_point(module_scope)
