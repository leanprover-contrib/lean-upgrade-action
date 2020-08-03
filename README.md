# lean-upgrade-action

This is a GitHub action for Lean projects.
At a scheduled time, it will try to update the Lean version and dependencies of your project
to their latest versions.
If the automatic upgrade fails,
it will create an issue in your project repository.

## Usage

### Set up a personal access token

Since this action can open issues in your repository,
it needs access to some GitHub account to post the issues.

Go to the [Personal access tokens](https://github.com/settings/tokens) page on GitHub,
and create a new token.
Make sure **repo** and **write:discussion** are checked.

Create a new secret in your project repository at
https://github.com/your-org/your-repo/settings/secrets
with name `PAT`. Use the token you just created as the value.

### Set up the Actions workflow

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
          access-token: ${{ secrets.PAT }}
```

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

If you don't know what this means, you can probably ignore it.
Just copy the first block of code into your project.

## Options

The above workflow will run once per day at 02:00 UTC.
Modify the [cron expression](https://crontab.guru/) to reschedule.