# django2dbdiagram

A simple script to convert Django Models to DBML (Data Base Markup Language) code (usable at dbdiagram.io).

## Pre-requisites

You need to have Django installed in your python environment.

## How to use?

* Download `main.py` to your Django project.
* Set the `DJANGO_SETTINGS_MODULE` environment variable to reflect your projects settings inside `main.py`
* Run `python main.py`

## Expectations

This is a script that works to convert your Django project's models to a DB diagram written in DBML. It is not meant to be feature complete, hence expected to work more as a boilerplate DB diagram generator.