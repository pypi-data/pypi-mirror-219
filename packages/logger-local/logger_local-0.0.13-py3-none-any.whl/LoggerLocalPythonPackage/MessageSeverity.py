from enum import Enum


class MessageSeverity(Enum):

    Debug = 600
    Verbose = 500
    Information = 400
    Warning = 300
    Error = 200
    Critical = 100
    Start=700
    End=800
    Exception=900
    Init=1000