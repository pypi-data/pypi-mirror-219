========
idem-tls
========

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

The Idem TLS provider

About
=====

An Idem plugin to work with TLS keys and certificates.

The plugin fetches TLS certificate information for use with other Idem plugins, such as ``idem-aws``, when creating resources that expose TLS services.

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring together concepts and wisdom from the history of computing in new ways to solve modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.7+
* git *(if installing from source or contributing to the project)*

  To contribute to the project and set up your local development environment, see ``CONTRIBUTING.rst`` in the source repository for this project.

Installation
------------

You can install ``idem-tls`` with the Python package installer (PyPI) or from source.

Install from PyPI
+++++++++++++++++

.. code-block:: bash

      pip install idem-tls

Install from Source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@<your-project-path>/idem-tls.git
   cd idem-tls

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .

Usage
=====

Setup
-----

After installation, ``idem-tls`` execution and state modules are accessible to the pop *hub*.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop hub <https://pop-book.readthedocs.io/en/latest/main/hub.html#>`__

To set the TLS method that ``idem-tls`` uses, configure it in your credentials.yaml file.

Credentials for ``idem-tls`` are optional. If you don't configure a TLS method, the plugin uses TLSv1 by default.

credentials.yaml:

..  code:: sls

    tls:
      default:
        method: TLSv1_2

For more about Idem credentials files, including recommended steps for encryption and environment variables, see `Authenticating with Idem <https://docs.idemproject.io/getting-started/en/latest/topics/gettingstarted/authenticating.html>`__

You are now ready to use idem-tls.

Exec Module
-----------

An SLS file specifies the desired state of a resource. You can run an exec module within an SLS file using the ``exec.run`` state, where the exec module returns a new state that can be referenced with argument binding.

The ``idem-tls`` plugin exec module supports TLS certificate ``get`` and ``list`` operations.

* ``tls.certificate.get``

  Return the root CA certificate for a given URL.

* ``tls.certificate.list``

  Return the certificate chain for a given URL.

Syntax:

..  code:: sls

    [Idem-state-name]:
      exec.run:
        - path: tls.certificate.get
        - kwargs:
            url: 'string'

Example:

..  code:: sls

    unmanaged-tls_certificate:
      exec.run:
        - path: tls.certificate.get
        - kwargs:
            url: https://oidc.eks.us-east-2.amazonaws.com/id/sample
    oidc.eks.us-east-2.amazonaws.com/id/sample:
        aws.iam.open_id_connect_provider.present:
          name: oidc.eks.us-east-2.amazonaws.com/id/sample
          resource_id: oidc.eks.us-east-2.amazonaws.com/id/sample
          url:  https://oidc.eks.us-east-2.amazonaws.com/id/sample
          client_id_list:
            - sample_client
          thumbprint_list:
            - ${exec:unmanaged-tls_certificate:sha1_fingerprint}
          tags:
            - Key: tag-key-1
              Value: tag-value-1
            - Key: tag-key-2
              Value: tag-value-2

Idem command line example:

.. code:: bash

     idem exec exec.tls.certificate.list url=https://oidc.eks.us-east-2.amazonaws.com/id/sample

Current Supported Resource States
---------------------------------

tls
+++

certificate
