#!/bin/bash


a2enmod ratelimit
echo "<Directory /var/www/html/>" > /etc/apache2/mods-available/ratelimit.conf
echo "SetOutputFilter RATE_LIMIT" >> /etc/apache2/mods-available/ratelimit.conf
echo "SetEnv rate-limit 20" >> /etc/apache2/mods-available/ratelimit.conf
echo "</Directory>" >> /etc/apache2/mods-available/ratelimit.conf
ln -s /etc/apache2/mods-available/ratelimit.conf /etc/apache2/mods-enabled/
service apache2 restart



