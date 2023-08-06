from LoggerLocalPythonPackage.MessageSeverity import MessageSeverity
from LoggerLocalPythonPackage.Writer import Writer
import os
debug = os.getenv("debug")

class LoggerService:

    

    def __init__(self):
        self._writer = Writer()
        self.component_id = 0

    def init(self,component_id,*args, **kwargs):
        self.component_id=component_id
        if debug: print('LoggerService.init(args='+args+' kwargs='+kwargs )
        if args:
            self._writer.add_message(args[0], MessageSeverity.Init.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Init.value
                kwargs['object']['component_id'] = self.component_id
                self._writer.add(**kwargs)

    def start(self, *args, **kwargs):
        if debug: print('LoggerService.start(args='+args+' kwargs='+kwargs )
        if args:
            self._writer.add_message(args[0], MessageSeverity.Start.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Start.value
                kwargs['object']['component_id'] = self.component_id
                self._writer.add(**kwargs)

    def end(self, *args, **kwargs):
        if args:
            self._writer.add_message(args[0], MessageSeverity.End.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.End.value
                kwargs['object']['component_id'] = self.component_id
                self._writer.add(**kwargs)

    def exception(self, *args, **kwargs):
        if args:
            self._writer.add_message(args[0], MessageSeverity.Exception.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Exception.value
                kwargs['object']['component_id'] = self.component_id
                self._writer.add(**kwargs)

    def info(self, *args, **kwargs):
        if args:
            self._writer.add_message(args[0], MessageSeverity.Information.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Information.value
                self._writer.add(**kwargs)

    def error(self, *args, **kwargs):
        if args:
            self._writer.add_message(args[0], MessageSeverity.Error.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Error.value
                kwargs['object']['component_id'] = self.component_id
                self._writer.add(**kwargs)

    def warn(self, *args, **kwargs):
        if args:
            self._writer.add_message(args[0], MessageSeverity.Warning.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Warning.value
                kwargs['object']['component_id'] = self.component_id
                self._writer.add(**kwargs)

    def debug(self, *args, **kwargs):
        if args:
            self._writer.add_message(args[0], MessageSeverity.Debug.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Debug.value
                kwargs['object']['component_id'] = self.component_id
                self._writer.add(**kwargs)

    def verbose(self, *args, **kwargs):
        if args:
            self._writer.add_message(args[0], MessageSeverity.Verbose.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Verbose.value
                kwargs['object']['component_id'] = self.component_id
                self._writer.add(**kwargs)

