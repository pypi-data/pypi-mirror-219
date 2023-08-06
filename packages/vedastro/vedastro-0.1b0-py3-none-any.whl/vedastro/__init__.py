import os
from pythonnet import load


def _initialize_library():
    """
    Initialize the library by loading the necessary DLL and setting up the runtime configuration.
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(current_path, 'dlls', 'VedAstro.Library.dll')
    full_path = os.path.abspath(dll_path)

    runtime_config_path = os.path.abspath(os.path.join(current_path, 'runtimeconfig.json'))

    load("coreclr", runtime_config=runtime_config_path)
    import clr
    clr.AddReference(full_path)


# Call the function to initialize the library
_initialize_library()
