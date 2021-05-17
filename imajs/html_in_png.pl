#!/usr/bin/perl
#
#                                  .       .
#                                 / `.   .' \
#                         .---.  <    > <    >  .---.
#                         |    \  \ - ~ ~ - /  /    |
#                          ~-..-~             ~-..-~
#                      \~~~\.'   stegosploit      `./~~~/
#                       \__/                        \__/
#                         /  .    -.                  \
#                  \~~~\/   {       \       .-~ ~-.    -._ _._
#                   \__/    :        }     {       \     ~{  p'-._
#    .     .   |~~. .'       \       }      \       )      \  ~--'}
#    \\   //   `-..'       _ -\      |      _\      )__.-~~'='''''
# `-._\\_//__..-'      .-~    |\.    }~~--~~  \=   / \
#  ``~---.._ _ _ . - ~        ) /=  /         /+  /   }
#                            /_/   /         {   } |  |
#                              `~---o.       `~___o.---'
#
#
# by Saumil Shah @therealsaumil
#
# This script creates an HTML+PNG polyglot
#
# Requires PNGDATA.pm, CRC32.pm

use FindBin;
use lib $FindBin::Bin;
use PNGDATA;

$| = 1;

$RANDOM_DATA_SIZE = 1900;

$htmlfile = $ARGV[0];
$pngfile = $ARGV[1];
$outfile = $ARGV[2];

print <<"EOT";

                                  .       .
                                 / `.   .' \\
                         .---.  <    > <    >  .---.
                         |    \\  \\ - ~ ~ - /  /    |
                          ~-..-~             ~-..-~
                      \\~~~\\.'   stegosploit      `./~~~/
                       \\__/                imajs   \\__/
                         /  .    -.                 \\
                  \\~~~\\/   {       \       .-~ ~-.    -._ _._
                   \\__/    :        }     {       \\     ~{  p'-._
    .     .   |~~. .'       \\       }      \\       )      \\  ~--'}
    \\\\   //   `-..'       _ -\\      |      _\\      )__.-~~'='''''
 `-._\\\\_//__..-'      .-~    |\\.    }~~--~~  \\=   / \\
  ``~---.._ _ _ . - ~        ) /=  /         /+  /   }
                            /_/   /         {   } |  |
                              `~---o.       `~___o.---'

EOT

if($#ARGV < 2) {
   print "Usage: $0 <html source> <png source> <output>\n";
   exit;
}

local $/;

$htmldata = "";

if($htmlfile ne '-') {
   open(HTMLFILE, $htmlfile) || die("Cannot open $htmlfile\n");
   $htmldata = <HTMLFILE>;
   close(HTMLFILE);
}

$htmldata =~ s/[\r\n]+$//;    # remove trailing newline characters

open(PNGFILE, $pngfile) || die("Cannot open $pngfile\n");
$pngdata = <PNGFILE>;
close(PNGFILE);

my @png = ();

@png = PNGDATA::read_png($pngdata);

# insert a tEXt chunk with an HTML comment
# after the PNG header and the IHDR chunk
# i.e. as the 3rd array element
$open_comment = PNGDATA::make_text_chunk("<html>", "<!-- ");
splice(@png, 2, 0, $open_comment);
$htmldata =~ s/<html>//i;
#$htmldata .= "<!-- <![CDATA[";
$htmldata = " -->" . $htmldata . "<script type='text/undefined'>/*";   # works best in blocking the rest of the data

# add some random data at the end of the HTML data

$padding_length = int(rand($RANDOM_DATA_SIZE));

print "Appending $padding_length random bytes\n";

for($i = 0; $i < $padding_length; $i++) {
   while(1) {
      $x = int(rand(255));
      if($x >= 32 && $x != 0 && $x != ord('<') && $x != ord('>') && $x != ord('/')) {
         last;
      }
   }
   $htmldata = chr($x) . $htmldata;
}

$html_content = PNGDATA::make_text_chunk("_", $htmldata);
splice(@png, 3, 0, $html_content);

PNGDATA::print_png_data(@png);

$newpng = join('', @png);

open(OUTPUT, ">$outfile") || die("Cannot write to $outfile\n");
print OUTPUT $newpng;
close(OUTPUT);

print "Written $outfile\n";

