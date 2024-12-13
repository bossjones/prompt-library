"""
This type stub file was generated by pyright.
"""

"""implementations of simple readline edit operations

just the ones that fit the model of transforming the current line
and the cursor location
based on http://www.bigsmoke.us/readline/shortcuts"""
INDENT = ...
getargspec = ...
class AbstractEdits:
    default_kwargs = ...
    def __init__(self, simple_edits=..., cut_buffer_edits=...) -> None:
        ...
    
    def add(self, key, func, overwrite=...): # -> None:
        ...
    
    def add_config_attr(self, config_attr, func): # -> None:
        ...
    
    def call(self, key, **kwargs):
        ...
    
    def call_without_cut(self, key, **kwargs):
        """Looks up the function and calls it, returning only line and cursor
        offset"""
        ...
    
    def __contains__(self, key): # -> bool:
        ...
    
    def __getitem__(self, key):
        ...
    
    def __delitem__(self, key): # -> None:
        ...
    


class UnconfiguredEdits(AbstractEdits):
    """Maps key to edit functions, and bins them by what parameters they take.

    Only functions with specific signatures can be added:
        * func(**kwargs) -> cursor_offset, line
        * func(**kwargs) -> cursor_offset, line, cut_buffer
        where kwargs are in among the keys of Edits.default_kwargs
    These functions will be run to determine their return type, so no side
    effects!

    More concrete Edits instances can be created by applying a config with
    Edits.mapping_with_config() - this creates a new Edits instance
    that uses a config file to assign config_attr bindings.

    Keys can't be added twice, config attributes can't be added twice.
    """
    def mapping_with_config(self, config, key_dispatch): # -> ConfiguredEdits:
        """Creates a new mapping object by applying a config object"""
        ...
    
    def on(self, key=..., config=...): # -> Callable[..., Any]:
        ...
    


class ConfiguredEdits(AbstractEdits):
    def __init__(self, simple_edits, cut_buffer_edits, awaiting_config, config, key_dispatch) -> None:
        ...
    
    def add_config_attr(self, config_attr, func):
        ...
    
    def add(self, key, func, overwrite=...):
        ...
    


edit_keys = ...
def kills_behind(func):
    ...

def kills_ahead(func):
    ...

@edit_keys.on(config="left_key")
@edit_keys.on("<LEFT>")
def left_arrow(cursor_offset, line): # -> tuple[int, Any]:
    ...

@edit_keys.on(config="right_key")
@edit_keys.on("<RIGHT>")
def right_arrow(cursor_offset, line): # -> tuple[int, Any]:
    ...

@edit_keys.on(config="beginning_of_line_key")
@edit_keys.on("<HOME>")
def beginning_of_line(cursor_offset, line): # -> tuple[Literal[0], Any]:
    ...

@edit_keys.on(config="end_of_line_key")
@edit_keys.on("<END>")
def end_of_line(cursor_offset, line): # -> tuple[int, Any]:
    ...

forward_word_re = ...
@edit_keys.on("<Esc+f>")
@edit_keys.on("<Ctrl-RIGHT>")
@edit_keys.on("<Esc+RIGHT>")
def forward_word(cursor_offset, line): # -> tuple[Any, Any]:
    ...

def last_word_pos(string): # -> int:
    """returns the start index of the last word of given string"""
    ...

@edit_keys.on("<Esc+b>")
@edit_keys.on("<Ctrl-LEFT>")
@edit_keys.on("<Esc+LEFT>")
def back_word(cursor_offset, line): # -> tuple[int, Any]:
    ...

@edit_keys.on("<DELETE>")
def delete(cursor_offset, line): # -> tuple[Any, Any]:
    ...

@edit_keys.on("<BACKSPACE>")
@edit_keys.on(config="backspace_key")
def backspace(cursor_offset, line): # -> tuple[Literal[0], Any] | tuple[Any, Any]:
    ...

@edit_keys.on(config="clear_line_key")
def delete_from_cursor_back(cursor_offset, line): # -> tuple[Literal[0], Any]:
    ...

delete_rest_of_word_re = ...
@edit_keys.on("<Esc+d>")
@kills_ahead
def delete_rest_of_word(cursor_offset, line): # -> tuple[Any, Any, Literal['']] | tuple[Any, Any, Any]:
    ...

delete_word_to_cursor_re = ...
@edit_keys.on(config="clear_word_key")
@kills_behind
def delete_word_to_cursor(cursor_offset, line): # -> tuple[Any | Literal[0], Any, Any]:
    ...

@edit_keys.on("<Esc+y>")
def yank_prev_prev_killed_text(cursor_offset, line, cut_buffer): # -> tuple[Any, Any]:
    ...

@edit_keys.on(config="yank_from_buffer_key")
def yank_prev_killed_text(cursor_offset, line, cut_buffer): # -> tuple[Any, Any]:
    ...

@edit_keys.on(config="transpose_chars_key")
def transpose_character_before_cursor(cursor_offset, line): # -> tuple[Any, Any] | tuple[int, Any]:
    ...

@edit_keys.on("<Esc+t>")
def transpose_word_before_cursor(cursor_offset, line): # -> tuple[Any, Any]:
    ...

@edit_keys.on("<Esc+u>")
def uppercase_next_word(cursor_offset, line): # -> tuple[Any, Any]:
    ...

@edit_keys.on(config="cut_to_buffer_key")
@kills_ahead
def delete_from_cursor_forward(cursor_offset, line): # -> tuple[Any, Any, Any]:
    ...

@edit_keys.on("<Esc+c>")
def titlecase_next_word(cursor_offset, line): # -> tuple[Any, Any]:
    ...

delete_word_from_cursor_back_re = ...
@edit_keys.on("<Esc+BACKSPACE>")
@edit_keys.on("<Meta-BACKSPACE>")
@kills_behind
def delete_word_from_cursor_back(cursor_offset, line): # -> tuple[Any, Any, Literal['']] | tuple[Any, Any, Any]:
    """Whatever my option-delete does in bash on my mac"""
    ...
