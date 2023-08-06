# TorScrape

TorScrape: Efficient Web Scraping for Data Extraction


## Features

-   **Information Retreival**: Easily fetch information of any TikTok user profile.

-   **Flexible Customization**: Customize the number of video links to retrieve for optimal data collection.

-   **No API Dependency**: Independently collect TikTok video links without relying on TikTok APIs.

-   **Pythonic and Easy-to-Use**: Follows Pythonic conventions with an intuitive interface for seamless integration.



## Installation

Install TorScrape using pip:
-   pip install -r requirements.txt
-   pip install torscrape

# note
-   TorScrape requires Python 3.6 or later.

## Documentation
-   For detailed usage instructions and additional functionality, please refer to the documentation on the github page.

## Contributing
-   We welcome contributions to TorScrape! If you encounter issues, have suggestions for improvements, or would like to contribute new features, please feel free to open an issue or submit a pull request on GitHub.


## License
-   This package is licensed under the MIT License. See the LICENSE file for more information.


### Example

```shell
Here's an example of how to fetch the latest video links from a TikTok user profile:
```

```python
import TorScrape

username = "example_user"
count = 10

ToreScrape.get_latest_vid_links(username, count)
```