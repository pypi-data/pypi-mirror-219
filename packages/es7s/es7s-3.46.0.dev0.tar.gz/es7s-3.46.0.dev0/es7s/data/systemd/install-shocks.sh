#!/bin/bash

sudo cp es7s-shocks.service /etc/systemd/system/
sudo sed /etc/systemd/system/es7s-shocks.service -i -Ee "s/%UID/$(id -u)/g; s/%USER/$(id -un)/g"
sudo systemctl enable es7s-shocks.service
sudo systemctl daemon-reload
sudo systemctl restart es7s-shocks.service
sudo systemctl status es7s-shocks.service
