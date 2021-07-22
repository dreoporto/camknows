# Dre-Moe

### Image and motion capture for the Raspberry Pi

## Linux Job Commands Reference

### Run Dre-Moe in background

`nohup python3 dre-moe.py &`

### Single instance only

`flock -n /tmp/dre-moe-lock python3 dre-moe.py`

### Crontab Entry Examples

```
# run dre-moe at 35 minutes past every hour, unless already running
35 * * * * flock -n /tmp/dre-moe-lock python3 /mnt/sandisk-64/dre-moe/dre-moe/dre-moe.py
```

```
# run dre-moe every minute, unless already running (with logging)
* * * * * flock -n /tmp/dre-moe-lock python3 /mnt/sandisk-64/dre-moe/dre-moe/dre-moe.py > /mnt/sandisk-64/myjob.log 2>&1
```

## Misc

## Beyond Compare Sync Filters

```
-*config*.json;-*.mp4;-.\.git\;-.\.idea\;-.\dre-moe\media-files\
```
