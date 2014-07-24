#!/usr/bin/perl

# ----------
# ode.cgi
# ----------

# Author: Rob Reed
# Contact: rob at ode-is-simple.com

# Project: Ode (pronounced oh-dee)
# Website: ode-is-simple.com/
# Weblog:  news.ode-is-simple.com/weblog
# Forum:   ode-is-simple.com/vanilla2_forum/

# License
# ----------

# Creative Commons Attribution-Share Alike 3.0 United States

# For more information refer to:
# http://creativecommons.org/licenses/by-sa/3.0/us/

#
#

#

#
#

# --------------------
# Version Information
# --------------------

# Version: 1.2.3
# build: 2012_1115_00_00_01

# About this version: -


# --------------------
# Changes in this revision and things to be done:
# --------------------

# 1. Fixed a problem with anchor links
# introduced with the behavior for handling relative paths in themes
# with release (r1_2_1).

# ----------
# From the 'description_of_changes' included in the 1.2.1 release:
# ----------
# More about these relative links

# On their own relative links will not work under Ode. Why?

# Relative paths are always interpreted as relative to the request.

# Because Ode is assembling the page from themes which are
# not directly tied to the request path,
# relative paths won't work.

# ...

# Generally speaking, as far as Ode is concerned a URI
# isn't a request for a page at all.
# It's something more like a set of instructions the script can use to
# assemble a page in response to the request.
# ----------

# All of this means that the script must identify, interpret
# and rewrite relative links in theme files
# so that they behave as expected.

# It's just as important that the script interpret and rewrite ONLY
# the relative links.

# In that earlier release I said there are four cases
# we need to be aware of:

# 1. A relative link
# 2. An absolute link
# 3. A link whose value is a complete URI
# 4. A link that starts with a scalar variable name

# But I should have added a 5th:

# 5. anchor links.

# An anchor link, which looks something like:

# a href="#some_anchor"

# Is a special link pointing to a a named anchor tag on the same page
# as the link itself.


# The whole question of relative versus absolute links,
# and the idea of rewriting a link's path,
# is irrelevant with anchor links.

# True, we could create a link to the same page by
# appending the anchor link,
# but that's not a good idea.

# For one thing it's inefficient

# There is no reason to reload the current page.
# (We already have the page loaded.)

# So, we don't want to touch anchor links.

# Luckily, they're easy to identify.

# As far as Ode is concerned,
# any link value beginning with a pound symbol '#'
# is an anchor link.

# With release 1.2.3 the script now leaves these anchor links alone.

# Before 1.2.3 the script treated these as relative links,
# which meant that each anchor link was
# redirected to some other,
# most likely nonexistent, page.

# This has been fixed.

# --------------------

# 2. Revisited how the script manages tags by reworking 3 key subroutines:

# add_tag,
# destroy_tag
# get_tag_value,


# Indexette, which made available along with ode r1.2.3,
# features an 'index-date' tag, which
# the addin uses to manage post dates (see Indexette's documentation
# for more info).

# Indexette makes more extensive use of
# Ode's tags than the few addins that have come before it.
# So this was a good opportunity to
# look at what Ode was doing to manage these tags.

# This was a modification, not a fix.
# There is no change in behavior
# associated with this.


# Let's take a quick look at one of these routines, add_tag.


# add_tag(), that does the work of
# forming a tag and adding it to the post for us, when provided with
# all of the required tag elements:

# 1. The name of the addin
# 2. The tag name
# 3. The tag value
# 4. The absolute path to the post file.

# The routine returns a true value when the tag is added
# successfully, and undef when it is
# unable to add the tag for some reason.

# An invocation of add_tag would look something like:

# &ode::add_tag (
#   addin name,
#   tag name,
#   tag value,
#   absolute path to the post file
# )

# The other two routines are similar.

# (Read the relevant documentation
# or refer to the subroutine definitions in ode.cgi
# for more info about these.)

# --------------------

# 3. Updated version and build numbers.

# --------------------
# --------------------

# Previous Version:

# Version: 1.2.2
# build: 2010_0504_00_00_01

# Previous build: -

# About previous version: -


# ----------
# Message
# ----------

# Welcome to Ode release 1.2.3


# ----------
# Upgrade info
# ----------

# 1. To upgrade the script, replace the current copy of ode.cgi
# with the updated version.

# 2. This does not affect the configuration of your site.
# Furthermore, it should not usually be necessary to replace the config file
# as part of the upgrade process.

# 3. You may need to edit the two configurable variables...

# 1. $config_dir_f,
# 2. $config_filename_f

# ...in the clearly marked 'CONFIGURATION SECTION' (below), so that
# the script can locate the config file.


# ----------
# Notes
# ----------

# 1. If you are installing or configuring Ode
# you will want to jump to the short configuration section
# just below.


# ----------
# About the project name and mascot:
# ----------

# o d e

# The project name may change.

# I'd like to stick with something very close to 'Ode',
# but I'd prefer a name that's a bit more
# phonetic (o-dee).

# Also, it would suggested to me that it might be better
# to choose a unique name that
# turns up only relevant results when searching.

# Any ideas?


# c o d

# The project mascot, as featured on the ode-is-simple.com site
# is an Atlantic Cod.

# The fish is historically important to the economy of the eastern United
# States, which places
# the origin of the project geographically.

# Why this image?

# This particular image is in the public domain (from the US National
# Oceanic and Atmospheric Administration.

# http://en.wikipedia.org/wiki/File:Atlantic_cod.jpg

# It's well designed and intricate enough to be distinctive without being
# fancy or embellished.

# It looks like an 'Odie' to me.

# It's perfect for a t-shirt.


# ^ Info
# --------------
# v Beginning of source code


package ode;

require v5.6;

use strict;                 # http://perldoc.perl.org/strict.html

use Time::Local;            # http://perldoc.perl.org/Time/Local.html
use File::Find;             # http://perldoc.perl.org/File/Find.html
use File::Spec;             # http://perldoc.perl.org/File/Spec.html
use File::Basename;         # http://perldoc.perl.org/File/Basename.html
use File::stat;             # http://perldoc.perl.org/File/stat.html
use CGI;                    # http://perldoc.perl.org/CGI.html
use POSIX qw(tzset tzname); # http://perldoc.perl.org/POSIX.html

use constant VERSION_NUMBER => "1.2.1";
use constant BUILD_NUMBER => "2010_0427_00_00_01";

use constant MIN_ERROR_LEVEL => 1;
use constant MAX_ERROR_LEVEL => 4;

use constant WARNING_THRESHOLD => 3;

use constant EARLIEST_YEAR => 1969;

my (
    $config_dir_f,
    $config_filename_f,

    $config_file_f,
);



# CONFIGURATION SECTION -----------------------------------------------------


# $config_dir_f
# -------------

# The value of $config_dir_f is a string specifying
# the absolute path to the directory containing the config file.

# Note: The string _should begin_ with a leading forward slash
# (because the value should be an absolute path)
# _and end_ with a trailing forward slash
# (because strings which specify paths in the script
# always end with a trailing path delimiter as a matter of convention),

# !Also note that the forward slash is always used as the path-delimiter
# regardless of platform!

# (See the note immediately following the configuration section for
# more info.)

# Default value:
# ''

# Example:
# $config_dir_f = '/Library/WebServer/Data/ode/';

$config_dir_f = '';


# $config_filename_f
# ------------------

# The value of $config_filename_f is a string specifying the name of
# the config file. It is appended to
# the end of the value at $config_dir_f
# to construct the full path to the configuration file
# at $config_file_f.

# (Do not include any path info here - that's what $config_dir_f is for.)

# Default value:
# 'ode_config'

# Recommended value:
# 'ode_config'

# Example:
# $config_filename_f = 'ode_config';

$config_filename_f = 'ode_config';


# END, CONFIGURATION SECTION -----------------------------------------------



# You should not need to make ANY modifications to below this point.

# Of course you are free to make whatever changes you like
# (restricted only by the terms license above),
# but you should realize that you will no longer be working within the bounds
# of this project if you do so
# (which is a-ok as long as you understand this point).

# If you would rather continue working on this project, and you think that
# you need to modify something about the script to accomplish
# whatever it is that you want to do, please bring it up so that we can
# discuss your proposed changes.


# About using a forward slash is used as the path delimiter.

# Though it might seem that this is not a portable way to handle paths,
# (different platforms use different path delimiters),
# Perl, left to its on devices, handles this issue quite well.

# In fact standard modules like File::Spec,
# which are intended to deal with file specifications
# in platform-specific ways are used sparingly.
# This is because it can be more difficult
# to resolve the sorts of inconsistencies and eccentricities
# introduced by these modules than it is to simply leave the issue to perl.

# Refer to the Perl documentation for more information about
# File::Spec
# http://perldoc.perl.org/File/Spec.html

# Please be consistent about this to avoid introducing annoying bugs.

# ^ End of Configuration
# --------------
# v Start of package global declarations

our (
    $version, $build, $min_error_level, $max_error_level, $use_local_time_g,
    $tz_uniform_name_g, $req_string, $req_base_url, $req_path_with_file,
    $req_path_wo_file, $req_fs_path_with_file, $req_fs_path_wo_file,
    $req_year_in_path, $req_month_num_in_path, $req_month_day_in_path,
    $req_hour_in_path, $req_min_in_path, $req_sec_in_path, $req_filename,
    $req_theme, $req_breadcrumb_trail, $discover_posts, $find_req_theme,
    $interpolate, $posts_sort, %manipulate_request_addins,
    %pre_filter_posts_addins, %filter_posts_addins, $mtime_cur_post,
    %access_head_theme_early_addins, %access_date_theme_early_addins,
    %mod_post_file_before_read_addins, $found_theme_url,
    %access_title_tags_and_body_early_addins, $exempt_file_g,
    %access_posts_theme_early_addins, %access_foot_theme_early_addins,
    %access_page_late_addins, $path, $post_breadcrumb_trail, $filename,
    $title, $tags, $body, $year, $month_name, $month_num, $month_day,
    $wkday_name, $time, $hour, $hour_12, $am_pm, $min, $sec,
    $post_advertised_time_zone, $page_title, $first_post, $num_posts,
    $previous_count, $previous_first_post, $previous_post_string, $next_count,
    $next_first_post, $next_post_string, $previous_and_next_post_string,
    $show_tags_g, $response, $response_string, $skip_page_generation_g,
    $request_type, $request_is_type_root_g, $request_is_type_post_g,
    $request_is_type_category_g, $req_is_date_restricted_g,
    $req_path_is_date_restricted_g, $req_includes_date_range_param_g,
    %req_components_at_sub, %req_components_final,
    %req_query_string_components_at_sub, %req_query_string_components_final,
    $data_theme_message, $test_sort_sub
);

my (
    $cgi_req_object_f, %req_components_working_f, $ffp_to_post_unixtime_hrf,
    %req_query_string_components_working_f, $date_string_in_path_f,
);

sub discover_posts_baked_in
{
    my (

        %ffp_to_post_unixtime_hrs,

        $compare_paths_and_posts_to_exempt_s,

        @exemption_rules_s,

        $at_least_one_exemption_s,
    );

    $compare_paths_and_posts_to_exempt_s = undef;

    $compare_paths_and_posts_to_exempt_s =
        $config::compare_paths_and_posts_to_exempt;

    @exemption_rules_s = ();

    if ($compare_paths_and_posts_to_exempt_s)
    {

        if ( !(open (EXEMPTION_FILE, "< $exempt_file_g")) )
        {

            { # Naked block

                my ($warn_level_l, $resp_level_l,);

                $warn_level_l = $min_error_level +1;
                $resp_level_l = $max_error_level -1;

                &handle_warning_and_response (
                    "ode : discover_posts",

                    "Cannot open file containing exemption rules at:\n" .
                    "$exempt_file_g\n" .
                    "Continuing with exemption mechanism disabled.\n" .
                    "Check the path and permissions.\n" .
                    "System msg: $!\n",

                    "Cannot read exemption rules. Exemptions are disabled.\n",

                    $warn_level_l, $resp_level_l
                );

            } # End, Naked block

            $compare_paths_and_posts_to_exempt_s = 0;

        } # End, if ( !(open (EXEMPTION_FILE, "< $exempt_file_g")) )

        else
        {

            $at_least_one_exemption_s = undef;

            $at_least_one_exemption_s = 0;

            foreach my $line_l (<EXEMPTION_FILE>)
            {

                next if $line_l !~ m/[^\s]/;

                chomp $line_l;

                $line_l =~ s/(^\s+)//;

                $line_l =~ s/(\s+$)//;

                push(@exemption_rules_s, $line_l);

            } # End, foreach my $line_l (<EXEMPTION_FILE>)

            $at_least_one_exemption_s = 1 if @exemption_rules_s;

        } # End, else

    } # End, if ($compare_paths_and_posts_to_exempt_s)

    find (

        sub
        {
            my (
                $config_post_file_ext_length_l,
                $post_date_l,
            );

            $config_post_file_ext_length_l = length $config::post_file_ext;

            if ( substr($_, -($config_post_file_ext_length_l +1)) eq ".$config::post_file_ext" and
                $_ ne "index.$config::post_file_ext" and
                $File::Find::name !~ m!/themes/! and
                !( &item_is_disabled($File::Find::name) ) and
                (  ( ($post_date_l = stat($File::Find::name)->mtime) <= time ) or $config::show_future_posts  ) and
                -f _ and
                -r _ )
            {

                if ($compare_paths_and_posts_to_exempt_s and
                    $at_least_one_exemption_s)
                {
                    foreach my $rule_l (@exemption_rules_s)
                    {
                        if ($File::Find::name =~ m/$rule_l/)
                        {

                            { # Naked block

                                my ($warn_level_l, $resp_level_l,);

                                $warn_level_l = $max_error_level -1;
                                $resp_level_l = $max_error_level;

                                &handle_warning_and_response (
                                    "ode : discover_posts",

                                    "Skipping file: $File::Find::name\n" .
                                    "The post is exempt\n" .
                                    "Continuing.\n",

                                    "Skipping exempt post: " .
                                        "$File::Find::name\n",

                                    $warn_level_l, $resp_level_l
                                );

                            } # End, Naked block

                            return;

                        } # End, if ($File::Find::name =~ m/$rule/)

                    } # End, foreach my $rule_l (@exemption_rules_s)

                } # End, if ($compare_paths_and_posts_to_exempt_s and...

                $ffp_to_post_unixtime_hrs{$File::Find::name} = $post_date_l;

            } # End, if ( substr($_, -($config_post_file_ext_length_l +1))...

        }, $config::document_root

    ); # End, find (

    return \%ffp_to_post_unixtime_hrs;

}; # End, sub discover_posts_baked_in

