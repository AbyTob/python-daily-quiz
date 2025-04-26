# python-daily-quiz

## Set-up crontab

```bash
chmod +x cronjob.sh
```

```cron
# m h  dom mon dow   command
* */8 * * * bash /<your_path>/cronjob.sh >> /<your_path>/cronlog.log 2>&1

```