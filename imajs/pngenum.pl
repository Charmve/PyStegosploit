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
# Simple PNG enumerator utility

use FindBin;
use lib $FindBin::Bin;

use PNGDATA;

$| = 1;

if($#ARGV < 0) {
   print "Usage: pngenum.pl <png>\n";
   exit;
}

$pngfile = $ARGV[0];

local $/;

open(PNGFILE, $pngfile) || die("Cannot open $pngfile\n");
$pngdata = <PNGFILE>;
close(PNGFILE);

my @png = ();

@png = PNGDATA::read_png($pngdata);
PNGDATA::print_png_data(@png);
