# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mercurial-changeset.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from . import lint_pb2 as lint__pb2
from . import shared_pb2 as shared__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mercurial-changeset.proto',
  package='hgitaly',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x19mercurial-changeset.proto\x12\x07hgitaly\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\nlint.proto\x1a\x0cshared.proto\"\xc3\x01\n\x12MercurialChangeset\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nparent_ids\x18\x02 \x03(\t\x12\r\n\x05title\x18\x03 \x01(\x0c\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\x0c\x12\x0e\n\x06\x61uthor\x18\x05 \x01(\x0c\x12(\n\x04\x64\x61te\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06\x62ranch\x18\x07 \x01(\x0c\x12\r\n\x05topic\x18\x08 \x01(\x0c\x12\x10\n\x08obsolete\x18\t \x01(\x08\"\xc0\x01\n\x1eListMercurialChangesetsRequest\x12,\n\nrepository\x18\x01 \x01(\x0b\x32\x12.gitaly.RepositoryB\x04\x98\xc6,\x01\x12.\n\x04view\x18\x02 \x01(\x0e\x32 .hgitaly.MercurialRepositoryView\x12\x0e\n\x06revset\x18\x03 \x01(\x0c\x12\x30\n\x06\x66ields\x18\x04 \x03(\x0e\x32 .hgitaly.MercurialChangesetField\"R\n\x1fListMercurialChangesetsResponse\x12/\n\nchangesets\x18\x01 \x03(\x0b\x32\x1b.hgitaly.MercurialChangeset*\x89\x01\n\x17MercurialChangesetField\x12\x07\n\x03\x41LL\x10\x00\x12\x0e\n\nPARENT_IDS\x10\x01\x12\t\n\x05TITLE\x10\x02\x12\x0f\n\x0b\x44\x45SCRIPTION\x10\x03\x12\n\n\x06\x41UTHOR\x10\x04\x12\x08\n\x04\x44\x41TE\x10\x05\x12\n\n\x06\x42RANCH\x10\x06\x12\t\n\x05TOPIC\x10\x07\x12\x0c\n\x08OBSOLETE\x10\x08*6\n\x17MercurialRepositoryView\x12\x0b\n\x07VISIBLE\x10\x00\x12\x0e\n\nUNFILTERED\x10\x01\x32\x93\x01\n\x19MercurialChangesetService\x12v\n\x17ListMercurialChangesets\x12\'.hgitaly.ListMercurialChangesetsRequest\x1a(.hgitaly.ListMercurialChangesetsResponse\"\x06\xfa\x97(\x02\x08\x02\x30\x01\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,lint__pb2.DESCRIPTOR,shared__pb2.DESCRIPTOR,])

_MERCURIALCHANGESETFIELD = _descriptor.EnumDescriptor(
  name='MercurialChangesetField',
  full_name='hgitaly.MercurialChangesetField',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ALL', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PARENT_IDS', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TITLE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DESCRIPTION', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='AUTHOR', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATE', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BRANCH', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TOPIC', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OBSOLETE', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=575,
  serialized_end=712,
)
_sym_db.RegisterEnumDescriptor(_MERCURIALCHANGESETFIELD)

MercurialChangesetField = enum_type_wrapper.EnumTypeWrapper(_MERCURIALCHANGESETFIELD)
_MERCURIALREPOSITORYVIEW = _descriptor.EnumDescriptor(
  name='MercurialRepositoryView',
  full_name='hgitaly.MercurialRepositoryView',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='VISIBLE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNFILTERED', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=714,
  serialized_end=768,
)
_sym_db.RegisterEnumDescriptor(_MERCURIALREPOSITORYVIEW)

MercurialRepositoryView = enum_type_wrapper.EnumTypeWrapper(_MERCURIALREPOSITORYVIEW)
ALL = 0
PARENT_IDS = 1
TITLE = 2
DESCRIPTION = 3
AUTHOR = 4
DATE = 5
BRANCH = 6
TOPIC = 7
OBSOLETE = 8
VISIBLE = 0
UNFILTERED = 1



_MERCURIALCHANGESET = _descriptor.Descriptor(
  name='MercurialChangeset',
  full_name='hgitaly.MercurialChangeset',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='hgitaly.MercurialChangeset.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='parent_ids', full_name='hgitaly.MercurialChangeset.parent_ids', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='title', full_name='hgitaly.MercurialChangeset.title', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='hgitaly.MercurialChangeset.description', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author', full_name='hgitaly.MercurialChangeset.author', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='date', full_name='hgitaly.MercurialChangeset.date', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='branch', full_name='hgitaly.MercurialChangeset.branch', index=6,
      number=7, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='topic', full_name='hgitaly.MercurialChangeset.topic', index=7,
      number=8, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='obsolete', full_name='hgitaly.MercurialChangeset.obsolete', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=98,
  serialized_end=293,
)


