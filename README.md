# lean-upgrade-action

This is a GitHub action for Lean projects.
At a scheduled time, it will try to update the Lean version and dependencies of your project
to their latest versions.
If the automatic upgrade fails,
it will create an issue in your project repository.

The upgrade logic works like this:
* If your project depends on mathlib, it will call `leanproject upgrade-mathlib`. That is,
  - The Lean version will be bumped to the Lean version of mathlib master.
  - The mathlib dependency will be bumped to mathlib master.
  - All other dependencies will be bumped to the same Lean version, if they have a corresponding branch.
* If your project does not depend on mathlib, but the Lean version is comparable to that of mathlib master,
  e.g. both are `leanprover-community/lean`:
  - The Lean version will be bumped to the Lean version of mathlib master.
  - All other dependencies will be bumped to the same Lean version, if they have a corresponding branch.
* If your project uses a Lean version incomparable to that of mathlib:
  - The Lean version will not change.
  - All other dependencies will be bumped to the latest releases for your current Lean version.

## Usage

Create a file in your Lean project directory, `/.github/workflows/upgrade_lean.yml`, with contents:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'

jobs:
  upgrade_lean:
    runs-on: ubuntu-latest
    name: Bump Lean and dependency versions
    steps:
      - name: checkout project
        uses: actions/checkout@v2
      - name: upgrade Lean and dependencies
        uses: leanprover-contrib/lean-upgrade-action@master
        with:
          repo: ${{ github.repository }}
          access-token: ${{ secrets.GITHUB_TOKEN }}
      - name: update version branches
        uses: leanprover-contrib/update-versions-action@master
```

### Advanced notes

If you are running this action from a repo other than the one it is updating,
or if you have set up branch protection rules on your `lean-x.y.z` branches,
you will have to modify the checkout step to point to the right repo with write permissions.
For instance:

```yaml
    - name: checkout project
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


This action is often used in combination with the 
[update versions action](https://github.com/leanprover-contrib/update-versions-action).
Unfortunately, due to limitations in the GitHub Actions API,
that action will only be triggered by this one when a token other than `secrets.GITHUB_TOKEN` is used.
If you change the token away from GitHub's default,
you should probably remove the `update version branches` step from the workflow.

If you don't know what any of this means, you can probably ignore it.
Just copy the first block of code into your project.

## Options

The above workflow will run once per day at 02:00 UTC.
Modify the [cron expression](https://crontab.guru/) to reschedule.