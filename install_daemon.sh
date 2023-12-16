#!/bin/bash


SERVICE_NAME="daysu_daemon@"
SERVICE_FILE="$SERVICE_NAME.service"
SERVICE_DESTINATION="/etc/systemd/system/"

if [[ "$EUID" -ne 0 ]]; then
    echo "script must be run as root"
    exit 1
fi

cp "$SERVICE_FILE" "$SERVICE_DESTINATION"

echo "$SERVICE_NAME$SUDO_USER.service"
systemctl enable "$SERVICE_NAME$SUDO_USER.service"
systemctl start "$SERVICE_NAME$SUDO_USER.service"

systemctl status "$SERVICE_NAME$SUDO_USER.service"

echo "Installation complete"
