# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: suggestions.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11suggestions.proto\x12\x0bsuggestions\"C\n\x0cOrderRequest\x12\x11\n\tuser_name\x18\x01 \x01(\t\x12 \n\x05items\x18\x02 \x03(\x0b\x32\x11.suggestions.Item\"&\n\x04Item\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"6\n\x04\x42ook\x12\x0f\n\x07\x62ook_id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\";\n\rOrderResponse\x12*\n\x0fsuggested_books\x18\x01 \x03(\x0b\x32\x11.suggestions.Book2X\n\x0bSuggestions\x12I\n\x0eGetSuggestions\x12\x19.suggestions.OrderRequest\x1a\x1a.suggestions.OrderResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'suggestions_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ORDERREQUEST']._serialized_start=34
  _globals['_ORDERREQUEST']._serialized_end=101
  _globals['_ITEM']._serialized_start=103
  _globals['_ITEM']._serialized_end=141
  _globals['_BOOK']._serialized_start=143
  _globals['_BOOK']._serialized_end=197
  _globals['_ORDERRESPONSE']._serialized_start=199
  _globals['_ORDERRESPONSE']._serialized_end=258
  _globals['_SUGGESTIONS']._serialized_start=260
  _globals['_SUGGESTIONS']._serialized_end=348
# @@protoc_insertion_point(module_scope)