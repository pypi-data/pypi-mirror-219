# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: wcf.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\twcf.proto\x12\x03wcf\"\xc8\x02\n\x07Request\x12\x1c\n\x04\x66unc\x18\x01 \x01(\x0e\x32\x0e.wcf.Functions\x12\x1b\n\x05\x65mpty\x18\x02 \x01(\x0b\x32\n.wcf.EmptyH\x00\x12\r\n\x03str\x18\x03 \x01(\tH\x00\x12\x1b\n\x03txt\x18\x04 \x01(\x0b\x32\x0c.wcf.TextMsgH\x00\x12\x1c\n\x04\x66ile\x18\x05 \x01(\x0b\x32\x0c.wcf.PathMsgH\x00\x12\x1d\n\x05query\x18\x06 \x01(\x0b\x32\x0c.wcf.DbQueryH\x00\x12\x1e\n\x01v\x18\x07 \x01(\x0b\x32\x11.wcf.VerificationH\x00\x12\x1c\n\x01m\x18\x08 \x01(\x0b\x32\x0f.wcf.AddMembersH\x00\x12\x1a\n\x03xml\x18\t \x01(\x0b\x32\x0b.wcf.XmlMsgH\x00\x12\x1b\n\x03\x64\x65\x63\x18\n \x01(\x0b\x32\x0c.wcf.DecPathH\x00\x12\x1b\n\x02tf\x18\x0b \x01(\x0b\x32\r.wcf.TransferH\x00\x42\x05\n\x03msg\"\xab\x02\n\x08Response\x12\x1c\n\x04\x66unc\x18\x01 \x01(\x0e\x32\x0e.wcf.Functions\x12\x10\n\x06status\x18\x02 \x01(\x05H\x00\x12\r\n\x03str\x18\x03 \x01(\tH\x00\x12\x1b\n\x05wxmsg\x18\x04 \x01(\x0b\x32\n.wcf.WxMsgH\x00\x12\x1e\n\x05types\x18\x05 \x01(\x0b\x32\r.wcf.MsgTypesH\x00\x12$\n\x08\x63ontacts\x18\x06 \x01(\x0b\x32\x10.wcf.RpcContactsH\x00\x12\x1b\n\x03\x64\x62s\x18\x07 \x01(\x0b\x32\x0c.wcf.DbNamesH\x00\x12\x1f\n\x06tables\x18\x08 \x01(\x0b\x32\r.wcf.DbTablesH\x00\x12\x1b\n\x04rows\x18\t \x01(\x0b\x32\x0b.wcf.DbRowsH\x00\x12\x1b\n\x02ui\x18\n \x01(\x0b\x32\r.wcf.UserInfoH\x00\x42\x05\n\x03msg\"\x07\n\x05\x45mpty\"\xa0\x01\n\x05WxMsg\x12\x0f\n\x07is_self\x18\x01 \x01(\x08\x12\x10\n\x08is_group\x18\x02 \x01(\x08\x12\x0c\n\x04type\x18\x03 \x01(\x05\x12\n\n\x02id\x18\x04 \x01(\t\x12\x0b\n\x03xml\x18\x05 \x01(\t\x12\x0e\n\x06sender\x18\x06 \x01(\t\x12\x0e\n\x06roomid\x18\x07 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x08 \x01(\t\x12\r\n\x05thumb\x18\t \x01(\t\x12\r\n\x05\x65xtra\x18\n \x01(\t\"7\n\x07TextMsg\x12\x0b\n\x03msg\x18\x01 \x01(\t\x12\x10\n\x08receiver\x18\x02 \x01(\t\x12\r\n\x05\x61ters\x18\x03 \x01(\t\")\n\x07PathMsg\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x10\n\x08receiver\x18\x02 \x01(\t\"G\n\x06XmlMsg\x12\x10\n\x08receiver\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\x12\x0c\n\x04path\x18\x03 \x01(\t\x12\x0c\n\x04type\x18\x04 \x01(\x05\"a\n\x08MsgTypes\x12\'\n\x05types\x18\x01 \x03(\x0b\x32\x18.wcf.MsgTypes.TypesEntry\x1a,\n\nTypesEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x87\x01\n\nRpcContact\x12\x0c\n\x04wxid\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0e\n\x06remark\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x05 \x01(\t\x12\x10\n\x08province\x18\x06 \x01(\t\x12\x0c\n\x04\x63ity\x18\x07 \x01(\t\x12\x0e\n\x06gender\x18\x08 \x01(\x05\"0\n\x0bRpcContacts\x12!\n\x08\x63ontacts\x18\x01 \x03(\x0b\x32\x0f.wcf.RpcContact\"\x18\n\x07\x44\x62Names\x12\r\n\x05names\x18\x01 \x03(\t\"$\n\x07\x44\x62Table\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03sql\x18\x02 \x01(\t\"(\n\x08\x44\x62Tables\x12\x1c\n\x06tables\x18\x01 \x03(\x0b\x32\x0c.wcf.DbTable\"\"\n\x07\x44\x62Query\x12\n\n\x02\x64\x62\x18\x01 \x01(\t\x12\x0b\n\x03sql\x18\x02 \x01(\t\"8\n\x07\x44\x62\x46ield\x12\x0c\n\x04type\x18\x01 \x01(\x05\x12\x0e\n\x06\x63olumn\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\x0c\"%\n\x05\x44\x62Row\x12\x1c\n\x06\x66ields\x18\x01 \x03(\x0b\x32\x0c.wcf.DbField\"\"\n\x06\x44\x62Rows\x12\x18\n\x04rows\x18\x01 \x03(\x0b\x32\n.wcf.DbRow\"5\n\x0cVerification\x12\n\n\x02v3\x18\x01 \x01(\t\x12\n\n\x02v4\x18\x02 \x01(\t\x12\r\n\x05scene\x18\x03 \x01(\x05\"+\n\nAddMembers\x12\x0e\n\x06roomid\x18\x01 \x01(\t\x12\r\n\x05wxids\x18\x02 \x01(\t\"D\n\x08UserInfo\x12\x0c\n\x04wxid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06mobile\x18\x03 \x01(\t\x12\x0c\n\x04home\x18\x04 \x01(\t\"#\n\x07\x44\x65\x63Path\x12\x0b\n\x03src\x18\x01 \x01(\t\x12\x0b\n\x03\x64st\x18\x02 \x01(\t\"4\n\x08Transfer\x12\x0c\n\x04wxid\x18\x01 \x01(\t\x12\x0c\n\x04tfid\x18\x02 \x01(\t\x12\x0c\n\x04taid\x18\x03 \x01(\t*\xee\x03\n\tFunctions\x12\x11\n\rFUNC_RESERVED\x10\x00\x12\x11\n\rFUNC_IS_LOGIN\x10\x01\x12\x16\n\x12\x46UNC_GET_SELF_WXID\x10\x10\x12\x16\n\x12\x46UNC_GET_MSG_TYPES\x10\x11\x12\x15\n\x11\x46UNC_GET_CONTACTS\x10\x12\x12\x15\n\x11\x46UNC_GET_DB_NAMES\x10\x13\x12\x16\n\x12\x46UNC_GET_DB_TABLES\x10\x14\x12\x16\n\x12\x46UNC_GET_USER_INFO\x10\x15\x12\x11\n\rFUNC_SEND_TXT\x10 \x12\x11\n\rFUNC_SEND_IMG\x10!\x12\x12\n\x0e\x46UNC_SEND_FILE\x10\"\x12\x11\n\rFUNC_SEND_XML\x10#\x12\x15\n\x11\x46UNC_SEND_EMOTION\x10$\x12\x18\n\x14\x46UNC_ENABLE_RECV_TXT\x10\x30\x12\x19\n\x15\x46UNC_DISABLE_RECV_TXT\x10@\x12\x16\n\x12\x46UNC_EXEC_DB_QUERY\x10P\x12\x16\n\x12\x46UNC_ACCEPT_FRIEND\x10Q\x12\x16\n\x12\x46UNC_RECV_TRANSFER\x10R\x12\x16\n\x12\x46UNC_DECRYPT_IMAGE\x10`\x12\x19\n\x15\x46UNC_ADD_ROOM_MEMBERS\x10p\x12\x19\n\x15\x46UNC_DEL_ROOM_MEMBERS\x10qB\r\n\x0b\x63om.iamteerb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'wcf_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\013com.iamteer'
  _MSGTYPES_TYPESENTRY._options = None
  _MSGTYPES_TYPESENTRY._serialized_options = b'8\001'
  _FUNCTIONS._serialized_start=1820
  _FUNCTIONS._serialized_end=2314
  _REQUEST._serialized_start=19
  _REQUEST._serialized_end=347
  _RESPONSE._serialized_start=350
  _RESPONSE._serialized_end=649
  _EMPTY._serialized_start=651
  _EMPTY._serialized_end=658
  _WXMSG._serialized_start=661
  _WXMSG._serialized_end=821
  _TEXTMSG._serialized_start=823
  _TEXTMSG._serialized_end=878
  _PATHMSG._serialized_start=880
  _PATHMSG._serialized_end=921
  _XMLMSG._serialized_start=923
  _XMLMSG._serialized_end=994
  _MSGTYPES._serialized_start=996
  _MSGTYPES._serialized_end=1093
  _MSGTYPES_TYPESENTRY._serialized_start=1049
  _MSGTYPES_TYPESENTRY._serialized_end=1093
  _RPCCONTACT._serialized_start=1096
  _RPCCONTACT._serialized_end=1231
  _RPCCONTACTS._serialized_start=1233
  _RPCCONTACTS._serialized_end=1281
  _DBNAMES._serialized_start=1283
  _DBNAMES._serialized_end=1307
  _DBTABLE._serialized_start=1309
  _DBTABLE._serialized_end=1345
  _DBTABLES._serialized_start=1347
  _DBTABLES._serialized_end=1387
  _DBQUERY._serialized_start=1389
  _DBQUERY._serialized_end=1423
  _DBFIELD._serialized_start=1425
  _DBFIELD._serialized_end=1481
  _DBROW._serialized_start=1483
  _DBROW._serialized_end=1520
  _DBROWS._serialized_start=1522
  _DBROWS._serialized_end=1556
  _VERIFICATION._serialized_start=1558
  _VERIFICATION._serialized_end=1611
  _ADDMEMBERS._serialized_start=1613
  _ADDMEMBERS._serialized_end=1656
  _USERINFO._serialized_start=1658
  _USERINFO._serialized_end=1726
  _DECPATH._serialized_start=1728
  _DECPATH._serialized_end=1763
  _TRANSFER._serialized_start=1765
  _TRANSFER._serialized_end=1817
# @@protoc_insertion_point(module_scope)
