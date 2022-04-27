#!/usr/bin/perl
#
# dlu 10-Mar-2003
#

use strict;
use CGI;

$CGI::DISABLE_UPLOADS = 1;
$CGI::POST_MAX  = 102_400; # 100KB

my @listtime = localtime;
my $scalartime = localtime;

my $q = new CGI;

print "Content-type: text/html\n\n";
print "<HTML>";
print "@listtime<P>$scalartime<P>";
print $listtime[4]+1, "/", $listtime[3],"/", $listtime[5]+1900, "<P>";
$scalartime =~ /(\d\d:\d\d:\d\d)/;
print $1, "<P>";
print "Remote Host:", $ENV{REMOTE_HOST}, "<P>",  "IP:", $ENV{REMOTE_ADDR}, "<P>";
print "HTTP Host:", $ENV{HTTP_HOST}, "<P>",   "IP:", $ENV{HTTP_ADDR}, "<P>";
print "<P>Referer:", $ENV{HTTP_REFERER};

if ( defined($q->param('deftest'))) {
    print "<P>defined!" }
     else { print "<P>undefined!"}

print "</HTML>";
exit;

