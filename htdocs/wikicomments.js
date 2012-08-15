
// Add the toolbar to all <textarea> elements on the page with the class
// 'wikitext'.
jQuery(document).ready(function($) {


  function addWikiCommentButton( textarea ) {
    function encloseSelection(prefix, suffix) {
          textarea.focus();
          var start, end, sel, scrollPos, subst;
          if (document.selection != undefined) {
            sel = document.selection.createRange().text;
          } else if (textarea.setSelectionRange != undefined) {
            start = textarea.selectionStart;
            end = textarea.selectionEnd;
            scrollPos = textarea.scrollTop;
            sel = textarea.value.substring(start, end);
          }
          if (sel.match(/ $/)) { // exclude ending space char, if any
            sel = sel.substring(0, sel.length - 1);
            suffix = suffix + " ";
          }
          subst = prefix + sel + suffix;
          if (document.selection != undefined) {
            var range = document.selection.createRange().text = subst;
            textarea.caretPos -= suffix.length;
          } else if (textarea.setSelectionRange != undefined) {
            textarea.value = textarea.value.substring(0, start) + subst +
                             textarea.value.substring(end);
            if (sel) {
              textarea.setSelectionRange(start + subst.length, start + subst.length);
            } else {
              textarea.setSelectionRange(start + prefix.length, start + prefix.length);
            }
            textarea.scrollTop = scrollPos;
          }
      }

        function randomString() {
            var chars = "0123456789abcdef";
            var string_length = 32;
            var key = '';
            for (var i=0; i<string_length; i++) {
                var rnum = Math.floor(Math.random() * chars.length);
                key += chars.substring(rnum,rnum+1);
            }
            return key;
        }

      var commentButton = $('<a href="#" id="wikicomment" title="Comment" tabindex="400">Comment</a>');
      $(".wikitoolbar").width( $(".wikitoolbar").width() + 26 );
      $(".wikitoolbar").append( $(commentButton) );
      $(".wikitoolbar").children().last().click( function() { 
        console.log("hi!"); 
        var id = randomString();
        encloseSelection(
            '\n{{{#!WikiComments author="jaroslav meloun" date="2012-07-12 12:10:31" id="'+id+'"\n',
            '\n='+id+'\n}}}\n'
        );
      });
  }

  $("textarea.wikitext").each(function() { addWikiCommentButton(this) });
});
