## Import default constants
from __future__ import annotations

from .src import (
    LogLevel,
    default_color_fmt,
    default_fmt,
    default_log_dir,
    log_levels,
    valid_compression_strs,
)
from .src import add_sink, init_logger
from .src import (
    default_app_log_file_sink,
    default_error_log_file_sink,
    default_sinks,
    default_stderr_color_sink,
    default_stderr_sink,
    default_stdout_color_sink,
    default_stdout_sink,
    default_trace_log_file_sink,
)

from .src import validate_compression_str, validate_level, validate_logger
