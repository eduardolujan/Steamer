# -*- coding: utf-8 -*-

''' José Manuel Fardello, 2012. 
A quick'n dirty django-flatpages builder for sphinx...
It worked for me but it needs a better integration with django
and some configuration variables in the sphinx config file.
'''

import os 
import sys
from sphinx.builders.html import SerializingHTMLBuilder
from sphinx.builders.html import JSONHTMLBuilder
from sphinx.util import jsonimpl

sys.path.append(os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + '../../../'))
doc_root = os.path.normpath( os.path.dirname(os.path.abspath(__file__)) + '/build/html/' )
os.environ['DJANGO_SETTINGS_MODULE'] = 'steamer.settings'
from django.core.management import setup_environ
from django.contrib.sites.models import Site
from steamer import settings

setup_environ(settings)

from django.contrib.flatpages.models import FlatPage


class SerializingFlatPageBuilder(SerializingHTMLBuilder):
    prepend_uri="sphinx"
    site = Site.objects.get(id=settings.SITE_ID)

    def dump_context(self, context, filename):
        self.info("Called for %s" % self.current_docname)
        if context.get('body'):
            if self.current_docname == 'index':
                fp_name = '/%s/' % self.prepend_uri
            else:
                fp_name = '/%s/%s/' % (self.prepend_uri, self.current_docname)
            f, cted = FlatPage.objects.get_or_create(url=fp_name)
            f.content = context['body']
            f.title = context['title']
            f.sites.add(self.site)
            f.save()
        
class FlatpagesBuilder(SerializingFlatPageBuilder):
    """A dumb builder that dumps the generated HTML into django-flatpages."""

    implementation = jsonimpl
    implementation_dumps_unicode = True
    indexer_format = jsonimpl
    indexer_dumps_unicode = True
    name = 'flatpages'
    out_suffix = ''
    globalcontext_filename = 'globalcontext.json'
    searchindex_filename = 'searchindex.json'
    prepend_uri="doc"

    def init(self):
        if jsonimpl.json is None:
            raise SphinxError(
                'The module simplejson (or json in Python >= 2.6) '
                'is not available. FlatpagesBuilder will not work.')
        self.init_templates()
        self.init_translator_class()
        self.init_highlighter()


def setup(app):
    app.info('Initializing FlatpagesBuilder')
    app.add_builder(FlatpagesBuilder)
    return
