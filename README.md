# Speedtest Monitor

## Setup

First, set up a Gmail account to use.  Put the information for that account in the file called `email_config.json`. This file should be in the same directory as `speedtest_logger.py`

Follow the instructions [here](https://github.com/sivel/speedtest-cli) to download `speedtest-cli`, the command line interface to speedtest.net

## Running from the command line

The most basic command is basically a wrapper around the speedtest-cli:

`python speedtest_logger.py`

There are some options you can use as well, including:

	-t or --testing : Skip communicating with speedtest and print dummy data.  Can be helpful to set up logging or email
	-v or --verbose : Prints more detailed information
	-l              : Prints logs to a default file location, which is `/home/pi/log_speedtest.csv`
	--log           : Requires that you provide a log file path to which logs will be printed
	--email         : Sends an email to the provided email address with the results of the test

## Running with cron

Cron lets you schedule tasks to run every period of time.  I've used this script to run every hour or every day.  To run every day start crontab by running `crontab -e`

Then, add the command you want to run to the file.  Daily looks something like this:

	0 12 * * * python /home/pi/speedtest_logger/speedtest_logger.py --log /home/pi/log_speedtest_cron_daily.csv --email emailReceivingData@gmail.com >> /home/pi/cron_speedtest_daily.txt 2>&1

I push the output into a log file as well, as you can see with the `>>`.  This command will run every day, append the data to `/home/pi/log_speedtest_cron_daily.csv`, and email the results each time to emailReceivingData@gmail.com.  This email address is likely, though not necessarily, different than the one sending the data.

To run hourly:

	0 * * * * python /home/pi/speedtest_logger/speedtest_logger.py --log /home/pi/log_speedtest_cron_hourly.csv --email emailReceivingData@gmail.com >> /home/pi/cron_speedtest_hourly.txt 2>&1

[This website](https://crontab.guru) is helpful when scheduling with cron.

