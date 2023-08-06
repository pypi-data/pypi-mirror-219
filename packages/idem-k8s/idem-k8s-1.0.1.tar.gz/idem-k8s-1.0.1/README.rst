========
idem-k8s
========

The Idem Kubernetes provider

About
=====

An Idem plugin to manage Kubernetes resources.

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

You can install ``idem-k8s`` with the Python package installer (PyPI) or from source.

Install from PyPI
+++++++++++++++++

.. code-block:: bash

      pip install idem-k8s

Install from source
+++++++++++++++++++

.. code-block:: bash

   # Clone repo
   git clone git@<your-project-path>/idem-k8s.git
   cd idem-k8s

   # Set up venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .

Development
===========

The ``idem-k8s`` plugin has built-in automatic code generation to extend support for additional Kubernetes resources. Automatic code generation creates over 90% of the code required to support a new Kubernetes resource.

Automatically generate a Kubernetes resource state file with the following command:

.. code-block:: bash

   pop-create k8s \
   --directory ~/idem_k8s/autogen/dummy \  # directory in which the generated state files are stored
   -tv \
   -n idem_k8s \
   --resource apps/v1/DaemonSet  # resource for which state files are generated

The ``resource`` argument follows the format: ``group/version/kind``

For example, to add a resource state for Deployment, the argument is: ``apps/v1/Deployment``

For more information, see the `Kubernetes resource objects documentation <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/#-strong-api-groups-strong>`__.

Usage
=====

Setup
-----

After installation, ``idem-k8s`` execution and state modules are accessible to the pop *hub*.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop hub <https://pop-book.readthedocs.io/en/latest/main/hub.html#>`__

To use ``idem-k8s`` execution and state modules to manage cluster resources, you need to set up authentication in one of the following ways.

**With environment variables**

Set KUBE_CONFIG_PATH and KUBE_CTX environment variables to the Kubernetes configuration file and context found in your ``kube_config`` file.

**In the Idem config file**

Edit the Idem config file to include the ``kube_config_path`` and ``context`` under account extras. Use the following example as a guideline.

.. code:: sls

    acct:
      extras:
        k8s:
          default:
            kube_config_path: ~/.kube/config
            context: default

**In a credentials.yaml file**

Create or edit an Idem credentials.yaml file to add the ``kube_config_path`` and ``context`` to a Kubernetes profile. Use the following example as a guideline.

..  code:: sls

    k8s:
      default:
        kube_config_path: ~/.kube/config
        context: default

For more about Idem credentials files, including recommended steps for encryption and environment variables, see `Authenticating with Idem <https://docs.idemproject.io/getting-started/en/latest/topics/gettingstarted/authenticating.html>`__

You are now ready to use idem-k8s.

States
------

Idem SLS files use states to ensure that resources are in a desired configuration. An idem-k8s SLS file supports three state functions: *present*, *absent*, and *describe*.

present
+++++++

The *present* function ensures that a resource exists. If a resource doesn't exist, running *present* creates it. If the resource already exists, running *present* might leave it unchanged, or update it if there are any configuration changes.

absent
++++++

The *absent* function ensures that a resource does not exist. If the resource exists, running *absent* deletes it. If the resource doesn't exist, running *absent* has no effect.

describe
++++++++

The *describe* function returns a list of all resources in the Kubernetes cluster of the same type as specified in the credential profile.

Accessing States
----------------

States can be accessed by their relative location in ``idem-k8s/k8s/states``.

For example, a Kubernetes deployment state can be created with the *present* function as shown in the following SLS file.

k8s_deployment.sls:

.. code:: sls

    nginx-deployment:
      k8s.apps.v1.deployment.present:
      - metadata:
          name: nginx-deployment
          namespace: default
      - spec:
          replicas: 3
          selector:
            match_labels:
              app: nginx
          strategy:
            rolling_update:
              max_surge: 25%
              max_unavailable: 25%
            type: RollingUpdate
          template:
            metadata:
              labels:
                app: nginx
            spec:
              containers:
              - image: nginx:1.14.20
                image_pull_policy: IfNotPresent
                name: nginx
                ports:
                - container_port: 80
                  protocol: TCP
                termination_message_path: /dev/termination-log
                termination_message_policy: File
              restart_policy: Always

The Idem command to create the preceding deployment state is:

.. code:: bash

    idem state $PWD/k8s_deployment.sls

Current Supported Resources
---------------------------
apiregistration_k8s_io.v1
+++++++++++++++++++++++++

api_service

apps.v1
+++++++

daemon_set

deployment

core.v1
+++++++

config_map

namespace

secret

service_account

service

persistent_volume_claim

rbac.v1
+++++++

cluster_role

cluster_role_binding

role_binding

storage_k8s_io.v1
+++++++++++++++++

storage_class
