#!/usr/bin/bash
locate `xclip -selection primary -o` | head -n 1 | xargs okular &

