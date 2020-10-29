from ..engine_advanced_settings import EngineAdvancedSettings
from ..engine import Engine
from ..file import File
from ..operation import Operation

from typing import Final, Dict, Type, Union, Sequence, List
import logging

logger = logging.getLogger(__name__)

engines_advanced_settings_map : Final[Dict[Type[Engine], Type[EngineAdvancedSettings]]] = dict()

engines_exported_filetype_map : Final[Dict[Type[Engine], Type[File]]] = dict()

filetypes_supported_operations_map : Final[Dict[Type[File], List[Type[Operation]]]] = dict()


def with_advanced_settings(engine_advanced_settings: Type[EngineAdvancedSettings]):
    ''' Decorator for Engine classes, to be used when some of their
        settings have been delegated to an advanced settings window
        OPTIONAL.'''
    def _with_advanced_settings(cls: Type[Engine]):
        logger.debug(f'with_advanced_settings: {engine_advanced_settings.__name__} -> {cls.__name__}')
        if not issubclass(cls, Engine):
            logger.error(f'with_advanced_settings can only be used to decorate classes that extend Engine')
            return cls
        engines_advanced_settings_map[cls] = engine_advanced_settings
        return cls
    return _with_advanced_settings

# This may need to be changed later, if an engine can record multiple filetypes...
def exported_filetype(filetype: Type[File]):
    '''Decorator for Engine classes that declares which filetype
       it will be looking out for. MANDATORY. Without this decorator,
       the engine cannot be tied to operations.'''
    def _exported_filetype(cls: Type[Engine]):
        logger.debug(f'exported_filetype: {filetype.__name__} -> {cls.__name__}')
        if not issubclass(cls, Engine):
            logger.error(f'exported_filetype can only be used to decorate classes that extend Engine')
            return cls
        engines_exported_filetype_map[cls] = filetype
        return cls
    return _exported_filetype

def supported_filetypes(filetypes: Union[Type[File], Sequence[Type[File]]]):
    '''Decorator for Operation classes that should be used to declare
       which filetype(s) it supports. OPTIONAL. If unused, then the operation
       will be assumed to support regular files only!'''
    def _supported_filetypes(cls: Type[Operation]):
        logger.debug(f'exported_filetype: {filetypes.__name__} -> {cls.__name__}')
        if not issubclass(cls, Operation):
            logger.error(f'supported_filetypes can only be used to decorate classes that extend Operation')
            return cls
        if issubclass(filetypes, File):
            filetypes = [filetypes]
        for filetype in filetypes:
            if filetype in filetypes_supported_operations_map:
                filetypes_supported_operations_map[filetype].append(cls)
            else:
                filetypes_supported_operations_map[filetype] = list(cls)
        return cls
    return _supported_filetypes
    