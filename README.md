# aide_design [![Travis Build Status](https://travis-ci.org/AguaClara/aide_design.svg?branch=master)](https://travis-ci.org/AguaClara/aide_design) [![codecov](https://codecov.io/gh/AguaClara/aide_design/branch/master/graph/badge.svg)](https://codecov.io/gh/AguaClara/aide_design)

Design an AguaClara Water Treatment Plant with just a couple lines of code! Or just design a few components - your choice with aide_design. Aide_design parametrically designs plant components from basic physics equations. In a nutshell, you can generate a design yaml for a whole plant and print it to your console stream like so:

```python
from aide_design.play import *
from aide_render import render
import sys
my_plant = Plant(HP(30, u.L/u.s))
render(my_plant, sys.stdout)
```

## Installing
```bash
pip install aide_design
```

## Installing as a developer
If you want to make pushes to aide_design, then you should clone this repo and make the package available locally, using the following commands:
```bash
git clone https://github.com/AguaClara/aide_design.git
cd aide_design
pip install --editable . -U --user
```
The editable flag makes it so that you don't have to continuously install with pip to make the changes you just made visible.

## Contributing: (v0.0.1 -> v0.1.0)
1. Write your code!
2. When you are ready to commit it, make a new branch that describes your changes and push it to github:
    ```bash
    $ git add . #add local files to staging area
    $ git checkout -b the_name_of_my_new_branch #create new branch locally and move to it
    $ git commit -m "my detailed commit message describing what I did" #commit to the new branch
    $ git push -u origin the_name_of_my_new_branch #push the new branch and all the commits you made to GitHub.
    ```
3. Keep making changes and committing them as you finish your feature. Once you are ready to push your code to the master branch, go online and make a pull request to the master branch.
4. The pull request will initiate several 'checks.' This will take about 5 minutes to run. The first is the Travis CI check. Travis is a cloud-based continuous integration tool that automatically runs all defined tests. Once the tests pass, Travis generates a coverage report. This report analyzed what percentage of the code was "hit" during the testing process, also known as what percentage was 'covered'.
5. If all the checks passed, you can ping a repo manager to ask them to accept your pull request.
6. If the repo manager accepts the request, then the next time a version of master is tagged as a release version, the code will be packaged as a source distribution (sdist) and sent off to [pypi](https://pypi.org/search/?q=aide_design).

## Changelog
**aide_design design is in RAPID development. Things will shange significantly!**

We're not tracking changes at the moment here. Once development is at a more reasonable pace, we'll start tracking improvements and bug fixes more carefully!

## Structure
The aide_design package has three distinct levels that work together to design a plant. The first level is composed of base classes that define chemicals, quantities, and other parameters. These classes are created and used within the functional layer to define some basic engineering equations. Lastly, the component classes correspond to objects that are modeled in Fusion 360.

    +----------------------------+
    | COMPONENT CLASSES (.parts) |
    +-------------+              |
    | Classes that correspond to |
    | Fusion components.         |    ^
    +------------+---------------+    |
                 ^                    |
                 |                    |
    +-----------------------+         |
    |  FUNCTIONAL|LAYER     |         | Each layer
    +--------------+        |         | depends on the
    |  This layer has only  |         | layers below
    |  functions that rely  |         | it to function.
    |  on quantity class    |         |
    |  inputs.              |         |
    +------------+----------+         |
                 ^                    |
                 |                    |
    +------------+---------------+    |
    |BASE CLASSES                |    |
    +-----------                 |    |
    |Classes needed to make the  |    |
    |functional and component    |    +
    |class layers work. Such as  |
    |Quantity, HP and DP.        |
    +----------------------------+
