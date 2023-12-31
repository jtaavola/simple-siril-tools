# simple-siril-tools
Simple [Siril](https://siril.org) astro tools

## disabled_seq_imgs.py

This is a simple tool to get the paths of the disabled images of a Siril sequence. It uses the
Siril generated conversion and sequence files to do this. This is useful if you want to
cleanup/delete bad sub-exposures that you didn't end up using in Siril.

## Usage

```sh
./tools/disabled_seq_imgs.py -s path/to/seq_file.seq -c path/to/conversions_file.txt
```

You can delete the returned images if you wish with:
```sh
./tools/disabled_seq_imgs.py -s path/to/seq_file.seq -c path/to/conversions_file.txt | xargs rm
```

### Example files

Example seq file `r_pp_light_.seq`:
```
I 1 0
I 2 1
I 3 1
```

Example conversion file `light_conversions.txt`:
```
'/path/to/IMG_3214.CR2' -> '../process/light_00001.fit'
'/path/to/IMG_3215.CR2' -> '../process/light_00002.fit'
'/path/to/IMG_3216.CR2' -> '../process/light_00003.fit'
```

Using these two files would return `/path/to/IMG_3214.CR2` since the corresponding `.fit` file is
disabled in the Siril sequence.

