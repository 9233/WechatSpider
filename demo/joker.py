# -*- coding: utf-8 -*-

import mitmproxy.http
from mitmproxy import ctx, http


class Joker:
    def request(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host != "www.baidu.com" or not flow.request.path.startswith("/s"):
            return

        if "wd" not in flow.request.query.keys():
            ctx.log.warn("can not get search word from %s" % flow.request.pretty_url)
            return

        ctx.log.info("catch search word: %s" % flow.request.query.get("wd"))
        flow.request.query.set_all("wd", ["360 search"])

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host != "www.so.com":
            return

        text = flow.response.get_text()
        text = text.replace("search", "please use google")
        flow.response.set_text(text)

    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host == "www.google.com":
            flow.response = http.HTTPResponse.make(404)