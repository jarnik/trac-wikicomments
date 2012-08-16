# -*- coding: utf-8 -*-
#
# WikiComments plugin for Trac 0.12.3
#
# Author: Jaroslav Meloun <jaroslav dot meloun at gmail dot com>
# License: BSD
# http://trac.edgewall.org/wiki/TracDev/PluginDevelopment

from trac.core import *
from trac.wiki.macros import WikiMacroBase
from trac.wiki import Formatter
from trac.wiki import WikiPage
from trac.web.api import IRequestFilter
from trac.web.chrome import ITemplateProvider, add_script, add_script_data
from trac.web import IRequestHandler
import StringIO
import trac.perm
import random
import string
from datetime import datetime

__all__ = ['WikiCommentsPlugin']

class WikiCommentsPlugin(Component):
    implements(IRequestHandler, IRequestFilter, ITemplateProvider)
    #implements(INavigationContributor, IRequestHandler)

    """WikiMacro formats a given to look like a comment, adding a form to submit followup comments.

    The followup forms are submitted to a <env_name>/wikicomments page, inserted into a page text, and then 
    you are redirected back to the page itself, with an anchor to a new comment.

    Has to be used in a following multi-line macro format:
    
    Example:
    `{{{#!WikiComments author="jaroslav meloun" date="2012-8-16 10:39:11" id="2eb188da0aee2f6272b9651e2b8f1a11"
    Hey, this a comment text!
    =2eb188da0aee2f6272b9651e2b8f1a11
    }}}`

    Upon entering first comment via toolbar button, author name, date and id are filled in automatically (thanks to 
    wikicommentsplugin javascript).
    In followups, they are also filled in automatically (now thanks to the wikicommentsplugin itself).
    """

    # ITemplateProvider#get_htdocs_dirs
    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename
        return [('wikicomments', resource_filename(__name__, 'htdocs'))]
    
    # ITemplateProvider#get_templates_dirs
    def get_templates_dirs(self):
        return []

     # IRequestFilter#pre_process_request
    def pre_process_request(self, req, handler):
        return handler

    # IRequestFilter#post_process_request
    def post_process_request(self, req, template, data, content_type):
        add_script(req, 'wikicomments/wikicomments.js')
        add_script_data(req, { '_wikicomments_author': req.authname })
        return template, data, content_type        
    
    def match_request(self, req):
        return req.path_info == '/add-wiki-comment' and req.args['comment_submit'] == u'Submit'
    def process_request(self, req):
        req.perm.assert_permission ('WIKI_MODIFY')
        page_name = req.args['target_page'][req.args['target_page'].find('wiki')+5:]
        p = WikiPage(self.env, page_name )

        author_name = req.authname
        comment_text = req.args['comment']
        comment_parent = req.args['comment_parent']
        dt = datetime.now()
        comment_date = dt.strftime("%Y-%m-%d %H:%M:%S")
        comment_id = "%032x" % random.getrandbits(128)
        redirect_url = "%s%s#%s" % (req.base_path, req.args['target_page'],comment_id)
        changeset_comment = "%s..." % comment_text[:20]

        insertion_index = string.find( p.text, "=%s" % comment_parent )
        if ( insertion_index != -1 ):
            heads = string.count(p.text,"{{{#!WikiComments",0,insertion_index)
            tails = string.count(p.text,"}}}",0,insertion_index)
            level = heads - tails
            padding = ""
            comment_out = '%s{{{#!WikiComments author="%s" date="%s" id="%s""\n%s%s\n%s=%s\n%s}}}\n' \
                % (padding, author_name,comment_date,comment_id,padding,comment_text,padding,comment_id,padding)
            p.text = p.text[:insertion_index]+comment_out+p.text[insertion_index:]

        p.save( author_name, changeset_comment, req.remote_addr )
        req.redirect(redirect_url)

        #for debug purposes
        #content = req.remote_user+'Hello World!'
        #req.send_response(200)
        #req.send_header('Content-Type', 'text/plain')
        #req.send_header('Content-Length', len(content))
        #req.end_headers()
        #req.write(content)

