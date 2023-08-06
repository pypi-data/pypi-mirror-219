# VerNum

Version numbering and git tagging for project releases

[Watch the video](https://www.youtube.com/watch?v=JD8WdVNv1ac)

## Installation

Requires Python 3 to run the command; your project can be anything.

```
pip3 install vernum
```

## What it does

- Maintain a file at the root of a project called simply "version" with the version number, e.g. "5.6.2"
- Update the release file for major, minor, or patch releases - patch is the default
- Optionally create and push a git tag with the version number in it

## Usage

Requirements:

- CD to the root of the project before running it
- Be on the branch that you use for releases (i.e. `master`)
- Be fully up-to-date in git (i.e. merged, committed, and pushed)

Then run the command:

- `vernum major` to update the major version level, i.e. 5.6.2 -> 6.0.0
- `vernum minor` to update the minor version level, i.e. 5.6.2 -> 5.7.0
- `vernum patch` to update the patch version level, i.e. 5.6.2 -> 5.6.3

Note that `patch` is the default so you can just say `vernum` for a patch release

Reference the `.version` file within your code when it needs to know the version. For example, see `pyproject.toml` in this project.

VerNum looks at the most recent git tag that fits the format, then increments it appropriately. It also generates the `.version` file.

Options:

- `--push-tag` create a git tag for the version and push it
- `--dry-run` just output the information; don't do anything