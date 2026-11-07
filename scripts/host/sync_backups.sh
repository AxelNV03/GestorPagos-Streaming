#!/bin/bash
# /home/anv/proyectos/GestorPagos-Streaming/sync_backups.sh

rclone sync /home/anv/proyectos/GestorPagos-Streaming/storage gdrive:GestorPagos-Backups --progress
