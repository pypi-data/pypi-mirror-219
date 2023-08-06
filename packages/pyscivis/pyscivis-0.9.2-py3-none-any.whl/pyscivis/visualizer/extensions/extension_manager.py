import logging
import os
from typing import Optional, Tuple, Union, List, Sequence

from pyscivis.visualizer.dataclasses.config import Config
from pyscivis.visualizer.extensions import FlatExtension, NestedExtension

#########################################################################
#                      !!!Enable Extensions here!!!                     #
#                                                                       #
# Import your Extension-Class here and put it into 'enabled_extensions' #
#########################################################################

from .mrd import MRDExtension
from .pil.pil_flat import PILExtensionFlat
from .pil.pil_nested import PILExtensionNested
from .pil.pil_rgba import PILExtensionRGBA

enabled_extensions = [MRDExtension, PILExtensionFlat, PILExtensionNested, PILExtensionRGBA]

#########################################################################
#                                                                       #
#########################################################################

"""
This module includes functions used to validate and use
custom extensions.
"""

logger = logging.getLogger(__name__)


def get_extension_handler(path: Union[str, Sequence[str]],
                          extension_name: Optional[str],
                          config: Config
                          ) -> Union[FlatExtension, NestedExtension]:
    """
    Get the ExtensionHandler for a file.

    Use the extension name to choose an extension, if not specified use the filename-extension, e.g., ".jpg".

    Args:
        path: Path(s) of file(s) to be handled.
        extension_name: Name of extension to be used to handle the file.
        config: Config object.

    Returns:
        An ExtensionHandler (subclassing either FlatExtension or NestedExtension).
    """
    if extension_name is None:
        return get_extension_handler_from_path(path, config)
    else:
        return get_extensions_handler_from_name(extension_name, path, config)


def get_extension_handler_from_path(path: Union[str, Sequence[str]],
                                    config: Config
                                    ) -> Union[FlatExtension, NestedExtension]:
    """
    Get the appropriate ExtensionHandler for the specified file(-path).

    Args:
        path: Path(s) of file(s) to be handled.
        config: Config object.

    Returns:
        An ExtensionHandler (subclassing either FlatExtension or NestedExtension).

    Raises:
        ValueError: If the specified file (first file for Sequences) does not have a file-extension.
        NotImplementedError: If no extensions supports the path's file-extension.
        IndexError: If the file-extension is not unique to an extension, but multiple extensions support it.
    """

    file_ext_name: str
    # use first path for detecting the extension if path is a Sequence of strings
    if not isinstance(path, str):
        _, file_ext_name = os.path.splitext(path[0])
    else:
        _, file_ext_name = os.path.splitext(path)

    if not file_ext_name:
        raise ValueError("Could not find file-extension in path.")

    file_ext_name_no_dot: Optional[str] = None
    if file_ext_name.startswith("."):
        file_ext_name_no_dot = file_ext_name[1:]

    valid_extensions = list()
    for ext in enabled_extensions:
        if file_ext_name in ext.supported_files or file_ext_name_no_dot in ext.supported_files:
            valid_extensions.append(ext)

    if len(valid_extensions) == 1:
        return valid_extensions[0](path, config)
    elif len(valid_extensions) == 0:
        raise NotImplementedError(f"'{file_ext_name}'-files are not currently supported.")
    else:  # len(valid_extensions) > 1
        raise IndexError(f"'{file_ext_name}'-files are supported by multiple extensions.")


def get_extensions_handler_from_name(extension_name: str,
                                     path: Union[str, Sequence[str]],
                                     config: Config
                                     ) -> Union[FlatExtension, NestedExtension]:
    """
    Get the appropriate ExtensionHandler for the specified file(path) using the specified extension.

    Args:
        extension_name: Name of extensions to be used.
        path: Path(s) of file(s) to be handled.
        config: Config object.

    Returns:
        An ExtensionHandler (subclassing either FlatExtension or NestedExtension).

    Raises:
        NotImplementedError: If no extension with the specified name exists.
    """
    for ext in enabled_extensions:
        if ext.alias == extension_name:
            return ext(path, config)
    raise NotImplementedError(f"Extension with name '{extension_name}' does not exist.")


