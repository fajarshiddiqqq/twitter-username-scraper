# Twitter Username Scraper

## Overview

The Twitter Username Scraper is a Python script designed to extract data such as likes, retweets, and replies from a given tweet url on Twitter or X. It utilizes the [`twscrape`](https://github.com/vladkens/twscrape) library to interact with Twitter's API.

## Setup

#### Prerequisites

-   Python 3.11 installed on your system
-   Access to the internet

#### Installation

1. Clone or download this repository to your local machine.
2. Navigate to the project directory in your terminal or command prompt.

##### If using a conda environment:

3. Create a conda environment:

```bash
conda create --name [your_env] python=3.11
```

4. Activate the conda environment:

```bash
conda activate [your_env]
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

##### If not using a virtual environment:

3.  Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:

```
python main.py
```

2. Enter your Twitter account credentials when prompted. These credentials are required to access Twitter's API.

3. Enter the URL of the tweet you want to scrape data from (e.g., https://twitter.com/user/status/1234567890).

4. After successful execution, the scraped data will be stored in the `results/` directory.

## Note

-   Ensure you have a stable internet connection while running the script.
-   <b>All credentials are stored locally and are not shared with any third-party services.</b>
