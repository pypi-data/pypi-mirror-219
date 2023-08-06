def urlhostmerge(hoststring, host, port):
    if host == None and port == None:
        return hoststring
    r_host = None
    r_port = None

    if hoststring != None:
        if isinstance(hoststring, bytes) or isinstance(hoststring, bytearray):
            hoststring = hoststring.decode('utf-8')
        try:
            (r_host, r_port) = hoststring.split(':')
        except ValueError:
            r_host = hoststring
    if host != None:
        r_host = host
    if port != None:
        r_port = str(port)
    if r_port == None:
        return r_host
    return r_host + ':' + r_port


def urlmerge(default_url, *args):
    r = ['', '', '', '', '']
    if default_url != None:
        for i, v in enumerate(default_url):
            if v == None:
                continue
            r[i] = default_url[i]
    for url in args:
        for i, v in enumerate(url):
            if v == None:
                v = ''
            if len(v) != 0:
                r[i] = url[i]
    return (r[0], r[1], r[2], r[3], r[4],)
