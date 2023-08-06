import traceback
from LoggerLocalPythonPackage.MessageSeverity import MessageSeverity
from LoggerLocalPythonPackage.Writer import Writer
import os
debug = os.getenv("debug")

class LoggerService:

    

    def __init__(self):
        self._writer = Writer()
        self.fields = self.get_logger_table_fields()
        for field in self.fields:
            setattr(self, field, None)

    def init(self,*args, **kwargs):
        if debug: print('LoggerService.init(args= '+args+' kwargs= '+kwargs )
        if args and 'object' in kwargs:
            self.insertVariables(**kwargs)
            kwargs['object']['severity_id'] = MessageSeverity.Init.value
            self._writer.addMessageAndPayload(args[0],**kwargs)
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.Init.value)
            else:
                if 'object' in kwargs:
                    self.insertVariables(**kwargs)
                    kwargs['object']['severity_id'] = MessageSeverity.Init.value
                    self._writer.add(**kwargs)

    def start(self, *args, **kwargs):
        if debug: print('LoggerService.start(args='+args+' kwargs='+kwargs )
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Start.value
            self.insert_To_object(**kwargs)   
            self._writer.addMessageAndPayload(args[0],**kwargs)
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.Start.value)
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Start.value
                    self.insert_To_object(**kwargs)              
                    self._writer.add(**kwargs)

    def end(self, *args, **kwargs):
        if debug: print('LoggerService.start(args='+args+' kwargs='+kwargs )
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.End.value
            self.insert_To_object(**kwargs)   
            self._writer.addMessageAndPayload(args[0],**kwargs)
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.End.value)
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.End.value
                    self.insert_To_object(**kwargs) 
                    self._writer.add(**kwargs)

    def exception(self, *args, **kwargs):
        if debug: print('LoggerService.start(args='+args+' kwargs='+kwargs )
        if args and 'object' in kwargs:
            stack_trace = traceback.format_exception(type(kwargs['object']), kwargs['object'], kwargs['object'].__traceback__)
            object_exp = {
                    'severity_id': MessageSeverity.Exception.value,
                    'error_stack': str(stack_trace)
                }
            self.insert_To_object(object=object_exp)  
            self._writer.addMessageAndPayload(args[0],object=object_exp)
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.Exception.value)
            else:
                if 'object' in kwargs:
                    stack_trace = traceback.format_exception(type(kwargs['object']), kwargs['object'], kwargs['object'].__traceback__)
                    object_exp = {
                        'severity_id': MessageSeverity.Exception.value,
                        'error_stack': str(stack_trace)
                    }
                    self.insert_To_object(object=object_exp) 
                    self._writer.add(object=object_exp)



    def info(self, *args, **kwargs):
        if debug: print('LoggerService.start(args='+args+' kwargs='+kwargs )
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Information.value
            self.insert_To_object(**kwargs)   
            self._writer.addMessageAndPayload(args[0],**kwargs)
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.Information.value)
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Information.value
                    self.insert_To_object(**kwargs) 
                    self._writer.add(**kwargs)

    def error(self, *args, **kwargs):
        if debug: print('LoggerService.start(args='+args+' kwargs='+kwargs )
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Error.value
            self.insert_To_object(**kwargs)   
            self._writer.addMessageAndPayload(args[0],**kwargs)
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.Error.value)
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Error.value
                    self.insert_To_object(**kwargs) 
                    self._writer.add(**kwargs)

    def warn(self, *args, **kwargs):
        if debug: print('LoggerService.start(args='+args+' kwargs='+kwargs )
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Error.value
            self.insert_To_object(**kwargs)   
            self._writer.addMessageAndPayload(args[0],**kwargs)
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.Warning.value)
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Warning.value
                    self.insert_To_object(**kwargs) 
                    self._writer.add(**kwargs)

    def debug(self, *args, **kwargs):
        if debug: print('LoggerService.start(args='+args+' kwargs='+kwargs )
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Debug.value
            self.insert_To_object(**kwargs)   
            self._writer.addMessageAndPayload(args[0],**kwargs)
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.Debug.value)
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Debug.value
                    self.insert_To_object(**kwargs) 
                    self._writer.add(**kwargs)

    def verbose(self, *args, **kwargs):
        if debug: print('LoggerService.start(args='+args+' kwargs='+kwargs )
        if args and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Verbose.value
            self.insert_To_object(**kwargs)   
            self._writer.addMessageAndPayload(args[0],**kwargs)
        else:
            if args:
                self._writer.add_message(args[0], MessageSeverity.Verbose.value)
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Verbose.value
                    self.insert_To_object(**kwargs) 
                    self._writer.add(**kwargs)

    def insertVariables(self,**object):
        object_data = object.get("object", {})
        for field in self.fields:
            setattr(self, field, object_data.get(field, getattr(self, field)))
    def insert_To_object(self, **kwargs):
        object_data = kwargs.get("object", {})
        for field in self.fields:
            if field not in object_data:
                field_value = getattr(self, field)
                if field_value is not None:
                    object_data[field] = field_value


    def get_logger_table_fields(self):
        fields = ['client_ip_v4', 'client_ip_v6', 'server_ip_v4', 'server_ip_v6', 'location_id', 'user_id',
                  'profile_id', 'activity', 'activity_id', 'message', 'record', 'payload',
                  'component_id', 'error_stack', 'severity_id', 'status_id', 'group_id', 'relationship_type_id',
                  'state_id', 'variable_id', 'variable_value_old', 'variable_value_new', 'created_user_id',
                  'updated_user_id']
        return fields
    def clean_variables(self):
        for field in self.fields:
            setattr(self, field, None)