"""Merge versions form different buildout files.

This is a helper script for merging the Grok versions.cfg file with
the official KGS versions file.

Download the KGS versions file, for example:
http://download.zope.org/zope3.4/versions-3.4.0c1.cfg
and call it versions.kgs.

Then run this script and it will print the merged versions, with
warnings where necessary.

It picks the most recent version from both files.  If unsure, it will
warn you, in which case you need to manually edit the result.

So something like:

wget http://download.zope.org/zope3.4/versions-3.4.0c1.cfg
mv versions-3.4.0c1.cfg versions.kgs
python utilities/merge-versions.py > candidate.cfg

"""

from pkg_resources import parse_version


def make_versions(filename):
    versions_file = open(filename)
    versions = {}
    for line in versions_file.readlines():
        line = line.strip()
        split_line = line.split(' = ')
        if len(split_line) == 2:
            package = split_line[0]
            if package == 'extends':
                continue
            original = split_line[1]
            parsed = parse_version(original)
            # Store both the original and the parsed version.
            versions[package] = dict(
                original=original, parsed=parsed)
    return versions


# Hardcoded for now.
# TODO: maybe read arguments from the command line.
grok_versions = make_versions('versions.cfg')
kgs_versions = make_versions('versions.kgs')

print "[versions]"
for package, grok_version in sorted(grok_versions.items()):
    if package not in kgs_versions:
        # Extra package needed by Grok
        print "%s = %s" % (package, grok_version['original'])
    else:
        kgs_version = kgs_versions[package]
        if grok_version['parsed'] > kgs_version['parsed']:
            print "%s = %s" % (package, grok_version['original'])
        else:
            print "%s = %s" % (package, kgs_version['original'])
