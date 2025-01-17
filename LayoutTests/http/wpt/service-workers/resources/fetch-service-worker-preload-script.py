import os
import hashlib
import json


def main(request, response):
    token = request.GET[b'token']
    testId = hashlib.md5(token).hexdigest()
    countId = hashlib.md5(token + b'-count').hexdigest()

    if request.method == "POST":
        request.server.stash.take(testId)
        request.server.stash.put(testId, request.GET[b'value'])
        response.headers.set(b"Content-Type", b"text/ascii")
        return b"updated to " + request.GET[b'value']

    if request.GET.first(b"count", False):
        count = request.server.stash.take(countId)
        if not count:
            count = 0
        response.headers.set(b"Content-Type", b"text/ascii")
        return str(count)

    count = request.server.stash.take(countId)
    if not count:
        count = 0
    count = count + 1
    request.server.stash.put(countId, count)

    value = request.server.stash.take(testId)
    if not value:
        value = b"nothing"
    response.headers.set(b"Cache-Control", b"no-cache")

    if b"download" in request.GET:
        response.headers.set(b"Content-Type", b"text/vcard")
        return value.decode()

    response.headers.set(b"Content-Type", b"text/html")
    return "<html><body><script>window.value = '%s';</script></body></html>" % value.decode()
