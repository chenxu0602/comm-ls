#!/bin/sh


for ticker in \
    PSX DK DINO MUSA CASY FTI OII \
    DHT FRO TNK STNG INSW \
    AVNT ASH CE DOW EMN HUN LYB WLK \
    ATI CRS ERO TECK NEXA \
    SPY XLE XME
do
   echo "Updating $ticker..."
   uv run comm-ls download-equities --ticker "$ticker"
done
