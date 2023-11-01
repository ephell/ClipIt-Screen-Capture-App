from win32event import CreateMutex
from win32api import CloseHandle, GetLastError
from winerror import ERROR_ALREADY_EXISTS


class SingleInstanceChecker:

    def __init__(self):
        self.__mutex_name = "ClipIt_App_Instance_Mutex"
        self.__mutex = CreateMutex(None, False, self.__mutex_name)
        self.__lasterror = GetLastError()
    
    def __del__(self):
        if self.__mutex:
            CloseHandle(self.__mutex)

    def is_another_instance_already_running(self):
        return self.__lasterror == ERROR_ALREADY_EXISTS
