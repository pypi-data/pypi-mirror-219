# Kognic Keyring Auth
A keyring to let users authenticate using GCloud credentials to the Kognic PyPI server. 
This keyring piggy-backs on the GCloud keyring

https://github.com/GoogleCloudPlatform/artifact-registry-python-tools/blob/main/README.md

You can install this with

```pip install kognic-keyring```

Or if you are using `pipx`, inject it into the env for `keyring`

```pipx install keyring && pipx inject keyring kognic-keyring```
