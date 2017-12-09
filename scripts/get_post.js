var page = require('webpage').create();
var system = require('system');
var fs = require('fs');

var args = system.args

if(args.length < 3)
{
  console.log("USAGE: phantomjs get_post.js <image board page URL> <post number> [optional output directory]");
  phantom.exit(1);
}

var url = args[1];
// TODO: test proper formedness for URL
var chin_regex = new RegExp("boards.4chan.org");
var is_4chin = chin_regex.test(url);

var post_num = args[2];
var s = '#p' + post_num
var out_dir = "."

if(args.length >2)
{
  out_dir = args[3];
}

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
        _txt = e.querySelector('.post_data');
      }
      // is this an OP? It is if it has the class 'thread'(archives)
      // or it has clas op, (4chin)
      if(e.classList.contains('thread') || e.classList.contains('op'))
      {
        //var _posts = e.querySelector('.posts');
        // the lower bound of the OP is tough to find. The image may extend down
        // farther than the pXXX element we already have.
        var img = e.querySelector('.fileThumb');
        // fall back to archive format
        if(!img){
          img = e.querySelector('.thread_image_box');
        }
        if(img)
        {
          var img_bounds = img.getBoundingClientRect();
          //var height = rect.height;
          var _text_rect = _txt.getBoundingClientRect();
          var text_bottom = _text_rect.top + _text_rect.height;
          var img_bottom = img_bounds.top + img_bounds.height;
          var height = text_bottom - rect.top;
          if(img_bottom > text_bottom)
          {
            height = img_bottom - rect.top;
          }
          var r = {
            'top' : rect.top,
            'left' : rect.left,
            'width' : rect.width,
            //'height' : _post_bounds.top,
            'height' : height,
            'text' : _txt.innerText,
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
            'text' : _txt.innerText,
          };
          return r;
        }
      }
      else
      {
        // this is not an OP.
        // 4chin has a class 'reply'. If we have that we can use the
        // selected element as the bounds
        var _post_wrapper = e.querySelector('.post_wrapper');
        if(!e.classList.contains('reply') && _post_wrapper)
        {
          rect = _post_wrapper.getBoundingClientRect();
        }
        // also extract post text
        var r = {
            'top' : rect.top,
            'left' : rect.left,
            'width' : rect.width,
            'height' : rect.height,
            'text' : _txt.innerText,
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
    page.render(out_dir + '/' + image_filename);
    
    // extract post text
    //var txt = page.evaluate(function(s){
    //  return document.querySelector(s).textContent;
    //},s);
    //console.log('TEXT: ', txt);

    var txt = clipRect.text;
    console.log('TEXT: ', txt);
    if(txt.length > 0)
    {
      fs.write(out_dir + '/' + text_filename, txt, 'w');
    }
    
    phantom.exit();
});

