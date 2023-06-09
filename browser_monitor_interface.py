from abc import ABC, abstractmethod


class ProcessMonitorInterface(ABC):
    @abstractmethod
    def get_process_id(self, process_name):
        pass

    @abstractmethod
    def get_process_handle(self, process_id):
        pass

    @abstractmethod
    def initialize_driver(self):
        pass

    @abstractmethod
    def wait_for_all_handles(self):
        pass

    @abstractmethod
    def get_default_browser_processes(self):
        pass

    @abstractmethod
    def pid_is_running(self, pid):
        pass

