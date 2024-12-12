"""
This type stub file was generated by pyright.
"""

import io
from typing import Optional, Union
from marimo._output.hypertext import Html
from marimo._output.rich_help import mddoc

@mddoc
def video(src: Union[str, bytes, io.BytesIO, io.BufferedReader], controls: bool = ..., muted: bool = ..., autoplay: bool = ..., loop: bool = ..., width: Optional[Union[int, str]] = ..., height: Optional[Union[int, str]] = ..., rounded: bool = ...) -> Html:
    """Render an video as HTML.

    **Example.**

    ```python3
    mo.video(
        src="https://v3.cdnpk.net/videvo_files/video/free/2013-08/large_watermarked/hd0992_preview.mp4",
        controls=False,
    )
    ```

    **Args.**

    - `src`: the URL of the video or a file-like object
    - `controls`: whether to show the controls
    - `muted`: whether to mute the video
    - `autoplay`: whether to autoplay the video.
        the video will only autoplay if `muted` is `True`
    - `loop`: whether to loop the video
    - `width`: the width of the video in pixels or a string with units
    - `height`: the height of the video in pixels or a string with units
    - `rounded`: whether to round the corners of the video

    **Returns.**

    `Html` object
    """
    ...
