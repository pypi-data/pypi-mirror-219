#!/usr/bin/bash
echo "Stoppe Smart Home Controller auf gandalf"
ssh root@gandalf systemctl stop smart-home-tng
echo "Lösche bisheriges Frontend"
ssh shc@gandalf rm -r /var/lib/shc/smart_home_tng/frontend
echo "Kopiere aktuelle Version auf gandalf"
scp -rq smart_home_tng shc@gandalf:/var/lib/shc
echo "Starte Smart Home Controller auf gandalf"
ssh root@gandalf systemctl start smart-home-tng
ssh root@gandalf systemctl status smart-home-tng

