#coding: utf-8
from tornado.httpclient import AsyncHTTPClient, HTTPError, HTTPRequest
from tornado import gen

GITHUB_API = 'https://api.github.com'
AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")


@gen.coroutine
def follow(username, token):
    client = AsyncHTTPClient()
    url = '%s/user/following/%s?access_token=%s' % (GITHUB_API, username, token)
    print url
    try:
        req = HTTPRequest(url=url, method="PUT", body='')
        res = yield client.fetch(req, raise_error=False)
        if res.code == 204:
            raise gen.Return(True)
    except HTTPError, e:
        print "code:%d, message:%s" % (e.code, e.message)
    raise gen.Return(False)

@gen.coroutine
def unfollow(username, token):
    client = AsyncHTTPClient()
    url = '%s/user/following/%s?access_token=%s' % (GITHUB_API, username, token)
    try:
        req = HTTPRequest(url=url, method="DELETE", body='')
        res = yield client.fetch(req, raise_error=False)
        if res.code == 204:
            raise gen.Return(True)
    except HTTPError, e:
        print "code:%d, message:%s" % (e.code, e.message)
    raise gen.Return(False)

