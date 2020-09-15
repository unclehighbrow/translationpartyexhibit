#!/usr/bin/perl -w

use strict;

while (<ARGV>) {
  $_ =~ m/^(\+\d+),(.*?),(\w+),(.*?),(\d{10,}),(.*?),(\d+)\s*$/;
  my $phone = $1;
  my $ctime = $2;
  my $source = $3;
  my $json = $4;
  my $key = $5;
  my $phrase = $6;
  my $rando = $7;
  
  my $steps =()= $json =~ /""lang"":/gi;
  
  $json =~ m/.+""en"", ""string"": ""(.*?)""}]"$/;
  my $result = $1;  
  
  $result = clean_string($result);
  $phrase = clean_string($phrase);

  
  print "\"$phone\",\"$ctime\",\"$phrase\",\"$steps\",\"$result\"\n";
}

sub clean_string() {
  my $string = shift;
  $string =~ s/"+/"/g;
  $string =~ s/\\//g;
  $string =~ s/\\//g;  
  $string =~ s/^"|"$//g;
  $string =~ s/"/'/g;
  return $string;
}