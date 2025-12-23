#!/bin/bash

# Sync the entire unified Trident project (including Veil subsystem)
rsync -avh --delete \
    ~/projects/trident/ \
    "/mnt/c/The Veil/trident/"

echo "✔ Full Trident sync complete — Windows now mirrors Linux."
