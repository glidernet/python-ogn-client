#!/usr/bin/perl -w                                                                                                                                                                                                                
use strict;
use Ham::APRS::IS;
use Ham::APRS::FAP qw(parseaprs);
use Data::Dumper;
use warnings;
 
print "connecting to server\n";

# my $is = new Ham::APRS::IS('aprs.glidernet.org:14580', 'PerlEx', 'appid' => 'Perl Example App', 'filter'=>'r/+45.557/+5.976/201.4');
# my $is = new Ham::APRS::IS('aprs.glidernet.org:14580', 'PerlEx', 'appid' => 'Perl Example App', 'filter'=>'r/+48.751171/+11.466587/500');
my $is = new Ham::APRS::IS('glidern3.glidernet.org:14580', 'PerlEx', 'appid' => 'Perl Example App', 'filter'=>'r/+48.751171/+11.466587/500');

$is->connect('retryuntil' => 3) || die "Failed to connect: $is->{error}";
 
my $lastkeepalive = time();
 
while($is->connected()) {
 
    # make sure we send a keep alive every 240 seconds or so                                                                                                                                                                      
    my $now = time();
    if( $now - $lastkeepalive > 240 ) {
        $is->sendline('# example code');
        $lastkeepalive = $now;
    }
 
    # read the line from the server                                                                                                                                                                                               
    my $line = $is->getline();
    next if (!defined $line);
 
    # parse the aprs packet                                                                                                                                                                                                       
    my %packetdata;
    my $retval = parseaprs($line, \%packetdata);
 
    # and display it on the screen                                                                                                                                                                                                
    if ($retval == 1) {
        print "$line\n"; 
	# print Dumper( \%packetdata );
        # say $fh Dumper( \%packetdata );
    }
}

$is->disconnect() || die "Failed to disconnect: $is->{error}";

