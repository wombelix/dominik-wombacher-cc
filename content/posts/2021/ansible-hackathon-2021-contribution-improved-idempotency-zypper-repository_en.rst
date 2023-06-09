Ansible Hackathon 2021 Contribution: Improved idempotency - zypper_repository
#############################################################################

:date: 2021-10-01
:modified: 2021-10-01
:tags: Ansible, Contribution, Community, Hackathon
:description: Ansible Hackathon 2021 Contribution
:category: Code
:slug: ansible-hackathon-2021-contribution-improved-idempotency-zypper-repository
:author: Dominik Wombacher
:lang: en
:transid: ansible-hackathon-2021-contribution-improved-idempotency-zypper-repository 
:status: published

Parallel to the `Ansible Contributor Summit 2021.09 <https://hackmd.io/@ansible-community/contrib-summit-202109>`_ and the 
`Ansible Fest 2021 <https://reg.ansiblefest.redhat.com/flow/redhat/ansible21/regGenAttendee/login>`_ 
there was a **Hackathon** with focus on first time Contributor. 
Even though I use Ansible since years, but mainly from a User perspective (Playbooks, Roles, Collections), 
I wasn't officially Contributing to a Plugin or Module yet.

I did some smaller bugfixing or improvements in the past, but mainly for myself or a very unique use case at work. 
So far I never worked on one of the GitHub Issues or created a PR for any of the 
`community modules <https://github.com/ansible-collections/>`_, something I always wanted to change.

As already mentioned a `few days ago <{filename}pipx-behave-different-than-pip-if-package-already-exists_en.rst>`_, 
I started putting all my configs in Ansible Playbook(s). 
I'm using openSUSE Tumbleweed with some additional repositories and wanted to managed them also via Ansible. 
I prefer *.repo* files, they are very convinient, you don't have to manage anything manually. 
There is a Module available (*community.general.zypper_repository*) but there was a 
`bug <https://github.com/ansible-collections/community.general/issues/1791>`_ regarding the idempotency when using *.repo* files.

You could add a new repository by using a *.repo* file but then every future run will fail, 
also removing a repository the same way wasn't working either.

So I decided to work on this Issue during the Hackathon and get some Hands-On Experience contributing to Ansible Collections. 

Due to the fact that you need at least a `name` and `baseurl` to identify if something need to be added, changed or removed, 
I decided to download the *.repo* file, parse it and work with the actual values. 
The previous Implementation was calling `zypper` more or less directly with the URL to the file as Parameter, which caused the reported issues. 

Now the **community.general.zypper_repository** module supports *.repo* files via URL or from a local path, 
behave as expected in regards to idempotency and is fully covered by integration tests.

There were always `Ansible Community.General Maintainer <https://github.com/ansible-collections/community.general/blob/main/commit-rights.md#people>`_ 
available via Matrix to answer questions, pointing into the right direction and assisting in case of any problems. 

It was a great experience for me! I can just recommend such Events, I've learned a lot during these two days and finished my 
`Pull Request <https://github.com/ansible-collections/community.general/pull/3474>`_, 
which also fixes a `second issue <https://github.com/ansible-collections/community.general/issues/3466>`_.

All CI tests are finally passed, feedback from the first Reviewer is positive, 
fingers crossed everything will be fine and the PR merged soon :)

I will write a little more about the Summit, my expiriences and things learned or found useful, 
to get started contributing, within the next days in a separate post.

Even though you can find all details in my `Pull Request on GitHub <https://github.com/ansible-collections/community.general/pull/3474>`_, 
I don't want to force navigating to a different site, so let me share the *diff* (at time of writing) here as well:

