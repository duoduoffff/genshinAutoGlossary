# genshinAutoGlossary

Update your input method preferences as Genshin Impact updates and rolls out a new version, just some keystrokes away.

## Attention

1. As of the time when macOS Sonoma was released, Apple has disabled the use of pip3 by declaring "externally managed" when you run pip. Thus use of third-party libs are restricted.
1. This software was tested on a macOS device having Python ~~3.9~~ **3.13** installed. It may also work on some other Linux or BSD distros but probably not on a Windows device
2. You have to git clone <https://github.com/Dimbreath/GenshinData> to your local PC first

## How to use

1. git clone this repository to your local disk
2. Find `Common/conf.py` and change the `dataPath` and `prodPath` variables.
3. `pip3 install opencc pypinyin`
4. cd to `{ProjectRoot}` and run `python3 app.py`
5. The program will run and produce some output to console.
6. The generated files required by Rime (Squirrel) will be produced at `{ProjectRoot}/Build` folder. Copy all the three files there to your Rime config folder.
7. Re-deploy your input method and enjoy

## For Yuhao-Guanghua users

To make Yuhao-compatible wordlib, first make sure that the file 
~~`~/Library/Rime/yuhao.full.dict`~~ `~/.local/share/fcitx5/rime/yuhao/yulight.full.dict.yaml` exists before proceeding as follows:

1. Make sure that GenshinData is present and run yuhao.py.
2. Copy `Build/yuhao.genshin.dict.yaml` to `~/.local/share/fcitx5/rime`.
3. Find `~/Library/Rime/yulight.full.dict.yaml` and append `yuhao.genshin` under 
node `import_tables`. Adding to `yuhao.dict.custom.yaml` is **NOT** going to 
work. You have to make this change every time the input scheme updates.
4. Re-deploy and use it.

Attention, to prevent too many words taking the same input sequence, we 
have excluded `Artifact` and `Homeworld` by default. To add these back, 
you have to alter the function parameters. See 
<https://github.com/duoduoffff/genshinAutoGlossary/blob/master/Common/gen.py#L61>.


## Notes for macOS Monterey and above

If Python complains about missing openCC, try installing it using 
`brew install opencc`. If it continues complaining that the opencc library 
is missing, find that (it is typically installed under 
`/opt/homebrew/Cellar/opencc/1.1.6/lib`), and add it to your .zshrc 
environment variable by adding `export 
LIBOPENCC='/opt/homebrew/Cellar/opencc/1.1.6/lib/libopencc.dylib'`, and 
then source it.
