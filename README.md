Trac Wiki comments plugin
=================

TRAC plugin for comments inside wiki pages

Default installation of Trac does not include any way to conveniently annotate and comment wiki pages.
I made a plugin for that, compatible with Trac 0.12.3

## Screenshots:


## Installation:
- download [WikiComments-1.0-py2.6.egg](http://www.jarnik.com/wordpress/wp-content/uploads/2012/08/WikiComments-1.0-py2.6.egg) (or see [link](http://trac-hacks.org/wiki/WikiCommentsPlugin))
- copy it into your /plugins directory within your [Trac](http://trac.edgewall.org/) installation path
- go to Administration > Plugins > WikiComments and check all options

## How it works:
- first comment has to be inserted using edit mode – just click bubble icon (see syntax below)
- followup comments can be attached using a simple form in view mode (see pictures above)

## Wiki Syntax:
```
Single comment: {{{#!WikiComments author="jaroslav meloun" date="2012-8-28 23:18:58" id="96734058255559d6db4de2b565034914" Also rocks extensively! =96734058255559d6db4de2b565034914}}}

Nested reply: {{{#!WikiComments author="jaroslav meloun" date="2012-8-28 23:18:58" id="96734058255559d6db4de2b565034914" Also rocks extensively! {{{#!WikiComments author="jaroslav meloun" date="2012-08-28 23:22:11" id="75d3140a2d081753ee3f8ebb642e9fe6"" Bump! =75d3140a2d081753ee3f8ebb642e9fe6 }}} =96734058255559d6db4de2b565034914 }}}
```

## License: BSD 3-Clause
