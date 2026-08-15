# Worked example: an undocumented binary save file

## Artifact inventory

Preserve two untouched saves and record application version, platform, file hashes, sizes, and timestamps. Work only on copies.

## Observable interface map

Create controlled saves that differ in one visible value. A repeated header remains fixed; a four-byte region changes with the visible score; the last bytes change after any edit.

## Competing hypotheses

- The score is a little-endian integer and the tail is a checksum.
- The changing region is an index into a table and the tail is compressed metadata.

## Probe

Change the score from 1 to 2, 255, 256, and 257 in fresh saves. The four bytes follow little-endian integer boundaries. Copying those bytes without updating the tail makes the application reject the file.

## Minimal replica

Write a parser that reads the header and score, plus a checksum hypothesis derived from differential samples. Predict the tail for a score not used during fitting, generate a copy, and open it in an isolated profile.

## Warning label

The model explains one version and two fields. Inventory layout, compatibility, corruption recovery, and checksum coverage remain unknown. Do not publish proprietary sample files.

## Why this is Nitori-shaped

The result is a mechanism map and predictive replica—not merely proof that editing one byte once appeared to work.
