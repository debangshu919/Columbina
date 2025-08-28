import toml
import yaml
import pathlib
import sys
import os

def bump(version: str, message: str) -> str:
    major, minor, patch = map(int, version.split("."))

    msg = message.lower()
    if "feat" in msg:
        minor += 1
        patch = 0
    elif "fix" in msg:
        patch += 1

    return f"{major}.{minor}.{patch}"

def main():
    # --- Load pyproject.toml ---
    pyproject_path = pathlib.Path("pyproject.toml")
    pyproject = toml.load(pyproject_path)
    old_version = pyproject["project"]["version"]

    # Commit message is passed as an arg
    commit_msg = sys.argv[1] if len(sys.argv) > 1 else ""

    new_version = bump(old_version, commit_msg)

    if new_version == old_version:
        print(f"No version bump needed. Current version: {old_version}")
        sys.exit(0)

    # Update pyproject.toml
    pyproject["project"]["version"] = new_version
    with pyproject_path.open("w") as f:
        toml.dump(pyproject, f)

    # Update config.yaml if exists
    config_path = pathlib.Path("config.yaml")
    if config_path.exists():
        config = yaml.safe_load(config_path.read_text()) or {}
        config["version"] = new_version
        with config_path.open("w") as f:
            yaml.safe_dump(config, f, sort_keys=False)

    # Output for GitHub Actions
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        f.write(f"version={new_version}\n")

if __name__ == "__main__":
    main()
