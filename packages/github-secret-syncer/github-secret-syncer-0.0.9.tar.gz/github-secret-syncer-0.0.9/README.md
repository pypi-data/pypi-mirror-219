# Github Secret Syncer

Synchronize Github secrets with local `.env` file.

![Screenshot](https://raw.githubusercontent.com/thejimmylin/github-secret-syncer/master/docs/quickstart.png)

# Quickstart

Install it with pip:

```
pip install github-secret-syncer
```

Have a `.env` and `quickstart.py`

```python
from pathlib import Path

import github_secret_syncer

base_dir = Path(__file__).parent

github_secret_syncer.sync_secrets(
    dotenv_path=base_dir / ".env",
    owner="your_github_username",
    repo="your_github_repo_name",
    pat="your_github_personal_access_token",
)
```

You will get some output like this:

![Screenshot](https://raw.githubusercontent.com/thejimmylin/github-secret-syncer/master/docs/quickstart.png)
