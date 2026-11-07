#!/bin/bash

apt-get update
apt-get install -y python3-pip git

cd /opt

git clone https://github.com/peiomi/asteroid_watch.git

cd asteroid_watch

pip3 install --break-system-packages -r discord_bot/bot_requirements.txt

cat > /etc/systemd/system/asteroid-bot.service << 'EOF'
[Unit]
Description=Asteroid Watch Discord Bot
After=network.target

[Service]
WorkingDirectory=/opt/asteroid_watch
Environment=PYTHONPATH=/opt/asteroid_watch
ExecStart=/usr/bin/python3 -m discord_bot.bot
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable asteroid-bot
systemctl start asteroid-bot
