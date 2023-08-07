#!/bin/zsh

coverage run -m pytest
coverage report -m --sort=Cover
