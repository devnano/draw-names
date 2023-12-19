
[ -z "$RAILWAY_VOLUME_MOUNT_PATH/db.sqlite3" ] && cp db.sqlite3 $RAILWAY_VOLUME_MOUNT_PATH/db.sqlite3
ls $RAILWAY_VOLUME_MOUNT_PATH
gunicorn secret_santa.wsgi