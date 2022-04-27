#!/usr/bin/perl
# check password and redirect to survey questions or error page
#
#
# dlu 10-Mar-2003
#

use strict;
use CGI;

$CGI::DISABLE_UPLOADS = 1;
$CGI::POST_MAX  = 102_400; # 100KB

# constants
my $security_redirect = 'http://yahoo.com';
my $ok_redirect = '../survey/SurveyQs.html';
my @error_redirect = qw(../survey/SurveyPassword2.html ../survey/SurveyPassword3.html );      # should come from form
my $password = '101';

# form data
my $q = new CGI;
my $error_page = $q->param('error_page');
my $pw = $q->param('password');




# were we invoked by the right page on the right machine?
&check_referer;

if ($pw eq $password) {
    redirect('ok') }
else {
    redirect('bad_pw') }



# check refering url and host
sub check_referer {
    if ((( ! $ENV{HTTP_HOST} =~  m/swc.math.arizona.edu/) && 
            ($ENV{HTTP_ADDR} ne '128.196.224.10')) ||
	! (($ENV{HTTP_REFERER} =~ m{survey}) || 
	   ($ENV{HTTP_REFERER} =~ m{cgi}))) {
	&redirect('go_away');}
}

sub redirect {
    if($_[0] eq 'ok') {
	copy_html($ok_redirect); exit;}
    else {if($_[0] eq 'bad_pw') {
	copy_html($error_redirect[$error_page]); exit;}
	  else {print "Location: $security_redirect\n\n"; exit;}}
}

sub copy_html {
    open(INPUT, "<$_[0]")
  	or die "Could not open $_[0]: $!";
    print "Content-type: text/html\n\n";
    while (<INPUT>) {
	print "$_";
    }
    close INPUT or die "Error closing output file";
}
