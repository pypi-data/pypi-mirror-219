"""Define dl_hf_model."""
from pathlib import Path
from typing import Tuple
from urllib.parse import urlparse

from huggingface_hub import hf_hub_download
from loguru import logger


def get_repo_id_model_file_revision(url: str) -> Tuple[str, str, str]:
    """Fetch repo_id, mode_file, revision."""
    model_file = Path(url).name
    _ = urlparse(url).path.strip("/").split("/")
    repo_id = "/".join(_[:2])
    revision = Path(url).parent.name
    # model_type = AutoConfig(repo_id).model_type

    return repo_id, model_file, revision


def dl_hf_model(
    url: str,
    local_dir: str = "models",
) -> Tuple[str, float]:
    """Download and cache a hf model gievn by url, save to local_dir."""
    repo_id, model_file, revision = get_repo_id_model_file_revision(url)
    try:
        model_file = hf_hub_download(
            repo_id=repo_id,
            filename=model_file,
            local_dir=local_dir,  # "models"
            revision=None if revision in ["main"] else revision
            # local_dir_use_symlinks=True,
        )
    except Exception as exc:
        logger.error(exc)
        raise

    try:
        st_size = round(Path(model_file).stat().st_size / 10**9, 2)
    except Exception as exc:
        logger.error(exc)
        raise

    return model_file, st_size
