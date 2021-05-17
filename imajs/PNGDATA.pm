#!/usr/bin/perl
#
# by Saumil Shah

use FindBin;
use lib $FindBin::Bin;

package PNGDATA;

use CRC32;

our $pos;

# function to read the PNG file in chunks,
# and create a PNG array
#
# input - pngdata: entire PNG file data
# returns - array of PNG chunks
sub read_png {
   my($data) = @_;
   my @png_chunks;

   push(@png_chunks, &get_png_header($data));

   while($pos < length($data)) {
      push(@png_chunks, &get_next_chunk($data));
   }
   return(@png_chunks);
}

# function to print the PNG data from
# the array
# input - png_chunks: array of PNG chunks
# returns - nothing
sub print_png_data {
   my(@png_chunks) = @_;
   my $i;

   &print_png_header($png_chunks[0]);
   for($i = 1; $i <= $#png_chunks; $i++) {
      &print_chunk($png_chunks[$i]);
   }
}

# function to return the PNG header (1st 8 bytes)
# input - pngdata: entire PNG file data
# output - PNG header data
sub get_png_header {
   my($pngdata) = @_;
   my $data;

   $pos = 0;   # position within the PNG data
   $data = substr($pngdata, $pos, 8);
   $pos += 8;
   return($data);
}

# function to return the next chunk from the PNG file
# input - png_chunks: array of PNG chunks
# returns - next chunk
sub get_next_chunk {
   my($pngdata) = @_;
   my $len;
   my $fourcc;
   my $chunk_data;
   my $crc;

   $len = unpack("N", substr($pngdata, $pos, 4));
   $pos += 4;

   $fourcc = substr($pngdata, $pos, 4);
   $pos += 4;

   $chunk_data = substr($pngdata, $pos, $len);
   $pos += $len;

   $crc = substr($pngdata, $pos, 4);
   $pos += 4;

   return(pack("N", $len) . $fourcc . $chunk_data . $crc);
}

# function to read the PNG header and print it
# input - PNG header
# returns - nothing
sub print_png_header {
   my($pngheader) = @_;
   my $i;
   my $status = "OK";

   printf("PNG Header: ");

   for($i = 0; $i < 8; $i++) {
      printf("%02X ", ord(substr($pngheader, $i, 1)));
   }

   if($pngheader != "\x89PNG\x0D\x0A\x1A\x0A") {
      $status = "Error";
   }
   print " - $status \n";
}

# function to print a PNG print_chunk
# input - PNG chunk
# returns - nothing
sub print_chunk {
   my($chunk) = @_;
   my $len, $p;
   my $fourcc;
   my $chunk_data, $crc_data;
   my $crc, $computed_crc;
   my $status;

   $p = 0;

   $len = unpack("N", substr($chunk, $p, 4));
   $p += 4;

   $fourcc = substr($chunk, $p, 4);
   $p += 4;

   $chunk_data = substr($chunk, $p, $len);
   $p += $len;

   $crc = unpack("N", substr($chunk, $p, 4));

   $crc_data = $fourcc . $chunk_data;

   CRC32::clear();
   CRC32::add(\$crc_data);

   $computed_crc = CRC32::result();
   $status = "OK";
   if($computed_crc != $crc) {
      $status = "Error";
   }

   printf("%s %d bytes CRC: 0x%08X (computed 0x%08X) %s\n", $fourcc, $len, $crc, $computed_crc, $status);
}

# function to create a tEXt chunk
#
# input - name, value
# returns - [length][tEXt][name...][00][value...][CRC]
sub make_text_chunk {
   my($name, $value) = @_;
   my $fourcc = "tEXt";
   my $crc;
   my $data, $chunk;

   $data = $name . "\x00" . $value;
   my $len = length($data);

   $data = $fourcc . $data;
   CRC32::clear();
   CRC32::add(\$data);
   $crc = CRC32::result();

   $chunk = pack("N", $len) . $data . pack("N", $crc);
   return($chunk);
}

# function to create an IEND chunk
#
# input - nothing
# returns - [00000000][IEND][CRC = 0xAE426082]
sub make_iend_chunk {
   my $chunk;

   $chunk = pack("N", 0x0) . "IEND" . pack("N", 0xAE426082);
   return($chunk);
}

1;