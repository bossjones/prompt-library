"""
This type stub file was generated by pyright.
"""

"""
This type stub file was generated by pyright.
"""
html_escape = ...
xml_escapes = ...
def xml_escape(string):
    ...

def url_escape(string):
    ...

def trim(string):
    ...

class Decode:
    def __getattr__(self, key):
        ...
    


decode = ...
class XMLEntityEscaper:
    def __init__(self, codepoint2name, name2codepoint) -> None:
        ...
    
    def escape_entities(self, text):
        """Replace characters with their character entity references.

        Only characters corresponding to a named entity are replaced.
        """
        ...
    
    __escapable = ...
    def escape(self, text):
        """Replace characters with their character references.

        Replace characters by their named entity references.
        Non-ASCII characters, if they do not have a named entity reference,
        are replaced by numerical character references.

        The return value is guaranteed to be ASCII.
        """
        ...
    
    __characterrefs = ...
    def unescape(self, text):
        """Unescape character references.

        All character references (both entity references and numerical
        character references) are unescaped.
        """
        ...
    


_html_entities_escaper = ...
html_entities_escape = ...
html_entities_unescape = ...
def htmlentityreplace_errors(ex):
    """An encoding error handler.

    This python codecs error handler replaces unencodable
    characters with HTML entities, or, if no HTML entity exists for
    the character, XML character references::

        >>> 'The cost was \u20ac12.'.encode('latin1', 'htmlentityreplace')
        'The cost was &euro;12.'
    """
    ...

DEFAULT_ESCAPES = ...
