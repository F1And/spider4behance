# -*- coding: UTF-8 -*-

from scrapy import cmdline

# name = 'portfolio'
name = 'type'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
