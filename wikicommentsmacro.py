# -*- coding: utf-8 -*-
#
# WikiComments macro for Trac 0.12.3
#
# Author: Jaroslav Meloun <jaroslav dot meloun at gmail dot com>
# License: BSD

from trac.core import *
from trac.wiki.macros import WikiMacroBase
from trac.wiki import Formatter
import StringIO

__all__ = ['WikiCommentsMacro']

class WikiCommentsMacro(WikiMacroBase):
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
        <div class="comment_head" style="width: 600px; background:#eee;font-size:80%;padding:3px;">
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

