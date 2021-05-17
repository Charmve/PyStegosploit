/*
                                  .       .
                                 / `.   .' \
                         .---.  <    > <    >  .---.
                         |    \  \ - ~ ~ - /  /    |
                          ~-..-~             ~-..-~
                      \~~~\.'   stegosploit      `./~~~/
                       \__/                        \__/
                         /  .    -.                  \
                  \~~~\/   {       \       .-~ ~-.    -._ _._
                   \__/    :        }     {       \     ~{  p'-._
    .     .   |~~. .'       \       }      \       )      \  ~--'}
    \\   //   `-..'       _ -\      |      _\      )__.-~~'='''''
 `-._\\_//__..-'      .-~    |\.    }~~--~~  \=   / \
  ``~---.._ _ _ . - ~        ) /=  /         /+  /   }
                            /_/   /         {   } |  |
                              `~---o.       `~___o.---'


Draw a histogram in a canvas. Takes a source canvas, calculates the frequency of RGB
from it and then draws a histogram in the target canvas.

by Saumil Shah @therealsaumil
*/

var maxColourFrequency = 0;

function drawHistogram(srcCanvas, histogram) {
   var srcContext = srcCanvas.getContext('2d');
   var srcImg = srcContext.getImageData(0, 0, srcCanvas.width, srcCanvas.height);
   var pixData = srcImg.data;

   var reds = new Array(256);
   var greens = new Array(256);
   var blues = new Array(256);

   histogram.width = srcCanvas.width;
   histogram.height = srcCanvas.height;
   histogram.style.border = "1px solid black";

   var xScaleFactor = srcCanvas.width / 256;

   var maxred = 0, maxgreen = 0, maxblue = 0;

   var histogramContext = histogram.getContext('2d');
   histogramContext.clearRect(0, 0, histogram.width, histogram.height);
   histogramContext.scale(xScaleFactor, 1);

   // initialize the histogram
   for(var i = 0; i < 256; i++) {
      reds[i] = 0;
      greens[i] = 0;
      blues[i] = 0;
   }

   for(var i = 0; i < pixData.length; i += 4) {
      var r = pixData[i];
      var g = pixData[i + 1];
      var b = pixData[i + 2];

      if(r > 0) {
         maxred = ++reds[r] > maxred ? reds[r] : maxred;
      }
      if(g > 0) {
         maxgreen = ++greens[g] > maxgreen ? greens[g] : maxgreen;
      }
      if(b > 0) {
         maxblue = ++blues[b] > maxblue ? blues[b] : maxblue;
      }
   }
   maxColourFrequency = maxred > maxColourFrequency ? maxred : maxColourFrequency;
   maxColourFrequency = maxgreen > maxColourFrequency ? maxgreen : maxColourFrequency;
   maxColourFrequency = maxblue > maxColourFrequency ? maxblue : maxColourFrequency;

   // now draw the bars on the canvas
   histogramContext.globalAlpha = 0.66667;

   // first the blues
   histogramContext.fillStyle = "#0000FF";
   for(var i = 0; i < 256; i++) {
      var height = Math.round(blues[i] * histogram.height / maxColourFrequency);
      histogramContext.fillRect(i, histogram.height, 1, -height);
   }

   // then the greens
   histogramContext.fillStyle = "#00FF00";
   for(var i = 0; i < 256; i++) {
      var height = Math.round(greens[i] * histogram.height / maxColourFrequency);
      histogramContext.fillRect(i, histogram.height, 1, -height);
   }

   // lastly the reds
   histogramContext.fillStyle = "#FF0000";
   for(var i = 0; i < 256; i++) {
      var height = Math.round(reds[i] * histogram.height / maxColourFrequency);
      histogramContext.fillRect(i, histogram.height, 1, -height);
   }
}
