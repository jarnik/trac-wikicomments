# -*- coding: utf-8 -*-
#
# AutoNav macro for Trac 0.11
#
# Author: Anders Jansson <anders dot jansson at kastanj dot net>
# License: BSD
# Modified by: 
#   Andrew Stromnov <stromnov at gmail dot com>
#   Christian Boos <cboos at neuf fr>

from genshi.builder import tag
from genshi.core import Markup

from trac.core import *
from trac.wiki.api import parse_args
from trac.wiki.macros import WikiMacroBase
from trac.wiki import Formatter
import StringIO

__all__ = ['WikiCommentsMacro']

class WikiCommentsMacro(WikiMacroBase):
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
    
    def expand_macro(self, formatter, name, text, args):
        out = StringIO.StringIO()
        Formatter(self.env, formatter.context).format(text, out)
        text = out.getvalue()
        comment_author = args['author']
        comment_date = args['date']
        comment_id = args['id']
        comment_body = text[:text.rfind("=")] #skip last hashtag
        form_token = formatter.req.incookie['trac_form_token'].value
        form_url = formatter.req.base_path+"/add-wiki-comment"
        page_url = formatter.req.path_info
        return """
    <div class="comment" style="width: 600px;margin-left:30px;">
        <a name='"""+comment_id+"""'></a>
        <div class="comment_head" style="width: 600px; background:#eee;font-size:80%;">
            """+comment_author+""": """+comment_date+"""
            <a href="#reply" id='reply_"""+comment_id+"""'>Reply</a>
        </div>
        <div class="comment_body">"""+comment_body+"""
            <form action='"""+form_url+"""' method="POST" id='comment_"""+comment_id+"""' >
                <textarea name="comment" rows="4" cols="90"></textarea>
                <input type="submit" name="comment_submit" value="Submit">
                <input type="hidden" name="comment_parent" value='"""+comment_id+"""'>
                <input type="hidden" name="target_page" value='"""+page_url+"""' />
                <input type="hidden" name="__FORM_TOKEN" value='"""+form_token+"""' />
            </form>
        </div>
        <script type="text/javascript">
              jQuery(document).ready(function($) {
                var id = '"""+comment_id+"""';
                $('#comment_'+id).hide();
                var subcomments = $('#reply_'+id).parent().next().find('div.comment');
                if ( subcomments.length > 0 )
                    $('#comment_'+id).insertBefore($(subcomments).first());
                $('#reply_'+id).click(function(){
                    $('#comment_'+id).show();
                });
              });
        </script>
    </div>
    """