_LISTMERCURIALCHANGESETSREQUEST = _descriptor.Descriptor(
  name='ListMercurialChangesetsRequest',
  full_name='hgitaly.ListMercurialChangesetsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='repository', full_name='hgitaly.ListMercurialChangesetsRequest.repository', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\230\306,\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='view', full_name='hgitaly.ListMercurialChangesetsRequest.view', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='revset', full_name='hgitaly.ListMercurialChangesetsRequest.revset', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fields', full_name='hgitaly.ListMercurialChangesetsRequest.fields', index=3,
      number=4, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=296,
  serialized_end=488,
)


_LISTMERCURIALCHANGESETSRESPONSE = _descriptor.Descriptor(
  name='ListMercurialChangesetsResponse',
  full_name='hgitaly.ListMercurialChangesetsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='changesets', full_name='hgitaly.ListMercurialChangesetsResponse.changesets', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=490,
  serialized_end=572,
)

_MERCURIALCHANGESET.fields_by_name['date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_LISTMERCURIALCHANGESETSREQUEST.fields_by_name['repository'].message_type = shared__pb2._REPOSITORY
_LISTMERCURIALCHANGESETSREQUEST.fields_by_name['view'].enum_type = _MERCURIALREPOSITORYVIEW
_LISTMERCURIALCHANGESETSREQUEST.fields_by_name['fields'].enum_type = _MERCURIALCHANGESETFIELD
_LISTMERCURIALCHANGESETSRESPONSE.fields_by_name['changesets'].message_type = _MERCURIALCHANGESET
DESCRIPTOR.message_types_by_name['MercurialChangeset'] = _MERCURIALCHANGESET
DESCRIPTOR.message_types_by_name['ListMercurialChangesetsRequest'] = _LISTMERCURIALCHANGESETSREQUEST
DESCRIPTOR.message_types_by_name['ListMercurialChangesetsResponse'] = _LISTMERCURIALCHANGESETSRESPONSE
DESCRIPTOR.enum_types_by_name['MercurialChangesetField'] = _MERCURIALCHANGESETFIELD
DESCRIPTOR.enum_types_by_name['MercurialRepositoryView'] = _MERCURIALREPOSITORYVIEW
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MercurialChangeset = _reflection.GeneratedProtocolMessageType('MercurialChangeset', (_message.Message,), {
  'DESCRIPTOR' : _MERCURIALCHANGESET,
  '__module__' : 'mercurial_changeset_pb2'
  # @@protoc_insertion_point(class_scope:hgitaly.MercurialChangeset)
  })
_sym_db.RegisterMessage(MercurialChangeset)

ListMercurialChangesetsRequest = _reflection.GeneratedProtocolMessageType('ListMercurialChangesetsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTMERCURIALCHANGESETSREQUEST,
  '__module__' : 'mercurial_changeset_pb2'
  # @@protoc_insertion_point(class_scope:hgitaly.ListMercurialChangesetsRequest)
  })
_sym_db.RegisterMessage(ListMercurialChangesetsRequest)

ListMercurialChangesetsResponse = _reflection.GeneratedProtocolMessageType('ListMercurialChangesetsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTMERCURIALCHANGESETSRESPONSE,
  '__module__' : 'mercurial_changeset_pb2'
  # @@protoc_insertion_point(class_scope:hgitaly.ListMercurialChangesetsResponse)
  })
_sym_db.RegisterMessage(ListMercurialChangesetsResponse)


_LISTMERCURIALCHANGESETSREQUEST.fields_by_name['repository']._options = None

_MERCURIALCHANGESETSERVICE = _descriptor.ServiceDescriptor(
  name='MercurialChangesetService',
  full_name='hgitaly.MercurialChangesetService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=771,
  serialized_end=918,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListMercurialChangesets',
    full_name='hgitaly.MercurialChangesetService.ListMercurialChangesets',
    index=0,
    containing_service=None,
    input_type=_LISTMERCURIALCHANGESETSREQUEST,
    output_type=_LISTMERCURIALCHANGESETSRESPONSE,
    serialized_options=b'\372\227(\002\010\002',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MERCURIALCHANGESETSERVICE)

DESCRIPTOR.services_by_name['MercurialChangesetService'] = _MERCURIALCHANGESETSERVICE

# @@protoc_insertion_point(module_scope)
