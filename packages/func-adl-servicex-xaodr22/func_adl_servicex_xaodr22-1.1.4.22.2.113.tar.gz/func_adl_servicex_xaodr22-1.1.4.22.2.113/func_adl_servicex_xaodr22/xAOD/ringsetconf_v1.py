from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr22

_method_map = {
    'nRings': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'nRings',
        'return_type': 'unsigned int',
    },
    'nLayers': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'nLayers',
        'return_type': 'unsigned int',
    },
    'etaWidth': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'etaWidth',
        'return_type': 'float',
    },
    'phiWidth': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'phiWidth',
        'return_type': 'float',
    },
    'cellMaxDEtaDist': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'cellMaxDEtaDist',
        'return_type': 'float',
    },
    'cellMaxDPhiDist': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'cellMaxDPhiDist',
        'return_type': 'float',
    },
    'doEtaAxesDivision': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'doEtaAxesDivision',
        'return_type': 'bool',
    },
    'doPhiAxesDivision': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'doPhiAxesDivision',
        'return_type': 'bool',
    },
    'layerStartIdx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'layerStartIdx',
        'return_type': 'unsigned int',
    },
    'sectionStartIdx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'sectionStartIdx',
        'return_type': 'unsigned int',
    },
    'layerEndIdx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'layerEndIdx',
        'return_type': 'unsigned int',
    },
    'sectionEndIdx': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'sectionEndIdx',
        'return_type': 'unsigned int',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'trackIndices': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'trackIndices',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::RingSetConf_v1',
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
            'name': 'xAODCaloRings/versions/RingSetConf_v1.h',
            'body_includes': ["xAODCaloRings/versions/RingSetConf_v1.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class RingSetConf_v1:
    "A class"

    def nRings(self) -> int:
        "A method"
        ...

    def nLayers(self) -> int:
        "A method"
        ...

    def etaWidth(self) -> float:
        "A method"
        ...

    def phiWidth(self) -> float:
        "A method"
        ...

    def cellMaxDEtaDist(self) -> float:
        "A method"
        ...

    def cellMaxDPhiDist(self) -> float:
        "A method"
        ...

    def doEtaAxesDivision(self) -> bool:
        "A method"
        ...

    def doPhiAxesDivision(self) -> bool:
        "A method"
        ...

    def layerStartIdx(self) -> int:
        "A method"
        ...

    def sectionStartIdx(self) -> int:
        "A method"
        ...

    def layerEndIdx(self) -> int:
        "A method"
        ...

    def sectionEndIdx(self) -> int:
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
