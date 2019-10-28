#!/bin/sh

ps -ef | grep "api.py" | grep -v grep | awk '{print $2}' | xargs kill
