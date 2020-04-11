#!/bin/bash

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/matheus/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/matheus/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/matheus/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/matheus/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

conda activate anki

python -c "import sys; print(sys.executable)"

/home/matheus/Downloads/subDirectories/anki-2.1.22/run

