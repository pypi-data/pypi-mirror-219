from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr22

_method_map = {
    'name': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'name',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'const string',
    },
    'removeObjectLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'removeObjectLink',
        'return_type': 'bool',
    },
    'removeObjectCollectionLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'removeObjectCollectionLinks',
        'return_type': 'bool',
    },
    'copyLinkFrom': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'copyLinkFrom',
        'return_type': 'bool',
    },
    'copyLinkCollectionFrom': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'copyLinkCollectionFrom',
        'return_type': 'bool',
    },
    'copyAllLinksFrom': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'copyAllLinksFrom',
        'return_type': 'bool',
    },
    'linkColNames': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'linkColNames',
        'return_type_element': 'string',
        'return_type_collection': 'const vector<string>',
    },
    'isRemapped': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'isRemapped',
        'return_type': 'bool',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'trackIndices': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'trackIndices',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TrigComposite_v1',
        'method_name': 'isAvailable',
        'return_type': 'bool',
    },
}


T = TypeVar('T')


def _add_method_metadata(s: ObjectStream[T], a: ast.Call) -> Tuple[ObjectStream[T], ast.Call]:
    '''Add metadata for a collection to the func_adl stream if we know about it
    '''
    assert isinstance(a.func, ast.Attribute)
    if a.func.attr in _method_map:
        s_update = s.MetaData(_method_map[a.func.attr])
        s_update = s_update.MetaData({
            'metadata_type': 'inject_code',
            'name': 'xAODTrigger/versions/TrigComposite_v1.h',
            'body_includes': ["xAODTrigger/versions/TrigComposite_v1.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class TrigComposite_v1:
    "A class"

    def name(self) -> func_adl_servicex_xaodr22.str.str:
        "A method"
        ...

    def removeObjectLink(self, name: str) -> bool:
        "A method"
        ...

    def removeObjectCollectionLinks(self, name: str) -> bool:
        "A method"
        ...

    def copyLinkFrom(self, other: TrigComposite_v1, name: str, newName: str) -> bool:
        "A method"
        ...

    def copyLinkCollectionFrom(self, other: TrigComposite_v1, name: str, newName: str) -> bool:
        "A method"
        ...

    def copyAllLinksFrom(self, other: TrigComposite_v1) -> bool:
        "A method"
        ...

    def linkColNames(self) -> func_adl_servicex_xaodr22.vector_str_.vector_str_:
        "A method"
        ...

    def isRemapped(self) -> bool:
        "A method"
        ...

    def index(self) -> int:
        "A method"
        ...

    def usingPrivateStore(self) -> bool:
        "A method"
        ...

    def usingStandaloneStore(self) -> bool:
        "A method"
        ...

    def hasStore(self) -> bool:
        "A method"
        ...

    def hasNonConstStore(self) -> bool:
        "A method"
        ...

    def clearDecorations(self) -> bool:
        "A method"
        ...

    def trackIndices(self) -> bool:
        "A method"
        ...

    @func_adl_parameterized_call(lambda s, a, param_1: func_adl_servicex_xaodr22.type_support.cpp_generic_1arg_callback('auxdataConst', s, a, param_1))
    @property
    def auxdataConst(self) -> func_adl_servicex_xaodr22.type_support.index_type_forwarder[str]:
        "A method"
        ...

    @func_adl_parameterized_call(lambda s, a, param_1: func_adl_servicex_xaodr22.type_support.cpp_generic_1arg_callback('isAvailable', s, a, param_1))
    @property
    def isAvailable(self) -> func_adl_servicex_xaodr22.type_support.index_type_forwarder[str]:
        "A method"
        ...
