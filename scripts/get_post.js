var page = require('webpage').create();
var system = require('system');
var fs = require('fs');

var args = system.args

if(args.length != 3)
{
  console.log("USAGE: phantomjs get_post.js <image board page URL> <post number>");
  phantom.exit(1);
}

var url = args[1];
// TODO: test proper formedness for URL
var chin_regex = new RegExp("boards.4chan.org");
var is_4chin = chin_regex.test(url);

var post_num = args[2];
var s = '#t' + post_num

if(!is_4chin)
{
  s = post_num;
  var n = s.substring(0, 1);
  s = s.substring(1, s.length);
  s = '#\\3' + n + ' ' + s;
}

var image_filename = post_num + '.png'
var text_filename = post_num + '.txt'
console.log("URL: ", url);
console.log("Selector: ", s);
console.log("Writing image to file: ", image_filename);

// Set cookies depending upon estimated board archive
// this is to ensure proper recognizable theme
var blue_board_regex = new RegExp("\/tv\/|\/a/\|\/fit\/|\/wsg\/|\/v\/|\/jp\/");
if(blue_board_regex.test(url))
{
  phantom.addCookie({
    'name': 'foolframe_2q1_theme',
    'value': 'foolz%2Ffoolfuuka-theme-yotsubatwo%2Fyotsuba-b',
    'domain': 'boards.fireden.net'
  });

  phantom.addCookie({
    'name': 'foolframe_5SU_theme',
    'value': 'foolz%2Ffoolfuuka-theme-yotsubatwo%2Fyotsuba-b',
    'domain': 'archive.4plebs.org'
  });

}else{

  phantom.addCookie({
    'name': 'foolframe_2q1_theme',
    'value': 'foolz%2Ffoolfuuka-theme-yotsubatwo%2Fyotsuba',
    'domain': 'boards.fireden.net'
  });

  phantom.addCookie({
    'name': 'foolframe_5SU_theme',
    'value': 'foolz%2Ffoolfuuka-theme-yotsubatwo%2Fyotsuba',
    'domain': 'archive.4plebs.org'
  });
}
page.open(url, function() {
    // being the actual size of the headless browser
    page.viewportSize = { width: 768, height: 1024 };
    
    // generate a post image
    var clipRect = page.evaluate(function(s){
      var e = document.querySelector(s);
      var rect = e.getBoundingClientRect();
      var _txt = e.querySelector('.text');
      if(!_txt)
      {
        // fallback to 4chin style
        _txt = e.querySelector('.postMessage');;
      }
      // is this an OP? It is if it has the class 'thread'
      if(e.classList.contains('thread'))
      {
        // look for an element of class "posts" which is the lower bound of the OP
        var _posts = e.querySelector('.posts');
        if(_posts)
        {
          var _post_bounds = _posts.getBoundingClientRect();
          var r = {
            'top' : rect.top,
            'left' : rect.left,
            'width' : rect.width,
            'height' : _post_bounds.top,
            'text' : _txt.textContent,
          };
          return r;
        }
        else
        {
          // no adjustment to bounds necessary
          var r = {
            'top' : rect.top,
            'left' : rect.left,
            'width' : rect.width,
            'height' : rect.top,
            'text' : _txt.textContent,
          };
          return r;

        }
      }
      else
      {
        var _post_wrapper = e.querySelector('.post_wrapper');
        var _rect = _post_wrapper.getBoundingClientRect();
        // also extract post text
        var r = {
            'top' : _rect.top,
            'left' : _rect.left,
            'width' : _rect.width,
            'height' : _rect.height,
            'text' : _txt.textContent,
          };
          return r;
      }
      
      // If this is an OP, find where the posts start
      // this should be where ,aside class="posts" starts, which may or may not be present
      // If it's a regular post, no further work is needed.
    },s);
   
    console.log("top: ", clipRect.top);
    console.log("left: ", clipRect.left);
    console.log("width: ", clipRect.width);
    console.log("height: ", clipRect.height);

    page.clipRect = {
      top:    clipRect.top,
      left:   clipRect.left,
      width:  clipRect.width,
      height: clipRect.height
    };
    page.render(image_filename);
    
    // extract post text
    //var txt = page.evaluate(function(s){
    //  return document.querySelector(s).textContent;
    //},s);
    //console.log('TEXT: ', txt);

    var txt = clipRect.text;
    console.log('TEXT: ', txt);
    if(txt.length > 0)
    {
      fs.write(text_filename, txt, 'w');
    }
    
    phantom.exit();
});