def extension_allows_multiple(extension_name: str) -> bool:
    """
    Check if the specified extension can handle multiple files or not.

    Args:
        extension_name: Name of extension to be checked.

    Returns:
        True if extension can handle multiple files, else False.

    Raises:
        ValueError: If no extension with specified name exists.
    """
    for ext in enabled_extensions:
        if ext.alias == extension_name:
            return ext.multiple
    raise ValueError(f"Extension with name '{extension_name}' does not exist.")


def get_supported_files() -> Tuple[Tuple[str, str, str], ...]:
    """
    Compile the supported file-extensions of all enabled extensions.

    Returns:
        A tuple of (extension-alias, extension-description, extension-filetypes)-tuples.

    Raises:
        TypeError: If an enabled extension did not set 'supported_files' correctly.
    """
    if not enabled_extensions:
        return ("NO-EXTENSION-LOADED", "NO-EXTENSION-LOADED", ".NO-EXTENSION-LOADED"),

    supported_files = list()
    for ext in enabled_extensions:
        if isinstance(ext.supported_files, str):
            file_ext = ext.supported_files if ext.supported_files.startswith((".", "*")) else f".{ext.supported_files}"
            supported_files.append((ext.alias, ext.file_description, file_ext))
        elif isinstance(ext.supported_files, Sequence):
            file_ext_list = [f if f.startswith((".", "*")) else f".{f}" for f in ext.supported_files]
            supported_files.append((ext.alias, ext.file_description, " ".join(file_ext_list)))
        else:
            raise TypeError(f"Extension {ext.__package__} has invalid type for variable 'supported_files. "
                            f"Expected type Union[str, Sequence], got type {type(ext.supported_files)}")

    return tuple(supported_files)


def get_extension_names_and_descriptions() -> Tuple[Tuple[str, str], ...]:
    """
    Get the names of all extensions.

    Returns: (extension-name, extension-description)-Tuple.
    """
    ret: List[Tuple[str, str]] = list()
    for ext in enabled_extensions:
        ret.append((ext.alias, ext.file_description))
    return tuple(ret)


def check_extension_validity() -> None:
    """
    Check that all enabled extensions fulfil basic requirements for extensions to function correctly.

    I.e., it is checked whether the fields 'file_description' and 'supported_files' exist and that the
    ExtensionHandler is a subclass of FlatExtension or NestedExtension.
    All invalid extensions are disabled.

    Returns:
        True if all extensions are valid, else false.
    """
    logger.info(f"Checking enabled extensions {[ext.__name__ for ext in enabled_extensions]} for validity.")

    if not enabled_extensions:
        logger.warning("No extension was enabled. The application will be missing most functionality.")

    errors = dict()
    for ext in enabled_extensions:
        errors[ext] = []

        if isinstance(ext.alias, property):
            errors[ext].append("missing required field 'alias'")
        elif not isinstance(ext.alias, str):
            errors[ext].append("field 'alias' is not string")

        if isinstance(ext.supported_files, property):
            errors[ext].append("missing required field 'supported_files'")
        elif not isinstance(ext.supported_files, (str, tuple)):
            errors[ext].append("field 'supported_files' is not string or tuple")

        if isinstance(ext.file_description, property):
            errors[ext].append("missing required field 'file_description'")
        elif not isinstance(ext.file_description, str):
            errors[ext].append("field 'file_description' is not string")

        if isinstance(ext.multiple, property):
            errors[ext].append("missing required field 'multiple'")
        elif not isinstance(ext.multiple, bool):
            errors[ext].append("field 'multiple' is not boolean")

        if not issubclass(ext, (FlatExtension, NestedExtension)):
            errors[ext].append("Extension does not subclass 'FlatExtension' or 'NestedExtension'")

    if any(errors.values()):
        logger.warning("Not all enabled extensions are configured correctly:")
        for ext, msgs in errors.items():
            if not msgs:
                continue

            logger.warning(f"Extension {ext.__name__} has the following errors and will be disabled: {', '.join(msgs)}.")
            enabled_extensions.remove(ext)
    else:
        logger.info("All Extensions were successfully validated.")
