# update-versions-action

This is a GitHub action for Lean projects.
Every time you push to your `master` branch of a Lean project repository,
the action will mirror your push to the appropriate `lean-x.y.z` version branch.
It determines this version from the `leanpkg.toml` file at the root of your project.

## Usage

Create a file in your Lean project directory, `/.github/workflows/version_update.yml`, with contents:

```yaml
on:
  push:
    branches:
      - master

jobs:
  update_lean_xyz_branch:
    runs-on: ubuntu-latest
    name: Update lean-x.y.z branch
    steps:

    - name: checkout project
      uses: actions/checkout@v2
      with:
        fetch-depth: 0

    - name: update branch
      uses: leanprover-contrib/update-versions-action@master
```

If you are running this action from a repo other than the one it is updating,
or if you have set up branch protection rules on your `lean-x.y.z` branches,
you will have to modify the checkout step to point to the right repo with write permissions.
For instance:

```yaml
    - name: checkout mathlib
      uses: actions/checkout@v2
      with:
        repository: leanprover-community/mathlib
        token: ${{ secrets.PA_TOKEN }}
        fetch-depth: 0
```

Alternatively, you can specify a remote name for the branch to push to; it defaults to `origin`.

```yaml
    - name: update branch
      uses: leanprover-contrib/update-versions-action@master
      with:
        remote: new-origin
```

If you don't know what this means, you can probably ignore it. 
Just copy the first block of code into your project.

## What this script does not do

This script will NOT update your master branch in any way.
It will NOT test that anything actually builds.

If you are waiting for a script that automatically updates your project to the latest Lean/mathlib
and checks if it builds:
that script is coming. It is not this one.

## Warning

We do not recommend manually updating the latest `lean-x.y.z` branch directly.
If it diverges from `master` this action will fail.
It is safe to manually update older version branches,
provided that you never revert `master` to that version.