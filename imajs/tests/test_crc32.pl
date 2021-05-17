#!/usr/bin/perl

# This test is to check that the python
# and the perl code are yielding the same
# values.
#
# Test Usage:
#	1) Use python crc32.main() to generate a value
#	2) Use `perl -I.. test_crc32.pl` to generate a value
#	3) Verify that the values are the same


use CRC32;

my $data = 'hello world';

CRC32::clear();
CRC32::add(\$data);

my $check_value = CRC32::result();

printf("Check value (in hex): %x\n", $check_value);