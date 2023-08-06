# standard imports
from socket import getservbyname
import urllib.parse


def url_apply_port(url_parts, as_origin=False):
    url_parts_origin_host = url_parts[1].split(":")
    host = url_parts_origin_host[0]
    port = None
    try:
        port = ':' + url_parts_origin_host[1]
    except IndexError:
        port = ':' + str(getservbyname(url_parts[0]))
        #logg.info('changed origin with missing port number from {} to {}'.format(url_parts[1], host))
    host += port
    path = ''
    query = ''
    fragment = ''
    if not as_origin:
        path=url_parts[2]
        query=url_parts[3]
        fragment=url_parts[4]

    return urllib.parse.SplitResult(
            scheme=url_parts[0],
            netloc=host,
            path=path,
            query=query,
            fragment=fragment,
            )


def url_apply_port_string(url_string, as_origin=False):
    url_parts = urllib.parse.urlsplit(url_string)
    u = url_apply_port(url_parts, as_origin=as_origin)
    return urllib.parse.urlunsplit(u)
