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
#from StringIO import StringIO
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
    
    #def render_macro(self, formatter, name, args):
    def expand_macro(self, formatter, name, text, args):
        out = StringIO.StringIO()
        Formatter(self.env, formatter.context).format(text, out)
        text = out.getvalue()
        comment_author = "moto" #args['author']
        comment_date = "foko" #args['date']
        comment_body = text[:text.rfind("#")]
        return """
    <div class="comment" style="width: 600px;margin-left:30px;">
        <div class="comment_head" style="width: 600px;">
            <span class="comment_buttons" style="float:right;">
                <span class="comment_button">
                    <a href="#reply">Reply</a>
                </span>
            </span>
            """+comment_author+""": """+comment_date+"""
        </div>
        <div class="comment_body">"""+comment_body+"""</div>
    </div>
    """
                
	#cursor = formatter.db.cursor()
	#
	## get the refere page name
	#thispage = formatter.context.id
	#
	## process arguments
	#pages, kw = parse_args(args)
	#
	## query to get the latest version of a page
	#query = """
	#    SELECT w1.name 
	#    FROM wiki w1, 
	#        ( 
	#	    SELECT name, MAX(version) AS version 
	#	    FROM wiki 
	#	    GROUP BY name 
	#	) w2 
	#    WHERE 
	#        w1.version = w2.version AND 
	#	w1.name = w2.name AND 
	#	w1.text LIKE \'%%%s%%\' 
	#    ORDER BY w1.name""" % thispage
	#
	## TODO: use named parameters
	#cursor.execute(query)
	#
	## for each answer store in page
    #    for page, in cursor:
	#    if page == thispage:
	#        continue
	#    pages.append(page)
	#
	#pages.sort()
	#
	## get the references to each list
    #    def link(page):
    #        return tag.a(page, href=formatter.href.wiki(page))
    #    
	#return tag(tag.strong('Navigation:'), '(',
    #               [[link(page), ', '] for page in pages[:-2]],
    #               link(page), ')')
