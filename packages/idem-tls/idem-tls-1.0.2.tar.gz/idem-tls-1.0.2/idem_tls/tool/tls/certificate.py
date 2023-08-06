import socket
from datetime import datetime
from urllib.parse import urlparse

from OpenSSL import SSL


async def get_translated_resource(hub, cert, url):
    """
    Converts the raw ssl certificate response to idem exec state output format
    Args:
        cert: TLS certificate details
        url(string): The URL of the website to get the certificates from.
    Returns: Dict with certificate details in output format
    """
    resource_translated = {"url": url}
    resource_translated["resource_id"] = cert.get_serial_number()
    resource_translated["sha1_fingerprint"] = (
        cert.digest("sha1").decode("utf-8").replace(":", "").lower()
    )
    resource_translated["issuer"] = {
        k.decode("utf8"): v.decode("utf8")
        for k, v in dict(cert.get_issuer().get_components()).items()
    }
    resource_translated["not_after"] = str(
        datetime.strptime(cert.get_notAfter().decode("utf-8"), "%Y%m%d%H%M%SZ")
    )
    resource_translated["not_before"] = str(
        datetime.strptime(cert.get_notBefore().decode("utf-8"), "%Y%m%d%H%M%SZ")
    )
    resource_translated["subject"] = {
        k.decode("utf8"): v.decode("utf8")
        for k, v in dict(cert.get_subject().get_components()).items()
    }
    resource_translated["version"] = str(cert.get_version())
    resource_translated["signature_algorithm"] = cert.get_signature_algorithm().decode(
        "utf-8"
    )
    resource_translated["serial_number"] = cert.get_serial_number()
    return resource_translated


async def get_ssl_connection(hub, ctx, url):
    """
    Get the SSL connection for given website URL
    Args:
        url(string): The URL of the website to get the certificates from.
    Returns: SSL connection for url
    """
    method = SSL.TLSv1_2_METHOD
    # Retrieve method from credentials if provided
    if ctx.acct.get("method", None) and getattr(SSL, f"{ctx.acct.method}_METHOD", None):
        method = getattr(SSL, f"{ctx.acct.method}_METHOD", None)
    url_parts = urlparse(url).netloc.split(":")
    host = url_parts[0].strip()
    port = int(url_parts[1]) if len(url_parts) > 1 else 443
    context = SSL.Context(method=method)
    conn = SSL.Connection(
        context, socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    )
    conn.settimeout(5)
    conn.connect((host, port))
    conn.setblocking(1)
    return conn
