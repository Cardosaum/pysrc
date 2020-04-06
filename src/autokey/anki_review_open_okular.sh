#!/usr/bin/bash
locate -r "/mcs/.*`xclip -selection primary -o`$" | head -n 1 | xargs okular &

