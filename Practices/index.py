from croniter import croniter
from datetime import datetime

now = datetime.now()

# min hour day month week
cron = croniter('0 10,14,16 * * *')
print (cron.get_next(datetime))