.. SPDX-FileCopyrightText: 2025 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

New release of sr.ht go lib and terraform provider to fix update repo bug
#########################################################################

:date: 2025-07-28
:modified: 2025-07-28
:tags: sourcehut, sr.ht, Go, Golang, OpenTofu, Terraform, OpenSource, Bugfix
:description: A bugfix release for the sourcehut Go library and OpenTofu/Terraform provider to fix issues when updating a repository.
:category: Code
:slug: new-release-of-srht-go-lib-and-terraform-provider-to-fix-update-repo-bug
:author: Dominik Wombacher
:lang: en
:transid: new-release-of-srht-go-lib-and-terraform-provider-to-fix-update-repo-bug
:status: published

Today I released new versions of `terraform-provider-sourcehut <https://git.sr.ht/~wombelix/terraform-provider-sourcehut>`_ (v0.2.1)
and the related Go library `sourcehut-go <https://git.sr.ht/~wombelix/sourcehut-go>`_ (v0.1.1).
This is a bugfix release to address an issue when updating a repository description.

End of last year, I published the `initial version of the provider and library <{filename}/posts/2024/release-sourcehut-srht-opentofu-terraform-provider-and-go-library_en.rst>`_
and started using it for my `OpenTofu based management of my git repositories <{filename}/posts/2025/opentofu-based-management-of-my-git-repositories_en.rst>`_.
When I tried to update the description of an existing repository, the provider failed with a very generic error:

:code:`Multiple API errors occured`

This wasn't very helpful, so I started to dig into the code to find the root cause.

The issue was in the `sourcehut-go` library itself. The error handling for multiple errors was just
returning a static string instead of the actual error details from the API.
I improved the error handling to be more specific:

.. code-block:: diff

  --- a/errors.go
  +++ b/errors.go
  @@ -4,6 +4,8 @@

   package sourcehut

  +import "strings"
  +
   // Ensure that the build fails if Error and Errors don't implement error.
   var _, _ error = (*Error)(nil), (*Errors)(nil)

  @@ -34,7 +36,18 @@ type Errors []Error

   // Error satisfies the error interface for Errors.
   func (err Errors) Error() string {
  -       return "Multiple API errors occured"
  +       if len(err) == 0 {
  +               return "[WARN] Errors.Error() triggered with err length 0"
  +       }
  +       if len(err) == 1 {
  +               return err[0].Error()
  +       }
  +
  +       var details []string
  +       for _, e := range err {
  +               details = append(details, e.Reason)
  +       }
  +       return strings.Join(details, "; ")
   }

   // StatusCode returns the HTTP status code of the request that unmarshaled this

With this change in place, the error message became much more useful:

:code:`A repository with this name already exists.; validation failed`

This new error pointed me in the right direction. I checked the
`git.sr.ht legacy API documentation <https://web.archive.org/web/20250207112955/https://man.sr.ht/git.sr.ht/api.md#repository-resource>`__
and found the problem. The API endpoint for updating a repository treats the `name` field as optional.
If you provide a name that is different from the current one, it triggers a rename and a redirect.
If you provide the same name, it fails because a repository with that name already exists.

To fix this, I changed the `UpdateRepo` function to only include the `name`
in the payload if it's actually different from the old name.

.. code-block:: diff

  --- a/git/git.go
  +++ b/git/git.go
  @@ -8,6 +8,7 @@ package git
   import (
          "bytes"
          "encoding/json"
  +       "fmt"
          "io"
          "net/http"
          "net/url"
  @@ -152,15 +153,25 @@ func (c *Client) NewRepo(name, description string, visibility RepoVisibility) (*
   // If repo.Name differs from oldName, a redirect from the old name to the new
   // name.
   func (c *Client) UpdateRepo(oldName string, repo *Repo) error {
  -       jsonRepo, err := json.Marshal(struct {
  -               Name string `json:"name"`
  -               Desc string `json:"description"`
  -               Visi string `json:"visibility"`
  -       }{
  -               Name: repo.Name,
  -               Desc: repo.Description,
  -               Visi: string(repo.Visibility),
  -       })
  +       updateData := make(map[string]interface{})
  +
  +       // Only include name if it's different from oldName (for renaming)
  +       if repo.Name != "" && repo.Name != oldName {
  +               updateData["name"] = repo.Name
  +       }
  +
  +       // Always include description, allows empty as well
  +       updateData["description"] = repo.Description
  +
  +       if repo.Visibility != "" {
  +               // Validate visibility value
  +               if repo.Visibility != VisibilityPublic && repo.Visibility != VisibilityUnlisted && repo.Visibility != VisibilityPrivate {
  +                       return fmt.Errorf("invalid visibility: %s (must be public, unlisted, or private)", repo.Visibility)
  +               }
  +               updateData["visibility"] = string(repo.Visibility)
  +       }
  +
  +       jsonRepo, err := json.Marshal(updateData)
          if err != nil {

I used the opportunity to refactor the code a bit and to add a value validation for the repo visibility.

With these two fixes, updating a repository description with my sourcehut terraform provider now works as expected.

The new versions are available in the `OpenTofu <https://search.opentofu.org/provider/wombelix/sourcehut/latest>`_
and `Terraform <https://registry.terraform.io/providers/wombelix/sourcehut/latest>`_ registry.

The OpenTofu Registry WebUI is often behind the API, even if it doesn't show v0.2.1 yet, it is already available.
You can verify it by running :code:`curl https://registry.opentofu.org/v1/providers/wombelix/sourcehut/versions`.
