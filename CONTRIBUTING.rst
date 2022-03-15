Contributing
============

Contributions are welcome in the form of bug reports or pull requests.

Bug Reports
-----------
Please report any bugs and enhancement requests by opening issues on github.

There are plenty of `good resources <http://www.drmaciver.com/2013/09/how-to-submit-a-decent-bug-report/>`_ describing how to create
good bug reports. They will not be repeated in detail here, but in general, the bug report include where appropriate:

* relevant software versions (Python runtime, driver version, cython version, server version)
* details for how to produce (e.g. a test script or written procedure)
  * any effort to isolate the issue in reproduction is much-appreciated
* stack trace from a crashed runtime

Pull Requests
-------------
If you're able to fix a bug yourself, you can `fork the repository <https://help.github.com/articles/fork-a-repo/>`_ and submit a `Pull Request <https://help.github.com/articles/using-pull-requests/>`_ with the fix.
Please include tests demonstrating the issue and fix. 

Contribution License Agreement
------------------------------


Design and Implementation Guidelines
------------------------------------
- We support Python 2.7+, so any changes must work in any of these runtimes (we use ``six``, ``futures``, and some internal backports for compatability)
- We have integrations (notably Cassandra cqlsh) that require pure Python and minimal external dependencies. We try to avoid new external dependencies. Where compiled extensions are concerned, there should always be a pure Python fallback implementation.
- This project follows `semantic versioning <http://semver.org/>`_, so breaking API changes will only be introduced in major versions.
- Legacy ``cqlengine`` has varying degrees of overreaching client-side validation. Going forward, we will avoid client validation where server feedback is adequate and not overly expensive.
- When writing tests, try to achieve maximal coverage in unit tests (where it is faster to run across many runtimes). Integration tests are good for things where we need to test server interaction, or where it is important to test across different server versions (emulating in unit tests would not be effective).
