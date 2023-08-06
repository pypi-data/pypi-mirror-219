# Yumee

**Embed metadata into your music files, whatever the type**  
Yumee stands for *Yet Unother MEtadata Embedder*

## Features

- Automatic type detection based on the file extension
    - Currently supported : MP3, M4A, FLAC, OGG (Vorbis), OPUS
- Detection of badly formatted files
- Easy to use, straightforward interface
- Possible to use via DI integration

## Installation

### Pip

```
pip install yumee
```

### Poetry

[Poetry](https://python-poetry.org/) is a Python dependency management and packaging tool. I actually use it for this project.

```
poetry add yumee
```

## Usage

There are 2 ways to use this library : using the SongMetadataEmbedder object or via the DI.

### Using SongMetadataEmbedder

The library exposes the SongMetadataEmbedder class. This class has 2 method : `open_file` and `embed`.

`open_file` opens an audio file at a provided path and returns a `BaseSongFile` to manipulate its metadata. `embed` opens an audio file and modifies its metadata according to the data provided.

**Example 1 :**

```python
from pathlib import Path
from yumee import SongMetadataEmbedder

embedder = SongMetadataEmbedder()
path = Path("path/to/file.mp3")

with embedder.open_file(path) as song_file:
    song_file.title = "New Title"
```

*It is recommended to use 'open_file' with the 'with' statement as it will ensure that the modifications are saved as you exit the block. Otherwise, you have to make sure to call 'save' to save the modifications.*

**Example 2 :**

```python
from pathlib import Path
from yumee import SongMetadataEmbedder, SongMetadata

embedder = SongMetadataEmbedder()
path = Path("path/to/file.mp3")
metadata = SongMetadata(title="New Title")

embedder.embed(path, metadata)
```

### Using DI

The library also exposes a `BaseSongFileProvider` interface and a `add_yumee` function for [Taipan-DI](https://github.com/Billuc/Taipan-DI).

In this function, SongFileProviders are registered as a Pipeline. Each SongFileProvider correspond to a specific file type and generates a `BaseSongFile`. Resolve the pipeline and execute it to have a `BaseSongFile` you can then manipulate.

**Example :**

```python
from yumee import BaseSongFileProvider, add_yumee
from taipan_di import DependencyCollection

services = DependencyCollection()
add_yumee(services)
provider = services.build()

song_file_provider = provider.resolve(BaseSongFileProvider)
path = Path("path/to/file.mp3")

with song_file_provider.exec(path) as song_file:
    ...
```

## Inspirations

This library is partially inspired by spotDL's [spotify-downloader](https://github.com/spotDL/spotify-downloader) and utilises [mutagen](https://mutagen.readthedocs.io/en/latest/).
