var page = require('webpage').create();
var system = require('system');
var fs = require('fs');

var args = system.args
var url = 'http://google.com'
var s = '#hplogo'
var outfile = 'post'

if(args.length > 1)
{
  url = args[1];
}
if(args.length > 2)
{
  s = args[2];
  // escape selectors that start with a number
  var r = new RegExp("^\#[0-9]{1}");
  if(r.test(s))
  {
    s = s.substring(1, s.length);
    var n = s.substring(0, 1);
    s = s.substring(1, s.length);
    s = '#\\3' + n + ' ' + s;
  }
}
if(args.length > 3)
{
  outfile = args[3]
}

console.log("URL: ", url);
console.log("Selector: ", s);
console.log("Outfile: ", outfile);

phantom.addCookie({
  'name': 'foolframe_2q1_theme',
  'value': 'foolz%2Ffoolfuuka-theme-yotsubatwo%2Fyotsuba-b',
  'domain': 'boards.fireden.net'
});

page.open(url, function() {
    // being the actual size of the headless browser
    page.viewportSize = { width: 768, height: 1024 };
    
    // generate a post image
    var clipRect = page.evaluate(function(s){
      var e = document.querySelector(s);
      var rect = e.getBoundingClientRect();
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
          };
          return r;
        }
        else
        {
          // no adjustment to bounds necessary
          return rect;
        }
      }
      else
      {
        // TODO: drill down further to actual post element
        // TODO: extract post text etc..
        return rect;
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
    page.render(outfile + '.png');
    
    // extract post text
    var txt = page.evaluate(function(s){
      return document.querySelector(s).textContent;
    },s);
    //console.log('TEXT: ', txt);


    if(txt.length > 0)
    {
      var textFilePath = outfile + '.post.txt';
      fs.write(textFilePath, txt, 'w');
    }
    
    phantom.exit();
});

