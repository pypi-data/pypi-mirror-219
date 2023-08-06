from __future__ import annotations

from typing import Any

from .constants import (
    default_cache_dir,
    default_timeout_dict,
    valid_key_types,
    valid_tag_types,
    valid_val_types,
)

from .operations import (
    convert_to_seconds,
    get_cache,
    check_cache,
    get_cache_size,
    delete_val,
    get_val,
    set_expire,
    set_val,
    cache_tag_index,
    check_exists,
    clear_cache,
)

from .validators import (
    validate_cache,
    validate_expire,
    validate_key,
    validate_read,
    validate_retry,
    validate_tag,
    validate_tags,
    validate_val,
)

## Define a default cache object
default_cache_conf: dict[str, Any] = {
    "directory": default_cache_dir,
    "timeout": convert_to_seconds(
        unit=default_timeout_dict["unit"], amount=default_timeout_dict["amount"]
    ),
}
