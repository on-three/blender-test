var page = require('webpage').create();
var system = require('system');

var args = system.args
//var url = 'http://google.com'
var url = 'https://boards.fireden.net/a/thread/145649654'
//var s = '#hplogo'
var s = "#\\31 45650295"
var outfile = 'post.png'

if(args.length > 1)
{
  url = args[1];
}
if(args.length > 2)
{
  s = args[2];
}
if(args.length > 3)
{
  outfile = args[3]
}

console.log("URL: ", url);
console.log("Selector: ", s);
console.log("Outfile: ", outfile);

page.open(url, function() {
    // being the actual size of the headless browser
    page.viewportSize = { width: 768, height: 1024 };
    var clipRect = page.evaluate(function(s){
      return document.querySelector(s).getBoundingClientRect();
    },s);
    page.clipRect = {
      top:    clipRect.top,
      left:   clipRect.left,
      width:  clipRect.width,
      height: clipRect.height
    };
      
    page.render(outfile);
      phantom.exit();
});
