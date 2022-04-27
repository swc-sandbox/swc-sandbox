#!/usr/bin/perl
#
# Process responses from survey form
#
# dlu 7-Mar-2003
#

use strict;
use CGI;

$CGI::DISABLE_UPLOADS = 1;
$CGI::POST_MAX  = 102_400; # 100KB

# constants
my $security_redirect = 'http://yahoo.com';
my $ok_redirect = '../survey/CollectName.html';
my @error_redirect = ();      # list of error pages
my $error_page ='';           # comes from form.  Index for previous array
my $output_file = '../survey/Results.xml';
my @names = qw(
EducationalExp EducationalExpComments Theme ThemeComments 
Interactions InteractionsComments Expectations ExpectationsComments 
Lectures LecturesComments Notes NotesComments Projects ProjectsComments 
Website WebsiteComments CoursesComments FutureOrgComments FutureTopicsComments 
OtherComments Status StatusComments Project Funding 
AWS1998 AWS1999 AWS2000 AWS2001 AWS2002 AWS2003);

# env variables
my $user_ip = $ENV{REMOTE_ADDR};
my @listtime = localtime;
my $scalartime = localtime;


# form data
my $q = new CGI;
my ($name, $value );


# check url etc.:
&check_referer;

open(OUTPUT, ">>$output_file")
  	or die "Could not open $output_file: $!";

print OUTPUT "<RESPONSE>\n";
print OUTPUT "     <IP>", $ENV{REMOTE_ADDR}, "</IP>\n";
print OUTPUT "     <Date>", $listtime[4]+1, "/", $listtime[3], "/", $listtime[5]+1900, "</Date>\n";
$scalartime =~ /(\d\d:\d\d:\d\d)/;
print OUTPUT "     <Time>", $1, "</Time>\n";

foreach $name (@names) {
    if ( defined($q->param($name))) {
	$value = $q->param($name);
	$value =~ s/&/&amp;/g;
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;
	$value =~ s/"/&quot;/g;
	$value =~ s/'/&apos;/g;
	print OUTPUT "     ", "<$name>$value</$name>\n";}
    else {
        print OUTPUT "     ", "<$name></$name>\n"; }
}

print OUTPUT "</RESPONSE>\n";

close OUTPUT or die "Error closing $output_file: $!";

&redirect('ok');

exit;

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
