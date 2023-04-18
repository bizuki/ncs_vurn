import inspect
import pkgutil
import importlib
import sys
from types import ModuleType
from loguru import logger
from dataclasses import dataclass
from typing import List, Optional
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer


@dataclass
class _ChildModuleSpec:
    name: str
    module: ModuleType
    submodules: List[ModuleType]
    router: Optional[APIRouter]


def _get_all_submodules(base_name: str, module: ModuleType):
    res: List[ModuleType] = []
    for m in pkgutil.walk_packages(path=module.__path__, prefix=f'{base_name}.'):
        if m.ispkg:
            continue
        res.append(importlib.import_module(m.name, package='src'))
    return res

# NOTE: is not gonna work if the 'routes' module is a package, instead of a single-file module
def _get_router(submodules: List[ModuleType]):
    module = None
    for m in submodules:
        if m.__name__.endswith('routes'):
            module = m
    
    if not module:
        return None

    members = inspect.getmembers(module)
    for name, obj in members:
        if name == 'router' and isinstance(obj, APIRouter):
            return obj
    
    return None


class ApplicationAutoConfig:
    def __init__(self, module: str):
        try:
            self._parent_module_name = module
            self._parent_module = importlib.import_module(module, package='src')
        except ModuleNotFoundError:
            logger.error(f'Parent module for the application functionality {module} could not be found')
            sys.exit(1)
        
        self._process_children()

    def _process_children(self):
        self._children_modules: List[_ChildModuleSpec] = []

        for child in pkgutil.iter_modules(self._parent_module.__path__):
            mname = f'{self._parent_module_name}.{child.name}'
            m = importlib.import_module(mname, package='src')
            sub = _get_all_submodules(mname, m)
            router = _get_router(sub)
            self._children_modules.append(_ChildModuleSpec(mname, m, sub, router))

    def wire_submodules(self, container: DeclarativeContainer):
        for m in self._children_modules:
            container.wire(modules=m.submodules)

    def get_routers(self):
        return [m.router for m in self._children_modules if m.router is not None]
