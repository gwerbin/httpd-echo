#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# httpd-echo
# Copyright (C) 2017 rpatterson
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# httpd-echo
# Copyright (C) 2021 Greg Werbin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

""" A Simple Python HTTP server that echoes the request. """

import socket
import email.message
from six.moves.urllib import parse

try:
    from email.generator import BytesGenerator
except ImportError:
    # BBB Python 2 compatibility
    from email.generator import Generator as BytesGenerator

from six.moves import BaseHTTPServer


class EchoHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ A Simple Python HTTP server that echos the request. """
    def do_GET(self):
        """ Echo a request without a body. """
        message = self.get_message()
        self.send_head()
        BytesGenerator(self.wfile).flatten(message, unixfrom=False)

    do_HEAD = do_GET
    do_OPTIONS = do_GET
    do_DELETE = do_GET

    def do_POST(self):
        """ Echo a request with a body. """
        message = self.get_message()
        try:
            length = int(self.headers["Content-Length"])
        except (TypeError, ValueError) as exc:
            message.set_payload("Invalid Content-Length: {exc}".format(exc))
        else:
            message.set_payload(self.rfile.read(length))
        finally:
            self.send_head()
            BytesGenerator(self.wfile).flatten(message, unixfrom=False)

    do_PUT = do_POST
    do_PATCH = do_POST

    def send_head(self):
        """ Send all the basic, required headers. """
        self.send_response(200)
        self.send_header("Content-Type", "text/rfc822-headers; charset=UTF-8")
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()

    def get_message(self):
        """ Assemble the basic message including query parameters. """
        message = email.message.Message()
        message["Method"] = self.command
        message["Path"] = self.path

        server_url = parse.SplitResult(
            "http",
            "{0}:{1}".format(self.server.server_name, self.server.server_port),
            "",
            "",
            "",
        )

        request_url = parse.urlsplit(server_url.geturl() + self.path)

        for header, value in parse.parse_qs(request_url.query).items():
            message.add_header(header, value[0])

        return message


def build_arg_parser():
    import argparse
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--address",
        "-a",
        default="localhost",
        help="Hostname or IP address to accept requests on.",
    )
    parser.add_argument(
        "--port",
        "-p",
        help="Port to accept requests on.  "
        "If not specified, use the first available port after 8000.",
    )
    return parser


def main(args=None, default_port=8000):
    """ Run the echo HTTP server. """
    args = build_arg_parser().parse_args(args)

    port = args.port
    if port is None:
        port = default_port
        bound = False
        while not bound:
            try:
                httpd = BaseHTTPServer.HTTPServer(
                    (args.address, port), EchoHTTPRequestHandler
                )
            except socket.error:
                port += 1
                if port > 65535:
                    raise ValueError("No available port found")
            else:
                bound = True
    else:
        httpd = BaseHTTPServer.HTTPServer(
            (args.address, int(port)), EchoHTTPRequestHandler
        )

    print("httpd-echo, Copyright © 2017 rpatterson, 2021 Greg Werbin")
    print("This program comes with ABSOLUTELY NO WARRANTY.")
    print("This is Free Software, and you are welcome to redistribute it under certain conditions.")
    print("Echoing HTTP at http://{0}:{1} ...".format(args.address, port))
    httpd.serve_forever()


if __name__ == "__main__":
    main()
