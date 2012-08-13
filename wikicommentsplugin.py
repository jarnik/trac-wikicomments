# -*- coding: utf-8 -*-
#
# AutoNav macro for Trac 0.11
#
# Author: Anders Jansson <anders dot jansson at kastanj dot net>
# License: BSD
# Modified by: 
#   Andrew Stromnov <stromnov at gmail dot com>
#   Christian Boos <cboos at neuf fr>
# http://trac.edgewall.org/wiki/TracDev/PluginDevelopment

from genshi.builder import tag
from genshi.core import Markup

from trac.core import *
from trac.wiki.api import parse_args
from trac.wiki.macros import WikiMacroBase
from trac.wiki import Formatter
from trac.wiki import WikiPage
from trac.web.chrome import INavigationContributor
from trac.web import IRequestHandler
from trac.util.html import html
import StringIO
import trac.perm

__all__ = ['WikiCommentsPlugin']


class WikiCommentsPlugin(Component):
    implements(INavigationContributor, IRequestHandler)

    """AutoNav finds all references in the wiki section to this Document

    It then shows them in a sorted list.

    Used with no arguments only produces a list from the database. Arguments
    sent to AutoNav will be merged inside the list too. Separate the
    arguments with comma.
    
    Example:
    `[[AutoNav()]]`	-> only references
    
    `[[AutoNav(MyPage)]]` -> references merged and sorted with MyPage
         
    `[[AutoNav(MyPage, MyPageToo, MyPageThree)]]` -> references merged with MyPage, MyPageToo and MyPageThree
    """
    # INavigationContributor methods
    def get_active_navigation_item(self, req):
        #self.env.log.debug("*** Hey, nav item  ")
        return 'helloworld'
    def get_navigation_items(self, req):
        #self.env.log.debug("*** Hey, nav getitem  ")
        yield ('mainnav', 'helloworld',
            html.A('Hello world', href= req.href.helloworld()))
    
    def match_request(self, req):
        #self.env.log.debug("*** Hey, req match  ")
        #return req.path_info == '/helloworld'
        self.env.log.debug("*** Hey, req args %s " % req.args )
        return req.args['hello'] == u'1'
    def process_request(self, req):
        #self.env.log.debug("*** Hey, req process  ")
        #self.perm.assert_permission (perm.WIKI_MODIFY)
        #self.req.hdf.setValue('wiki.action', 'addComment')
        p = WikiPage(self.env, "TestParent")

        author_name = req.remote_user
        comment_text = "lorem ipsum dolor sit amet"
        #comment_text = req.args['comment']
        comment_parent = '12312'
        comment_date = '2012-07-12 12:10:31'
        comment_id = "%032x" % random.getrandbits(128)
        comment_out = '{{{#!WikiComments author="sykysanchan" date="2012-10-20 15:45:30" id="1""\n%s\n}}}' 
            % (author_name,comment_date,comment_id,comment_text)

        changeset_comment = "%s..." % comment_text[:20]

        # add comment to wiki page text
        p.text = p.text + comment_out

        p.save( author_name, changeset_comment, req.remote_addr )

        content = 'Hello World!'+p.text.encode('ascii','ignore')
        req.send_response(200)
        req.send_header('Content-Type', 'text/plain')
        req.send_header('Content-Length', len(content))
        req.end_headers()
        req.write(content)
    

