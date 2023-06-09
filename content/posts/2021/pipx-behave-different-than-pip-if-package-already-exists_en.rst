pipx behave different than pip if package already exists
########################################################

:date: 2021-09-23
:modified: 2021-09-23
:tags: Python, Code, pipx, pip
:description: pipx rc 1 if package exists
:category: Code
:slug: pipx-behave-different-than-pip-if-package-already-exists
:author: Dominik Wombacher
:lang: en
:transid: pipx-behave-different-than-pip-if-package-already-exists 
:status: published

I decided to put as much as possible of my local config into an Ansible Playbook. 
Makes it easier to track what I install and change, also to setup from scratch should it necessary.

In the past I mainly used `pip` in combination with `venv` to install Python stuff. 
Changing for most of it to `pipx` seems logical, it will take care about the necessary *venvs* on it's own.

Just had to learn that the return code of `pip` is **0** but from `pipx` it's **1** in case a package already exists. 

Why does it matter? Not the most elegant solution but I decided to just use `command` to trigger *pip* / *pipx* from my Playbook:

.. code-block:: yaml

  - name: Python Package Installation (pip)
    command: "python3 -m pip install --user {{ item }}"
    changed_when: false
    loop:
      - pipx
      - nox

  - name: Python Package Installation (pipx)
    command: "pipx install {{ item }}"
    changed_when: false
    loop:
      - poetry
      - duplicity
      - pre-commit

No problem with `pip`, but `pipx` failed after the first run.

There was an older `GitHub Issue <https://github.com/pypa/pipx/issues/125>`_, based on the comments, 
`pipx` was supposed to behave smilar as `pip` and also use return code 0 since v0.13 already. 
After some research I found the `Pull Request <https://github.com/pypa/pipx/pull/560>`_ 
that reverted the earlier change during some re-factoring.

Thanks to the great improvements in that PR, it was just a very small change necessary to restore the 
functionality introduced in `Commit 11b853e <https://github.com/pypa/pipx/commit/11b853e9c6926b32133b27822516b2a5b4f35411>`_:

.. code-block:: diff

  diff --git a/docs/changelog.md b/docs/changelog.md
  index 0a95ce15..67d14929 100644
  --- a/docs/changelog.md
  +++ b/docs/changelog.md
  @@ -1,6 +1,7 @@
   dev
   
   - Fixed `pipx list` output phrasing to convey that python version displayed is the one with which package was installed. 
  +- Fixed `pipx install` to provide return code 0 if venv already exists, similar to pip’s behavior. (#736)
   
   0.16.4
   
  diff --git a/src/pipx/constants.py b/src/pipx/constants.py
  index 4fe2d58b..11fc013f 100644
  --- a/src/pipx/constants.py
  +++ b/src/pipx/constants.py
  @@ -21,7 +21,7 @@
   # pipx shell exit codes
   EXIT_CODE_OK = ExitCode(0)
   EXIT_CODE_INJECT_ERROR = ExitCode(1)
  -EXIT_CODE_INSTALL_VENV_EXISTS = ExitCode(1)
  +EXIT_CODE_INSTALL_VENV_EXISTS = ExitCode(0)
   EXIT_CODE_LIST_PROBLEM = ExitCode(1)
   EXIT_CODE_UNINSTALL_VENV_NONEXISTENT = ExitCode(1)
   EXIT_CODE_UNINSTALL_ERROR = ExitCode(1)
  diff --git a/tests/test_install.py b/tests/test_install.py
  index 941f4c01..0eb2d9cc 100644
  --- a/tests/test_install.py
  +++ b/tests/test_install.py
  @@ -109,7 +109,7 @@ def test_install_no_packages_found(pipx_temp_env, capsys):
   
   def test_install_same_package_twice_no_force(pipx_temp_env, capsys):
       assert not run_pipx_cli(["install", "pycowsay"])
  -    assert run_pipx_cli(["install", "pycowsay"])
  +    assert not run_pipx_cli(["install", "pycowsay"])
       captured = capsys.readouterr()
       assert (
           "'pycowsay' already seems to be installed. Not modifying existing installation"

Related Pull Request: https://github.com/pypa/pipx/pull/736

Merged into `pipx/main` on 25th September 2021

That's a good example why I love and prefer Open Source, I could fix the Problem on my own and share the improvement with the community, within a few days it was already merged and will be part of the next Release.