.. code-block:: diff

  diff --git a/changelogs/fragments/3474-zypper_repository_improve_repo_file_idempotency.yml b/changelogs/fragments/3474-zypper_repository_improve_repo_file_idempotency.yml
  new file mode 100644
  index 00000000000..4f3b56329cb
  --- /dev/null
  +++ b/changelogs/fragments/3474-zypper_repository_improve_repo_file_idempotency.yml
  @@ -0,0 +1,7 @@
  +bugfixes:
  +  - zypper_repository - when an URL to a .repo file was provided in option 
  +    ``repo=`` and ``state=present`` only the first run was successful, 
  +    future runs failed due to missing checks prior starting zypper.
  +    Usage of ``state=absent`` in combination with a .repo file was not 
  +    working either (https://github.com/ansible-collections/community.general/issues/1791,
  +    https://github.com/ansible-collections/community.general/issues/3466).

  diff --git a/plugins/modules/packaging/os/zypper_repository.py b/plugins/modules/packaging/os/zypper_repository.py
  index 38aeab618e8..a29650a17ef 100644
  --- a/plugins/modules/packaging/os/zypper_repository.py
  +++ b/plugins/modules/packaging/os/zypper_repository.py
  @@ -137,6 +137,10 @@
   
   from ansible.module_utils.basic import AnsibleModule, missing_required_lib
   
  +from ansible.module_utils.urls import fetch_url
  +from ansible.module_utils.common.text.converters import to_text
  +from ansible.module_utils.six.moves import configparser, StringIO
  +from io import open
   
   REPO_OPTS = ['alias', 'name', 'priority', 'enabled', 'autorefresh', 'gpgcheck']
   
  @@ -382,12 +386,62 @@ def exit_unchanged():
           if not alias and state == "present":
               module.fail_json(msg='Name required when adding non-repo files.')
   
  +    # Download / Open and parse .repo file to ensure idempotency
  +    if repo and repo.endswith('.repo'):
  +        if repo.startswith(('http://', 'https://')):
  +            response, info = fetch_url(module=module, url=repo, force=True)
  +            if not response or info['status'] != 200:
  +                module.fail_json(msg='Error downloading .repo file from provided URL')
  +            repofile_text = to_text(response.read(), errors='surrogate_or_strict')
  +        else:
  +            try:
  +                with open(repo, encoding='utf-8') as file:
  +                    repofile_text = file.read()
  +            except IOError:
  +                module.fail_json(msg='Error opening .repo file from provided path')
  +
  +        repofile = configparser.ConfigParser()
  +        try:
  +            repofile.readfp(StringIO(repofile_text))
  +        except configparser.Error:
  +            module.fail_json(msg='Invalid format, .repo file could not be parsed')
  +
  +        # No support for .repo file with zero or more than one repository
  +        if len(repofile.sections()) != 1:
  +            err = "Invalid format, .repo file contains %s repositories, expected 1" % len(repofile.sections())
  +            module.fail_json(msg=err)
  +
  +        section = repofile.sections()[0]
  +        repofile_items = dict(repofile.items(section))
  +        # Only proceed if at least baseurl is available
  +        if 'baseurl' not in repofile_items:
  +            module.fail_json(msg='No baseurl found in .repo file')
  +
  +        # Set alias (name) and url based on values from .repo file
  +        alias = section
  +        repodata['alias'] = section
  +        repodata['url'] = repofile_items['baseurl']
  +
  +        # If gpgkey is part of the .repo file, auto import key
  +        if 'gpgkey' in repofile_items:
  +            auto_import_keys = True
  +
  +        # Map additional values, if available
  +        if 'name' in repofile_items:
  +            repodata['name'] = repofile_items['name']
  +        if 'enabled' in repofile_items:
  +            repodata['enabled'] = repofile_items['enabled']
  +        if 'autorefresh' in repofile_items:
  +            repodata['autorefresh'] = repofile_items['autorefresh']
  +        if 'gpgcheck' in repofile_items:
  +            repodata['gpgcheck'] = repofile_items['gpgcheck']
  +
       exists, mod, old_repos = repo_exists(module, repodata, overwrite_multiple)
   
  -    if repo:
  -        shortname = repo
  -    else:
  +    if alias:
           shortname = alias
  +    else:
  +        shortname = repo
   
       if state == 'present':
           if exists and not mod:

  diff --git a/tests/integration/targets/zypper_repository/files/systemsmanagement_Uyuni_Utils.repo b/tests/integration/targets/zypper_repository/files/systemsmanagement_Uyuni_Utils.repo
  new file mode 100644
  index 00000000000..1df76802a70
  --- /dev/null
  +++ b/tests/integration/targets/zypper_repository/files/systemsmanagement_Uyuni_Utils.repo
  @@ -0,0 +1,7 @@
  +[systemsmanagement_Uyuni_Utils]
  +name=Several utilities to develop, build or release Uyuni (openSUSE_Leap_15.3)
  +type=rpm-md
  +baseurl=https://download.opensuse.org/repositories/systemsmanagement:/Uyuni:/Utils/openSUSE_Leap_15.3/
  +gpgcheck=1
  +gpgkey=https://download.opensuse.org/repositories/systemsmanagement:/Uyuni:/Utils/openSUSE_Leap_15.3/repodata/repomd.xml.key
  +enabled=1

  diff --git a/tests/integration/targets/zypper_repository/meta/main.yml b/tests/integration/targets/zypper_repository/meta/main.yml
  new file mode 100644
  index 00000000000..1810d4bec98
  --- /dev/null
  +++ b/tests/integration/targets/zypper_repository/meta/main.yml
  @@ -0,0 +1,2 @@
  +dependencies:
  +  - setup_remote_tmp_dir

  diff --git a/tests/integration/targets/zypper_repository/tasks/test.yml b/tests/integration/targets/zypper_repository/tasks/test.yml
  index e2b2f8473b6..1033ee1e7d5 100644
  --- a/tests/integration/targets/zypper_repository/tasks/test.yml
  +++ b/tests/integration/targets/zypper_repository/tasks/test.yml
  @@ -19,6 +19,8 @@
           - testrefresh
           - testprio
           - Apache_PHP_Modules
  +        - systemsmanagement_Uyuni_Stable
  +        - systemsmanagement_Uyuni_Utils
   
       - name: collect repo configuration after test
         shell: "grep . /etc/zypp/repos.d/*"

  diff --git a/tests/integration/targets/zypper_repository/tasks/zypper_repository.yml b/tests/integration/targets/zypper_repository/tasks/zypper_repository.yml
  index 4490ddca7db..dbd9bb0064b 100644
  --- a/tests/integration/targets/zypper_repository/tasks/zypper_repository.yml
  +++ b/tests/integration/targets/zypper_repository/tasks/zypper_repository.yml
  @@ -4,6 +4,11 @@
       state: absent
     register: zypper_result
   
  +- name: verify no change on test repo deletion
  +  assert:
  +    that:
  +      - "not zypper_result.changed"
  +
   - name: Add test repo
     community.general.zypper_repository:
       name: test
  @@ -51,7 +56,8 @@
     command: zypper -x lr testrefresh
     register: zypper_result
   
  -- assert:
  +- name: verify autorefresh option set properly
  +  assert:
       that:
         - '"autorefresh=\"0\"" in zypper_result.stdout'
   
  @@ -66,7 +72,8 @@
     command: zypper -x lr testprio
     register: zypper_result
   
  -- assert:
  +- name: verify priority option set properly
  +  assert:
       that:
         - '"priority=\"55\"" in zypper_result.stdout'
   
  @@ -88,7 +95,8 @@
     command: zypper lr chrome2
     register: zypper_result2
   
  -- assert:
  +- name: ensure same url cause update of existing repo even if name differ
  +  assert:
       that:
         - "zypper_result1.rc != 0"
         - "'not found' in zypper_result1.stderr"
  @@ -108,7 +116,8 @@
     command: zypper lr samename
     register: zypper_result
   
  -- assert:
  +- name: ensure url get updated on repo with same name
  +  assert:
       that:
         - "'/science/' not in zypper_result.stdout"
         - "'/devel:/languages:/ruby/' in zypper_result.stdout"
  @@ -140,7 +149,8 @@
       state: present
     register: add_repo_again
   
  -- assert:
  +- name: no update in case of $releasever usage in url
  +  assert:
       that:
         - add_repo is changed
         - add_repo_again is not changed
  @@ -151,10 +161,21 @@
       state: absent
     register: remove_repo
   
  -- assert:
  +- name: verify repo was removed
  +  assert:
       that:
         - remove_repo is changed
   
  +- name: get list of files in /etc/zypp/repos.d/
  +  command: ls /etc/zypp/repos.d/
  +  changed_when: false
  +  register: releaseverrepo_etc_zypp_reposd
  +
  +- name: verify removal of file releaseverrepo.repo in /etc/zypp/repos.d/
  +  assert:
  +    that:
  +      - "'releaseverrepo' not in releaseverrepo_etc_zypp_reposd.stdout"
  +
   - name: add a repo by basearch
     community.general.zypper_repository:
       name: basearchrepo
  @@ -169,7 +190,8 @@
       state: present
     register: add_repo_again
   
  -- assert:
  +- name: no update in case of $basearch usage in url
  +  assert:
       that:
         - add_repo is changed
         - add_repo_again is not changed
  @@ -180,6 +202,74 @@
       state: absent
     register: remove_repo
   
  -- assert:
  +- name: verify repo was removed
  +  assert:
       that:
         - remove_repo is changed
  +
  +- name: add new repository via url to .repo file
  +  community.general.zypper_repository:
  +    repo: http://download.opensuse.org/repositories/systemsmanagement:/Uyuni:/Stable/openSUSE_Leap_{{ ansible_distribution_version }}/systemsmanagement:Uyuni:Stable.repo
  +    state: present
  +  register: added_by_repo_file
  +
  +- name: get repository details from zypper
  +  command: zypper lr systemsmanagement_Uyuni_Stable
  +  register: get_repository_details_from_zypper
  +
  +- name: verify adding via .repo file was successful
  +  assert:
  +    that:
  +      - "added_by_repo_file is changed"
  +      - "get_repository_details_from_zypper.rc == 0"
  +      - "'/systemsmanagement:/Uyuni:/Stable/' in get_repository_details_from_zypper.stdout"
  +
  +- name: add same repository via url to .repo file again to verify idempotency
  +  community.general.zypper_repository:
  +    repo: http://download.opensuse.org/repositories/systemsmanagement:/Uyuni:/Stable/openSUSE_Leap_{{ ansible_distribution_version }}/systemsmanagement:Uyuni:Stable.repo
  +    state: present
  +  register: added_again_by_repo_file
  +
  +- name: verify nothing was changed adding a repo with the same .repo file
  +  assert:
  +    that:
  +      - added_again_by_repo_file is not changed
  +
  +- name: remove repository via url to .repo file
  +  community.general.zypper_repository:
  +    repo: http://download.opensuse.org/repositories/systemsmanagement:/Uyuni:/Stable/openSUSE_Leap_{{ ansible_distribution_version }}/systemsmanagement:Uyuni:Stable.repo
  +    state: absent
  +  register: removed_by_repo_file
  +
  +- name: get list of files in /etc/zypp/repos.d/
  +  command: ls /etc/zypp/repos.d/
  +  changed_when: false
  +  register: etc_zypp_reposd
  +
  +- name: verify removal via .repo file was successful, including cleanup of local .repo file in /etc/zypp/repos.d/
  +  assert:
  +    that:
  +      - "removed_by_repo_file"
  +      - "'/systemsmanagement:/Uyuni:/Stable/' not in etc_zypp_reposd.stdout"
  +
  +- name: Copy test .repo file
  +  copy:
  +    src: 'files/systemsmanagement_Uyuni_Utils.repo'
  +    dest: '{{ remote_tmp_dir }}'
  +
  +- name: add new repository via local path to .repo file
  +  community.general.zypper_repository:
  +    repo: "{{ remote_tmp_dir }}/systemsmanagement_Uyuni_Utils.repo"
  +    state: present
  +  register: added_by_repo_local_file
  +
  +- name: get repository details for systemsmanagement_Uyuni_Utils from zypper
  +  command: zypper lr systemsmanagement_Uyuni_Utils
  +  register: get_repository_details_from_zypper_for_systemsmanagement_Uyuni_Utils
  +
  +- name: verify adding repository via local .repo file was successful
  +  assert:
  +    that:
  +      - "added_by_repo_local_file is changed"
  +      - "get_repository_details_from_zypper_for_systemsmanagement_Uyuni_Utils.rc == 0"
  +      - "'/systemsmanagement:/Uyuni:/Utils/' in get_repository_details_from_zypper_for_systemsmanagement_Uyuni_Utils.stdout"
