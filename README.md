# UCSC-custom-track-automator
Script to automatically generate custom tracks to load in the [UCSC Genome Browser](https://genome.ucsc.edu/). 

# Usage

Simply pass the script a list of your input files, and the base URL for UCSC to access the files from. 

```bash
./make-tracks.py test1.bw test2.bw -url http://myserver.edu.external/

UCSC Tracks output to file:
UCSC_custom_tracks-2017-04-04-16-45-46.txt
```

Output will look like this:

```bash
track type=bigWig name="test1.bw" bigDataUrl=http://myserver.edu.external/test1.bw
track type=bigWig name="test2.bw" bigDataUrl=http://myserver.edu.external/test2.bw
```

You can pass a mixed list of files, and the script will create a track tailored for each file's type. An output file can also be specified, instead of the default timestamped file (warning: output file will be overwritten).

```bash
find sample-data/mixed/ -type f ! -name "*.bai" | xargs ./make-tracks.py -url http://myserver.edu.external/ -p bigwig_params.txt -o my_custom_tracks.txt

UCSC Tracks output to file:
my_custom_tracks.txt
```

In this case, our output file `my_custom_tracks.txt` looks like this:

```bash
track type=BED name="test.bed" url=http://myserver.edu.external/test.bed visibility=full autoScale=off alwaysZero=on maxHeightPixels=50 graphType=bar viewLimits=0:0.3
track type=BAM name="test.bam" bigDataUrl=http://myserver.edu.external/test.bam visibility=full autoScale=off alwaysZero=on maxHeightPixels=50 graphType=bar viewLimits=0:0.3
track type=bigWig name="test.bw" bigDataUrl=http://myserver.edu.external/test.bw visibility=full autoScale=off alwaysZero=on maxHeightPixels=50 graphType=bar viewLimits=0:0.3
```

## Params file

Extra params to be included in each track can be placed in a separate `params` file. This file should contain items to be included in **every** track, with one item per line. The `params` file argument can be invoked like this:

```bash
./make-tracks.py sample-data/bigwigs/test1.bw sample-data/bigwigs/test2.bw -url http://myserver.edu.external/ -p bigwig_params.txt
```

Where `bigwig_params.txt` is our `params` file, and contains:

```bash
visibility=full
autoScale=off
alwaysZero=on
maxHeightPixels=50
graphType=bar
viewLimits=0:0.3
```
Resulting in tracks that looks like this:

```bash
track type=bigWig name="test1.bw" bigDataUrl=http://myserver.edu.external/test1.bw visibility=full autoScale=off alwaysZero=on maxHeightPixels=50 graphType=bar viewLimits=0:0.3
track type=bigWig name="test2.bw" bigDataUrl=http://myserver.edu.external/test2.bw visibility=full autoScale=off alwaysZero=on maxHeightPixels=50 graphType=bar viewLimits=0:0.3
```
# Notes

## URL

The URL supplied must be reachable by UCSC. If the URL requires a user-login, it will not work. If you are not sure, you should test the URL for one or more tracks by trying to navigate to them from your web browser; login screens and network restrictions may prevent them from working for UCSC. 

## Supported Types

Currently, only the following file formats are supported by the script:

- bigWig: ".bw"
- BED: ".bed"
- bigBed: ".bb"
- VCF: ".vcf"
- BAM: ".bam"
- bedGraph: ".bg"

More types may be added later (or you can add them yourself in the script).

## Unsupported Customizations

This script is designed to apply attributes to tracks for all given files; it is currently not set up to include browser customizations such as:

```
browser position chr22:10000000-10020000
browser hide all
```

These options are easy enough to copy/paste into your tracks text file as-is.

# More information

Information on track customization can be found here:

- https://genome.ucsc.edu/goldenpath/help/hgTracksHelp.html
- https://genome.ucsc.edu/goldenpath/help/customTrack.html


You can load your custom tracks here:
- https://genome.ucsc.edu/cgi-bin/hgCustom

# Software Requirements
- Python 2.7+ (tested on 2.7.3 and 3.4.3)
