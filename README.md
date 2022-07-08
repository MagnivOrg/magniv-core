<div align="center">

<img src="https://www.magniv.io/static/media/textlogo.e9b53078962edf01fb96e8f0eeab7880.svg" width="400px">

**One line data science infra.**

<a href="https://actions-badge.atrox.dev/MagnivOrg/magniv-core/goto?ref=master"><img alt="Build" src="https://img.shields.io/github/workflow/status/MagnivOrg/magniv-core/CI%20tests/master?style=for-the-badge" /></a>
<a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/-Python 3.8+-blue?style=for-the-badge&logo=python&logoColor=white"></a>
<a href="https://docs.magniv.io"><img alt="Docs" src="https://custom-icon-badges.herokuapp.com/badge/docs-magniv-blue.svg?logo=magniv&style=for-the-badge&logoColor=white"></a>
<a href="https://www.loom.com/share/35ae5bb7a4b54200a9c5442e50c54aca"><img alt="Demo with Loom" src="https://img.shields.io/badge/Demo-loom-552586.svg?logo=loom&style=for-the-badge&labelColor=gray"></a>

______________________________________________________________________

<div align="left">

Magniv is the easiest way to build and deploy data applications, pipelines, or cron-like jobs. A Python decorator based orchestration library at the core, Magniv allows data scientists and developers to schedule arbitrary functions in one line. Monitoring, CI/CD, and compute management all come out of the box using the Magniv in a fully-managed context.

## Quickstart ⚡

To get Magniv running with a simple "Hello, World" example, follow these three steps:

<span>1.</span> Install Magniv from pip.

```bash
pip install magniv
```

<span>2.</span> Create /tasks/requirements.txt every Magniv project requires at least one requirements.txt

<span>3.</span> Run the code below as a Python script or in a Python notebook (or in a colab notebook).

```python
from magniv.core import task


@task(schedule="@hourly")
def hello_world():
    print("Hello world")
```

## Monitoring

Using the Magniv dashboard makes it easy to monitor running jobs. Each Magniv task is displayed with its previous run information, logs, code snippets, and other details. Users also have the ability to disable tasks and manually trigger new runs.

<div align="center">
  <img src="https://miro.medium.com/max/1160/1*F0JkAaq8e3fKiLj7gZCfzQ.gif" max-height="250px">
</div>

## Git CI/CD

Similar to tools like Heroku or Netlify, Magniv sets up a CI/CD pipeline from your GitHub repository. After connecting a Magniv workspace to a GitHub repo, every new commit will trigger a new build and update your tasks.

<div align="center">
  <img src="https://miro.medium.com/max/1240/1*4xigR6AHkwdB9Jfi779UDA.gif" max-height="250px">
</div>
