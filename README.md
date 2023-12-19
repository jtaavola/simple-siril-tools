# simple-siril-tools
Simple [Siril](https://siril.org) astro tools

## disabled_seq_imgs.py

This is a simple tool to get the paths of the disabled images of a Siril sequence. It uses the
Siril generated conversion and sequence files to do this. This is useful if you want to
cleanup/delete bad sub-exposures that you didn't end up using in Siril.

## Usage

Example seq file `r_pp_light_.seq`:
```
...
I 1 0
I 2 1
I 3 1
...
```

Example conversion file `light_conversions.txt`:
```
'/path/to/IMG_3214.CR2' -> '../process/light_00001.fit'
'/path/to/IMG_3215.CR2' -> '../process/light_00002.fit'
'/path/to/IMG_3216.CR2' -> '../process/light_00003.fit'
```

Running this tool returns the disabled images:
```sh
./disabled_seq_imgs.py -s path/to/r_pp_light_.seq -c path/to/light_conversions.txt
```

```
/path/to/IMG_3214.CR2
```

You can delete these images if you wish with:
```sh
./disabled_seq_imgs.py -s path/to/r_pp_light_.seq -c path/to/light_conversions.txt | xargs rm
```

