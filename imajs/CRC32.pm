#!/usr/bin/perl

# use CRC32;
# 
# my $data = 'Hello World';
# 
# CRC32::clear();
# CRC32::add(\$data);
# 
# my $check_value = CRC32::result();
# 
# printf("Check value (in hex): %x\n", $check_value);
#
# Reference
# http://www.dispersiondesign.com/articles/graphics/png_crc32_calculations

package CRC32;

our $crc = 0xFFFFFFFF;
our $crc_table;

sub clear {
   $crc = 0xFFFFFFFF;
}


sub build_table {
   my $table = [];
   for(my $n = 0; $n < 256; $n++) {
      my $c = $n;
      for( my $k = 0; $k < 8; $k++ ) {
         $c = ($c >> 1 ) ^ (($c & 1) ? 0xEDB88320 : 0);
      }
      $table->[$n] = $c;
   }
   return $table;
}


sub add {
   my($data_ptr) = @_;

   if(!defined $crc_table) {
      $crc_table = build_table();  
   }

   my @bytes = unpack("C*", $$data_ptr);
   foreach my $byte (@bytes) {
      $crc = $crc_table->[($crc ^ $byte) & 0xFF] ^ ($crc >> 8);
   }
}


sub result {
   return ($crc ^ 0xFFFFFFFF);
}

1;