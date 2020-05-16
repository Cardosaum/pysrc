#!/usr/bin/bash

# locate --basename "`xclip -selection primary -o`" | head -n 1 | xargs okular &
fd --absolute-path --ignore-case "`xclip -selection primary -o`" ~/mcs/study/anki/allPDFs | head -n 1 | xargs okular
