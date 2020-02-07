# spotify\_collage
'spotify\_collage' provides a simple method of retrieving all unique album art from either a Spotify playlist or artist on Spotify and creating a collage from the query.

## Installation:
```bash
git clone https://github.com/orioncrocker/spotify_images
```

## Setup:
Before using this program, you'll need to get credentials from [Spotify's API](https://developer.spotify.com/documentation/web-api/quick-start/). An account on Spotify will provide two credentials: 'client id' and 'client secret.' In order to use your own credentials, you will have to create a file named `config.py.`

Your `config.py` file should have these two fields:
```python
client\_id = 'your client id'
client_secret = 'your client secret'
```

## Usage:
Download all album artwork from a specific artist on Spotify
```bash
python3 main.py -a 'Carpenter Brut'
```
```
7 saved to results/carpenter_brut
```

This option did not take advantage of the `verbose` flag `-v` or `collage` flag `-c`. When using both of these flags, the output will look as such.

```bash
python3 main.py -vca 'Carpenter Brut'
```
```
results/carpenter\_brut/trilogy.jpeg
results/carpenter\_brut/leather\_teeth.jpeg
results/carpenter\_brut/carpenterbrutlive.jpeg
results/carpenter\_brut/night\_stalker\_(from_"the\_rise\_of\_the\_synths").jpeg
results/carpenter\_brut/hush\_sally,\_hush!.jpeg
results/carpenter\_brut/maniac\_(live).jpeg
results/carpenter\_brut/turbo\_killer\_(live).jpeg
7 saved to results/carpenter\_brut
Total unique pictures: 7
Rows: 2	Cols: 3
Collage saved as: results/carpenter\_brut.jpeg```
```
The resulting collage:
[![Carpenter Brut Collage](examples/collage.jpeg)]()

To save all images of a playlist, you will need to URI of the playlist from Spotify. This can be found on Spotify's application or web browser

[![Example URI](examples/uri.jpeg)]()


```bash
python3 main.py -vcp spotify:playlist:1l3ttggvijrdbYX8lsZ7eI
```
```
results/outrun\_ynthwave/near\_dark.jpeg
results/outrun\_synthwave/into\_the\_abyss.jpeg
results/outrun\_synthwave/send\_the\_signal.jpeg
results/outrun\_synthwave/the\_shape.jpeg
results/outrun\_synthwave/volume\_1.jpeg
results/outrun\_synthwave/trilogy.jpeg
results/outrun\_synthwave/this\_means\_war.jpeg
results/outrun\_synthwave/dangerous\_days.jpeg
results/outrun\_synthwave/the\_wrath\_of\_code.jpeg
results/outrun\_synthwave/bad\_mood\_(deluxe).jpeg
results/outrun\_synthwave/gunship.jpeg
results/outrun\_synthwave/the\_real\_deal.jpeg
results/outrun\_synthwave/storm\_city.jpeg
results/outrun\_synthwave/leather\_teeth.jpeg
14 images saved to results/outrun\_synthwave
Total unique pictures: 14
Rows: 3	Cols: 4
Collage saved as: results/outrun\_synthwave.jpeg
```
The resulting collage:
[![Outrun Collage](exaples/outrun.jpeg)]()

To specify the output location and name of a collage file, use the `-o` flag.
```bash
python3 main.py -cp spotify:playlist:1l3ttggvijrdbYX8lsZ7eI -o output
```
```
Collage saved as: output.jpeg
```

There is no need to add a file extension to the name, as the default always saves as a `.jpeg`.

## Planned features:
Specific width and height, for the purposes of creating wallpapers for screens of various resolutions. This requires more math and time than my small brain can comprehend in a small amount of time.
