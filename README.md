# Smart-Mirror

Raspberry powered mirror which can display the news, weather, and time. This is an updated fork of the HackerShackOfficial Smart Mirror project.

## Installation and Updating

### Get Code

If you have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed, clone the repository.

```
git clone https://github.com/rhelmstedter/Smart-Mirror.git
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

### Get data for your location

Create an account at [OpenWeather](https://openweathermap.org). 

Use your favorite editor to modify the script. I prefer vim. 

```
vim smartmirror.py
```
**Warning** if you are new to vim, it has modes. This means you can't start typing whatever you want write away. If you panic and don't want to mess up press the escape key and then type the following: `:q!`. The escape key means you will enter normal mode if you aren't already. Then `:q!` tells vim to quit without saving. That way you won't change the file accidentally. Once you are confident, press the `i` key to enter insert mode. Then navigate to where ever you need to go using the arrow keys. If you are not new to vim, you know what to do.

Replace the value of `API_KEY` with the token you got from OpenWeather. Replace the value of `CITY` with your city. Replace the value of `STATE` with your state. Replace the value of `ZIP` with your 5-digit ZIP code. These should all be stored as strings. If you are located outside of the US check out the [OpenWeather docs](https://openweathermap.org/current).

To leave insert mode press escape. Then press `:wq` to save and close the file.

### Running

To run the application run the following command in this folder

```
python3 smartmirror.py
```

## Demo and Build Instructions 

This is from the original people who built this project. 

(Click image for link to video.)
[![Link to youtube how-to video](http://i.imgur.com/cMyaSHT.png)](https://youtu.be/fkVBAcvbrjU)
