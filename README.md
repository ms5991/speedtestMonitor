# Speedtest Monitor

## Setup

First, set up a Gmail account to use.  Put the information for that account in the file called `email_config.json`. This file should be in the same directory as `speedtest_logger.py`

Follow the instructions [here](https://github.com/sivel/speedtest-cli) to download `speedtest-cli`, the command line interface to speedtest.net

## Running from the command line

The most basic command is basically a wrapper around the speedtest-cli:

`python speedtest_logger.py`

There are some options you can use as well, including:

`-t` or `--testing`: Skip communicating with speedtest and print dummy data.  Can be helpful to set up logging or email
`-v` or `--verbose`: Prints more detailed information
`l`                : Prints logs to a default file location, which is `/home/pi/log_speedtest.csv`
`--log`	           : Requires that you provide a log file path to which logs will be printed
`--email`          : Sends an email to the provided email address with the results of the test




