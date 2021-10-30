# Smart-Mirror

Raspberry powered mirror which can display the news, weather, and time.

## Installation and Updating

### Get Code

If you have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed, clone the repository.

```
git clone git@github.com:HackerHouseYT/Smart-Mirror.git
```

Or if you have [GitHub](https://cli.github.com/) installed, clone the repository.

```
gh repo clone rhelmstedter/Smart-Mirror
```

Alternatively, you can download a zip file containing the project (green button on the repository page).

Navigate to the folder for the repository.

```
cd Smart-Mirror
```

### Install your dependencies 

Make sure you have [pip](https://pip.pypa.io/en/stable/installing/) installed before doing this.

```
sudo pip install -r requirements.txt
```

If using [homebrew](https://brew.sh/) for macOS.

```
brew install python-tk@3.9
```

If using Linux install the package.

```
sudo apt install python-imaging-tk
```

If using Windows, may god have mercy on your soul.

TODO: figure this out for windows.

### Add your api token for weather

Create an account at [OpenWeather](https://openweathermap.org). 

Use your favorite editor to modify the script. I prefer vim.

```
vim smartmirror.py
```

Replace the value of `API_KEY` with the token you got from OpenWeather. It should be saved as a string.

### Running

To run the application run the following command in this folder

```
python3 smartmirror.py
```

## Demo and Build Instructions 

This is from the original people who built this project. 

(Click image for link to video.)
[![Link to youtube how-to video](http://i.imgur.com/cMyaSHT.png)](https://youtu.be/fkVBAcvbrjU)
