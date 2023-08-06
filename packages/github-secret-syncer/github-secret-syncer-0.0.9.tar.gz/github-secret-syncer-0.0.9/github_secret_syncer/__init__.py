import logging
from base64 import b64encode
from pathlib import Path
from typing import Any, TypedDict, cast

import dotenv
import requests
from nacl import encoding, public

logger = logging.getLogger(__name__)

__all__ = ["GithubSecretManager", "sync_secrets"]


class PublicKey(TypedDict):
    key: str
    key_id: str


class SecretBrief(TypedDict):
    name: str
    created_at: str
    updated_at: str


class SecretListReponse(TypedDict):
    total_count: int
    secrets: list[SecretBrief]


class GithubSecretManager:
    """Manage Github Secrets"""

    _public_key: PublicKey | None

    def __init__(self, owner: str, repo: str, pat: str, api_version: str = "2022-11-28"):
        self.owner = owner
        self.repo = repo
        self.pat = pat
        self.api_version = api_version
        self._public_key = None

    @property
    def public_key(self) -> PublicKey:
        if self._public_key is None:
            self._public_key = self._get_public_key()
        return self._public_key

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.pat}",
            "X-GitHub-Api-Version": f"{self.api_version}",
        }

    def _get_public_key(self) -> PublicKey:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/actions/secrets/public-key"
        response = requests.get(url, headers=self.headers)
        public_key = response.json()
        return public_key

    def _encrypt(self, secret_value: str) -> str:
        key_bytes = self.public_key["key"].encode("utf-8")
        public_key = public.PublicKey(key_bytes, cast(Any, encoding.Base64Encoder()))
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return b64encode(encrypted).decode("utf-8")

    def list_repo_secrets(self) -> SecretListReponse:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/actions/secrets"
        response = requests.get(url, headers=self.headers)
        secrets = response.json()
        return secrets

    def put_repo_secret(self, secret_name: str, secret_value: str) -> None:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/actions/secrets/{secret_name}"
        payload = {"encrypted_value": self._encrypt(secret_value), "key_id": self.public_key["key_id"]}
        response = requests.put(url, headers=self.headers, json=payload)
        if response.status_code not in (requests.codes.CREATED, requests.codes.NO_CONTENT):
            raise ValueError(f"Failed to put secret: `{response = }`, `{response.json() = }`")

    def delete_repo_secret(self, secret_name) -> None:
        "https://api.github.com/repos/OWNER/REPO/actions/secrets/SECRET_NAME"
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/actions/secrets/{secret_name}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code != requests.codes.NO_CONTENT:
            raise ValueError(f"Failed to delete secret: `{response = }`, `{response.json() = }`")


def sync_secrets(
    dotenv_path: Path,
    owner: str,
    repo: str,
    pat: str,
    delete_missing: bool = True,
    api_version: str = "2022-11-28",
    show_info=False,
) -> None:
    """Sync secrets from dotenv to Github Actions

    This function can be seen as an example of how to use GithubSecretManager.
    Feel free to copy and modify it to fit your needs.
    """
    if show_info:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    secret_manager = GithubSecretManager(owner, repo, pat, api_version)
    secrets = secret_manager.list_repo_secrets()
    _dotenv_secrets = dotenv.dotenv_values(dotenv_path)

    # Ignore secrets like `foo` (without `=`)
    # This will not ignore secrets like `bar=` (it's value will be `""`)
    dotenv_secrets: dict[str, str] = {}
    for secret_name, secret_value in _dotenv_secrets.items():
        if secret_value is not None:
            dotenv_secrets[secret_name] = secret_value

    if delete_missing:
        # Delete secrets that are in Github but not in dotenv
        for secret in secrets["secrets"]:
            if secret["name"] not in dotenv_secrets:
                logger.info(f"Deleting secret `{secret['name']}` from Github")
                secret_manager.delete_repo_secret(secret["name"])

    # Put secrets that are in dotenv
    for secret_name, secret_value in dotenv_secrets.items():
        logger.info(f"Putting secret `{secret_name}` to Github")
        secret_manager.put_repo_secret(secret_name, secret_value)
