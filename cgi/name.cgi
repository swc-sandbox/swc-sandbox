#!/usr/bin/perl
#
# Process name and e-mail from survey form
# generates a thank you message to respondent
# and a message with name and e-mail to secretary.
#
# dlu 7-Mar-2003
#

use strict;
use CGI;

$CGI::DISABLE_UPLOADS = 1;
$CGI::POST_MAX  = 102_400; # 100KB

# constants
my $mailprog = '/usr/sbin/sendmail -i -t';
my $secretary = 'braun@math.arizona.edu';
my $max_name_length = 40;
my $security_redirect = 'http://yahoo.com';
my $ok_redirect = '../survey/Thanks.html';
my @error_redirect 
         = qw(../survey/CollectName2.html);
         # list of error pages
my $error_page ='';           # comes from form.  Index for previous array



# env variables
my $user_ip = $ENV{REMOTE_HOST} || $ENV{REMOTE_ADDR};
my $time = localtime;


# form data
my $q = new CGI;
my $user_name = $q->param('name');
my $user_email = $q->param('email');
my $error_page = $q->param('error_page');


# truncate user supplied strings to be safe
$user_name = substr($user_name,0,$max_name_length);
$user_email = substr($user_email,0,$max_name_length);
$error_page = substr($error_page,0,$max_name_length);


# were we invoked by the right page on the right machine?
&check_referer;

# make sure the e-mail address submitted is (somewhat) valid
&check_email;

&send_secretary_mail;
&send_user_mail;
&redirect('ok');

#################

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
    else {if($_[0] eq 'bad_email') {
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


# if e-mail ok, do nothing, otherwise redirect
sub check_email {
    $user_email = &validate_email_address($user_email);
    unless ($user_email) {&redirect('bad_email');} 
}


# send mail to secretary
sub send_secretary_mail {
    open MAIL, "| $mailprog"
	or die "Could not open sendmail: $!";
    print MAIL <<EOM;
To: $secretary
From: swcenter\@swc.math.arizona.edu
Subject: $user_name has completed the AWS survey

$user_name completed the AWS survey on $time
from host $user_ip.
EOM
    close MAIL or die "Error closing sendmail: $!";
}


# send mail to user
sub send_user_mail {
    open MAIL, "| $mailprog"
	or die "Could not open sendmail: $!";
    print MAIL <<EOM;
To: $user_email
From: swcenter\@swc.math.arizona.edu
Subject: Thank you for completing the AWS survey

According to our records, you completed the AWS survey 
on $time from internet host $user_ip.

If you believe you have received this message in error, please reply
to swcenter\@swc.math.arizona.edu as soon as possible.
EOM
    close MAIL or die "Error closing sendmail: $!";
}


# e-mail address validator taken from "CGI Programming with Perl"
# returns a cleaned up address or false
sub validate_email_address {
    my $addr_to_check = shift;
    $addr_to_check =~ s/("(?:[^"\\]|\\.)*"|[^\t "]*)[ \t]*/$1/g;
    
my $esc         = '\\\\';
my $space       = '\040';
my $ctrl        = '\000-\037';
my $dot         = '\.';
my $nonASCII    = '\x80-\xff';
my $CRlist      = '\012\015';
my $letter      = 'a-zA-Z';
my $digit       = '\d';
    
my $atom_char   = qq{ [^$space<>\@,;:".\\[\\]$esc$ctrl$nonASCII] };
    my $atom        = qq{ $atom_char+ };
    my $byte        = qq{ (?: 1?$digit?$digit | 
                              2[0-4]$digit    | 
                              25[0-5]         ) };
    
    my $qtext       = qq{ [^$esc$nonASCII$CRlist"] };
my $quoted_pair = qq{ $esc [^$nonASCII] };
my $quoted_str  = qq{ " (?: $qtext | $quoted_pair )* " };
    
my $word        = qq{ (?: $atom | $quoted_str ) };
my $ip_address  = qq{ \\[ $byte (?: $dot $byte ){3} \\] };
my $sub_domain  = qq{ [$letter$digit]
    [$letter$digit-]{0,61} [$letter$digit]};
my $top_level   = qq{ (?: $atom_char ){2,4} };
my $domain_name = qq{ (?: $sub_domain $dot )+ $top_level };
my $domain      = qq{ (?: $domain_name | $ip_address ) };
my $local_part  = qq{ $word (?: $dot $word )* };
my $address     = qq{ $local_part \@ $domain };
    
return $addr_to_check =~ /^$address$/ox ? $addr_to_check : "";
}
