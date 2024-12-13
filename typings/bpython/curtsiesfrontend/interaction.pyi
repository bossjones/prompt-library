"""
This type stub file was generated by pyright.
"""

from ..repl import Interaction

class StatusBar(Interaction):
    """StatusBar and Interaction for Repl

    Passing of control back and forth between calls that use interact api
    (notify, confirm, file_prompt) like bpython.Repl.write2file and events on
    the main thread happens via those calls and
    self.wait_for_request_or_notify.

    Calling one of these three is required for the main thread to regain
    control!

    This is probably a terrible idea, and better would be rewriting this
    functionality in a evented or callback style, but trying to integrate
    bpython.Repl code.
    """
    def __init__(self, config, permanent_text=..., request_refresh=..., schedule_refresh=...) -> None:
        ...
    
    def push_permanent_message(self, msg): # -> None:
        ...
    
    def pop_permanent_message(self, msg): # -> None:
        ...
    
    @property
    def has_focus(self): # -> bool:
        ...
    
    def message(self, msg, schedule_refresh=...): # -> None:
        """Sets a temporary message"""
        ...
    
    def process_event(self, e) -> None:
        """Returns True if shutting down"""
        ...
    
    def add_normal_character(self, e): # -> None:
        ...
    
    def escape(self): # -> None:
        """unfocus from statusbar, clear prompt state, wait for notify call"""
        ...
    
    @property
    def current_line(self): # -> str:
        ...
    
    @property
    def should_show_message(self): # -> bool:
        ...
    
    def notify(self, msg, n=..., wait_for_keypress=...): # -> None:
        ...
    
    def confirm(self, q): # -> Any:
        """Expected to return True or False, given question prompt q"""
        ...
    
    def file_prompt(self, s): # -> Any:
        """Expected to return a file name, given"""
        ...
    

