# genshinAutoGlossary

Update your input method preferences as Genshin Impact updates and rolls out a new version, just some keystrokes away.

## Attention

1. This software was tested on a macOS device having Python 3.9 installed. It may also work on some other Linux or BSD distros but probably not on a Windows device
2. You have to git clone <https://github.com/Dimbreath/GenshinData> to your local PC first

## How to use

1. git clone this repository to your local disk
2. Find `Common/conf.py` and change the `dataPath` and `prodPath` variables.
3. `pip3 install opencc pypinyin`
4. cd to `{ProjectRoot}` and run `python3 app.py`
5. The program will run and produce some output to console.
6. The generated files required by Rime (Squirrel) will be produced at `{ProjectRoot}/Build` folder. Copy all the three files there to your Rime config folder.
7. Re-deploy your input method and enjoy

## Notes for macOS Monterey and above

If Python complains about missing openCC, try installing it using 
`brew install opencc`. If it continues complaining that the opencc library 
is missing, find that (it is typically installed under 
`/opt/homebrew/Cellar/opencc/1.1.6/lib`), and add it to your .zshrc 
environment variable by adding `export 
LIBOPENCC='/opt/homebrew/Cellar/opencc/1.1.6/lib/libopencc.dylib'`, and 
then source it.
