#!/bin/bash
PYTHONPATH=.:$PYTHONPATH py.test -vv -s --tb=short --showlocals \
                                 jinja2schema ./tests "$@"
