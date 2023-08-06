"""Exec module for TLS certificates."""
from typing import Dict

from dict_tools.typing import Computed
from OpenSSL import SSL

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, url: str) -> Computed[Dict]:
    """Get information about the TLS certificates securing a host.

    Args:
      url(str):
        The URL of the website to get the certificates from.

     Returns:
        .. code-block:: python

            {"result": True|False, "comment": list, "ret": None|dict}

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec exec.tls.certificate.get url=https://oidc.eks.us-east-2.amazonaws.com/id/sample

    Request Syntax:
      .. code-block:: sls

          [Idem-state-name]:
            exec.run:
              path: tls.certificate.get
              kwargs:
                  url: 'string'

    Sample response:
        .. code-block:: sls

            url: https://oidc.eks.us-east-2.amazonaws.com/id/sample
            sha1_fingerprint: 9e99a48a9960b14926bb7f3b02e22da2b0ab7280
            issuer:
              C: US
              O: Starfield Technologies, Inc.
              OU: Starfield Class 2 Certification Authority
            not_after: 2034-06-28 17:39:16
            not_before: 2009-09-02 00:00:00
            subject:
              C: US
              ST: Arizona
              L: Scottsdale
              O: Starfield Technologies, Inc.
              CN: Starfield Services Root Certificate Authority - G2
            version: 2
            signature_algorithm: sha256WithRSAEncryption
            serial_number: 12037640545166866303
            resource_id: 12037640545166866303

    Example Usage:
        .. code-block:: sls

            unmanaged-tls_certificate:
              exec.run:
                - path: tls.certificate.get
                - kwargs:
                    url: https://oidc.eks.us-east-2.amazonaws.com/id/sample

            arn:aws:iam::537227425989:www.sample-2.com:
              aws.iam.open_id_connect_provider.absent:
                - name: www.sample-2.com
                - url: https://www.sample-2.com/
                - client_id_list:
                    - sts.amazonaws.com
                - thumbprint_list:
                    - ${exec:unmanaged-tls_certificate:sha1_fingerprint}
                - tags:
                    - Key: alpha.eksctl.io/eksctl-version
                      Value: 0.77.0
                    - Key: alpha.eksctl.io/cluster-name
                      Value: pr-ssc-eks-poc

    """
    result = dict(comment=[], ret=None, result=True)

    try:
        conn = await hub.tool.tls.certificate.get_ssl_connection(ctx, url)
        conn.do_handshake()
    except SSL.WantReadError as e:
        # ignore handshake error, connection has server certificate chain
        hub.log.info(f"SSL handshake error {e.__class__.__name__}: {e}")
    except (SSL.Error, Exception) as e:
        result["comment"].append(f"{e.__class__.__name__}: {e}")
        result["result"] = False
        return result

    try:
        cert = conn.get_peer_cert_chain()[-1]
    finally:
        conn.close()

    resource_translated = await hub.tool.tls.certificate.get_translated_resource(
        cert, url
    )

    result["comment"].append(f"fetched certificate information for url {url}")
    result["ret"] = resource_translated
    return result


async def list_(hub, ctx, url: str) -> Computed[Dict]:
    """Get list of TLS certificate in chain securing a host.

    List information about TLS certificates.

    Args:
      url(str):
        The URL of the website to get the certificates from.

     Returns:
        .. code-block:: python

            {"result": True|False, "comment": list, "ret": list}

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec exec.tls.certificate.list url=https://oidc.eks.us-east-2.amazonaws.com/id/sample

    Request Syntax:
      .. code-block:: sls

          [Idem-state-name]:
            exec.run:
              path: tls.certificate.list
              kwargs:
                  url: 'string'

    Example Usage:
        .. code-block:: sls

            unmanaged-tls_certificate:
              exec.run:
                - path: tls.certificate.list
                - kwargs:
                    url: https://oidc.eks.us-east-2.amazonaws.com/id/sample

    """
    result = dict(comment=[], ret=[], result=True)

    try:
        conn = await hub.tool.tls.certificate.get_ssl_connection(ctx, url)
        conn.do_handshake()
    except SSL.Error as e:
        # ignore handshake error, connection has server certificate chain
        hub.log.info(f"SSL handshake error {e.__class__.__name__}: {e}")
    except Exception as e:
        result["comment"].append(f"{e.__class__.__name__}: {e}")
        result["result"] = False
        return result

    try:
        certs = conn.get_peer_cert_chain()
    finally:
        conn.close()

    ret = []
    for cert in certs:
        resource_translated = await hub.tool.tls.certificate.get_translated_resource(
            cert, url
        )
        ret.append(resource_translated)
    result["ret"] = ret

    result["comment"].append(f"fetched certificates information for url {url}")
    return result
