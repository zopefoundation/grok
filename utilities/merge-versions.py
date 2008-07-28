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

from distutils.version import LooseVersion
from distutils.version import StrictVersion


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
            try:
                version = StrictVersion(split_line[1])
            except ValueError:
                version = LooseVersion(split_line[1])
            versions[package] = version
    return versions


# Hardcoded for now.
# TODO: maybe read arguments from the command line.
grok_versions = make_versions('versions.cfg')
kgs_versions = make_versions('versions.kgs')

warnings = 0
print "[versions]"
for package, grok_version in sorted(grok_versions.items()):
    if package not in kgs_versions:
        # Extra package needed by Grok
        print "%s = %s" % (package, grok_version)
    else:
        kgs_version = kgs_versions[package]
        if isinstance(grok_version, LooseVersion) or \
                isinstance(kgs_version, LooseVersion):
            # Loose versions cannot reliably be compared...
            if isinstance(grok_version, LooseVersion) and \
                isinstance(kgs_version, LooseVersion) and \
                grok_version == kgs_version:
                # ... unless they are both loose versions and exactly
                # the same.
                print "%s = %s" % (package, kgs_version)
            else:
                warnings += 1
                print "#WARNING: package %s has a loose version number." % package
                print "#GROK: %s = %s" % (package, grok_version)
                print "#ZOPE: %s = %s" % (package, kgs_version)
        elif grok_version > kgs_version:
            print "%s = %s" % (package, grok_version)
        elif grok_version <= kgs_version:
            print "%s = %s" % (package, kgs_version)

if warnings > 0:
    print "#There were warnings; manual work needed; please check."