$find_req_theme = sub
{

    my ($num_posts_s, ) = @_;

    my (
        @bpath_cmpnts_s, $ffp_theme_file_s, %theme_components_s,
        @theme_file_names_s, %theme_cmpnts_s, %error_theme_s,

        $req_theme_name_working_s,
        $req_theme_component_name_working_s,
    );

    %error_theme_s = ();

    while (<DATA>)
    {

        last if /^(__END__)$/;

        {   # Start of naked block.

            my (
                $theme_l, $component_l,
                $content_l,
            );

            ($theme_l, $component_l, $content_l) = /^(\S+)\s(\S+)\s*(.*)$/
                or next;

            $content_l =~ s/\\n/\n/mg;

            $error_theme_s{$component_l} .= $content_l . "\n";

        } # End, Naked block

    } # End, while (<DATA>)

    $req_theme_name_working_s = undef;

    $req_theme_component_name_working_s = $req_theme_name_working_s = $req_components_final{theme};

    @bpath_cmpnts_s = split(/\//, $req_components_final{fs_path_wo_file});

    shift @bpath_cmpnts_s if $bpath_cmpnts_s[0] eq '';

    @theme_file_names_s = ();

    if ($num_posts_s > 0)
    {
        @theme_file_names_s = qw( content_type date page );
    }

    else
    {
        @theme_file_names_s = qw( content_type date page_no_posts );
    }

    %theme_components_s = ();

    %theme_components_s = (
        content_type    => undef,
        date            => undef,
        head            => undef,
        posts           => undef,
        foot            => undef,
    );

    if (!$config::use_site_look_date)
    {

        do {{

            my (
                $bpath_working_l, $ffp_to_themes_dir_working_l,
                $ffp_to_req_theme_working_l, @sorted_req_theme_archives_l,
                @themes_dir_contents_l,
            );

            $bpath_working_l = undef;

            $bpath_working_l = join '/', @bpath_cmpnts_s;

            $ffp_to_themes_dir_working_l = undef;

            $ffp_to_themes_dir_working_l = $config::document_root;

            $ffp_to_themes_dir_working_l .= '/' . $bpath_working_l
                if $bpath_working_l;

            $ffp_to_themes_dir_working_l .= '/' . 'themes' . '/';

            $ffp_to_req_theme_working_l = undef;

            $ffp_to_req_theme_working_l = $ffp_to_themes_dir_working_l . $req_theme_name_working_s . '/';

            if ( !(-d $ffp_to_req_theme_working_l and -r _ and -x _) )
            {

                if (-d _)
                {

                    if ( !(-r _) and !(-x _) )
                    {

                        { # Naked block

                            my ($warn_level_l, $resp_level_l,);

                            $warn_level_l = $min_error_level +1;
                            $resp_level_l = $max_error_level;

                            &handle_warning_and_response (
                                "ode : find_req_theme",

                                "The requested theme was found at:\n" .
                                "$ffp_to_req_theme_working_l\n" .
                                "but the theme directory cannot be read\n" .
                                "and cannot be executed \n" .
                                "(component files cannot be found).\n" .
                                "You must correct _both_ problems.\n" .
                                "Skipping and continuing to " .
                                    "look for themes.\n",

                                "Unreadable version of theme encountered. " .
                                    "Continuing\n",

                                $warn_level_l, $resp_level_l
                            );

                        } # End, Naked block

                    } # End, if ( !(-r _) and !(-x _) )

                    elsif (!(-r _))
                    {

                        { # Naked block

                            my ($warn_level_l, $resp_level_l,);

                            $warn_level_l = $min_error_level +1;
                            $resp_level_l = $max_error_level;

                            &handle_warning_and_response (
                                "ode : find_req_theme",

                                "The requested theme was found at:\n" .
                                "$ffp_to_req_theme_working_l\n" .
                                "but the theme directory cannot be read. \n" .
                                "Skipping and continuing to " .
                                    "look for themes.\n",

                                "Unreadable version of theme encountered. " .
                                    "Continuing\n",

                                $warn_level_l, $resp_level_l
                            );

                        } # End, Naked block

                    } # End, elsif (!(-r _))

                    else
                    {

                        { # Naked block

                            my ($warn_level_l, $resp_level_l,);

                            $warn_level_l = $min_error_level +1;
                            $resp_level_l = $max_error_level;

                            &handle_warning_and_response (
                                "ode : find_req_theme",

                                "The requested theme was found at:\n" .
                                "$ffp_to_req_theme_working_l\n" .
                                "but the theme directory " .
                                    "cannot be executed \n" .
                                "(component files cannot be read).\n" .
                                "Skipping and continuing to " .
                                    "look for themes.\n",

                                "Unreadable version of theme encountered. " .
                                    "Continuing\n",

                                $warn_level_l, $resp_level_l
                            );

                        } # End, Naked block

                    } # End, else

                } # End, if (-d _)

                next;

            } # End, if ( !(-d $ffp_to_req_theme_working_l and -r _ and -x _) )

            foreach my $theme_file_name_l (@theme_file_names_s)
            {

                $ffp_theme_file_s = $ffp_to_req_theme_working_l . "$theme_file_name_l.$req_theme_component_name_working_s";

                if (open THEME_FILE, "< $ffp_theme_file_s")
                {

                    if ($theme_file_name_l eq 'content_type')
                    {
                        $theme_components_s{content_type} =
                            join '', <THEME_FILE>;

                        $theme_components_s{content_type} =~ s/\n$//;
                    }

                    elsif ($theme_file_name_l eq 'date')
                    {
                        $theme_components_s{date} = join '', <THEME_FILE>;
                    }

                    elsif ($theme_file_name_l eq 'page' or $theme_file_name_l eq 'page_no_posts')
                    {

                        my (
                            $page_section_l,
                        );

                        $page_section_l = 'head';

                        while (my $line = <THEME_FILE>)
                        {

                            if ( substr($line, 0,
                                   length($config::page_delimiter_head_posts))
                                     eq $config::page_delimiter_head_posts
                               )
                            {
                                $page_section_l = 'posts';
                                next;
                            }

                            if ( substr($line, 0,
                                   length($config::page_delimiter_posts_foot))
                                     eq $config::page_delimiter_posts_foot
                               )
                            {
                                $page_section_l = 'foot';
                                next;
                            }

                            if ($page_section_l eq 'head')
                            {
                                $theme_components_s{head} .= $line;
                            }
                            elsif ($page_section_l eq 'posts')
                            {
                                $theme_components_s{posts} .= $line;
                            }
                            elsif ($page_section_l eq 'foot')
                            {
                                $theme_components_s{foot} .= $line;
                            }

                        } # End, while (my $line = <THEME_FILE>)

                    } # End, elsif ($theme_file_name_l eq 'page' or ...)

                } # End, if (open THEME_FILE, "< $ffp_theme_file_s")

                else
                {

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $max_error_level;

                        &handle_warning_and_response (
                            "ode : find_req_theme",

                            "Unable to open theme file at:\n" .
                            "'$ffp_theme_file_s'\n" .
                            "The file may be missing or check permissions.\n" .
                            "System msg: $!\n",

                            "Unable to open one of the files " .
                                "for the found theme.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                    return \%error_theme_s;

                } # End, else

            } # End, foreach my $theme_file_name_l (@theme_file_names_s)

            $found_theme_url = undef;

            $found_theme_url = $config::document_root_url;

            ($found_theme_url) .= substr($ffp_to_req_theme_working_l, length
            $config::document_root);

            return \%theme_components_s;

        }} while (pop @bpath_cmpnts_s);

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $min_error_level;

            &handle_warning_and_response (
                "ode : find_req_theme",

                "Unable to find requested theme: " .
                    "$req_components_at_sub{theme}\n" .
                "along the path to the post.\n" .
                "Returning baked-in error theme instead.\n",

                "There doesn't seem to be a '$req_theme' theme. " .
                    "Try dropping the suffix from the requested page name " .
                    "to use the default theme.\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return \%error_theme_s;

    } # End, if (!$config::use_site_look_date)

    else
    {

        if (!$req_query_string_components_final{site_look_date})
        {

            do {{

                my (
                    $bpath_working_l, $ffp_to_themes_dir_working_l,
                    $ffp_to_req_theme_working_l, @sorted_req_theme_archives_l,
                    @themes_dir_contents_l
                );

                $bpath_working_l = undef;

                $bpath_working_l = join '/', @bpath_cmpnts_s;

                $ffp_to_themes_dir_working_l = undef;

                $ffp_to_themes_dir_working_l = $config::document_root;

                $ffp_to_themes_dir_working_l .= '/' . $bpath_working_l
                    if $bpath_working_l;

                $ffp_to_themes_dir_working_l .= '/' . 'themes' . '/';

                if ( !(opendir(THEMES_DIR, $ffp_to_themes_dir_working_l)) )
                {

                    if (-d $ffp_to_themes_dir_working_l)
                    {

                        { # Naked block

                            my ($warn_level_l, $resp_level_l,);

                            $warn_level_l = $min_error_level +1;
                            $resp_level_l = $max_error_level;

                            &handle_warning_and_response (
                                "ode : find_req_theme",

                                "The themes directory: " .
                                    "'$ffp_to_themes_dir_working_l' \n" .
                                "exists but cannot be opened. \n" .
                                "Continung to look for themes further from " .
                                    "the request.\n",

                                "Cannot open themes directory encountered. " .
                                    "Continuing. \n",

                                $warn_level_l, $resp_level_l
                            );

                        } # End, Naked block

                    } # End, if (-d $ffp_to_themes_dir_working_l)

                    next;

                } # End, if ( !(opendir(THEMES_DIR, $ffp_to_themes_dir_w...

                if ( !(@themes_dir_contents_l = readdir(THEMES_DIR)) )
                {

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $max_error_level;

                        &handle_warning_and_response (
                            "ode : find_req_theme",

                            "The themes directory: " .
                                "'$ffp_to_themes_dir_working_l' \n" .
                            "exists but cannot be read. \n" .
                            "Continuing to look for themes further from " .
                                "the request. \n",

                            "Unreadable themes directory encountered. " .
                                "Continuing. \n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                    next;

                } # End, if ( !(@themes_dir_contents_l = readdir(THEMES_D ...

                @sorted_req_theme_archives_l = undef;

                @sorted_req_theme_archives_l = grep (
                    {/^$req_theme_name_working_s[-]\d{4}_*\d{2}_*\d{2}$/
                    && -d "$ffp_to_themes_dir_working_l/$_"} sort
                        site_look_date_sort @themes_dir_contents_l );

                next if @sorted_req_theme_archives_l == 0;

                $req_theme_name_working_s = $sorted_req_theme_archives_l[$#sorted_req_theme_archives_l];

                $ffp_to_req_theme_working_l = undef;

                $ffp_to_req_theme_working_l = $ffp_to_themes_dir_working_l . $req_theme_name_working_s . '/';

                if ( !(-d $ffp_to_req_theme_working_l and -r _ and -x _) )
                {

                    if (-d _)
                    {

                        if ( !(-r _) and !(-x _) )
                        {

                            { # Naked block

                                my ($warn_level_l, $resp_level_l,);

                                $warn_level_l = $min_error_level +1;
                                $resp_level_l = $max_error_level;

                                &handle_warning_and_response (
                                    "ode : find_req_theme",

                                    "The requested theme was found at:\n" .
                                    "$ffp_to_req_theme_working_l\n" .
                                    "but the theme directory cannot " .
                                        "be read\n" .
                                    "and cannot be executed \n" .
                                    "(component files cannot be found).\n" .
                                    "You must correct _both_ problems.\n" .
                                    "Skipping and continuing to look for " .
                                        "themes.\n",

                                    "Unreadable version of theme " .
                                        "encountered. Continuing\n",

                                    $warn_level_l, $resp_level_l
                                );

                            } # End, Naked block

                        } # End, if ( !(-r _) and !(-x _) )

                        elsif (!(-r _))
                        {

                            { # Naked block

                                my ($warn_level_l, $resp_level_l,);

                                $warn_level_l = $max_error_level -1;
                                $resp_level_l = $max_error_level;

                                &handle_warning_and_response (
                                    "ode : find_req_theme",

                                    "The requested theme was found at:\n" .
                                    "$ffp_to_req_theme_working_l\n" .
                                    "but the theme directory " .
                                        "cannot be read. \n" .
                                    "Skipping and continuing to look for " .
                                        "themes.\n",

                                    "Unreadable version of theme " .
                                        "encountered. Continuing\n",

                                    $warn_level_l, $resp_level_l
                                );

                            } # End, Naked block

                        } # End, elsif (!(-r _))

                        else
                        {

                            { # Naked block

                                my ($warn_level_l, $resp_level_l,);

                                $warn_level_l = $min_error_level +1;
                                $resp_level_l = $max_error_level;

                                &handle_warning_and_response (
                                    "ode : find_req_theme",

                                    "The requested theme was found at:\n" .
                                    "$ffp_to_req_theme_working_l\n" .
                                    "but the theme directory " .
                                        "cannot be executed \n" .
                                    "(component files cannot be read).\n" .
                                    "Skipping and continuing to look for " .
                                        "themes.\n",

                                    "Unreadable version of theme " .
                                    "encountered. Continuing\n",

                                    $warn_level_l, $resp_level_l
                                );

                            } # End, Naked block

                        } # End, else

                    } # End, if (-d _)

                    next;

                } # End, if ( !(-d $ffp_to_req_theme_working_l and -r _ and -x _) )

                foreach my $theme_file_name_l (@theme_file_names_s)
                {

                    $ffp_theme_file_s = $ffp_to_req_theme_working_l . "$theme_file_name_l.$req_theme_component_name_working_s";

                    if (open THEME_FILE, "< $ffp_theme_file_s")
                    {

                        if ($theme_file_name_l eq 'content_type')
                        {
                            $theme_components_s{content_type} =
                                join '', <THEME_FILE>;

                            $theme_components_s{content_type} =~ s/\n$//;
                        }

                        elsif ($theme_file_name_l eq 'date')
                        {
                            $theme_components_s{date} = join '', <THEME_FILE>;
                        }

                        elsif ($theme_file_name_l eq 'page' or $theme_file_name_l eq 'page_no_posts')
                        {

                            my (
                                $page_section_l,
                            );

                            $page_section_l = 'head';

                            while (my $line = <THEME_FILE>)
                            {

                                if ( substr($line, 0, length($config::page_delimiter_head_posts)) eq $config::page_delimiter_head_posts )
                                {
                                    $page_section_l = 'posts';
                                    next;
                                }

                                if ( substr($line, 0, length($config::page_delimiter_posts_foot)) eq $config::page_delimiter_posts_foot )
                                {
                                    $page_section_l = 'foot';
                                    next;
                                }

                                if ($page_section_l eq 'head')
                                {
                                    $theme_components_s{head} .= $line;
                                }
                                elsif ($page_section_l eq 'posts')
                                {
                                    $theme_components_s{posts} .= $line;
                                }
                                elsif ($page_section_l eq 'foot')
                                {
                                    $theme_components_s{foot} .= $line;
                                }

                            } # End, while (my $line = <THEME_FILE>)

                        } # End, elsif ($theme_file_name_l eq 'page' or ...)

                    } # End, if (open THEME_FILE, "< $ffp_theme_file_s")

                    else
                    {

                        { # Naked block

                            my ($warn_level_l, $resp_level_l,);

                            $warn_level_l = $min_error_level +1;
                            $resp_level_l = $max_error_level;

                            &handle_warning_and_response (
                                "ode : find_req_theme",

                                "Unable to open theme file at:\n" .
                                "'$ffp_theme_file_s'\n" .
                                "The file may be missing or check " .
                                    "permissions.\n" .
                                "System msg: $!\n",

                                "Unable to open one of the files " .
                                    "for the found theme.\n",

                                $warn_level_l, $resp_level_l
                            );

                        } # End, Naked block

                        return \%error_theme_s;

                    } # End, else

                } # End, foreach my $theme_file_name_l (@theme_file_names_s)

                $found_theme_url = undef;

                $found_theme_url = $config::document_root_url;

                ($found_theme_url) .= substr($ffp_to_req_theme_working_l, length $config::document_root);

                return \%theme_components_s;

            }} while (pop @bpath_cmpnts_s);

            { # Naked block

                my ($warn_level_l, $resp_level_l,);

                $warn_level_l = $min_error_level +1;
                $resp_level_l = $min_error_level;

                &handle_warning_and_response (
                    "ode : find_req_theme",

                    "Unable to find requested theme: " .
                        "$req_components_at_sub{theme}\n" .
                    "along the path to the post.\n" .
                    "Returning baked-in error theme instead.\n",

                    "There doesn't seem to be a '$req_theme' theme. " .
                        "Try dropping the suffix from the " .
                            "requested page name to use the " .
                            "default theme.\n",

                    $warn_level_l, $resp_level_l
                );

            } # End, Naked block

            return \%error_theme_s;

        } # End, if (!$req_query_string_components_final{site_look_date})

        else
        {

            my (
                $ffp_to_best_fit_theme_working_l,
                $ffp_to_current_closest_theme_l, $ffp_to_req_theme_working_l,
            );

            do {{

                my (
                    $bpath_working_l, $ffp_to_themes_dir_working_l,
                    @sorted_req_theme_archives_l,
                    @themes_dir_contents_l, $theme_date_substr_l,
                    $cur_best_fit_date_substr_l,
                );

                $bpath_working_l = undef;

                $bpath_working_l = join '/', @bpath_cmpnts_s;

                $ffp_to_themes_dir_working_l = undef;

                $ffp_to_themes_dir_working_l = $config::document_root;

                $ffp_to_themes_dir_working_l .= '/' . $bpath_working_l
                    if $bpath_working_l;

                $ffp_to_themes_dir_working_l .= '/' . 'themes' . '/';

                if ( !(opendir(THEMES_DIR, $ffp_to_themes_dir_working_l)) )
                {

                    if (-d $ffp_to_themes_dir_working_l)
                    {

                        { # Naked block

                            my ($warn_level_l, $resp_level_l,);

                            $warn_level_l = $min_error_level +1;
                            $resp_level_l = $max_error_level;

                            &handle_warning_and_response (
                                "ode : find_req_theme",

                                "The themes directory: " .
                                    "'$ffp_to_themes_dir_working_l' \n" .
                                "exists but cannot be opened. \n" .
                                "Continung to look for themes further from " .
                                    "the request.\n",

                                "Cannot open themes directory encountered. " .
                                    "Continuing. \n",

                                $warn_level_l, $resp_level_l
                            );

                        } # End, Naked block

                    } # End, if (-d $ffp_to_themes_dir_working_l)

                    next;

                } # End, if ( !(opendir(THEMES_DIR, $ffp_to_themes_dir_w...

                if ( !(@themes_dir_contents_l = readdir(THEMES_DIR)) )
                {

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $max_error_level;

                        &handle_warning_and_response (
                            "ode : find_req_theme",

                            "The themes directory: " .
                                "'$ffp_to_themes_dir_working_l' \n" .
                            "exists but cannot be read. \n" .
                            "Continuing to look for themes further from " .
                                "the request. \n",

                            "Unreadable themes directory encountered. " .
                                "Continuing. \n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                    next;

                } # End, if ( !(@themes_dir_contents_l = readdir(THEMES_ ...

                @sorted_req_theme_archives_l = undef;

                @sorted_req_theme_archives_l = grep (
                    {/^$req_theme_name_working_s[-]\d{4}_*\d{2}_*\d{2}$/
                    && -d "$ffp_to_themes_dir_working_l/$_"} sort
                        site_look_date_sort @themes_dir_contents_l );

                next if @sorted_req_theme_archives_l == 0;

                if (!defined($ffp_to_current_closest_theme_l))
                {

                    $ffp_to_current_closest_theme_l = $ffp_to_themes_dir_working_l . $sorted_req_theme_archives_l[$#sorted_req_theme_archives_l] . '/';

                } # End, if (!defined($ffp_to_current_closest_theme_l))

                foreach my $theme_l (@sorted_req_theme_archives_l)
                {

                    $theme_date_substr_l =
                        $cur_best_fit_date_substr_l = undef;

                    if ($theme_l =~ m/^.*[-](\d{4})_*(\d{2})_*(\d{2})$/)
                    {
                        $theme_date_substr_l = "$1$2$3";
                    }
                    else
                    {
                        next;
                    }

                    if ($ffp_to_best_fit_theme_working_l =~ m!^.*(\d{4})_*(\d{2})_*(\d{2})/?$!)
                    {
                        $cur_best_fit_date_substr_l = "$1$2$3";
                    }

                    if (($theme_date_substr_l <= $req_query_string_components_final{site_look_date}) and ($theme_date_substr_l > $cur_best_fit_date_substr_l))
                    {

                        $ffp_to_best_fit_theme_working_l = $ffp_to_themes_dir_working_l . $theme_l . '/';

                    }

                    last if $theme_date_substr_l >= $req_query_string_components_final{site_look_date};

                } # End, foreach my $theme_l (@sorted_req_theme_archives_l)

                if ( defined($ffp_to_best_fit_theme_working_l) )
                {

                    @bpath_cmpnts_s = ();

                } # End, if ( defined($ffp_to_best_fit_theme_working_l) )

            }} while (pop @bpath_cmpnts_s); # End, while (pop @bpath_cmpnts_s)

            $ffp_to_req_theme_working_l = '';

            if (defined($ffp_to_best_fit_theme_working_l))
            {
                $ffp_to_req_theme_working_l = $ffp_to_best_fit_theme_working_l;
            }

            elsif (defined($ffp_to_current_closest_theme_l))
            {

                { # Naked block

                    my ($warn_level_l, $resp_level_l,);

                    $warn_level_l = $min_error_level +1;
                    $resp_level_l = $max_error_level -1;

                    &handle_warning_and_response (
                        "ode : find_req_theme",

                        "Unable to find a best fit (dated) theme matching: " .
                            "$req_components_at_sub{theme}\n" .
                        "along the path to the post.\n" .
                        "Requested date is earlier than all themes.\n" .
                        "Using current theme instead.\n",

                        "site_look_date value is earlier than all dated " .
                            "themes. " .
                            "Using current version theme.\n",

                        $warn_level_l, $resp_level_l
                    );

                } # End, Naked block

                $ffp_to_req_theme_working_l = $ffp_to_current_closest_theme_l;

            }

            else
            {

                { # Naked block

                    my ($warn_level_l, $resp_level_l,);

                    $warn_level_l = $min_error_level +1;
                    $resp_level_l = $min_error_level;

                    &handle_warning_and_response (
                        "ode : find_req_theme",

                        "Unable to find requested theme: " .
                            "'$req_components_at_sub{theme}'\n" .
                        "along the path to the post.\n" .
                        "Returning baked-in error theme instead.\n",

                        "There doesn't seem to be a '$req_theme' theme. " .
                            "Try dropping the suffix from the " .
                            "requested page " .
                            "name to use the default theme.\n",

                        $warn_level_l, $resp_level_l
                    );

                } # End, Naked block

                return \%error_theme_s;

            } # End, else

            if ( !(-d $ffp_to_req_theme_working_l and -r _ and -x _) )
            {

                if (-d _)
                {

                    if ( !(-r _) and !(-x _) )
                    {

                        { # Naked block

                            my ($warn_level_l, $resp_level_l,);

                            $warn_level_l = $min_error_level +1;
                            $resp_level_l = $max_error_level;

                            &handle_warning_and_response (
                                "ode : find_req_theme",

                                "The requested theme was found at:\n" .
                                "$ffp_to_req_theme_working_l\n" .
                                "but the theme directory cannot be read\n" .
                                "and cannot be executed \n" .
                                "(component files cannot be found).\n" .
                                "You must correct _both_ problems.\n" .
                                "Skipping and continuing to look for " .
                                    "themes.\n",

                                "Unreadable version of theme encountered. " .
                                    "Continuing\n",

                                $warn_level_l, $resp_level_l
                            );

                        } # End, Naked block

                    } # End, if ( !(-r _) and !(-x _) )

                    elsif (!(-r _))
                    {

                        { # Naked block

                            my ($warn_level_l, $resp_level_l,);

                            $warn_level_l = $min_error_level +1;
                            $resp_level_l = $max_error_level;

                            &handle_warning_and_response (
                                "ode : find_req_theme",

                                "The requested theme was found at:\n" .
                                "$ffp_to_req_theme_working_l\n" .
                                "but the theme directory cannot be read.\n" .
                                "Skipping and continuing to look for " .
                                    "themes.\n",

                                "Unreadable version of theme encountered. " .
                                    "Continuing\n",

                                $warn_level_l, $resp_level_l
                             );

                        } # End, Naked block

                    } # End, elsif (!(-r _))

                    else
                    {

                        { # Naked block

                            my ($warn_level_l, $resp_level_l,);

                            $warn_level_l = $min_error_level +1;
                            $resp_level_l = $max_error_level;

                            &handle_warning_and_response (
                                "ode : find_req_theme",

                                "The requested theme was found at:\n" .
                                "$ffp_to_req_theme_working_l\n" .
                                "but the theme directory " .
                                    "cannot be executed \n" .
                                "(component files cannot be read).\n" .
                                "Skipping and continuing to look for " .
                                    "themes.\n",

                                "Unreadable version of theme encountered. " .
                                    "Continuing\n",

                                $warn_level_l, $resp_level_l
                            );

                        } # End, Naked block

                    } # End, else

                } # End, if (-d _)

                return \%error_theme_s;

            } # End, if ( !(-d $ffp_to_req_theme_working_l and -r _ and -x _) )

            foreach my $theme_file_name_l (@theme_file_names_s)
            {

                $ffp_theme_file_s = $ffp_to_req_theme_working_l . "$theme_file_name_l.$req_theme_component_name_working_s";

                if (open THEME_FILE, "< $ffp_theme_file_s")
                {

                    if ($theme_file_name_l eq 'content_type')
                    {
                        $theme_components_s{content_type} =
                            join '', <THEME_FILE>;

                        $theme_components_s{content_type} =~ s/\n$//;
                    }

                    elsif ($theme_file_name_l eq 'date')
                    {
                        $theme_components_s{date} = join '', <THEME_FILE>;
                    }

                    elsif ($theme_file_name_l eq 'page' or $theme_file_name_l eq 'page_no_posts')
                    {

                        my (
                            $page_section_l,
                        );

                        $page_section_l = 'head';

                        while (my $line = <THEME_FILE>)
                        {

                            if ( substr($line, 0,
                                   length($config::page_delimiter_head_posts))
                                     eq $config::page_delimiter_head_posts
                               )
                            {
                                $page_section_l = 'posts';
                                next;
                            }

                            if ( substr($line, 0,
                                   length($config::page_delimiter_posts_foot))
                                     eq $config::page_delimiter_posts_foot
                               )
                            {
                                $page_section_l = 'foot';
                                next;
                            }

                            if ($page_section_l eq 'head')
                            {
                                $theme_components_s{head} .= $line;
                            }
                            elsif ($page_section_l eq 'posts')
                            {
                                $theme_components_s{posts} .= $line;
                            }
                            elsif ($page_section_l eq 'foot')
                            {
                                $theme_components_s{foot} .= $line;
                            }

                        } # End, while (my $line = <THEME_FILE>)

                    } # End, elsif ($theme_file_name_l eq 'page' or ...)

                } # End, if (open THEME_FILE, "< $ffp_theme_file_s")

                else
                {

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $max_error_level;

                        &handle_warning_and_response (
                            "ode : find_req_theme",

                            "Unable to open theme file at:\n" .
                            "'$ffp_theme_file_s'\n" .
                            "The file may be missing or check " .
                                "permissions.\n" .
                            "System msg: $!\n",

                            "Unable to open one of the files " .
                                "for the found theme.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                    return \%error_theme_s;

                } # End, else

            } # End, foreach my $theme_file_name_l (@theme_file_names_s)

            $found_theme_url = undef;

            $found_theme_url = $config::document_root_url;

            ($found_theme_url) .= substr($ffp_to_req_theme_working_l, length
            $config::document_root);

            return \%theme_components_s;

        } # End, else (Case 3)

    }   # End, else (mode 2, the site_look_date_mechanism is enabled)

}; # End, $find_req_theme = sub {

sub generate_page
{

    my $ffp_to_post_unixtime_hrf = shift @_;

    my (

        $page_s,

        %select_fp_unixtime_hs,

        $content_type_s,

        $header_hrs,

        %theme_component_contents_s, $select_num_posts_s, $num_posts_req_s,
        $posts_remaining_s, $first_post_s, $skip_count_s,
        $previous_count_s, $previous_first_post_s, $previous_query_string_s,
        $previous_post_or_posts_s, $next_count_s, $last_post_cur_page_s,
        $num_posts_after_last_cur_page_s, $next_first_post_s,
        $next_query_string_s, $next_post_or_posts_s, $previous_date_frmt_s,
        $post_file_content_s, $head_content_s,

    );

    $page_s = '';

    if ($skip_page_generation_g)
    {
        return $page_s;
    };

    { # Start naked block

        my $select_fp_unixtime_hrl;

        $select_fp_unixtime_hrl = select_posts($ffp_to_post_unixtime_hrf);

        %select_fp_unixtime_hs = %$select_fp_unixtime_hrl;

     } # End, Naked block

     $select_num_posts_s = undef;

     $select_num_posts_s = keys %select_fp_unixtime_hs;

    { # Start of naked block

        my (
            $theme_component_contents_hrl,
        );

        $theme_component_contents_hrl = &$find_req_theme($select_num_posts_s);

        %theme_component_contents_s = %$theme_component_contents_hrl;

    } # End, Naked block

    $content_type_s = $theme_component_contents_s{'content_type'};

    $content_type_s =~ s/^(?-s)(.*)(?s).*$/$1/s;

    $header_hrs = {-type=>$content_type_s};

    $num_posts_req_s = undef;

    if ( defined($num_posts_req_s = $req_query_string_components_final{num_posts}))
    {

        if ($num_posts_req_s =~ m/all/i)
        {
            $num_posts_req_s = $select_num_posts_s;
        }

    } # End, if ( defined($num_posts_req_s = ...

    else
    {

        $num_posts_req_s = $config::num_posts;
    }

    $num_posts = $num_posts_req_s;

    $posts_remaining_s = undef;

    if ($num_posts_req_s <= $select_num_posts_s)
    {
        $posts_remaining_s = $num_posts_req_s;
    }

    else
    {
        $posts_remaining_s = $select_num_posts_s;
    }

    $first_post_s = undef;

    if  (defined($req_query_string_components_final{first_post}) and $req_query_string_components_final{first_post} > 1 and $req_query_string_components_final{first_post} <= $select_num_posts_s)
    {
        $first_post_s = $req_query_string_components_final{first_post};
    }

    else
    {

        if( defined($req_query_string_components_final{first_post}) and $req_query_string_components_final{first_post} > $select_num_posts_s )
        {

            { # Naked block

                my ($warn_level_l, $resp_level_l,);

                $warn_level_l = $max_error_level -1;
                $resp_level_l = $min_error_level +1;

                &handle_warning_and_response (
                    "ode.cgi : generate_page",

                    "Requested first post: " .
                        "$req_query_string_components_final{first_post}\n" .
                    "exceeds the total number of " .
                        "posts matching the request: $select_num_posts_s\n" .
                    "Ignoring parameter and continuing.\n",

                    "Requested first post " .
                        "($req_query_string_components_final{first_post}) " .
                        "exceeds total available " .
                        "($select_num_posts_s). " .
                        "Ignoring first_post param.\n",

                    $warn_level_l, $resp_level_l
                );

            } # End, Naked block

        } # End, defined($req_query_string_components_final{first_post}) ...

        $first_post_s = 1;
    }

    $skip_count_s = undef;

    $skip_count_s = $first_post_s - 1;

    $first_post = $first_post_s;

    $previous_count_s = undef;

    $previous_post_string = undef;

    if ($first_post_s > 1)
    {

        $previous_count_s = $first_post_s - 1 > $num_posts_req_s ? $num_posts_req_s : $first_post_s - 1;

        $previous_count = undef;

        $previous_count = $previous_count_s;

        $previous_first_post_s = undef;

        $previous_first_post_s = $first_post - $previous_count_s;

        $previous_first_post = undef;

        $previous_first_post = $previous_first_post_s;

        $previous_query_string_s = undef;

        foreach my $parameter_l (keys %req_query_string_components_at_sub)
        {
            if ( ($parameter_l ne 'first_post') and ($parameter_l ne 'num_posts') )
            {

                $previous_query_string_s .=
                    $previous_query_string_s ? '&' : '?';

                $previous_query_string_s .= "$parameter_l=$req_query_string_components_at_sub{$parameter_l}";

            }
        }

        $previous_query_string_s .= $previous_query_string_s ? '&' : '?';

        $previous_query_string_s .= "first_post=$previous_first_post_s";

        $previous_query_string_s .= "&num_posts=$previous_count_s";

        $previous_post_or_posts_s = undef;

        $previous_post_or_posts_s = $previous_count_s > 1 ? 'posts' : 'post';

        $previous_post_string = "<a href=\"$req_components_at_sub{base_url}$req_components_at_sub{req_path_with_file}$previous_query_string_s\">Previous $previous_count_s $previous_post_or_posts_s</a>";

    } # End, if ($first_post_s > 1)

    else
    {

        $previous_count_s = 0;

        $previous_post_string = "No previous posts";

    } # End, else

    $next_count_s = undef;

    $last_post_cur_page_s = undef;

    $last_post_cur_page_s = $first_post_s + $posts_remaining_s - 1;

    $num_posts_after_last_cur_page_s = undef;

    $num_posts_after_last_cur_page_s = $select_num_posts_s - $last_post_cur_page_s;

    $next_first_post_s = undef;

    if ($num_posts_after_last_cur_page_s > 0)
    {

        $next_count_s = $num_posts_after_last_cur_page_s < $num_posts_req_s ?  $num_posts_after_last_cur_page_s : $num_posts_req_s;

        $next_count = undef;

        $next_count = $next_count_s;

        $next_first_post_s = $last_post_cur_page_s + 1;

        $next_first_post = undef;

        $next_first_post = $next_first_post_s;

        $next_query_string_s = undef;

        foreach my $parameter_l (keys %req_query_string_components_at_sub)
        {
            if ( ($parameter_l ne 'first_post') and ($parameter_l ne 'num_posts') )
            {

                $next_query_string_s .= $next_query_string_s ? '&' : '?';

                $next_query_string_s .= "$parameter_l=$req_query_string_components_at_sub{$parameter_l}";

            }
        }

        $next_query_string_s .= $next_query_string_s ? '&' : '?';

        $next_query_string_s .= "first_post=$next_first_post_s";

        $next_query_string_s .= "&num_posts=$next_count_s";

        $next_post_or_posts_s = undef;

        $next_post_or_posts_s = $next_count_s > 1 ? 'posts' : 'post';

        $next_post_string = "<a href=\"$req_components_at_sub{base_url}$req_components_at_sub{req_path_with_file}$next_query_string_s\">Next $next_count_s $next_post_or_posts_s</a>";

    } # End, if ($last_post_cur_page_s < $select_num_posts_s)

    else
    {

        $next_count_s = 0;

        $next_post_string = "No more posts";
    }

    $previous_and_next_post_string = undef;

    if ($request_type eq 'post')
    {
        $previous_and_next_post_string = $next_post_string = $previous_post_string = '';

    } # End, if ($request_type == 'post')

    else
    {
        $previous_and_next_post_string = "$previous_post_string&nbsp;|&nbsp;$next_post_string" ;

    } # End, else

    if ($select_num_posts_s <= 0)
    {

        $title = 'There are no posts matching that request';
        $body = '<p>Please try again.</p>';

        my $posts_content_l = $theme_component_contents_s{'posts'};

        $posts_content_l = &$interpolate($posts_content_l);

        $page_s .= $posts_content_l;
    }

    $previous_date_frmt_s = '';

    my $posts_content_l = $theme_component_contents_s{'posts'};

    $posts_content_l =~ s/((?:href)|(?:src))=(['"])(?!(?:[#\/\$])|(?:[a-zA-Z][a-zA-Z0-9+\.-]+:))(.+)\2/$1=$2$found_theme_url$3$2/g;

    foreach my $ffp_to_post_l (sort $posts_sort keys %select_fp_unixtime_hs)
    {

        my (

            $bpath_only_to_post_l,

            @bpath_only_to_post_components_l,

            $fpath_only_to_post_l,

            $filename_of_post_wo_ext_l,

            $filename_ext_only_of_post_l,

            $date_content_l, $cur_post_title_l, $cur_post_tags_l,
            $cur_post_body_l,

        );

        if ($skip_count_s > 0)
        {
            $skip_count_s--;

            next;
        }

        $filename_of_post_wo_ext_l = $fpath_only_to_post_l = $filename_ext_only_of_post_l = undef;

        ($filename_of_post_wo_ext_l, $fpath_only_to_post_l, $filename_ext_only_of_post_l) =
            fileparse($ffp_to_post_l, qr/\.[^.]*$/);

        $filename_ext_only_of_post_l =
            substr($filename_ext_only_of_post_l, 1);

        ($bpath_only_to_post_l) = substr($fpath_only_to_post_l, length $config::document_root);

        $filename = $filename_of_post_wo_ext_l;

        $path = $bpath_only_to_post_l;

        @bpath_only_to_post_components_l = split(/\//, $bpath_only_to_post_l);

        shift @bpath_only_to_post_components_l if $bpath_only_to_post_components_l[0] eq '';

        { # Naked block

            my (
                $breadcrumbs_path_to_post_l, $link_to_path_component_l,
                $path_so_far_l,
            );

            $breadcrumbs_path_to_post_l = "<a href=\"$req_base_url/\" title=\"Link to home\">$config::label_for_breadcrumb_trail_root</a>";

            foreach my $path_component (@bpath_only_to_post_components_l)
            {

                $path_so_far_l .= "$path_component/";

                $link_to_path_component_l = "<a href=\"$req_base_url/$path_so_far_l\" title=\"Link to $path_component\">$path_component</a>";

                $breadcrumbs_path_to_post_l .= "$config::breadcrumb_trail_category_separator$link_to_path_component_l";

            } # End, foreach my $path_component (@bpath_only_to_post ...

            $post_breadcrumb_trail = $breadcrumbs_path_to_post_l;

        } # End, Naked block

        $mtime_cur_post = undef;

        $mtime_cur_post = $select_fp_unixtime_hs{$ffp_to_post_l};

        my ($isdst_l);

        ($wkday_name, $month_name, $month_num, $month_day, $time,
         $sec, $year,
         $isdst_l) = parse_date($select_fp_unixtime_hs{$ffp_to_post_l});

        $post_advertised_time_zone = $isdst_l ? $config::advertised_time_zone_dst : $config::advertised_time_zone;

        ($hour, $min) = split( /:/, $time);

        ($hour_12, $am_pm) = $hour >= 12 ? ($hour - 12,'pm') : ($hour, 'am');

        $hour_12 = 12 if $hour_12 eq '0';

        $date_content_l = undef;

        $date_content_l = $theme_component_contents_s{'date'};

        { # Start of naked block

            my (

                $order_executed_l,
            );

            $order_executed_l = 0;

            foreach my $bundle_num_addin ( sort addins_sort keys %access_date_theme_early_addins )
            {
                if (defined $access_date_theme_early_addins{$bundle_num_addin})
                {
                    $date_content_l = $access_date_theme_early_addins{$bundle_num_addin}->($date_content_l, ++$order_executed_l);
                }
            }

        } # End, Naked block

        $date_content_l = &$interpolate($date_content_l);

        if ($previous_date_frmt_s ne $date_content_l)
        {
            $page_s .= $date_content_l;

            $previous_date_frmt_s = $date_content_l;
        }

        { # Start of naked block

            my (

                $order_executed_l,
            );

            $order_executed_l = 0;

            foreach my $bundle_num_addin ( sort addins_sort keys %mod_post_file_before_read_addins )
            {
                if (defined($mod_post_file_before_read_addins{$bundle_num_addin}))
                {
                    $mod_post_file_before_read_addins{$bundle_num_addin}->($ffp_to_post_l, \%select_fp_unixtime_hs, ++$order_executed_l);
                }
            }

        } # End, Naked block

        if (!(open POST_FH, "< $ffp_to_post_l"))
        {

            { # Naked block

                my ($warn_level_l, $resp_level_l,);

                $warn_level_l = $min_error_level +1;
                $resp_level_l = $max_error_level;

                &handle_warning_and_response (
                    "ode.cgi : generate_page",

                    "Unable to read the post file at: '$ffp_to_post_l'\n" .
                    "Skipping post and continuing.\n",

                    "Unreadable post file. Continuing.\n",

                    $warn_level_l, $resp_level_l
                );

            } # End, Naked block

            next;
        }

        $post_file_content_s = undef;

        $post_file_content_s = join '', <POST_FH>;

        close POST_FH;

        $cur_post_title_l = $cur_post_tags_l = $cur_post_body_l = undef;

        ($cur_post_title_l, $cur_post_tags_l, $cur_post_body_l) =  &split_post_title_tags_and_body(\$post_file_content_s);

        { # Start of naked block

            my (

                $order_executed_l,
                $cur_post_mtime_l,
            );

            $order_executed_l = 0;

            $cur_post_mtime_l = $select_fp_unixtime_hs{$ffp_to_post_l};

            foreach my $bundle_num_addin ( sort addins_sort keys %access_title_tags_and_body_early_addins )
            {

                if (defined($access_title_tags_and_body_early_addins{$bundle_num_addin}))
                {
                    $access_title_tags_and_body_early_addins{$bundle_num_addin}->(\$cur_post_title_l, \$cur_post_tags_l, \$cur_post_body_l, $ffp_to_post_l, $cur_post_mtime_l, ++$order_executed_l);
                }
            }

        } # End, Naked block

        $title = $tags = $body = undef;

        ($title, $tags, $body) = ($cur_post_title_l, $cur_post_tags_l, $cur_post_body_l);

        { # Start of naked block

            my (

                $order_executed_l,
            );

            $order_executed_l = 0;

            foreach my $bundle_num_addin ( sort addins_sort keys %access_posts_theme_early_addins )
            {
                if (defined($access_posts_theme_early_addins{$bundle_num_addin}))
                {
                    $posts_content_l = $access_posts_theme_early_addins{$bundle_num_addin}->($posts_content_l, ++$order_executed_l);
                }
            }

        } # End, Naked block

        $page_s .=  &$interpolate($posts_content_l);

        if (--$posts_remaining_s <= 0)
        {
            last;
        }

    } # End, foreach my $ffp_to_post_l ( &$posts_sort(\%select_fp_unixtime ...

    my $foot_content_l = $theme_component_contents_s{'foot'};

    $foot_content_l =~ s/((?:href)|(?:src))=(['"])(?!(?:[#\/\$])|(?:[a-zA-Z][a-zA-Z0-9+\.-]+:))(.+)\2/$1=$2$found_theme_url$3$2/g;

    { # Start of naked block

        my (

            $order_executed_l,
        );

        $order_executed_l = 0;

        foreach my $bundle_num_addin ( sort addins_sort keys %access_foot_theme_early_addins )
        {
            if (defined($access_foot_theme_early_addins{$bundle_num_addin}))
            {
                    $foot_content_l = $access_foot_theme_early_addins{$bundle_num_addin}->($foot_content_l, ++$order_executed_l);
            }
        }

    } # End, Naked block

    $foot_content_l = &$interpolate($foot_content_l);

    $page_s .= $foot_content_l;

    if ($request_is_type_post_g)
    {

        my (
            $post_page_title_l,
        );

        if ( ($post_page_title_l) = $tags =~ m!^tag\s*:\s*ode\s*:\s*ppt\s*:\s*(\S.*)$!m )
        {
            $page_title = " $config::site_title_short : $post_page_title_l";
        }

        else
        {
            $page_title = "$config::site_title_short : $title";
        }

    } # End, if ($request_is_type_post_g)

    elsif ($request_is_type_root_g)
    {

        if( !($req_is_date_restricted_g) )
        {
            $page_title = $config::site_title;
        }

        else
        {
            $page_title = $config::site_title_short;
        }

    } # End, elsif ($request_is_type_root_g)

    else
    {

        { # Start of naked block

            my (
                @category_components_l,
                $categories_string_l,
            );

            @category_components_l = split(/\//, $req_components_final{fs_path_wo_file});

            shift @category_components_l if $category_components_l[0] eq '';

            $categories_string_l = join $config::page_title_category_separator, @category_components_l;

            $page_title = "$config::site_title_short : $categories_string_l";

        } # End naked block

    } # End, else

    if( $req_is_date_restricted_g and ($request_is_type_root_g or
    $request_is_type_category_g) )
    {

        my (
            $page_title_date_part_l, @month_num2name_short_l,
            @month_num2name_full_l,
        );

        @month_num2name_full_l =
           qw/MOVEALONG January February March April May June July August September October November December/;

        @month_num2name_short_l =
           qw/MOVEALONG Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec/;

        if ( $req_path_is_date_restricted_g )
        {

            my (
                $page_title_hour_12_l, $page_title_am_pm_l,
                $request_time_zone_l, $request_time_l,
                $request_min_l, $request_sec_l, $request_isdst_l,
            );

             ($page_title_hour_12_l, $page_title_am_pm_l) =
                $req_components_final{hour_in_path} >= 12 ?
                ($req_components_final{hour_in_path} - 12,'pm') :
                ($req_components_final{hour_in_path}, 'am');

             $page_title_hour_12_l = 12 if $page_title_hour_12_l eq '0';

            if( $use_local_time_g )
            {

                if ($req_components_final{hour_in_path})
                {
                    $request_min_l = $req_components_final{min_in_path} ? $req_components_final{min_in_path} : '00';

                    $request_sec_l = $req_components_final{sec_in_path} ? $req_components_final{sec_in_path} : '00';

                    $request_time_l = timelocal($request_sec_l, $request_min_l, $req_components_final{hour_in_path}, $req_components_final{month_day_in_path}, ($req_components_final{month_num_in_path} -1), $req_components_final{year_in_path});

                    ($request_isdst_l) = ( localtime($request_time_l) )[8];

                    $request_time_zone_l = $request_isdst_l ? $config::advertised_time_zone_dst : $config::advertised_time_zone;

                } # End, if ($req_components_final{hour_in_path})

            } # End, if( $use_local_time_g )

            else
            {
                $request_time_zone_l = 'UTC';
            }

            if ( defined($req_components_final{year_in_path}) )
            {

                $page_title_date_part_l =
                    $req_components_final{year_in_path};

                if ( defined($req_components_final{month_num_in_path}) )
                {

                    $page_title_date_part_l = "@month_num2name_short_l[$req_components_final{month_num_in_path}] $page_title_date_part_l";

                    if ( defined($req_components_final{month_day_in_path}) )
                    {

                        $page_title_date_part_l = "@month_num2name_short_l[$req_components_final{month_num_in_path}] $req_components_final{month_day_in_path}, $req_components_final{year_in_path}";

                        if ( defined($req_components_final{hour_in_path}) )
                        {

                            $page_title_date_part_l .= " $page_title_hour_12_l:$request_min_l";

                            if ( defined($req_components_final{sec_in_path}) )
                            {

                                $page_title_date_part_l .= ":$req_components_final{sec_in_path}";

                            } # End, if ( defined($req_components_final{se ...

                            $page_title_date_part_l .= " $page_title_am_pm_l";

                            $page_title_date_part_l .=
                                " ($request_time_zone_l)";

                        } # End, if ( defined($req_components_final{hour_ ...

                    } # End, if ( defined($req_components_final{month_day_ ...

                } # End, if ( defined($req_components_final{month_num_in_...

            } # End, if ( defined($req_components_final{year_in_path}) )

        } # End, if ( $req_path_is_date_restricted_g )

        else
        {

            my (
                $start_date_year_l, $start_date_month_l, $start_date_day_l,
                $start_date_string_l, $end_date_year_l, $end_date_month_l,
                $end_date_day_l, $end_date_string_l, $date_pattern_month_l,
                $date_pattern_day_l, $date_pattern_year_l,
                $date_pattern_string_l,
            );

            if($req_query_string_components_final{start_date})
            {

                ( $start_date_year_l, $start_date_month_l, $start_date_day_l) = $req_query_string_components_final{start_date} =~ m!^(\d{4})(\d{2})(\d{2})$!;

                $start_date_string_l =
                    "$month_num2name_short_l[$start_date_month_l] $start_date_day_l, $start_date_year_l";

            } # End, if($req_components_final{start_date})

            if($req_query_string_components_final{end_date})
            {

                ( $end_date_year_l, $end_date_month_l, $end_date_day_l) = $req_query_string_components_final{end_date} =~ m!^(\d{4})(\d{2})(\d{2})$!;

                $end_date_string_l =
                    "$month_num2name_short_l[$end_date_month_l] $end_date_day_l, $end_date_year_l";

            } # End, if($req_components_final{end_date})

            if($req_query_string_components_final{date_pattern})
            {

                ( $date_pattern_year_l, $date_pattern_month_l, $date_pattern_day_l) = $req_query_string_components_final{date_pattern} =~ m!^((?:\d|-){4})((?:\d|-){2})((?:\d|-){2})$!;

                $date_pattern_string_l .= "Year: ";

                if ($date_pattern_year_l eq '----')
                {
                    $date_pattern_string_l .= 'ANY';
                }
                else
                {
                    $date_pattern_string_l .= $date_pattern_year_l;
                }

                $date_pattern_string_l .= ', Month: ';

                if ($date_pattern_month_l eq '--')
                {
                    $date_pattern_string_l .= 'ANY';
                }
                else
                {
                    $date_pattern_string_l .= $date_pattern_month_l;
                }

                $date_pattern_string_l .= ', Day: ';

                if ($date_pattern_day_l eq '--')
                {
                    $date_pattern_string_l .= 'ANY';
                }
                else
                {
                    $date_pattern_string_l .= $date_pattern_day_l;
                }

            } # End, if($req_components_final{date_pattern})

            if ( defined($req_query_string_components_final{start_date}) and !(defined($req_query_string_components_final{end_date})) and !(defined($req_query_string_components_final{date_pattern})) )
            {
                $page_title_date_part_l = "Starting $start_date_string_l";
            }

            elsif ( defined($req_query_string_components_final{start_date}) and defined($req_query_string_components_final{end_date}) and !(defined($req_query_string_components_final{date_pattern})) )
            {
                $page_title_date_part_l = "$start_date_string_l to $end_date_string_l";
            }

            elsif ( defined($req_query_string_components_final{start_date}) and defined($req_query_string_components_final{date_pattern}) and !(defined( $req_query_string_components_final{end_date})) )
            {
                $page_title_date_part_l = "Starting $start_date_string_l ‚Äì $date_pattern_string_l";
            }

            elsif ( defined($req_query_string_components_final{start_date}) and defined($req_query_string_components_final{end_date}) and defined($req_query_string_components_final{date_pattern}) )
            {
                $page_title_date_part_l = "$start_date_string_l to $end_date_string_l ‚Äì $date_pattern_string_l";
            }

            elsif ( defined($req_query_string_components_final{end_date}) and !(defined($req_query_string_components_final{start_date})) and !(defined($req_query_string_components_final{date_pattern})) )
            {
                $page_title_date_part_l = "Ending $end_date_string_l";
            }

            elsif ( defined($req_query_string_components_final{end_date}) and defined($req_query_string_components_final{date_pattern}) and !(defined($req_query_string_components_final{start_date})) )
            {
                $page_title_date_part_l = "Ending $end_date_string_l ‚Äì $date_pattern_string_l";
            }

            elsif ( defined($req_query_string_components_final{date_pattern}) and !(defined($req_query_string_components_final{end_date})) and !(defined($req_query_string_components_final{start_date})) )
            {
                $page_title_date_part_l = "$date_pattern_string_l";
            }

        } # End, else

        $page_title .= " &#x007C; $page_title_date_part_l";

    } # End, if($req_is_date_restricted_g and ($request_is_type_root_g or ...

    $head_content_s = $theme_component_contents_s{'head'};

    $head_content_s =~ s/((?:href)|(?:src))=(['"])(?!(?:[#\/\$])|(?:[a-zA-Z][a-zA-Z0-9+\.-]+:))(.+)\2/$1=$2$found_theme_url$3$2/g;

    { # Start of naked block

        my (

            $order_executed_l,
        );

        $order_executed_l = 0;

        foreach my $bundle_num_addin (sort addins_sort keys %access_head_theme_early_addins)
        {
            if (defined($access_head_theme_early_addins{$bundle_num_addin}))
            {
                $head_content_s = $access_head_theme_early_addins{$bundle_num_addin}->($head_content_s, ++$order_executed_l)
            }
        }

    } # End, Naked block

    $head_content_s = &$interpolate($head_content_s);

    $page_s = $head_content_s . $page_s;

    { # Start of naked block

        my (

            $order_executed_l,
        );

        $order_executed_l = 0;

        foreach my $bundle_num_addin (sort addins_sort keys %access_page_late_addins)
        {
            if (defined ($access_page_late_addins{$bundle_num_addin}))
            {
                $access_page_late_addins{$bundle_num_addin}->(\$page_s, ++$order_executed_l);
            }
        }

    } # End, Naked block

    $page_s = CGI::header($header_hrs) . $page_s if $header_hrs;

    return $page_s;

} # End, sub generate_page

sub inventory_addins
{

    my (
        $discover_posts_replaced_s, $find_req_theme_replaced_s,
        $interpolate_replaced_s, $posts_sort_replaced_s,
    );

    if (!$config::addin_dir)
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (
                "ode.cgi : inventory_addins",

                "The addins directory:\n" .
                "\$config::addin_dir has not been specified.\n" .
                "Check your config file and try again.\n" .
                "All addins are disabled.\n",

                "The addins directory is not specified. " .
                    "All addins are disabled.\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return;
    }

    if (!opendir(ADDINS_DIR, $config::addin_dir))
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (
                "ode.cgi : inventory_addins",

                "The addins directory:\n" .
                "\$config::addin_dir cannot be opened.\n" .
                "Check the value of \$addin_dir in your config file.\n" .
                "All addins are disabled.\n",

                "The addins directory cannot be opened. " .
                    "All addins are disabled.\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return;
    }

    $discover_posts = \&discover_posts_baked_in;

    foreach my $bundle_id_l ( grep { /^\d+.*[^\d]/ && -d "${config::addin_dir}$_" } readdir(ADDINS_DIR) )
    {

        my (
            $ffp_to_bundle_l, $bundle_num_l,
            $bundle_name_l,
        );

        $bundle_num_l = $bundle_name_l = undef;

        ($bundle_num_l, $bundle_name_l) = $bundle_id_l =~ m/(^\d+)([^\d]+.*[^_]+)_*$/;

        $ffp_to_bundle_l = undef;

        $ffp_to_bundle_l = $config::addin_dir . $bundle_id_l;

        $ffp_to_bundle_l .= '/';

        if (&item_is_disabled($ffp_to_bundle_l))
        {

            next;
        }

        if (!(opendir (BUNDLE_DIR, $ffp_to_bundle_l)))
        {

            { # Naked block

                my ($warn_level_l, $resp_level_l,);

                $warn_level_l = $min_error_level +1;
                $resp_level_l = $min_error_level +1;

                &handle_warning_and_response (
                    "ode.cgi : inventory_addins",

                    "The following addin bundle cannot be opened:\n" .
                    "'$bundle_name_l'\n" .
                    "(Most likely due to a permissions issue.)\n" .
                    "The addin cannot be used and has been skipped.\n" .
                    "Continuing normally...\n",

                    "The addin bundle '$bundle_name_l' cannot be opened. " .
                        "Check permissions.\n",

                    $warn_level_l, $resp_level_l
                );

            } # End, Naked block

            next;
        }

        foreach my $bundle_entry_l (readdir(BUNDLE_DIR))
        {

            my (
                $ffp_to_bundle_entry_l, $addin_file_l,
                $ffp_to_addin_file_l,
            );

            next if substr($bundle_entry_l, -6) ne '_addin';

            $ffp_to_bundle_entry_l = undef;

            $ffp_to_bundle_entry_l = $ffp_to_bundle_l . $bundle_entry_l;

            next if !-f $ffp_to_bundle_entry_l;

            $ffp_to_addin_file_l = $addin_file_l = undef;

            $addin_file_l = $bundle_entry_l;

            $ffp_to_addin_file_l = $ffp_to_bundle_entry_l;

            next if &item_is_disabled($ffp_to_addin_file_l);

            require "$ffp_to_addin_file_l";

            if (!$addin_file_l->can('inventory_ping_response'))
            {

                { # Naked block

                    my ($warn_level_l, $resp_level_l,);

                    $warn_level_l = $min_error_level +1;
                    $resp_level_l = $min_error_level +1;

                    &handle_warning_and_response (
                       "ode.cgi : inventory_addins",

                        "'$addin_file_l' does not include req\n" .
                        "inventory_ping_response() routine\n" .
                        "Every addin must incl an instance of this routine.\n" .
                        "As it is, the addin will never be run.\n" .
                        "Continuing normally...\n",

                        "'$addin_file_l' is missing " .
                            "'inventory_ping_response' (will not run).\n",

                        $warn_level_l, $resp_level_l
                    );

                } # End, Naked block

                next;
            }

            $addin_file_l->inventory_ping_response() or next;

            {
                my $manipulate_request_ref_l;

                $manipulate_request_addins{"$bundle_num_l$addin_file_l"} =
                    $manipulate_request_ref_l
                        if $manipulate_request_ref_l = $addin_file_l->can('manipulate_request');
            }

            {
                my $pre_filter_posts_ref_l;

                $pre_filter_posts_addins{"$bundle_num_l$addin_file_l"} =
                    $pre_filter_posts_ref_l
                        if $pre_filter_posts_ref_l = $addin_file_l->can('pre_filter_posts');
            }

            {
                my $filter_posts_ref_l;

                $filter_posts_addins{"$bundle_num_l$addin_file_l"} =
                    $filter_posts_ref_l
                        if $filter_posts_ref_l = $addin_file_l->can('filter_posts');
            }

            {
                my $access_head_theme_early_ref_l;

                $access_head_theme_early_addins{"$bundle_num_l$addin_file_l"} =
                    $access_head_theme_early_ref_l
                        if $access_head_theme_early_ref_l = $addin_file_l->can('access_head_theme_early');
            }

            {
                my $access_date_theme_early_ref_l;

            $access_date_theme_early_addins{"$bundle_num_l$addin_file_l"} =
                    $access_date_theme_early_ref_l
                        if $access_date_theme_early_ref_l = $addin_file_l->can('access_date_theme_early');
            }

            {
                my $mod_post_file_before_read_ref_l;

                $mod_post_file_before_read_addins{"$bundle_num_l$addin_file_l"} =
                    $mod_post_file_before_read_ref_l
                        if $mod_post_file_before_read_ref_l = $addin_file_l->can('mod_post_file_before_read');
            }

            {
                my $access_title_tags_and_body_early_ref_l;

                $access_title_tags_and_body_early_addins{"$bundle_num_l$addin_file_l"} =
                    $access_title_tags_and_body_early_ref_l
                        if $access_title_tags_and_body_early_ref_l = $addin_file_l->can('access_title_tags_and_body_early');
            }

            {
                my $access_posts_theme_early_ref_l;

                $access_posts_theme_early_addins{"$bundle_num_l$addin_file_l"} =
                    $access_posts_theme_early_ref_l
                        if $access_posts_theme_early_ref_l = $addin_file_l->can('access_posts_theme_early');
            }

            {
                my $access_foot_theme_early_ref_l;

                $access_foot_theme_early_addins{"$bundle_num_l$addin_file_l"} =
                    $access_foot_theme_early_ref_l
                        if $access_foot_theme_early_ref_l = $addin_file_l->can('access_foot_theme_early');
            }

            {
                my $access_page_late_ref_l;

                $access_page_late_addins{"$bundle_num_l$addin_file_l"} =
                    $access_page_late_ref_l
                        if $access_page_late_ref_l = $addin_file_l->can('access_page_late');
            }

            { # Naked block

                my $discover_posts_replacement_ref_l;

                if (!$discover_posts_replaced_s and
                    defined( $discover_posts_replacement_ref_l =
                        $addin_file_l->can('replace_discover_posts') )
                )
                {

                    $discover_posts = $discover_posts_replacement_ref_l;
                    $discover_posts_replaced_s = 1;
                }

            } # End, Naked block

            { # Naked block

                my $find_req_theme_replacement_ref_l;

                if (!defined($find_req_theme_replaced_s)
                    and defined( $find_req_theme_replacement_ref_l =
                        $addin_file_l->can('replace_find_req_theme') )
                )
                {
                    $find_req_theme = $find_req_theme_replacement_ref_l;

                    $find_req_theme_replaced_s = 1;
                }

            } # End, Naked block

            { # Naked block

                my $interpolate_replacement_ref_l;

                if (!defined($interpolate_replaced_s)
                    and defined( $interpolate_replacement_ref_l =
                        $addin_file_l->can('replace_interpolate') )
                )
                {
                    $interpolate = $interpolate_replacement_ref_l;

                    $interpolate_replaced_s = 1;
                }

            } # End, Naked block

            { # Naked block

                my $posts_sort_replacement_ref_l;

                if (!defined($posts_sort_replaced_s)
                    and defined( $posts_sort_replacement_ref_l =
                        $addin_file_l->can('replace_posts_sort') )
                )
                {
                    $posts_sort = $posts_sort_replacement_ref_l;
                    $posts_sort_replaced_s = 1;
                }

            } # End, Naked block

        } # End, foreach my $bundle_entry_l (readdir(BUNDLE_DIR))

        close BUNDLE_DIR;

    }   # End, foreach my $bundle_id_l ( grep { /^\d+.*[^\d]/ && -d

    closedir ADDINS_DIR;

} # End, sub inventory_addins

sub parse_the_request
{

    my (
        $cgi_request_object_s, %req_components_s,
        %req_query_string_components_s,
        $directories_s, $file_s, $filename_s, $suffix_s,
        @path_components_s,
    );

    $cgi_request_object_s = shift @_;

    %req_components_s = undef;

    %req_components_s =
    (
        req_string          => undef,
        base_url            => undef,
        req_path_with_file  => undef,
        req_path_wo_file    => undef,
        fs_path_with_file   => undef,
        fs_path_wo_file     => undef,
        year_in_path        => undef,
        month_num_in_path   => undef,
        month_day_in_path   => undef,
        hour_in_path        => undef,
        min_in_path         => undef,
        sec_in_path         => undef,
        filename            => undef,
        theme               => undef,
    );

    $req_components_s{req_string} = undef;

    $req_components_s{req_string} =
        $cgi_request_object_s->url(-path_info=>1,-query=>1);

    $req_components_s{base_url} = undef;

    my $base_url_string_l = $cgi_request_object_s->url();

    $req_components_s{base_url} = $config::base_url ? $config::base_url : $cgi_request_object_s->url();

    $req_components_s{req_path_with_file} = undef;

    $req_components_s{req_path_with_file} =
        $cgi_request_object_s->path_info();

    @path_components_s = $directories_s = $file_s = $suffix_s =
        $filename_s = undef;

    $req_components_s{req_path_wo_file}         =
        $req_components_s{filename}             =
        $req_components_s{theme}                =
        $req_components_s{year_in_path}         =
        $req_components_s{month_num_in_path}    =
        $req_components_s{month_day_in_path}    =
        $req_components_s{hour_in_path}         =
        $req_components_s{min_in_path}          =
        $req_components_s{sec_in_path}          =
        $req_components_s{fs_path_with_file}    =
        $req_components_s{fs_path_wo_file}      = undef;

    if ($req_components_s{req_path_with_file})
    {

        $directories_s = $file_s = undef;

        ($directories_s, $file_s) =
            $req_components_s{req_path_with_file} =~ m!^(.*/)([^/]*)$!;

        $req_components_s{req_path_wo_file} = undef;

        $req_components_s{req_path_wo_file} = $directories_s;

        $suffix_s = $filename_s = undef;

        $file_s =~ m!\.! ? ($filename_s, $suffix_s) = $file_s =~ m!^(.*)\.([^\.]*)$! : $filename_s = $file_s;

        $req_components_s{filename} = undef;

        $req_components_s{filename} = $filename_s
            if $filename_s;

        $req_components_s{theme} = undef;

        $req_components_s{theme} = $suffix_s
            if $suffix_s;

        $req_components_s{fs_path_wo_file} = undef;

        if (!$config::use_path_date_restrictions)
        {

            $req_components_s{fs_path_wo_file} = $req_components_s{req_path_wo_file};

        }

        else
        {

            @path_components_s = undef;

            @path_components_s = split(/\//, $req_components_s{req_path_wo_file});

            shift @path_components_s if $path_components_s[0] eq '';

            $req_components_s{fs_path_wo_file} = '/';

            while ($path_components_s[0] and $path_components_s[0] !~ /^\d+$/)
            {
                $req_components_s{fs_path_wo_file} .= shift @path_components_s;

                $req_components_s{fs_path_wo_file} .= '/';
            }

            ( $req_components_s{year_in_path},
              $req_components_s{month_num_in_path},
              $req_components_s{month_day_in_path},
              $req_components_s{hour_in_path},
              $req_components_s{min_in_path},
              $req_components_s{sec_in_path},) = @path_components_s;

        } # End, else

        $req_components_s{fs_path_with_file} = undef;

        $req_components_s{fs_path_with_file} = $req_components_s{fs_path_wo_file};

        if ($req_components_s{filename})
        {
            $req_components_s{fs_path_with_file} .=
                $req_components_s{filename};

            $req_components_s{fs_path_with_file} .=
                ".$req_components_s{theme}" if $req_components_s{theme};

        } # End, if ($req_components_s{filename})

    } # End, if ($req_components_s{req_path_with_file})

    %req_query_string_components_s = undef;

    %req_query_string_components_s = $cgi_request_object_s->Vars();

    return (\%req_components_s, \%req_query_string_components_s);

} # End, sub parse_the_request

sub select_posts
{

    my (
        %select_fp_unixtime_hs, $ffp_to_req_s,
        $ffp_to_post_unixtime_hrs,
    );

    %select_fp_unixtime_hs = ();

    $ffp_to_post_unixtime_hrs = shift @_;

    $ffp_to_req_s = undef;

    if ($request_is_type_post_g)
    {

        $ffp_to_req_s = "$config::document_root$req_components_final{fs_path_with_file}";

        $ffp_to_req_s =~ s!^(.*)\.[^.]+$!$1!;

        $ffp_to_req_s .= ".$config::post_file_ext";

    } # End, if ($request_is_type_post_g)

    else
    {

        $ffp_to_req_s = "$config::document_root$req_components_final{fs_path_wo_file}";

    } # End, else

    if (!$req_is_date_restricted_g)
    {

        foreach my $fs_path_to_post_l (keys %$ffp_to_post_unixtime_hrs)
        {

            if (!($config::respect_case_of_request ? $fs_path_to_post_l =~ m/$ffp_to_req_s/ : $fs_path_to_post_l =~ m/$ffp_to_req_s/i))
            {
                next;
            }

            $select_fp_unixtime_hs{$fs_path_to_post_l} =
                $$ffp_to_post_unixtime_hrs{$fs_path_to_post_l};

        } # End, foreach my $fs_path_to_post_l (keys %$ffp_to_post_unixtime ...

        return \%select_fp_unixtime_hs;

    } # End, if (!$req_is_date_restricted_g)

    if (defined($req_components_final{year_in_path}))
    {
        my (
            $parse_date_wkday_name_l, $parse_date_month_name_l,
            $parse_date_month_num_l, $parse_date_month_day_l,
            $parse_date_time_l, $parse_date_sec_l, $parse_date_year_l,
            $parse_date_hour_l, $parse_date_min_l,
        );

        foreach my $fs_path_to_post_l ( sort { $ffp_to_post_unixtime_hrs->{$b} <=> $ffp_to_post_unixtime_hrs->{$a} } keys %$ffp_to_post_unixtime_hrs )
        {

            my (
                $path_date_string_l,
                $parse_date_string_l,
            );

            $parse_date_wkday_name_l =
            $parse_date_month_name_l =
            $parse_date_month_num_l  =
            $parse_date_month_day_l  =
            $parse_date_time_l       =
            $parse_date_sec_l        =
            $parse_date_year_l       = undef;

            ( $parse_date_wkday_name_l,
              $parse_date_month_name_l,
              $parse_date_month_num_l,
              $parse_date_month_day_l,
              $parse_date_time_l,
              $parse_date_sec_l,
              $parse_date_year_l,
            ) = parse_date($$ffp_to_post_unixtime_hrs{$fs_path_to_post_l});

            ($parse_date_hour_l, $parse_date_min_l) = split (/:/,$parse_date_time_l);

            $path_date_string_l = $parse_date_string_l = undef;

            $path_date_string_l = $req_components_final{year_in_path};

            $parse_date_string_l = $parse_date_year_l;

            if (defined($req_components_final{month_num_in_path}))
            {

                $path_date_string_l .=
                    $req_components_final{month_num_in_path};

                $parse_date_string_l .= $parse_date_month_num_l;

                if (defined($req_components_final{month_day_in_path}))
                {

                    $path_date_string_l .=
                        $req_components_final{month_day_in_path};

                    $parse_date_string_l .= $parse_date_month_day_l;

                    if (defined ($req_components_final{hour_in_path}))
                    {

                        $path_date_string_l .=
                            $req_components_final{hour_in_path};

                        $parse_date_string_l .= $parse_date_hour_l;

                        if (defined($req_components_final{min_in_path}))
                        {

                            $path_date_string_l .=
                                $req_components_final{min_in_path};

                            $parse_date_string_l .= $parse_date_min_l;

                            if (defined($req_components_final{sec_in_path}))
                            {

                                $path_date_string_l .=
                                    $req_components_final{sec_in_path};

                                $parse_date_string_l .=
                                        "$parse_date_sec_l";

                            } # End, if ($req_components_final {sec_in_ ...}

                        } # End, if ($req_components_final{min_in_path ...}

                    } # End, if ($req_components_final{hour_in_path ...}

                } # End, if ($req_components_final{month_day_in_path ...}

            } # End, if ($req_components_final{month_num_in_path ...}

            if ($parse_date_string_l gt $path_date_string_l)
            {

                next;

            } # End, if ($parse_date_string_l gt $path_date_string_l)

            elsif ($parse_date_string_l lt $path_date_string_l)
            {

                last;

            } # End, elsif ($parse_date_string_l lt $path_date_string_l)

            else
            {

                my (
                    $req_filename_w_post_file_ext_l,
                    $ffp_path_to_req_wo_filename_l,
                    $req_path_and_filename_match_post_l,
                );

                $req_filename_w_post_file_ext_l =
                    $ffp_path_to_req_wo_filename_l = undef;

                if (defined($req_components_final{filename}))
                {
                    $req_filename_w_post_file_ext_l = "$req_components_final{filename}.$config::post_file_ext";
                }

                $ffp_path_to_req_wo_filename_l =  "$config::document_root$req_components_final{fs_path_wo_file}";

                $req_path_and_filename_match_post_l = undef;

                if( defined($req_filename_w_post_file_ext_l) )
                {

                    if ( $config::respect_case_of_request
                                ?
                                ($fs_path_to_post_l =~
                                    m/^$ffp_path_to_req_wo_filename_l/ and
                                $fs_path_to_post_l =~
                                    m/\/$req_filename_w_post_file_ext_l$/)
                                :
                                ($fs_path_to_post_l =~
                                    m/^$ffp_path_to_req_wo_filename_l/i and
                                $fs_path_to_post_l =~
                                    m/\/$req_filename_w_post_file_ext_l$/i)
                    )
                    {
                        $req_path_and_filename_match_post_l = 1;

                    } # End, if ( $config::respect_case_of_request ...

                    else
                    {
                        $req_path_and_filename_match_post_l = 0;
                    }

                } # End, if($req_components_final{filename})

                else
                {

                    if ( $config::respect_case_of_requests
                                ?
                                ($fs_path_to_post_l =~
                                    m/^$ffp_path_to_req_wo_filename_l/)
                                :
                                ($fs_path_to_post_l =~
                                    m/^$ffp_path_to_req_wo_filename_l/i)
                    )
                    {
                        $req_path_and_filename_match_post_l = 1;

                    } # End, if ( $config::respect_case_of_request ...

                    else
                    {
                        $req_path_and_filename_match_post_l = 0;
                    }

                } # End, else

                if ( !$req_path_and_filename_match_post_l )
                {
                    next;
                }

                $select_fp_unixtime_hs{$fs_path_to_post_l} =
                    $$ffp_to_post_unixtime_hrs{$fs_path_to_post_l};

            } # End, else

        } # End, foreach my $fs_path_to_post_l ( sort { ...

        return \%select_fp_unixtime_hs;

    } # End, if (defined($req_components_final{year_in_path}))

    if (defined($req_query_string_components_final{start_date}))
    {

        my (
            $parse_date_month_num_l, $parse_date_month_day_l,
            $parse_date_year_l,
        );

        foreach my $fs_path_to_post_l ( sort { $ffp_to_post_unixtime_hrs->{$b} <=> $ffp_to_post_unixtime_hrs->{$a} } keys %$ffp_to_post_unixtime_hrs )
        {

            my (
                $path_date_string_l,
                $parse_date_string_l,
            );

            $parse_date_month_num_l  =
            $parse_date_month_day_l  =
            $parse_date_year_l       = undef;

            ( $parse_date_month_num_l,
              $parse_date_month_day_l,
              $parse_date_year_l )
            = (parse_date($$ffp_to_post_unixtime_hrs{$fs_path_to_post_l}))[2,3,6];

            $parse_date_string_l = undef;

            $parse_date_string_l = $parse_date_year_l . $parse_date_month_num_l . $parse_date_month_day_l;

            if ($parse_date_string_l lt  $req_query_string_components_final{start_date})
            {
                last;
            }

            if (defined($req_query_string_components_final{end_date}))
            {

                if ($parse_date_string_l gt $req_query_string_components_final{end_date})
                {

                    next;

                } # End, if ($parse_date_string_l gt $req_query_string_ ...

            } # End, if (defined($req_query_string_components_final{end_date}))

            if (defined($req_query_string_components_final{date_pattern}))
            {

                my (
                    $date_pattern_year_l, $date_pattern_month_num_l,
                    $date_pattern_month_day_l,
                );

                ($date_pattern_year_l, $date_pattern_month_num_l, $date_pattern_month_day_l) = $req_query_string_components_final{date_pattern} =~ /([\d-]{4})([\d-]{2})([\d-]{2})/;

                if ( !($date_pattern_year_l eq '----' or
                    $parse_date_year_l eq $date_pattern_year_l) )
                {
                    next;
                }
                if ( !($date_pattern_month_num_l eq '--' or
                    $parse_date_month_num_l eq $date_pattern_month_num_l) )
                {
                    next;
                }
                if ( !($date_pattern_month_day_l eq '--' or
                    $parse_date_month_day_l eq $date_pattern_month_day_l) )
                {
                    next;
                }

            } # End, if (defined($req_query_string_components_final{date_pa ...

            if (!($config::respect_case_of_request ? $fs_path_to_post_l =~ m/$ffp_to_req_s/ : $fs_path_to_post_l =~ m/$ffp_to_req_s/i))
            {
                next;
            }

            $select_fp_unixtime_hs{$fs_path_to_post_l} =
                $$ffp_to_post_unixtime_hrs{$fs_path_to_post_l};

        } # End, foreach my $fs_path_to_post_l ( sort { $ffp_to_post_unixti ...

        return \%select_fp_unixtime_hs;

    } # End, if (defined($req_query_string_components_final{start_date}))

    if (defined($req_query_string_components_final{end_date}))
    {

        my (
            $parse_date_month_num_l, $parse_date_month_day_l,
            $parse_date_year_l,
        );

        foreach my $fs_path_to_post_l ( sort { $ffp_to_post_unixtime_hrs->{$a} <=> $ffp_to_post_unixtime_hrs->{$b} } keys %$ffp_to_post_unixtime_hrs )
        {
            my (
                $path_date_string_l,
                $parse_date_string_l,
            );

            $parse_date_month_num_l  =
            $parse_date_month_day_l  =
            $parse_date_year_l       = undef;

            ( $parse_date_month_num_l,
              $parse_date_month_day_l,
              $parse_date_year_l )
            = (parse_date($$ffp_to_post_unixtime_hrs{$fs_path_to_post_l}))[2,3,6];

            $parse_date_string_l = undef;

            $parse_date_string_l = $parse_date_year_l . $parse_date_month_num_l . $parse_date_month_day_l;

            if ($parse_date_string_l gt $req_query_string_components_final{end_date})
            {
                last;
            }

            if (defined($req_query_string_components_final{date_pattern}))
            {

                my (
                    $date_pattern_year_l, $date_pattern_month_num_l,
                    $date_pattern_month_day_l,
                );

                ($date_pattern_year_l, $date_pattern_month_num_l, $date_pattern_month_day_l) = $req_query_string_components_final{date_pattern} =~ /([\d-]{4})([\d-]{2})([\d-]{2})/;

                if ( !($date_pattern_year_l eq '----' or
                    $parse_date_year_l eq $date_pattern_year_l) )
                {
                    next;
                }

                if ( !($date_pattern_month_num_l eq '--' or
                    $parse_date_month_num_l eq $date_pattern_month_num_l) )
                {
                    next;
                }

                if ( !($date_pattern_month_day_l eq '--' or
                    $parse_date_month_day_l eq $date_pattern_month_day_l) )
                {
                    next;
                }

            } # End, if (defined($req_query_string_components_final{date_ ...

            if (!($config::respect_case_of_request ? $fs_path_to_post_l =~ m/$ffp_to_req_s/ : $fs_path_to_post_l =~ m/$ffp_to_req_s/i))
            {
                next;
            }

            $select_fp_unixtime_hs{$fs_path_to_post_l} =
                $$ffp_to_post_unixtime_hrs{$fs_path_to_post_l};

        } # End, foreach my $fs_path_to_post_l ( sort { $ffp_to_post_unixt ...

        return \%select_fp_unixtime_hs;

    } # End, if (defined($req_query_string_components_final{end_date}))

    if (defined($req_query_string_components_final{date_pattern}))
    {

        my (
            $parse_date_month_num_l, $parse_date_month_day_l,
            $parse_date_year_l, $date_pattern_year_l,
            $date_pattern_month_num_l, $date_pattern_month_day_l,
        );

        ($date_pattern_year_l, $date_pattern_month_num_l, $date_pattern_month_day_l) = $req_query_string_components_final{date_pattern} =~ /([\d-]{4})([\d-]{2})([\d-]{2})/;

        if ( !($date_pattern_year_l eq '----') )
        {

            foreach my $fs_path_to_post_l ( sort { $ffp_to_post_unixtime_hrs->{$b} <=> $ffp_to_post_unixtime_hrs->{$a} } keys %$ffp_to_post_unixtime_hrs )
            {

                $parse_date_month_num_l  =
                $parse_date_month_day_l  =
                $parse_date_year_l       = undef;

                ( $parse_date_month_num_l,
                  $parse_date_month_day_l,
                  $parse_date_year_l )
                = (parse_date($$ffp_to_post_unixtime_hrs{$fs_path_to_post_l}))[2,3,6];

                if ( !($parse_date_year_l eq $date_pattern_year_l) )
                {
                    if ($parse_date_year_l lt $date_pattern_year_l)
                    {
                        last;
                    }
                    else
                    {
                        next;
                    }
                }

                if ( !($date_pattern_month_num_l eq '--' or
                    $parse_date_month_num_l eq $date_pattern_month_num_l) )
                {
                    next;
                }

                if ( !($date_pattern_month_day_l eq '--' or
                    $parse_date_month_day_l eq $date_pattern_month_day_l) )
                {
                    next;
                }

                if (!($config::respect_case_of_request ? $fs_path_to_post_l =~ m/$ffp_to_req_s/ : $fs_path_to_post_l =~ m/$ffp_to_req_s/i))
                {
                    next;
                }

                $select_fp_unixtime_hs{$fs_path_to_post_l} =
                    $$ffp_to_post_unixtime_hrs{$fs_path_to_post_l};

            } # End, foreach my $fs_path_to_post_l ( sort { $ffp_to_post_un ...

            return \%select_fp_unixtime_hs;

        } # End, if ( !($date_pattern_year_l eq '----'))

        if ($date_pattern_year_l eq '----')
        {

            foreach my $fs_path_to_post_l (keys %$ffp_to_post_unixtime_hrs)
            {

                $parse_date_month_num_l  =
                $parse_date_month_day_l  =
                $parse_date_year_l       = undef;

                ( $parse_date_month_num_l,
                  $parse_date_month_day_l,
                  $parse_date_year_l )
                = (parse_date($$ffp_to_post_unixtime_hrs{$fs_path_to_post_l}))[2,3,6];

                if ( !($date_pattern_month_num_l eq '--' or
                    $parse_date_month_num_l eq $date_pattern_month_num_l) )
                {
                    next;
                }

                if ( !($date_pattern_month_day_l eq '--' or
                    $parse_date_month_day_l eq $date_pattern_month_day_l) )
                {
                    next;
                }

                if (!($config::respect_case_of_request ? $fs_path_to_post_l =~ m/$ffp_to_req_s/ : $fs_path_to_post_l =~ m/$ffp_to_req_s/i))
                {
                    next;
                }

                $select_fp_unixtime_hs{$fs_path_to_post_l} =
                    $$ffp_to_post_unixtime_hrs{$fs_path_to_post_l};

            } # End, foreach my $fs_path_to_post_l (keys %$ffp_to_post_unix ...

            return \%select_fp_unixtime_hs;

        } # End, if ($date_pattern_year_l eq '----')

    } # End, if (defined($req_query_string_components_final{date_pattern}))

} # End, sub select_posts

sub addins_sort
{
    my ($num_a,) = $a =~ /^(\d+)/;
    my ($num_b,) = $b =~ /^(\d+)/;

    return $num_a <=> $num_b;

} # End, sub addins_sort

sub check_for_inconsistencies_in_req
{

    my ($req_components_hrs, $req_query_string_components_hrs) = @_;

    foreach my $param_name_l (keys %$req_query_string_components_hrs)
    {

        my $param_value_l = $req_query_string_components_hrs->{$param_name_l};

        if ( $req_components_hrs->{req_string} !~ m/$param_name_l=$param_value_l/ )
        {

            { # Naked block

                my ($warn_level_l, $resp_level_l,);

                $warn_level_l = $min_error_level +1;
                $resp_level_l = $max_error_level;

                &handle_warning_and_response (

                    "ode : check_for_inconsistencies_in_req",

                    "Query string parameter is inconsistent with " .
                        "req_string.\n" .
                    "The name/value pair:\n" .
                    "Parameter name: $param_name_l\n" .
                    "Parameter value: $param_value_l\n" .
                    "req_string is: $req_components_hrs->{req_string}\n",

                    "Inconsistency in parameter name/value pair and " .
                    "req_string\n",

                    $warn_level_l, $resp_level_l
                );

            } # End, Naked block

            return 0;

        } # End, if ( !($req_components_hrs->{req_string} =~ ...

    } # End, foreach my $param_name_l (keys %$req_query_string_components_hrs)

    if ( "$req_components_hrs->{base_url}/" ne
        substr ($req_components_hrs->{req_string}, 0,
            length $req_components_hrs->{base_url} +1) )
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (

                "ode : check_for_inconsistencies_in_req",

                "Request components are inconsistent.\n" .
                "The values of base_url and req_string disagree.\n" .
                "base_url is: $req_components_hrs->{base_url}\n" .
                "req_string is: $req_components_hrs->{req_string}\n",

                "Inconsistency in base_url and req_string values\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return 0;
    }

    if (  "$req_components_hrs->{base_url}$req_components_hrs->{req_path_with_file}" ne substr ($req_components_hrs->{req_string}, 0, length ( "$req_components_hrs->{base_url}$req_components_hrs->{req_path_with_file}")) )
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (

                "ode : check_for_inconsistencies_in_req",

                "Request components are inconsistent.\n" .
                "The combination of base_url and req_path_with_file\n" .
                "is inconsistent with req_string.\n" .
                "base_url followed by req_path_with_file is:\n" . "$req_components_hrs->{base_url}$req_components_hrs->{req_path_with_file}\n" .
                "req_string is: $req_components_hrs->{req_string}\n",

                "Inconsistency w/ base_url, req_path_with_file and " .
                    "req_string\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return 0;
    }

    if ( $req_components_hrs->{req_path_wo_file} ne
        substr ($req_components_hrs->{req_path_with_file}, 0,
            length $req_components_hrs->{req_path_wo_file}) )
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (

                "ode : check_for_inconsistencies_in_req",

                "Request components are inconsistent.\n" .
                "The values of req_path_wo_file and req_path_with_file " .
                    "disagree.\n" .
                "req_path_wo_file is: " .
                    "$req_components_hrs->{req_path_wo_file}\n" .
                "req_path_with_file is: " .
                    "$req_components_hrs->{req_path_with_file}\n",

                "Inconsistency in req_path_wo_file and req_path_with_file\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return 0;
    }

    if ( $req_components_hrs->{fs_path_wo_file} ne
        substr ($req_components_hrs->{fs_path_with_file}, 0,
            length $req_components_hrs->{fs_path_wo_file}) )
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (

                "ode : check_for_inconsistencies_in_req",

                "Request components are inconsistent.\n" .
                "The values of fs_path_wo_file and fs_path_with_file " .
                    "disagree.\n" .
                "fs_path_wo_file is: $req_components_hrs->{fs_path_wo_file}\n" .
                "fs_path_with_file is: " .
                    "$req_components_hrs->{fs_path_with_file}\n",

                "Inconsistency in fs_path_wo_file and fs_path_with_file\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return 0;
    }

    if ( (defined($req_components_hrs->{year_in_path})) and
        ($req_components_hrs->{year_in_path} !~ m/^(\d{4})/ or
        $req_components_hrs->{req_string} !~ m!/$req_components_hrs->{year_in_path}/!) )
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (

                "ode : check_for_inconsistencies_in_req",

                "Request components are inconsistent.\n" .
                "year_in_path is invalid or inconsistent with req_string.\n" .
                "year_in_path is: $req_components_hrs->{year_in_path}\n" .
                "req_string is: $req_components_hrs->{req_string}\n",

                "Inconsistency between year_in_path and req_string\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return 0;
    }

    if ( (defined($req_components_hrs->{month_num_in_path})) and
        (!defined($req_components_hrs->{year_in_path}) or
        $req_components_hrs->{month_num_in_path} !~ m/^(0[1-9])|(1[0-2])$/ or
        $req_components_hrs->{req_string} !~ m!/$req_components_hrs->{month_num_in_path}/!) )
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (

                "ode : check_for_inconsistencies_in_req",

                "Request components are inconsistent.\n" .
                "month_num_in_path is invalid or inconsistent " .
                    "with req_string.\n" .
                "month_num_in_path is: " .
                    "$req_components_hrs->{month_num_in_path}\n" .
                "req_string is: $req_components_hrs->{req_string}\n",

                "Inconsistency between month_num_in_path and req_string\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return 0;
    }

    if ( (defined($req_components_hrs->{month_day_in_path})) and
        (!defined($req_components_hrs->{month_num_in_path}) or
        $req_components_hrs->{month_day_in_path} !~ m/^(0[1-9])|([1,2][0-9])|(3[0,1])$/ or
        $req_components_hrs->{req_string} !~ m!/$req_components_hrs->{month_day_in_path}/!) )
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (
                "ode : check_for_inconsistencies_in_req",

                "Request components are inconsistent.\n" .
                "month_day_in_path is invalid or inconsistent " .
                    "with req_string.\n" .
                "month_day_in_path is: " .
                    "$req_components_hrs->{month_day_in_path}\n" .
                "req_string is: $req_components_hrs->{req_string}\n",

                "Inconsistency between month_day_in_path and req_string\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return 0;
    }

    if ( (defined($req_components_hrs->{hour_in_path})) and
        (!defined($req_components_hrs->{month_day_in_path}) or
        $req_components_hrs->{hour_in_path} !~ m/^([0,1][0-9])|(2[0-3])$/ or
        $req_components_hrs->{req_string} !~
            m!/$req_components_hrs->{hour_in_path}/!) )
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (
                "ode : check_for_inconsistencies_in_req",

                "Request components are inconsistent.\n" .
                "hour_in_path is invalid or inconsistent with req_string.\n" .
                "hour_in_path is: $req_components_hrs->{hour_in_path}\n" .
                "req_string is: $req_components_hrs->{req_string}\n",

                "Inconsistency between hour_in_path and req_string\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return 0;
    }

    if ( (defined($req_components_hrs->{min_in_path})) and
        (!defined($req_components_hrs->{hour_in_path}) or
        $req_components_hrs->{min_in_path} !~ m/^[0-5][0-9]$/ or
        $req_components_hrs->{req_string} !~
            m!/$req_components_hrs->{min_in_path}/!) )
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (
                "ode : check_for_inconsistencies_in_req",

                "Request components are inconsistent.\n" .
                "min_in_path is invalid or inconsistent with req_string.\n" .
                "min_in_path is: $req_components_hrs->{min_in_path}\n" .
                "req_string is: $req_components_hrs->{req_string}\n",

                "Inconsistency between min_in_path and req_string\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return 0;
    }

    if ( (defined($req_components_hrs->{sec_in_path})) and
        (!defined($req_components_hrs->{min_in_path}) or
        $req_components_hrs->{sec_in_path} !~ m/^[0-5][0-9]$/ or
        $req_components_hrs->{req_string} !~
            m!/$req_components_hrs->{sec_in_path}/!) )
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (
                "ode : check_for_inconsistencies_in_req",

                "Request components are inconsistent.\n" .
                "sec_in_path is invalid or inconsistent with req_string.\n" .
                "sec_in_path is: $req_components_hrs->{sec_in_path}\n" .
                "req_string is: $req_components_hrs->{req_string}\n",

                "Inconsistency between sec_in_path and req_string\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return 0;
    }

    if ( (defined($req_components_hrs->{filename})) and
        ($req_components_hrs->{req_string} !~
        m!^.*/$req_components_hrs->{filename}(\.[^.]*)?(\?.*)?$!) )
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (

                "ode : check_for_inconsistencies_in_req",

                "Request components are inconsistent.\n" .
                "filename is inconsistent with req_string.\n" .
                "filename is: $req_components_hrs->{filename}\n" .
                "req_string is: $req_components_hrs->{req_string}\n",

                "Inconsistency between filename and req_string\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return 0;
    }

    if ( $req_components_hrs->{theme} ne $config::default_theme and
        $req_components_hrs->{req_string} !~ m!^.*/$req_components_hrs->{filename}\.$req_components_hrs->{theme}(\?.*)?$! )
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (

                "ode : check_for_inconsistencies_in_req",

                "Request components are inconsistent.\n" .
                "theme is inconsistent with req_string.\n" .
                "theme is: $req_components_hrs->{theme}\n" .
                "req_string is: $req_components_hrs->{req_string}\n",

                "Inconsistency between theme and req_string\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return 0;
    }

    return 1;

} # End, sub check_for_inconsistencies_in_req

sub descending_mtime_sort
{

    $ffp_to_post_unixtime_hrf->{$b} <=> $ffp_to_post_unixtime_hrf->{$a};

}; # End, sub descending_mtime_sort

sub handle_warning_and_response
{

    my (
        $message_source_s, $warning_s, $response_s, $warning_level_s,
        $response_level_s, $response_level_is_valid_s,
        $warning_level_is_valid_s, $max_value_s,
        $min_value_s, $response_header_s, $response_footer_s,
        $warning_threshold_s,
    );

    ($message_source_s, $warning_s, $response_s, $warning_level_s, $response_level_s) = @_;

    $warning_threshold_s = undef;

    $warning_threshold_s = defined($config::warning_threshold) ? $config::warning_threshold : WARNING_THRESHOLD;

    $response_header_s = $response_footer_s = undef;

    $response_header_s = '<div id="ode_response">';
    $response_footer_s = '</div>';

    $max_value_s = $min_value_s = undef;

    $max_value_s = $max_error_level ? $max_error_level : MAX_ERROR_LEVEL;
    $min_value_s = $min_error_level ? $min_error_level : MIN_ERROR_LEVEL;

    $response_level_is_valid_s = $warning_level_is_valid_s = undef;

    $warning_level_s = $max_value_s if $warning_level_s eq undef;

    $response_level_s = $max_value_s if $response_level_s eq undef;

    if ($warning_level_s !~ m/^\d+$/)
    {

        if ($warning_threshold_s > $min_value_s)
        {
            warn "[ode] +---------\n" .
                 "[ode] | $message_source_s\n" .
                 "[ode] | Invalid warning " .
                    "level set: '$warning_level_s'\n." .
                 "[ode] | Must be an integer value\n" .
                 "[ode] +---------\n";

        } # End, if ($warning_threshold_s > $min_value_s)

        $warning_level_is_valid_s = 0;

    } # End, if ($warning_level_s !~ m/^\d+$/)

    else
    {

        if($warning_level_s > $max_value_s)
        {

            if ($warning_threshold_s > $min_value_s)
            {
                warn "[ode] +---------\n" .
                     "[ode] | $message_source_s\n" .
                     "[ode] | Warning level must be no greater than " .
                        "the maximum allowed.\n" .
                     "[ode] | Max allowed value is: $max_value_s\n" .
                     "[ode] | Warning level set: $warning_level_s\n" .
                     "[ode] | Resetting to Maximum value " .
                        "and continuing normally\n" .
                     "[ode] +---------\n";

            } # End, if ($warning_threshold_s > $min_value_s)

            $warning_level_s = $max_value_s;

        } # End, if($warning_level_s > $max_value_s)

        elsif($warning_level_s < $min_value_s)
        {

            if ($warning_threshold_s > $min_value_s)
            {
                warn "[ode] +---------\n" .
                     "[ode] | $message_source_s\n" .
                     "[ode] | Warning level must be no less than " .
                        "the minimum allowed.\n" .
                     "[ode] | Min allowed value is: $min_value_s\n" .
                     "[ode] | Warning level set: $warning_level_s\n" .
                     "[ode] | Resetting to Minimum value " .
                        "and continuing normally\n" .
                     "[ode] +---------\n";

            } # End, if ($warning_threshold_s > $min_value_s)

            $warning_level_s = $min_value_s;

        } # End, elsif($warning_level_s < $min_value_s)

        $warning_level_is_valid_s = 1;

    } # End, else

    if ($response_level_s !~ m/^\d+$/)
    {

        if ($warning_threshold_s > $min_value_s)
        {
            warn "[ode] +---------\n" .
                 "[ode] | $message_source_s\n" .
                 "[ode] | Invalid response " .
                    "level set: '$response_level_s'.\n" .
                 "[ode] | Must be an integer value.\n" .
                 "[ode] +---------\n";

        } # End, if ($warning_threshold_s > $min_value_s)

        $response_level_is_valid_s = 0;

    } # End, if ($response_level_s !~ m/^\d+$/)

    else
    {

        if($response_level_s > $max_value_s)
        {

            if ($warning_threshold_s > $min_value_s)
            {
                warn "[ode] +---------\n" .
                     "[ode] | $message_source_s\n" .
                     "[ode] | Response level must be no greater than " .
                        "the maximum allowed.\n" .
                     "[ode] | Max allowed value is: $max_value_s\n" .
                     "[ode] | Response level set: $response_level_s\n" .
                     "[ode] | Resetting to Maximum value " .
                        "and continuing normally\n" .
                     "[ode] +---------\n";

            } # End, if ($warning_threshold_s > $min_value_s)

            $response_level_s = $max_value_s;

        } # End, if($response_level_s > $max_value_s)

        elsif($response_level_s < $min_value_s)
        {

            if ($warning_threshold_s > $min_value_s)
            {

                warn "[ode] +---------\n" .
                     "[ode] | $message_source_s\n" .
                     "[ode] | Response level must be no less than " .
                        "the minimum allowed.\n" .
                     "[ode] | Min allowed value is: $min_value_s\n" .
                     "[ode] | Response level set: $response_level_s\n" .
                     "[ode] | Resetting to Minimum value " .
                        "and continuing normally\n" .
                     "[ode] +---------\n";

            } # End, if ($warning_threshold_s > $min_value_s)

            $response_level_s = $min_value_s;

        } # End, elsif($response_level_s < $min_value_s)

        $response_level_is_valid_s = 1;
    }

    if ($warning_level_is_valid_s)
    {

        if ($warning_level_s <= $warning_threshold_s)
        {
            warn "[ode] +---------\n" .
                 "[ode] | $message_source_s\n";

            foreach my $line_l (split /\n/, $warning_s)
            {
                if ($line_l !~ m/^\s*$/)
                {
                    warn "[ode] | $line_l\n";
                }
                else
                {
                    warn "$line_l\n";
                }
            }

            warn "[ode] +---------\n";

        } # End, if ($warning_level_s <= $warning_threshold_s)

    } # End, if ($warning_level_is_valid_s)

    if ($response_level_is_valid_s)
    {

        if ($response_level_s <= $warning_threshold_s)
        {

            $response_s =~ s!(^(<br>)|(<br />))|((<br>)|(<br />)$)!!g;

            $response .= (defined($response) && $response ne '') ? "<br />$response_s" : $response_s ;

            $response_string = $response_header_s . $response . $response_footer_s;

        } # End, if ($response_level_s <= $warning_threshold_s)

    } # End, if ($response_level_is_valid_s)

} # End, sub handle_warning_and_response

$interpolate = sub
{

    my ($content_s, ) = shift;

    $content_s =~ s/(\${?\w+(?:::\w+)*(?:(?:->)?{(['"]?)[-\w]+\2})?}?)/"defined $1 ? $1 : ''"/eeg;

    return $content_s;

}; # End, $interpolate = sub

$posts_sort = sub
{

    $ffp_to_post_unixtime_hrf->{$b} <=> $ffp_to_post_unixtime_hrf->{$a};

}; # End, $posts_sort = sub

sub site_look_date_sort
{
    my(
        $mod_a,
        $mod_b,
    );

    $mod_a = $a;

    if ($mod_a =~ m/^(.*)(\d{4})_*(\d{2})_*(\d{2})$/)
    {
        $mod_a =~ s/^(.*)(\d{4})_*(\d{2})_*(\d{2})$/$1$2$3$4/;
    }

    $mod_b = $b;

    if ($mod_b =~ m/^(.*)(\d{4})_*(\d{2})_*(\d{2})$/)
    {
        $mod_b =~ s/^(.*)(\d{4})_*(\d{2})_*(\d{2})$/$1$2$3$4/;
    }

    $mod_a cmp $mod_b;

}; # End, sub site_look_date_sort

sub split_post_title_tags_and_body
{

    my ($post_file_content_ref_s) = @_;

    my (
        $title_s, $tags_s,
        $body_s,
    );

    $$post_file_content_ref_s =~ s!(\r\n?)!\n!g;

    ($title_s, $body_s) = $$post_file_content_ref_s =~ m/^(.*?)\n+(.*)/s;

    foreach my $line_l (split(/\n/,$body_s))
    {
        if ($line_l !~ m/^(\s*$)|(\s*tag\s*:)/) {
            last;
        }

        if ($line_l =~ m/^\s*$/) {
            next;
        }

        else
        {
            $tags_s .= "$line_l\n";

            if (!$show_tags_g)
            {

                $body_s =~ s/$line_l//;

            } # End, if (!$show_tags_g)

        } # End, else

    } # End, foreach my $line_l (split(/\n/,$body_s))

    $tags_s =~ s!^\s*!!;
    $tags_s =~ s!\s*$!!;

    $body_s =~ s/^\s*//;

    return ($title_s, $tags_s, $body_s);

} # End, sub split_post_title_tags_and_body

sub item_is_disabled
{

    my (
        $string_to_test_s, $item_type_s,
        %item_types_s,
    );

    ($string_to_test_s, $item_type_s) = @_;

    %item_types_s = (
        bundle => '',
        addin => '',
        category => '',
        theme => '',
        post => '',
    );

    if (defined($item_type_s) and !(exists($item_types_s{$item_type_s})))
    {
        $item_type_s = undef;

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (
                "ode : item_is_disabled",

                "The item-type specified: $item_type_s\n" .
                "is not recognized.\n" .
                "The script will ignore the type and apply the set of " .
                    "general rules.\n" .
                "Continuing normally...\n",

                "Unrecognized item-type in call to item_is_disabled() " .
                    "routine\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

    } # End, if (defined($item_type_s) and !(exists($item_types_s{$item_ ...

    if ((substr($string_to_test_s, -1) eq '_') or (substr($string_to_test_s, -2) eq '_/'))
    {
        return 1;
    }

    if ($string_to_test_s =~ m!_/!)
    {
        return 1;
    }

    if ($string_to_test_s =~ m!^.*/\.[^/]*/?$!)
    {
        return 1;
    }

    if ($string_to_test_s =~ m!/\.!)
    {
        return 1;
    }

    return 0;

} # End, sub item_is_disabled

sub parse_date
{

    my ($timestamp_s) = @_;

    my (
        @day_num2name_s, @month_num2name_s,
        $sec_s, $min_s, $hour_s, $month_day_s, $month_num_s, $year_s,
        $wkday_num_s, $year_day_s, $isdst_s, $wkday_name_s,
        $month_name_s, $time_s,
    );

    @day_num2name_s =
        qw/Sun Mon Tue Wed Thu Fri Sat/;

    @month_num2name_s =
        qw/MOVEALONG Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec/;

    if($use_local_time_g)
    {

        (
            $sec_s,           # 0
            $min_s,           # 1
            $hour_s,          # 2
            $month_day_s,     # 3
            $month_num_s,     # 4
            $year_s,          # 5
            $wkday_num_s,     # 6
            $year_day_s,      # 7
            $isdst_s,         # 8
        ) = localtime($timestamp_s);

    } # End, if($use_local_time_g)

    else
    {

        (
            $sec_s,           # 0
            $min_s,           # 1
            $hour_s,          # 2
            $month_day_s,     # 3
            $month_num_s,     # 4
            $year_s,          # 5
            $wkday_num_s,     # 6
            $year_day_s,      # 7
            $isdst_s,         # 8
        ) = gmtime($timestamp_s);

    } # End, else

    $sec_s = sprintf("%02d", $sec_s);

    $min_s = sprintf("%02d", $min_s);

    $hour_s = sprintf("%02d", $hour_s);

    $month_day_s = sprintf("%02d", $month_day_s);

    $month_num_s = sprintf("%02d", $month_num_s);

    $year_s += 1900;

    $wkday_name_s = $day_num2name_s[$wkday_num_s];

    $month_num_s++;

    $month_name_s = $month_num2name_s[$month_num_s];

    $time_s = "$hour_s:$min_s";

    return ( $wkday_name_s, $month_name_s, $month_num_s, $month_day_s,
             $time_s, $sec_s, $year_s, $isdst_s);

} # End, sub parse_date

sub sanitize_req_components
{

    if ($req_components_working_f{req_path_wo_file} eq undef)
    {

        $req_components_working_f{req_path_wo_file}     =
        $req_components_working_f{req_path_with_file}   =
        $req_components_working_f{fs_path_wo_file}      =
        $req_components_working_f{fs_path_with_file}    = '/';

        if ($req_components_working_f{req_string} eq $req_components_working_f{base_url})
        {

            $req_components_working_f{req_string} .= '/';

        }

        else
        {

            $req_components_working_f{req_string} =~ s!^($req_components_working_f{base_url})(.*)!$1/$2!;

        }
    }

    { # Naked block

        my (
            $error_in_path_date_restriction_l,
            $query_string_from_req_string_l
        );

        { # Start of naked block

            if ( (defined($req_components_working_f{year_in_path})) and ($req_components_working_f{year_in_path} !~ m/\d{4}/ or $req_components_working_f{year_in_path} < EARLIEST_YEAR) )
            {
                $req_components_working_f{year_in_path} = undef;
                $error_in_path_date_restriction_l = 1;
                last;
            }

            if ( defined($req_components_working_f{month_num_in_path}) and $req_components_working_f{month_num_in_path} !~ m/^(0[1-9])|(1[0-2])$/ )
            {
                $req_components_working_f{month_num_in_path} = undef;
                $error_in_path_date_restriction_l = 1;
                last;
            }

            if ( defined($req_components_working_f{month_day_in_path}) and $req_components_working_f{month_day_in_path} !~ m/^(0[1-9])|([1,2][0-9])|(3[0,1])$/ )
            {
                $req_components_working_f{month_day_in_path} = undef;
                $error_in_path_date_restriction_l = 1;
                last;
            }

            if ( defined($req_components_working_f{hour_in_path}) and $req_components_working_f{hour_in_path} !~ m/^([0,1][0-9])|(2[0-3])$/ )
            {
                $req_components_working_f{hour_in_path} = undef;
                $error_in_path_date_restriction_l = 1;
                last;
            }

            if ( defined($req_components_working_f{min_in_path}) and $req_components_working_f{min_in_path} !~ m/^[0-5][0-9]$/ )
            {
                $req_components_working_f{min_in_path} = undef;
                $error_in_path_date_restriction_l = 1;
                last;
            }

            if ( defined($req_components_working_f{sec_in_path}) and $req_components_working_f{sec_in_path} !~ m/^[0-5][0-9]$/ )
            {
                $req_components_working_f{sec_in_path} = undef;
                $error_in_path_date_restriction_l = 1;
                last;
            }

        } # End, Naked block

        if ($error_in_path_date_restriction_l)
        {

            my (
                @date_restriction_components_l,
            );

            $req_components_working_f{req_path_wo_file} =
                $req_components_working_f{fs_path_wo_file};

            @date_restriction_components_l = qw (
                year_in_path
                month_num_in_path
                month_day_in_path
                hour_in_path
                min_in_path
                sec_in_path );

            while ($date_restriction_components_l[0])
            {
                my $date_component_l = shift @date_restriction_components_l;

                last if
                    !defined($req_components_working_f{$date_component_l});

                $req_components_working_f{req_path_wo_file} .=
                    $req_components_working_f{$date_component_l}
                    . "/";
            }

            foreach (@date_restriction_components_l)
            {
                $req_components_working_f{$_} = undef;
            }

            $req_components_working_f{req_path_with_file} = $req_components_working_f{req_path_wo_file};

            if (defined($req_components_working_f{filename}))
            {
                $req_components_working_f{req_path_with_file} .= $req_components_working_f{filename};

                $req_components_working_f{req_path_with_file} .= ".$req_components_working_f{theme}"
                    if $req_components_working_f{theme};
            }

            ( $query_string_from_req_string_l, ) = $req_components_working_f{req_string} =~ m/(\?.*)?$/;

            $req_components_working_f{req_string} =
                $req_components_working_f{base_url} .
                $req_components_working_f{req_path_with_file};

            $req_components_working_f{req_string} .= $query_string_from_req_string_l
                if defined($query_string_from_req_string_l);

        } # End, if ($error_in_path_date_restriction_l)

    } # End, Naked block

    if ($req_components_working_f{filename} eq 'index')
    {

        $req_components_working_f{filename} = undef;

        $req_components_working_f{req_path_with_file} =
            $req_components_working_f{req_path_wo_file};

        $req_components_working_f{fs_path_with_file} =
            $req_components_working_f{fs_path_wo_file};

        $req_components_working_f{req_string} =~ s!^(.*)index(?:\.$req_components_working_f{theme})?(\?.*)?$!$1$2!;

    } # End, if ($req_components_working_f{filename} eq 'index')

    if ( !defined($req_components_working_f{theme}) )
    {
        $req_components_working_f{theme} = $config::default_theme;

        if ( defined($req_components_working_f{filename}) )
        {

            $req_components_working_f{req_path_with_file} .=
                ".$config::default_theme";

            $req_components_working_f{fs_path_with_file} .=
                ".$config::default_theme";

            $req_components_working_f{req_string} =~  s!^(.*)$req_components_working_f{filename}(\?.*)?$!$1$req_components_working_f{filename}.$config::default_theme$2!;

        } # End, if ( defined($req_components_working_f{filename}) )

    } # End, if ( !defined($req_components_working_f{theme}) )

} # End, sub sanitize_req_components

sub sanitize_req_query_string_components
{

    { # Naked block

        my (
            $req_includes_date_range_param_l, $start_date_param_is_valid_l,
            $end_date_param_is_valid_l, $date_pattern_param_is_valid_l,
            $date_pattern_year_is_valid_l, $date_pattern_month_is_valid_l,
            $date_pattern_day_is_valid_l, $start_date_year_l,
            $start_date_month_l, $start_date_day_l, $end_date_year_l,
            $end_date_month_l, $end_date_day_l, $date_pattern_year_l,
            $date_pattern_month_l, $date_pattern_day_l,
        );

        $req_includes_date_range_param_l = undef;

        $req_includes_date_range_param_l = 0;

        $start_date_param_is_valid_l = undef;

        if (defined($req_query_string_components_working_f{start_date}))
        {

            $start_date_param_is_valid_l = 1;

            $req_query_string_components_working_f{start_date} =~ s/_//g;

            $start_date_year_l  =
            $start_date_month_l =
            $start_date_day_l   = undef;

            if ( !(($start_date_year_l, $start_date_month_l, $start_date_day_l) = $req_query_string_components_working_f{start_date} =~ m/^(\d{4})((?:\d{2})?)((?:\d{2})?)$/) )
            {

                $start_date_param_is_valid_l = 0;

                { # Naked block

                    my ($warn_level_l, $resp_level_l,);

                    $warn_level_l = $min_error_level +1;
                    $resp_level_l = $min_error_level +1;

                    &handle_warning_and_response (
                        "ode.cgi : sanitize_req_query_string_components",

                        "Invalid start_date parameter value: " . "$req_query_string_components_working_f{start_date}\n" .
                        "Only digits and underscores are allowed.\n" .
                        "Parameter length must be 4, 6, or 8 characters\n" .
                        "Check the value and try again.\n" .
                        "Ignoring parameter and continuing.\n",

                        "Invalid start_date value: Ignoring parameter and " .
                            "continuing.\n",
                    );

                } # End, Naked block

            } # End, if (!(($start_date_year_l, $start_date_month_l, ...

            else
            {

                $start_date_month_l = '01' if $start_date_month_l eq undef;
                $start_date_day_l   = '01' if $start_date_day_l eq undef;

                if ($start_date_year_l < EARLIEST_YEAR)
                {

                    $start_date_param_is_valid_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "Invalid start_date parameter value: " . "$req_query_string_components_working_f{start_date}\n" .
                            "Year is earlier than allowed threshold\n" .
                            "Check the value and try again.\n" .
                            "Ignoring parameter and continuing.\n",

                            "start_date year is too early: Ignoring " .
                                "parameter and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if ($start_date_year_l < EARLIEST_YEAR)

                if ($start_date_month_l !~ m/^(0[1-9])|(1[012])$/)
                {

                    $start_date_param_is_valid_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "Invalid start_date parameter value: " . "$req_query_string_components_working_f{start_date}\n" .

                            "Month is not valid.\n" .
                            "Value must be one of '01', '02', ..., '12'\n" .
                            "Check the value and try again.\n" .
                            "Ignoring parameter and continuing.\n",

                            "start_date month is not valid: Ignoring " .
                                "parameter and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if ($start_date_month_l !~ m/^(0[1-9])|(1[012])$/)

                if ($start_date_day_l !~ m/^([012][0-9])|(3[01])$/)
                {

                    $start_date_param_is_valid_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "Invalid start_date parameter value: " . "$req_query_string_components_working_f{start_date}\n" .

                            "Day is not valid.\n" .
                            "Value must be one of '01', '02', ..., '31'\n" .
                            "Check the value and try again.\n" .
                            "Ignoring parameter and continuing.\n",

                            "start_date day is not valid: Ignoring " .
                                "parameter and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if ($start_date_day_l !~ m/^([012][0-9])|(3[01])$/)

            } # End, else

            if ($start_date_param_is_valid_l)
            {

                $req_query_string_components_working_f{start_date} = "$start_date_year_l" . "$start_date_month_l" . "$start_date_day_l";

                $req_includes_date_range_param_l = 1;

                 $req_components_working_f{req_string} =~ s/start_date=[^&;]+/start_date=$req_query_string_components_working_f{start_date}/;

            } # End, if ($start_date_param_is_valid_l)

            else
            {

                $req_query_string_components_working_f{start_date} = undef;

                 $req_components_working_f{req_string} =~ s/start_date=[^&;]+//;

            } # End, else

        } # End, if (defined($req_query_string_components_working_f{start_date}))

        $end_date_param_is_valid_l = undef;

        if ( defined($req_query_string_components_working_f{end_date}) )
        {

            $end_date_param_is_valid_l = 1;

            $req_query_string_components_working_f{end_date} =~ s/_//g;

            $end_date_year_l  =
            $end_date_month_l =
            $end_date_day_l   = undef;

            if ( !(($end_date_year_l, $end_date_month_l, $end_date_day_l) = $req_query_string_components_working_f{end_date} =~ m/^(\d{4})((?:\d{2})?)((?:\d{2})?)$/) )
            {

                $end_date_param_is_valid_l = 0;

                { # Naked block

                    my ($warn_level_l, $resp_level_l,);

                    $warn_level_l = $min_error_level +1;
                    $resp_level_l = $min_error_level +1;

                    &handle_warning_and_response (
                        "ode.cgi : sanitize_req_query_string_components",

                        "Invalid end_date parameter value: " . "$req_query_string_components_working_f{end_date}\n" .
                        "Only digits and underscores are allowed.\n" .
                        "Parameter length must be 4, 6, or 8 characters\n" .
                        "Check the value and try again.\n" .
                        "Ignoring parameter and continuing.\n",

                        "Invalid end_date value: Ignoring parameter " .
                            "and continuing.\n",

                        $warn_level_l, $resp_level_l
                    );

                } # End, Naked block

            } # End, if (!(($end_date_year_l, $end_date_month_l, ...

            else
            {

                $end_date_month_l = '12' if $end_date_month_l eq undef;
                $end_date_day_l   = '31' if $end_date_day_l eq undef;

                if ($end_date_year_l < EARLIEST_YEAR)
                {

                    $end_date_param_is_valid_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "Invalid end_date parameter value: " . "$req_query_string_components_working_f{end_date}\n" .

                            "Year is earlier than allowed threshold\n" .
                            "Check the value and try again.\n" .
                            "Ignoring parameter and continuing.\n",

                            "end_date year is too early: Ignoring " .
                                "parameter and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if ($end_date_year_l < EARLIEST_YEAR)

                if ($end_date_month_l !~ m/^(0[1-9])|(1[012])$/)
                {

                    $end_date_param_is_valid_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "Invalid end_date parameter value: " . "$req_query_string_components_working_f{end_date}\n" .

                            "Month is not valid.\n" .
                            "Value must be one of '01', '02', ..., '12'\n" .
                            "Check the value and try again.\n" .
                            "Ignoring parameter and continuing.\n",

                            "end_date month is not valid: Ignoring " .
                                "parameter and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if ($end_date_month_l !~ m/^(0[1-9])|(1[012])$/)

                if ($end_date_day_l !~ m/^([012][0-9])|(3[01])$/)
                {

                    $end_date_param_is_valid_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "Invalid end_date parameter value: " . "$req_query_string_components_working_f{end_date}\n" .

                            "Day is not valid.\n" .
                            "Value must be one of '01', '02', ..., '31'\n" .
                            "Check the value and try again.\n" .
                            "Ignoring parameter and continuing.\n",

                            "end_date day is not valid: Ignoring parameter " .
                                "and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if ($end_date_day_l !~ m/^([012][0-9])|(3[01])$/)

            } # End, else

            if ($end_date_param_is_valid_l)
            {

                $req_query_string_components_working_f{end_date} =
                    "$end_date_year_l" . "$end_date_month_l" .
                    "$end_date_day_l";

                if ( !defined($req_query_string_components_working_f{start_date}) )
                {
                    $req_includes_date_range_param_l = 1;
                }

                elsif ($req_query_string_components_working_f{start_date} > $req_query_string_components_working_f{end_date})
                {

                    $req_query_string_components_working_f{end_date} = undef;
                }

            } # End, if ($end_date_param_is_valid_l)

            else
            {

                $req_query_string_components_working_f{end_date} = undef;
            }

            if (defined($req_query_string_components_working_f{end_date}))
            {

                 $req_components_working_f{req_string} =~ s/end_date=[^&;]+/end_date=$req_query_string_components_working_f{end_date}/;

            } # End, if (defined($req_query_string_components_working_f{end_date}))

            else
            {

                 $req_components_working_f{req_string} =~ s/end_date=[^&;]+//;

            } # End, else

        } # End, if (%req_query_string_components_working_f{end_date})

        $date_pattern_param_is_valid_l =
        $date_pattern_year_is_valid_l  =
        $date_pattern_month_is_valid_l =
        $date_pattern_day_is_valid_l   = undef;

        if (defined($req_query_string_components_working_f{date_pattern}))
        {

            $date_pattern_param_is_valid_l = 1;

            $req_query_string_components_working_f{date_pattern} =~ s/_//g;

            $date_pattern_year_l  =
            $date_pattern_month_l =
            $date_pattern_day_l   = undef;

            if ( !(($date_pattern_year_l, $date_pattern_month_l, $date_pattern_day_l) = $req_query_string_components_working_f{date_pattern} =~ m/^((?:\d{4})|(?:-{4}))((?:\d{2})|(?:-{2}))((?:\d{2})|(?:-{2}))$/) )
            {

                $date_pattern_param_is_valid_l = 0;

                { # Naked block

                    my ($warn_level_l, $resp_level_l,);

                    $warn_level_l = $min_error_level +1;
                    $resp_level_l = $min_error_level +1;

                    &handle_warning_and_response (
                        "ode.cgi : sanitize_req_query_string_components",

                        "Invalid date_pattern parameter value: " . "$req_query_string_components_working_f{date_pattern}\n" .
                        "Pattern is not valid.\n" .
                        "Pattern must contain exactly 8 such characters\n" .
                        "Only digits, underscores and the wildcard '-'" .
                            " are allowed.\n" .
                        "Check the value and try again.\n" .
                        "Ignoring parameter and continuing.\n",

                        "date_pattern is not valid: Ignoring parameter " .
                            "and continuing.\n",

                        $warn_level_l, $resp_level_l
                    );

                } # End, Naked block

            } # End, if (!(($date_pattern_year_l, $date_pattern_month_l,...

            else
            {

                if (($date_pattern_year_l ne '----') and
                    ($date_pattern_year_l < EARLIEST_YEAR))
                {

                    $date_pattern_param_is_valid_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "Invalid date_pattern parameter value: " . "$req_query_string_components_working_f{date_pattern}\n" .
                            "Year is earlier than allowed threshold\n" .
                            "Check the value and try again.\n" .
                            "Ignoring parameter and continuing.\n",

                            "date_pattern year is too early: Ignoring " .
                                "parameter and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if (($date_pattern_year_l ne '----') and...

                if (($date_pattern_month_l ne '--') and
                    ($date_pattern_month_l !~ m/^(0[1-9])|(1[012])$/))
                {

                    $date_pattern_param_is_valid_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "Invalid date_pattern parameter value: " . "$req_query_string_components_working_f{date_pattern}\n" .

                            "Month is not valid.\n" .
                            "Value must be one of '01', '02', ..., '12'\n" .
                            "Check the value and try again.\n" .
                            "Ignoring parameter and continuing.\n",

                            "date_pattern month is not valid: " .
                                "Ignoring parameter and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if (($date_pattern_month_l ne '--') and...

                if (($date_pattern_day_l ne '--') and
                    ($date_pattern_day_l !~ m/^((0[1-9])|([12][0-9]))|(3[01])$/))
                {

                    $date_pattern_param_is_valid_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "Invalid date _pattern parameter value: " . "$req_query_string_components_working_f{date_pattern}\n" .

                            "Day is not valid.\n" .
                            "Value must be one of '01', '02', ..., '31'\n" .
                            "Check the value and try again.\n" .
                            "Ignoring parameter and continuing.\n",

                            "date_pattern day is not valid: " .
                                "Ignoring parameter and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if (($date_pattern_day_l ne '--') and...

            } # End, else

            if ($date_pattern_param_is_valid_l)
            {

                $req_query_string_components_working_f{date_pattern} =
                    "$date_pattern_year_l" . "$date_pattern_month_l" . "$date_pattern_day_l";

                $req_includes_date_range_param_l = 1;

                 $req_components_working_f{req_string} =~ s/date_pattern=[^&;]+/date_pattern=$req_query_string_components_working_f{date_pattern}/;

            } # End, if ($date_pattern_param_is_valid_l)

            else
            {

                $req_query_string_components_working_f{date_pattern} = undef;

                 $req_components_working_f{req_string} =~ s/date_pattern=[^&;]+//;

                 $req_components_working_f{req_string} =~ s/;$//;

            } # End, else

        } # End, if (%req_query_string_components_working_f{date_pattern})

        if ($req_includes_date_range_param_l &&
            $req_components_working_f{year_in_path})
        {

            my (
                $query_string_l,
            );

            $req_components_working_f{year_in_path}          =
                $req_components_working_f{month_num_in_path} =
                $req_components_working_f{month_day_in_path} =
                $req_components_working_f{hour_in_path}      =
                $req_components_working_f{min_in_path}       =
                $req_components_working_f{sec_in_path}       = undef;

            $req_components_working_f{req_path_wo_file} = $req_components_working_f{fs_path_wo_file};

            $req_components_working_f{req_path_with_file} = $req_components_working_f{fs_path_with_file};

            $query_string_l = undef;

            $query_string_l = "?";

            foreach my $param (keys %req_query_string_components_working_f)
            {
                $query_string_l .=
                    "$param=$req_query_string_components_working_f{$param}&";
            }

            if (substr($query_string_l, -1, 1) eq '&')
            {
                $query_string_l = substr($query_string_l, 0, length ($query_string_l) -1);
            }

            $req_components_working_f{req_string} =
                $req_components_working_f{base_url} .
                $req_components_working_f{fs_path_with_file};

            $req_components_working_f{req_string} .=
                $query_string_l;

        } # End, if ($req_includes_date_range_param_l && ...

        $req_includes_date_range_param_g = undef;

        $req_includes_date_range_param_g = $req_includes_date_range_param_l;

    } # End, Naked block

    { # Naked block

        my (
            $req_includes_site_look_date_param_l,
            $site_look_date_param_is_valid_l,
            $site_look_year_l, $site_look_month_l, $site_look_day_l,
        );

        $req_includes_site_look_date_param_l =
            $site_look_date_param_is_valid_l = undef;

        if (defined($req_query_string_components_working_f{site_look_date}))
        {

            $req_includes_site_look_date_param_l = 1;

            $site_look_date_param_is_valid_l = 1;

            $req_query_string_components_working_f{site_look_date} =~ s/_//g;

            $site_look_year_l  =
            $site_look_month_l =
            $site_look_day_l   = undef;

            if (!(($site_look_year_l, $site_look_month_l, $site_look_day_l) = $req_query_string_components_working_f{site_look_date} =~ m/^(\d{4})((?:\d{2})?)((?:\d{2})?)$/))
            {

                $site_look_date_param_is_valid_l = 0;

                { # Naked block

                    my ($warn_level_l, $resp_level_l,);

                    $warn_level_l = $min_error_level +1;
                    $resp_level_l = $min_error_level +1;

                    &handle_warning_and_response (
                        "ode.cgi : sanitize_req_query_string_components",

                        "Invalid site_look_date parameter value: " . "$req_query_string_components_working_f{site_look_date}\n" .
                        "Only digits and underscores are allowed.\n" .
                        "Parameter length must be 4, 6, or 8 characters\n" .
                        "Check the value and try again.\n" .
                        "Ignoring parameter and continuing.\n",

                        "Invalid site_look_date value: Ignoring parameter " .
                            "and continuing.\n",

                        $warn_level_l, $resp_level_l
                    );

                } # End, Naked block

            } # End if (($site_look_year_l, $site_look_month_l, ...

            else
            {

                $site_look_month_l = '12' if $site_look_month_l eq undef;

                if ($site_look_day_l eq undef)
                {

                    if ( !defined( $site_look_day_l = determine_last_day_in_numeric_month($site_look_month_l, $site_look_year_l)) )
                    {
                        $site_look_day_l = '31';
                    }

                } # End, if ($site_look_day_l eq undef)

                if ($site_look_year_l < EARLIEST_YEAR)
                {

                    $site_look_date_param_is_valid_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "Invalid site_look_date parameter value: " . "$req_query_string_components_working_f{site_look_date}\n" .

                            "Year is earlier than allowed threshold\n" .
                            "Check the value and try again.\n" .
                            "Ignoring parameter and continuing.\n",

                            "site_look_date year is too early: " .
                                "Ignoring parameter and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if ($site_look_year_l < EARLIEST_YEAR)

                if ($site_look_month_l !~ m/^(0[1-9])|(1[012])$/)
                {

                    $site_look_date_param_is_valid_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "Invalid site_look_date parameter value: " . "$req_query_string_components_working_f{site_look_date}\n" .

                            "Month is not valid.\n" .
                            "Value must be one of '01', '02', ..., '12'\n" .
                            "Check the value and try again.\n" .
                            "Ignoring parameter and continuing.\n",

                            "site_look_date month is not valid: " .
                                "Ignoring parameter and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if ($site_look_month_l !~ m/^(0[1-9])|(1[012])$/)

                if ($site_look_day_l !~ m/^([012][0-9])|(3[01])$/)
                {

                    $site_look_date_param_is_valid_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "Invalid site_look_date parameter value: " . "$req_query_string_components_working_f{site_look_date}\n" .

                            "Day is not valid.\n" .
                            "Value must be one of '01', '02', ..., '31'\n" .
                            "Check the value and try again.\n" .
                            "Ignoring parameter and continuing.\n",

                            "site_look_date day is not valid: " .
                                "Ignoring parameter and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if ($site_look_day_l !~ m/^([012][0-9])|(3[01])$/)

            } # End, else

            if ($site_look_date_param_is_valid_l)
            {

                $req_query_string_components_working_f{site_look_date} = "$site_look_year_l" . "$site_look_month_l" . "$site_look_day_l";

                $req_includes_site_look_date_param_l = 1;

                 $req_components_working_f{req_string} =~ s/site_look_date=[^&;]+/site_look_date=$req_query_string_components_working_f{site_look_date}/;

            } # End, if ($site_look_date_param_is_valid_l)

            else
            {

                $req_query_string_components_working_f{site_look_date} =
                    undef;

                 $req_components_working_f{req_string} =~
                    s/site_look_date=[^&;]+//;

            } # End, else

        } # End, if (defined($req_query_string_components_working_f{site_l ...

    } # End, Naked block

    { # Naked block

        my (
            $req_includes_num_posts_param_l,
            $num_posts_param_is_valid_l, $num_posts_l,
        );

        $req_includes_num_posts_param_l =
        $num_posts_param_is_valid_l     = undef;

        if (defined($req_query_string_components_working_f{num_posts}))
        {

            $req_includes_num_posts_param_l = 1;

            $num_posts_param_is_valid_l = 1;

            $num_posts_l = undef;

            if ( ($num_posts_l) = $req_query_string_components_working_f{num_posts} =~ m/^(\d+)$/ )
            {
                ;
            }
            elsif ( ($num_posts_l) = $req_query_string_components_working_f{num_posts} =~ m/^all$/i )
            {
                $num_posts_l = 'all';
            }

            if ( !defined($num_posts_l) )
            {

                $num_posts_param_is_valid_l = 0;

                { # Naked block

                    my ($warn_level_l, $resp_level_l,);

                    $warn_level_l = $min_error_level +1;
                    $resp_level_l = $min_error_level +1;

                    &handle_warning_and_response (
                        "ode.cgi : sanitize_req_query_string_components",

                        "Invalid num_posts parameter value: " .
                        "$req_query_string_components_working_f{num_posts}\n" .
                        "Parameter must be an integer.\n" .
                        "Check the value and try again.\n" .
                        "Ignoring parameter and continuing.\n",

                        "num_posts value invalid: Ignoring parameter " .
                            " and continuing.\n",

                        $warn_level_l, $resp_level_l
                    );

                } # End, Naked block

            } # End if (($num_posts_l) = $req_query_string_components_work ...

            else
            {

                if ($num_posts_l < 0)
                {

                    $num_posts_l = 0;

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                             "num_posts parameter requested is less than " .
                                 "zero: $num_posts_l\n" .
                             "Setting the value to 0 and continuing.\n",

                             "Value of num_posts parameter is less than " .
                                 "zero. Using 0 instead and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                } # End, if ($num_posts_l < 0)

            } # End, else

            if ($num_posts_param_is_valid_l)
            {

                $req_query_string_components_working_f{num_posts} =
                    $num_posts_l;

                $req_includes_num_posts_param_l = 1;

                 $req_components_working_f{req_string} =~ s/num_posts=[^&;]+/num_posts=$req_query_string_components_working_f{num_posts}/;
            } # End, if ($num_posts_param_is_valid_l)

            else
            {

                $req_query_string_components_working_f{num_posts} = undef;

                 $req_components_working_f{req_string} =~ s/num_posts=[^&;]+//;

            } # End, else

        } # End, if (defined($req_query_string_components_working_f{num_posts}))

    } # End, Naked block

    { # Naked block

        my (
            $req_includes_first_post_param_l,
            $first_post_param_is_valid_l, $first_post_l,
        );

        $req_includes_first_post_param_l =
        $first_post_param_is_valid_l     = undef;

        if (defined($req_query_string_components_working_f{first_post}))
        {

            $req_includes_first_post_param_l = 1;

            $first_post_param_is_valid_l = 1;

            $first_post_l = undef;

            ($first_post_l) = $req_query_string_components_working_f{first_post} =~ m/^(\d+)$/;

            if ( !defined($first_post_l) )
            {

                $first_post_param_is_valid_l = 0;

                { # Naked block

                    my ($warn_level_l, $resp_level_l,);

                    $warn_level_l = $min_error_level +1;
                    $resp_level_l = $min_error_level +1;

                    &handle_warning_and_response (
                        "ode.cgi : sanitize_req_query_string_components",

                        "Invalid first_post parameter value: " .
                        "$req_query_string_components_working_f{first_post}\n" .
                        "Parameter must be an integer.\n" .
                        "Check the value and try again.\n" .
                        "Ignoring parameter and continuing.\n",

                        "first_post value invalid: Ignoring parameter " .
                            " and continuing.\n",

                        $warn_level_l, $resp_level_l
                    );

                } # End, Naked block

            } # End, if (($first_post_l) = $req_query_string_components ...

            else
            {

                if ($first_post_l < 1)
                {

                    { # Naked block

                        my ($warn_level_l, $resp_level_l,);

                        $warn_level_l = $min_error_level +1;
                        $resp_level_l = $min_error_level +1;

                        &handle_warning_and_response (
                            "ode.cgi : sanitize_req_query_string_components",

                            "first_post parameter requested is less than " .
                                "one: $first_post_l\n" .
                            "Setting the value to 1 and continuing.\n",

                            "Value of first_post parameter is less than " .
                                "one. Using 1 instead and continuing.\n",

                            $warn_level_l, $resp_level_l
                        );

                    } # End, Naked block

                    $first_post_l = 1;

                } # End, if ($first_post_l < 1)

            } # End, else

            if ($first_post_param_is_valid_l)
            {

                $req_query_string_components_working_f{first_post} =
                    $first_post_l;

                $req_includes_first_post_param_l = 1;

                 $req_components_working_f{req_string} =~ s/first_post=[^&;]+/first_post=$req_query_string_components_working_f{first_post}/;

            } # End, if ($first_post_param_is_valid_l)

            else
            {

                $req_query_string_components_working_f{first_post} = undef;

                 $req_components_working_f{req_string} =~ s/first_post=[^&;]+//;

            } # End, else

        } # End, if (defined($req_query_string_components_working_f{first_ ...

    } # End, Naked block

    $req_components_working_f{req_string} =~ s/([?;&]+)$//;

} # End, sub sanitize_req_query_string_components

sub add_tag
{

    my (
        $addin_name_s,
        $tag_name_s,
        $tag_value_s,
        $ffp_to_post_s,
    ) = @_;

    my (
        $tag_found_s, $new_tag_s, $temp_new_post_file_ext_s,
    );

    $tag_found_s = 0;

    $temp_new_post_file_ext_s = 'ode_add_tag_tmp';

    $new_tag_s = undef;

    $new_tag_s = "tag : $addin_name_s : $tag_name_s : $tag_value_s";

    if(!(open READ_FH, "< $ffp_to_post_s"))
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $ode::min_error_level +1;
            $resp_level_l = $ode::max_error_level -1;

            &ode::handle_warning_and_response (
                "ode : add_tag",

                "Attempting to add or update tag.\n" .
                "$new_tag_s\n" .
                "Can't read file:\n" .
                "$ffp_to_post_s\n" .
                "Check path and permissions.\n" .
                "$!\n",

                "Can't read file to add new tag. " .
                    "(See error log for details.)\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return undef;

    } # End, if(!(open FH, "< $ffp_to_post_s"))

    else
    {

        my (
            $post_title_l, $line_l, $ffp_to_temp_new_post_file_l,
        );

        $ffp_to_temp_new_post_file_l =
            $ffp_to_post_s.$temp_new_post_file_ext_s;

        if ( !(open WRITE_FH, "> $ffp_to_temp_new_post_file_l") )
        {

            { # Naked block

                my ($warn_level_l, $resp_level_l,);

                $warn_level_l = $ode::min_error_level +1;
                $resp_level_l = $ode::max_error_level;

                &ode::handle_warning_and_response (
                    "ode : add_tag",

                    "Attempting to add or update tag:\n" .
                    "$new_tag_s\n" .
                    "Can't create temp file:\n" .
                    "$ffp_to_temp_new_post_file_l\n" .
                    "$!\n",

                    "Can't create temp file while writing new tag. " .
                    "(See error log for details.)\n",

                    $warn_level_l, $resp_level_l
                );

            } # End, Naked block

            close READ_FH;

            return undef;

        } # End, if ( !(open WRITE_FH, "> $ffp_to_temp_new_post_file_l") )

        if ( defined ($post_title_l = <READ_FH>) )
        {
            chomp $post_title_l;

            print WRITE_FH "$post_title_l";
        }

        print WRITE_FH "\n";

        if ( defined ($line_l = <READ_FH>) )
        {
            chomp $line_l;
        }

        while(defined $line_l and $line_l =~ /^\s*$/)
        {
            $line_l = <READ_FH>;
        }

        if ( defined $line_l )
        {
            chomp $line_l;
        }

        if ( defined $post_title_l )
        {
            print WRITE_FH "\n";
        }

        while($line_l =~ /^tag\s*:/)
        {

            if ( $line_l =~  /^\s*tag\s*:\s*$addin_name_s\s*:\s*$tag_name_s\s*:/i )
            {

                print WRITE_FH "$new_tag_s\n";

                $tag_found_s = 1;

            } # End, if ( $line_l =~  /^\s*tag\s*:\s*$addin_name_s\s*: ...

            else
            {

                print WRITE_FH "$line_l\n";
            }

            chomp($line_l = <READ_FH>);

        } # End, while($line_l =~ /^tag\s*:/)

        if( !$tag_found_s )
        {

            print WRITE_FH "$new_tag_s\n";

        }

        while(defined $line_l and $line_l =~ /^\s*$/)
        {
            $line_l = <READ_FH>;
        }

        if( defined $line_l )
        {
            chomp $line_l;
        }

        print WRITE_FH "\n";

        while(defined $line_l)
        {
            print WRITE_FH "$line_l\n";
            chomp($line_l = <READ_FH>);
        }

        close READ_FH;
        close WRITE_FH;

        if ( !(unlink $ffp_to_post_s) )
        {

            { # Naked block

                my ($warn_level_l, $resp_level_l,);

                $warn_level_l = $ode::min_error_level +1;
                $resp_level_l = $ode::max_error_level;

                &ode::handle_warning_and_response (
                    "ode : add_tag",

                    "Can't delete original post file at:\n" .
                    "$ffp_to_post_s\n" .
                    "after successfully creating temp new post for tag:\n" .
                    "$new_tag_s\n" .
                    "Recovering by removing the temp new file.\n" .
                    "The post file will not include " .
                        "the new tag.\n" .
                    "$!\n",

                    "Unable add tag to post file because original can't " .
                        "be removed. (See error log.)\n",

                    $warn_level_l, $resp_level_l
                );

            } # End, Naked block

            if ( !(unlink "$ffp_to_temp_new_post_file_l") )
            {

                { # Naked block

                    my ($warn_level_l, $resp_level_l,);

                    $warn_level_l = $ode::min_error_level +1;
                    $resp_level_l = $ode::max_error_level;

                    &ode::handle_warning_and_response (
                        "ode : add_tag",

                        "Unable to remove the temp file at:\n" .
                        "$ffp_to_temp_new_post_file_l\n" .
                        "while attempting recover after not being to " .
                            "delete the original post file.\n" .
                        "You will need to manually resolve this issue.\n" .
                        "$!\n",

                        "Unable to remove temp file after failed " .
                            "attempt to add new tag. (See error log.)\n",

                        $warn_level_l, $resp_level_l
                    );

                } # End, Naked block

            } # End, if ( !(unlink "$ffp_to_temp_new_post_file_l") )

            return undef;

        } # End, if ( !(unlink $ffp_to_post_s) )

        if ( !(rename($ffp_to_temp_new_post_file_l, $ffp_to_post_s)) )
        {

            { # Naked block

                my ($warn_level_l, $resp_level_l,);

                $warn_level_l = $ode::min_error_level +1;
                $resp_level_l = $ode::max_error_level;

                &ode::handle_warning_and_response (
                    "ode : add_tag",

                    "Can't restore original filename after writing " .
                        "new tag.\n" .
                    "Updated file is preserved at:\n" .
                    "$ffp_to_temp_new_post_file_l\n" .
                    "You must manually rename the file before it will " .
                        "appear on the site\n" .
                    "$!\n",

                    "Can't restore original filename after writing " .
                        "new tag. (See error log.)\n",

                    $warn_level_l, $resp_level_l
                );

            } # End, Naked block

            return undef;

        } # End, if ( !(rename("$ffp_to_post_s.ode_new_tag_tmp", ...

        return 1;

    } # End, else

} # End, sub add_tag

sub destroy_tag
{

    my (
        $addin_name_s,
        $tag_name_s,
        $ffp_to_post_s,
    ) = @_;

    my (
        $tag_found_s, $tag_description_s, $temp_new_post_file_ext_s,
        $new_post_string_s,
    );

    $tag_found_s = 0;

    $tag_description_s = "tag : $addin_name_s : $tag_name_s : [tag value]";

    $temp_new_post_file_ext_s = 'ode_destroy_tag_tmp';

    if(!(open FH, "< $ffp_to_post_s"))
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $ode::min_error_level +1;
            $resp_level_l = $ode::max_error_level -1;

            &ode::handle_warning_and_response (
                "ode : destroy_tag",

                "Attempting to delete tag:\n" .
                "$tag_description_s\n" .
                "Can't read file:\n" .
                "$ffp_to_post_s\n" .
                "Check path and permissions.\n" .
                "$!\n",

                "Can't read file to delete tag. " .
                    "(See error log for details.)\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return undef;

    } # End, if(!(open FH, "< $ffp_to_post_s"))

    else
    {

        my (
            $post_title_l,
            $line_l, $ffp_to_temp_new_post_file_l,
        );

        $new_post_string_s = undef;

        if ( defined ($post_title_l = <READ_FH>) )
        {
            chomp $post_title_l;

            $new_post_string_s .= "$post_title_l\n";
        }

        if ( defined ($line_l = <READ_FH>) )
        {
            chomp $line_l;
        }

        while(defined $line_l and $line_l =~ /^\s*$/)
        {
            $line_l = <READ_FH>;
        }

        chomp($line_l);

        $new_post_string_s .= "\n";

        while($line_l =~ /^tag\s*:/)
        {

            if ( $line_l =~ /^\s*tag\s*:\s*$addin_name_s\s*:\s*$tag_name_s\s*:/i )
            {

                $tag_found_s = 1;

                next;

            } # End, if ( $line_l =~ /^\s*tag\s*:\s*$addin_name_s\s*: ...

            $new_post_string_s .= "$line_l\n";

            chomp($line_l = <READ_FH>);

        } # End, while($line_l =~ /^tag\s*:/)

        if ( !$tag_found_s )
        {

            close READ_FH;

            return 1;

        } # End, if ( !$tag_found_s )

        while(defined $line_l and $line_l =~ /^\s*$/)
        {
            $line_l = <READ_FH>;
        }

        chomp($line_l);

        $new_post_string_s .= "\n";

        while(defined $line_l)
        {
            $new_post_string_s .= "$line_l\n";

            chomp($line_l = <READ_FH>);
        }

        close READ_FH;

        $ffp_to_temp_new_post_file_l = undef;

        $ffp_to_temp_new_post_file_l =
            $ffp_to_post_s.$temp_new_post_file_ext_s;

        if ( !(open WRITE_FH, "> $ffp_to_temp_new_post_file_l") )
        {

            { # Naked block

                my ($warn_level_l, $resp_level_l,);

                $warn_level_l = $ode::min_error_level +1;
                $resp_level_l = $ode::max_error_level;

                &ode::handle_warning_and_response (
                    "ode : destroy_tag",

                    "Attempting to destroy tag:\n" .
                    "$tag_description_s\n" .
                    "Can't create temp file:\n" .
                    "$ffp_to_temp_new_post_file_l\n" .
                    "$!\n" ,

                    "Can't create temp file while attempting to remove " .
                    "tag. (See error log for details.)\n",

                    $warn_level_l, $resp_level_l
                );

            } # End, Naked block

            return undef;

        } # End, if ( !(open WRITE_FH, "> $ffp_to_temp_new_post_file_l") )

        print WRITE_FH "$new_post_string_s";

        close WRITE_FH;

        if ( !(unlink $ffp_to_post_s) )
        {

            { # Naked block

                my ($warn_level_l, $resp_level_l,);

                $warn_level_l = $ode::min_error_level +1;
                $resp_level_l = $ode::max_error_level;

                &ode::handle_warning_and_response (
                    "ode : destroy_tag",

                    "Can't update the post file at:\n" .
                    "$ffp_to_post_s\n" .
                    "while attempting to delete tag:\n" .
                    "$tag_description_s\n" .
                    "Recovering by removing the new temp file.\n" .
                    "The post file will still include " .
                        "the tag.\n" .
                    "$!\n",

                    "Unable delete tag because original post file can't " .
                        "be removed. (See error log.)\n",

                    $warn_level_l, $resp_level_l
                );

            } # End, Naked block

            if ( !(unlink $ffp_to_temp_new_post_file_l) )
            {

                { # Naked block

                    my ($warn_level_l, $resp_level_l,);

                    $warn_level_l = $ode::min_error_level +1;
                    $resp_level_l = $ode::max_error_level;

                    &ode::handle_warning_and_response (
                        "ode : destroy_tag",

                        "Unable to remove the temp file at:\n" .
                        "$ffp_to_temp_new_post_file_l\n" .
                        "while attempting recover after not being to " .
                            "remove the original post file.\n" .
                        "$!\n" .
                        "You will need to manually resolve this issue.\n",

                        "Unable to remove temp file after failed " .
                            "attempt to delete tag. (See error log.)\n",

                        $warn_level_l, $resp_level_l
                    );

                } # End, Naked block

            } # End, if ( !(unlink $ffp_to_temp_new_post_file_l) )

            return undef;

        } # End, if ( !(unlink $ffp_to_post_s) )

        if ( !(rename($ffp_to_temp_new_post_file_l, $ffp_to_post_s)) )
        {

            { # Naked block

                my ($warn_level_l, $resp_level_l,);

                $warn_level_l = $ode::min_error_level +1;
                $resp_level_l = $ode::max_error_level;

                &ode::handle_warning_and_response (
                    "ode : destroy_tag",

                    "Can't restore original filename after deleting tag.\n" .
                    "Updated file is preserved at:\n" .
                    "$ffp_to_temp_new_post_file_l\n" .
                    "You must manually rename the file before it will " .
                        "appear on the site\n" .
                    "$!\n",

                    "Can't restore original filename after deleting " .
                        "tag. (See error log.)\n",

                    $warn_level_l, $resp_level_l
                );

            } # End, Naked block

            return undef;

        } # End, if ( !(rename($ffp_to_temp_new_post_file_l, ...

        return 1;

    } # End, else

} # End, sub destroy_tag

sub get_tag_value
{

    my (
        $addin_name_s,
        $tag_name_s,
        $ffp_to_post_s,
        ) = @_;

    my (
        $tag_description_s,
    );

    $tag_description_s = "tag : $addin_name_s : $tag_name_s : [tag value]";

    if(!(open READ_FH, "< $ffp_to_post_s"))
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $ode::min_error_level +1;
            $resp_level_l = $ode::max_error_level -1;

            &ode::handle_warning_and_response (
                "ode : get_tag_value",

                "Attempting to get tag value:\n" .
                "$tag_description_s\n" .
                "Can't read file:\n" .
                "$ffp_to_post_s\n" .
                "Check path and permissions.\n" .
                "$!\n",

                "Can't read file to get tag value. " .
                    "(See error log for details.)\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block

        return undef;

    } # End, if(!(open FH, "< $ffp_to_post_s"))

    else
    {

        my (
            $post_title_l, $line_l,
            $target_tag_value_l,
        );

        return undef if !($post_title_l = <READ_FH>);

        return undef if !($line_l = <READ_FH>);

        while(defined $line_l and $line_l =~ /^\s*$/)
        {
            $line_l = <READ_FH>;
        }

        while($line_l =~ /^tag\s*:/)
        {

            if ( ($target_tag_value_l) = $line_l =~ /^\s*tag\s*:\s*$addin_name_s\s*:\s*$tag_name_s\s*:\s*([^\s].*[^\s])/i )
            {

                close READ_FH;

                return $target_tag_value_l;

            } # End, if ( ($target_tag_value_l) = $line_l =~ ...

            $line_l = <READ_FH>;

        } # End, while($line_l =~ /^tag\s*:/)

    } # End, else

    return undef;

} # End, sub get_tag_value

sub determine_last_day_in_numeric_month
{

    my ($month_num_s, $year_num_s) = @_;

    my (
        @days_in_month_s,
        $days_in_req_month_s
    );

    return undef if $month_num_s < 1 or $month_num_s > 12;

    if ($year_num_s !~ /^\d{4}$/)
    {
        $year_num_s = undef;
    }

    @days_in_month_s =
        (undef, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);

    $days_in_req_month_s = $days_in_month_s[$month_num_s];

    if (defined $year_num_s)
    {

        if ($month_num_s == 2)
        {

            if ( ($year_num_s % 4) == 0 )
            {

                if ( ($year_num_s % 100) == 0 )
                {

                    if ( ($year_num_s % 400) == 0 )
                    {

                        $days_in_req_month_s++;

                    } # End, if ( ($year_num_s % 400) == 0 )

                    else
                    {

                        ;
                    }

                } # End, if ( ($year_num_s % 100) == 0 )

                else
                {

                    $days_in_req_month_s++;
                }

            } # End, if ( ($year_num_s % 4) == 0 )

            else
            {

                ;
            }

        } # End, if ($month_num_s == 2)

    } # End, if (defined $year_num_s)

    return $days_in_req_month_s;

} # End, sub determine_last_day_in_numeric_month



# ^ End of subroutine definitions
# --------------
# v Start of execution


{ # Naked block

    my ($warn_level_l, $resp_level_l,);

    $warn_level_l = MAX_ERROR_LEVEL;
    $resp_level_l = MAX_ERROR_LEVEL;

    &handle_warning_and_response (
        "ode.cgi : -",

        "Start of execution (Good luck).\n",
        "Start of execution (Good luck).\n",

        $warn_level_l, $resp_level_l
    );

} # End, Naked block

$build = $version = undef;

$version = VERSION_NUMBER;
$build = BUILD_NUMBER;

$min_error_level = $max_error_level = undef;

$min_error_level = MIN_ERROR_LEVEL;
$max_error_level = MAX_ERROR_LEVEL;

$cgi_req_object_f = new CGI;

if (substr($config_dir_f, -1, 1) ne '/')
{
    $config_dir_f .= '/';

    { # Naked block

        my ($warn_level_l, $resp_level_l,);

        $warn_level_l = $min_error_level +1;
        $resp_level_l = $max_error_level;

        &handle_warning_and_response (
            "ode.cgi : -",

            "The variable '\$config_dir_f' should end " .
                "with a trailing path delimiter.\n" .
            "The script has added the missing character.\n" .
            "Update the value in the configuration section _of the\n" .
            "source file_ to eliminate this warning.\n" .
            "Continuing normally.\n",

            "Missing trailing path delimiter at \$config_dir_f\n",

            $warn_level_l, $resp_level_l
        );

    } # End, Naked block
}

$config_file_f = undef;

$config_file_f = $config_dir_f . $config_filename_f;

require $config_file_f;

$tz_uniform_name_g = $use_local_time_g = undef;

if($use_local_time_g = $config::use_local_time)
{

    if($config::local_time_zone =~ m!(Africa|America|Antarctica|Arctic|Asia|Atlantic|Australia|Europe|Indian|Pacific|Etc)/[\w-]+!)
    {

        $tz_uniform_name_g = $config::local_time_zone;

        $ENV{TZ} = $tz_uniform_name_g;

        tzset();

    } # End, if($config::local_time_zone =~ m!(Africa|America| ...

    else
    {

        { # Naked block

            my ($warn_level_l, $resp_level_l,);

            $warn_level_l = $min_error_level +1;
            $resp_level_l = $max_error_level;

            &handle_warning_and_response (
                "ode.cgi : -",

                "The value of the setting \$local_time_zone " .
                    "in the config file:\n" .
                "$config::local_time_zone\n" .
                "is not a recognized uniform time zone name.\n" .
                "UTC will be used instead.\n" .
                "Update the value for this option in the config file.\n",

                "Local time zone setting is not recognized (using UTC).\n",

                $warn_level_l, $resp_level_l
            );

        } # End, Naked block}

        $use_local_time_g = 0;

    } # End, else

} # End, if($use_local_time_g = $config::use_local_time)

if (substr($config::post_file_ext, 0, 1) eq '.')
{
    $config::post_file_ext = substr($config::post_file_ext, 1);

    { # Naked block

        my ($warn_level_l, $resp_level_l,);

        $warn_level_l = $min_error_level +1;
        $resp_level_l = $max_error_level;

        &handle_warning_and_response (
            "ode.cgi : -",

            "The variable '\$post_file_ext' should not begin with " .
                "a leading dot.\n" .
            "The script has taken care of removing it.\n" .
            "Update the value for this option in the config file\n" .
            "to eliminate this warning.\n" .
            "Continuing normally.\n",

            "Leading suffix delimiter at config::post_file_ext.\n",

            $warn_level_l, $resp_level_l
        );

    } # End, Naked block}

} # End, if (substr($config::post_file_ext, 0, 1) eq '.')

if (substr($config::default_theme, 0, 1) eq '.')
{
    $config::default_theme = substr($config::default_theme, 1);

    { # Naked block

        my ($warn_level_l, $resp_level_l,);

        $warn_level_l = $min_error_level +1;
        $resp_level_l = $max_error_level;

        &handle_warning_and_response (
            "ode.cgi : -",

            "The variable '\$default_theme' should not begin with " .
                "a leading dot.\n" .
            "The script has taken care of removing it.\n" .
            "Update the value for this option in the config file\n" .
            "to eliminate this warning.\n" .
            "Continuing normally.\n",

            "Leading suffix delimiter at \$config::default_theme.",

            $warn_level_l, $resp_level_l
        );

    } # End, Naked block

} # End, if (substr($config::default_theme, 0, 1) eq '.')

if (substr($config::document_root, -1, 1) eq '/')
{

    $config::document_root = substr($config::document_root, 0, length($config::document_root) - 1);

    { # Naked block

        my ($warn_level_l, $resp_level_l,);

        $warn_level_l = $min_error_level +1;
        $resp_level_l = $max_error_level;

        &handle_warning_and_response (
            "odi.cgi : -",

            "The variable '\$document_root' should _not_ end\n" .
            "with a trailing path delimiter.\n" .
            "The script has taken care of removing the character.\n" .
            "Update the value for this option in the config file\n" .
            "to eliminate this warning.\n" .
            "Continuing normally.\n",

            "Unexpected trailing path delimiter at \$config::document_root.",

            $warn_level_l, $resp_level_l
        );

    } # End, Naked block

} # End, if (substr($config::document_root, -1, 1) eq '/')

if ($config::compare_paths_and_posts_to_exempt)
{
    $exempt_file_g = $config_dir_f . $config::exempt_filename;
}

$show_tags_g = undef;

$show_tags_g = $config::show_tags;

%req_components_at_sub = undef;

%req_query_string_components_at_sub = undef;

%req_components_at_sub = (
    req_string          => undef,
    base_url            => undef,
    req_path_with_file  => undef,
    req_path_wo_file    => undef,
    fs_path_with_file   => undef,
    fs_path_wo_file     => undef,
    year_in_path        => undef,
    month_num_in_path   => undef,
    month_day_in_path   => undef,
    hour_in_path        => undef,
    min_in_path         => undef,
    sec_in_path         => undef,
    filename            => undef,
    theme               => undef,
);

%req_query_string_components_at_sub = (
    start_date      => undef,
    end_date        => undef,
    date_pattern    => undef,
    site_look_date  => undef,
    num_posts       => undef,
    first_post      => undef,
);

{ # Naked block

    my ($req_components_at_sub_hrl, $req_query_string_components_at_sub_hrl) =
        &parse_the_request($cgi_req_object_f);

    %req_components_at_sub = %$req_components_at_sub_hrl;

    %req_query_string_components_at_sub =
        %$req_query_string_components_at_sub_hrl;

} # End, Naked block

%req_components_working_f = undef;

%req_query_string_components_working_f = undef;

%req_components_working_f =
(
    req_string          => undef,
    base_url            => undef,
    req_path_with_file  => undef,
    req_path_wo_file    => undef,
    fs_path_with_file   => undef,
    fs_path_wo_file     => undef,
    year_in_path        => undef,
    month_num_in_path   => undef,
    month_day_in_path   => undef,
    hour_in_path        => undef,
    min_in_path         => undef,
    sec_in_path         => undef,
    filename            => undef,
    theme               => undef,
);

%req_query_string_components_working_f =
(
    start_date      => undef,
    end_date        => undef,
    date_pattern    => undef,
    site_look_date  => undef,
    num_posts       => undef,
    first_post      => undef,
);

%req_components_working_f = %req_components_at_sub;

%req_query_string_components_working_f = %req_query_string_components_at_sub;

sanitize_req_components();

sanitize_req_query_string_components();

&inventory_addins();

{ # Start of naked block

    my (

        $order_executed_l,

        %req_components_working_l,
        %req_query_string_components_working_l,
    );

    $order_executed_l = 0;

    foreach my $bundle_num_addin (sort addins_sort keys %manipulate_request_addins)
    {

        %req_components_working_l = %req_components_working_f;

        %req_query_string_components_working_l =
            %req_query_string_components_working_f;

        $manipulate_request_addins{$bundle_num_addin}->(
            \%req_components_working_l,
            \%req_query_string_components_working_l,
            ++$order_executed_l );

        if ( check_for_inconsistencies_in_req(\%req_components_working_l, \%req_query_string_components_working_l) )
        {

            %req_components_working_f = %req_components_working_l;

            %req_query_string_components_working_f =
                %req_query_string_components_working_l;
        }

    } # End, foreach my $bundle_num_addin (sort addins_sort keys...

} # End, Naked block

%req_components_final = undef;

%req_components_final =
(
    req_string          => undef,
    base_url            => undef,
    req_path_with_file  => undef,
    req_path_wo_file    => undef,
    fs_path_with_file   => undef,
    fs_path_wo_file     => undef,
    year_in_path        => undef,
    month_num_in_path   => undef,
    month_day_in_path   => undef,
    hour_in_path        => undef,
    min_in_path         => undef,
    sec_in_path         => undef,
    filename            => undef,
    theme               => undef,
);

%req_components_final = %req_components_working_f;

%req_query_string_components_final = undef;

%req_query_string_components_final =
(
    start_date      => undef,
    end_date        => undef,
    date_pattern    => undef,
    site_look_date  => undef,
    num_posts       => undef,
    first_post      => undef,
);

%req_query_string_components_final = %req_query_string_components_working_f;

%req_components_working_f = %req_query_string_components_working_f = undef;

$req_is_date_restricted_g = undef;

if ( defined($req_components_final{year_in_path}) or
    defined($req_query_string_components_final{start_date}) or
    defined($req_query_string_components_final{end_date}) or
    defined($req_query_string_components_final{date_pattern}) )
{
    $req_is_date_restricted_g = 1;
}
else
{
    $req_is_date_restricted_g = 0;
}

$req_string = $req_base_url = $req_path_with_file =
    $req_path_wo_file = $req_fs_path_with_file =
    $req_fs_path_wo_file = $req_year_in_path =
    $req_month_num_in_path = $req_month_day_in_path = $req_filename =
    $req_theme = undef;

$req_string             = $req_components_final{req_string};
$req_base_url           = $req_components_final{base_url};
$req_path_with_file     = $req_components_final{req_path_with_file};
$req_path_wo_file       = $req_components_final{req_path_wo_file};
$req_fs_path_with_file  = $req_components_final{fs_path_with_file};
$req_fs_path_wo_file    = $req_components_final{fs_path_wo_file};
$req_year_in_path       = $req_components_final{year_in_path};
$req_month_num_in_path  = $req_components_final{month_num_in_path};
$req_month_day_in_path  = $req_components_final{month_day_in_path};
$req_hour_in_path       = $req_components_final{hour_in_path};
$req_min_in_path        = $req_components_final{min_in_path};
$req_sec_in_path        = $req_components_final{sec_in_path};
$req_filename           = $req_components_final{filename};
$req_theme              = $req_components_final{theme};

{ # Naked block

    my ( @req_path_wo_file_components_l, $breadcrumbs_req_path_wo_file_l,
        $link_to_path_component_l, $path_so_far_l, );

    @req_path_wo_file_components_l = split(/\//, $req_path_wo_file);

    shift @req_path_wo_file_components_l
        if $req_path_wo_file_components_l[0] eq '';

    $breadcrumbs_req_path_wo_file_l = "<a href=\"$req_base_url/\" title=\"Link to home\">$config::label_for_breadcrumb_trail_root</a>";

    foreach my $path_component (@req_path_wo_file_components_l)
    {

        $path_so_far_l .= "$path_component/";

        $link_to_path_component_l = "<a href=\"$req_base_url/$path_so_far_l\" title=\"Link to $path_component\">$path_component</a>";

        $breadcrumbs_req_path_wo_file_l .= "$config::breadcrumb_trail_category_separator$link_to_path_component_l";

    } # End, foreach my $path_component (@req_path_wo_file_components_l)

    $req_breadcrumb_trail = $breadcrumbs_req_path_wo_file_l;

} # End, Naked block

$ffp_to_post_unixtime_hrf = undef;

$ffp_to_post_unixtime_hrf = &$discover_posts();

$request_is_type_root_g = $request_is_type_post_g =
  $request_is_type_category_g = undef;

$request_type = undef;

if ($req_components_final{fs_path_with_file} eq '/')
{
    $request_is_type_root_g = 1;
    $request_type = 'root';

    $request_is_type_post_g = $request_is_type_category_g = 0;

}

elsif ($req_components_final{filename})
{
    $request_is_type_post_g = 1;
    $request_type = 'post';

    $request_is_type_root_g = $request_is_type_category_g = 0;

}

else
{
    $request_is_type_category_g = 1;
    $request_type = 'category';

    $request_is_type_root_g = $request_is_type_post_g = 0;

}

$req_path_is_date_restricted_g = undef;

$req_path_is_date_restricted_g = $req_components_final{year_in_path} ? 1 : 0;

{ # start of naked block

    my (

        $order_executed_l,

        %ffp_to_post_unixtime_for_pfp_l,
    );

    %ffp_to_post_unixtime_for_pfp_l = undef;

    %ffp_to_post_unixtime_for_pfp_l = %$ffp_to_post_unixtime_hrf;

    $order_executed_l = 0;

    foreach my $bundle_num_addin (sort addins_sort keys %pre_filter_posts_addins)
    {
        $pre_filter_posts_addins{$bundle_num_addin}->(\%ffp_to_post_unixtime_for_pfp_l, ++$order_executed_l)
        if defined $pre_filter_posts_addins{$bundle_num_addin};
    }

} # end of a naked block

{ # start of naked block

    my (

        $order_executed_l,
    );

    $order_executed_l = 0;

    foreach my $bundle_num_addin (sort addins_sort keys %filter_posts_addins)
    {
        $filter_posts_addins{$bundle_num_addin}->($ffp_to_post_unixtime_hrf, ++$order_executed_l)
        if defined $filter_posts_addins{$bundle_num_addin};
    }

} # End, Naked block

print &generate_page($ffp_to_post_unixtime_hrf);

__DATA__
error content_type text/html

error date <h3>$wkday_name, $month_day $month_name $year</h3>

error head <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
error head  <html xmlns="http://www.w3.org/1999/xhtml">
error head  <head>
error head    <title>$config::site_title</title>
error head    <style type="text/css">
error head      body {
error head        font-family: Verdana, sans-serif;
error head        font-size: 13px;
error head      }
error head      body a {
error head        text-decoration: none;
error head      }
error head      body a[href]:hover {
error head        border-bottom: 1px solid #c6c6c6;
error head      }
error head      body h1, h2, h3, h4 {
error head        font-family: Verdana, sans-serif;
error head        font-size: 1em;
error head      }
error head      .warning {
error head        margin: 10px 0 20px 0;
error head        background-color: #FFE7E7; /* light red/pink */
error head        border-top: 1px solid #FE8989; /* light-med red-pink */
error head        border-bottom: 1px solid #FE8989; /* light-med red-pink */
error head        padding: 17px 30px 5px 60px;
error head        font-size: 1em;
error head        color: #525252; /* med-dark grey */
error head        font-weight: bold;
error head      }
error head    </style>
error head  </head>
error head  <body>
error head    <div class="warning">
error head      <p>Message</p>
error head      <p>$ode::response</p>
error head    </div>

error posts    <p><b>$title</b></p>
error posts    $body
error posts    <p><a href="$req_base_url/$year/$month_num/$month_day/#$filename">#</a></p>

error foot  </body>
error foot  </html>
__END__