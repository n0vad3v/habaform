# habaform

![](https://img.shields.io/pypi/pyversions/Django.svg)

> Manage Harbor projects and members with ease.


## Installation

```
pip3 install habaform
```

## Usage

### Init

After installation, you will need to parse the current Harbor Project/User model first, create a new git repository and run the following commands inside it:

```bash
export HARBOR_USERNAME="admin"
export HARBOR_PASSWORD="Harbor12345"
export HARBOR_URL="http://hub.nova.moe"

habaform parse
```

you will find these files inside your directory:

```
.
├── DO_NOT_TOUCH
│   └── habaform.hf
└── habaform.hf

1 directory, 2 files
```

Now you can commit and push thoses files to the GitHub repository.

### Workflow in local environment

Habaform can be used without GitOps like operation, if you'd like to use habaform in your local environment, here is the common workflow.

1. Edit `habaform.hf` under the project root directory.
2. Run `habaform plan` and make sure the changes are correctly reflecting your changes.
3. Run `habaform apply` to apply those changes to your Harbor.

### Workflow with GitHub Actions

Create two GitHub Actions workflow files as follows:

1. `plan.yml`

This will run when PR is made, and will give the preview change on issue.

```yaml
name: Plan Habaform
on: [pull_request]

jobs:
  Plan:
    runs-on: [self-hosted,X64]
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Setup Habaform
        run: |
          pip3 install habaform

      - name: Plan
        id: plan
        env:
          HARBOR_USERNAME: ${{secrets.HARBOR_USERNAME}}
          HARBOR_PASSWORD: ${{secrets.HARBOR_PASSWORD}}
          HARBOR_URL: ${{secrets.HARBOR_URL}}
        run: |
          echo 'HABAPLAN<<EOF' >> $GITHUB_ENV
          habaform plan >> $GITHUB_ENV
          echo 'EOF' >> $GITHUB_ENV

      - name: Preview Plan info
        uses: actions/github-script@v4
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            github.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `${{ env.HABAPLAN }}`
            })
```

2. `apply.yml`

This will run when PR is merged, will apply the changes to Harbor automatically.

```yaml
name: Apply Habaform

on:
  push:
    branches: [ master ]
    paths:
      - 'habaform.hf'

jobs:
  Apply:
    runs-on: [self-hosted,X64]
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Setup Habaform
        run: |
           pip3 install habaform

      - name: Apply
        id: apply
        env:
          HARBOR_USERNAME: ${{secrets.HARBOR_USERNAME}}
          HARBOR_PASSWORD: ${{secrets.HARBOR_PASSWORD}}
          HARBOR_URL: ${{secrets.HARBOR_URL}}
        run: |
          habaform apply

      - name: Sync config
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add .
          git commit -m "Sync hf file"
          git push
```

Then you should create three GitHub Secrets:

* HARBOR_USERNAME (e,g: `admin`)
* HARBOR_PASSWORD (e,g: `Harbor12345`)
* HARBOR_URL (e,g: `http://hub.nova.moe`)

After that, you can use PR to edit `habaform.hf` to make changes to your Harbor.

For more info, refer to [Habaform——用类似 IaC(Infrastructure as code) + GitOps 的方式管理 Harbor 的 Project 和 User](https://nova.moe/manage-harbor-projects-the-iac-way/) at this moment, through I can't promise there will be a better document soon.