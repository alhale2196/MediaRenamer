# MediaRenamer  

MediaRenamer is a lightweight and flexible tool for renaming and organizing your media files. It’s designed to quickly process large collections of movies, TV shows, music, or images, ensuring consistent and human-friendly file names.

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- Batch rename entire folders of media files  
- Customizable renaming templates (e.g., `{title} - S{season}E{episode}`)  
- Automatic metadata fetching (from sources like TMDB/IMDB if configured)  
- Smart handling of file extensions and duplicates  
- Dry-run mode to preview changes before applying  
- Cross-platform support (Windows, macOS, Linux)

## Installation

Download from pip repository:
```
pip install mediarenamer
```
### Or build from source

Clone the repository:  
```
git clone https://github.com/yourusername/MediaRenamer.git
cd MediaRenamer
```
Install dependencies:
```
pip install -r requirements.txt
```

## Usage

Basic usage:
```
mediarenamer --help
```

## Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to your fork (`git push origin feature-name`)
5. Open a pull request

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.