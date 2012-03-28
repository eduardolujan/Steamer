# -*- coding: iso-8859-15 -*-
#this is an in-progress rewrite of the import tool

# 2011 José Manuel Fardello

import uuid
import re
import os
import sys
import logging
import unicodedata
import shelve

import chardet

from django.db.models import NullBooleanField, ForeignKey, ManyToManyField
from django.utils.simplejson import dumps, JSONEncoder

from steamer.djagios import models
from steamer.djagios.models import Transform


import settings

logger = logging.getLogger(__name__)



''' Djagios import tool,

The Idea is fairly simple: don't make an exceptions based import script, treat all
the objects the same way if possible, custom & arcane twicking must live in the model
as class methods. Theres an abtract class that defines the default ones, that can be
overriden and the transormation routines will try to load field-specific and 
model-specific ones.

It is more or less like this: 

1 load all the nagios config to a cache dict of different types of nagios objects 
somewhere.

2 Loop through the cache.

    2.1 Prepare any kind of nagios object from the dict for database insertion: split lines
    create new objects, 

        2.1.1 Look for custom trasformations and apply them
        2.1.2 Transform default things, relations nullbooleans, etc.
        2.1.3 Store some related stuff so that it can be added after the objects 
        
    2.2 Add The objects (save() them so that they have an id in order to be related.)

    2.3 For each relation stored for that object add it via 
    ModelX.related_manager.add(*[list of rel objects]) if it is a m2m one or through 
    __setattr__ if it is a foreign key.

3 save
'''


def cleanse_empty(x):
    '''filter comments and empty lines'''
    if (len(x.strip()) ==0 or \
            x.strip().startswith("#") or \
            x.strip() == " " or \
            x.strip().startswith(";")): 
        return False
    else:
        return True

def cleanse_pullout_coments(x):
    '''Nagios ignores everything after a semicolon, 
            
    It is not possible to escape it, 
    see http://nagios.sourceforge.net/docs/3_0/objectdefinitions.html'''
    return x.split("#")[0].split(";")[0].strip()
             
def strip_accents(s):
    '''Try to normalize non 7bit stuff, sorry, nagios won't complain, but it won't work.'''
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

class WholeLineDefinition:
    '''Nagios config syntax is ambiguous & inconsitent, this class is for tracking 
    timeranges. think of this:

    define timeperiod{
        timeperiod_name     nonworkhours ; key -> val stuff, good.
        alias    Non-Work Hours, a long - long  line. ; key: just the first word -> value: all the rest. 
        thursday -1 november  00:00-24:00 ; theres no key, nor value here, just the line.
    }
    So in order to preserve isintance() checks, the last one will be stored:
      key = whole line
      val = WholeLineDefinition()
    '''
    def __repr__(self):
        return '<Djagios WholeLineDefinition>'

class DjagiosEncoder(JSONEncoder):
    '''json encoder for debugging'''
    def default(self, o):
        if isinstance(o, WholeLineDefinition):
            return '__dwld'

class Hashable(dict):
    '''Cached dicts must be hashable in order to build sets.

    Also, force the uniqness of a service by adding a v4 uuuid as it apears, nagios treats definitions
    as overridable instances of a definition, we can't do this with a uniq together Meta due to the 2 
    phase insert, as in the early step we have no fk, nor m2m fields (and also it is not possible in django
    to the use uniq together feature with m2m fields)
        '''
    def __init__(self, *args, **kwargs):
        self['id']=uuid.uuid4().hex
        self.update(*args, **kwargs)
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

class DjagiosConfigParser(object):
    nagios_etc_root="/opt/local/nagios/etc"
    _cache={}
    _configs=set()

    def __init__(self, **kwargs):
        if kwargs.get('debug'):
            #this is mainly for postmortem debugging.
            self._cache = shelve.open(".%s.djagios.debug" % uuid.uuid4().hex)
        self._cache['nagioscfg']=[{},]

    def read_file(self, filename, main=False):
        '''Saves the nagios config to the cache.
        All the config will be converted to  plain ascii, as of nagios 3.2 there are 
        some bugs when displaying non ascii data, wellcome back to the 7bits age.. :C.
        '''

        logger.debug('Parsing %s' % filename)

        with open(filename, 'rb') as fd:
            fstring = fd.read()
            #This ain't fast, it tries to save your strings while downgrading unicode to
            #ascii, ex: José -> Jose 
            try:
                if len(fstring) > 0: 
                    fstring = str(strip_accents( unicode(fstring, 
                                    chardet.detect(fstring).get('encoding')
                                    )).encode('ascii','ignore'))
            except UnicodeDecodeError as detail:
                def_enc = settings.DJAGIOS_IMPORTENCODING
                logger.error('while reading %s \n, retrying with %s' % (filename, def_enc))
                logger.debug(detail)
                try:
                    fstring = str(strip_accents( unicode(fstring, def_enc)).encode('ascii','ignore'))
                except UnicodeDecodeError as detail:
                    logger.error('sorry, couldn\'t make it, %s' % detail)
                    sys.exit(1)

            lines = fstring.split("\n")
            #clear half line comments
            lines = map(cleanse_pullout_coments, lines)
            #clear comments and empty lines
            lines = filter(cleanse_empty, lines)
            #reassemble the clean string, so that we can run regexps on it.
            fstring = "\n".join(lines)

            if main:
                #The main config file
                self.main_file = filename
                for line in lines:
                    splitted=line.split("=", 1)
                    if splitted[0] == 'cfg_dir' or splitted[0] == 'cfg_file': 
                        logger.debug('Gonna lookfor cfgs in: %s' % splitted[1])
                        self._configs = self._configs | self._get_includes(splitted[1])    
                    else:
                        #we want 'nagioscfg' key behave like the rest of definitions.
                        self._cache['nagioscfg'][0].update({splitted[0]:splitted[1]})
            else:
                schemas = re.finditer("define\s+(?P<def_type>\S*)\s*\{\n*(?P<content>.*?)\}", fstring, re.S)
                for schema in schemas:
                    instance=Hashable()
                    content=schema.group('content').split("\n") 
                    #regex matching will leave some gaps..
                    for cline in content:
                        if len(cline) == 0:
                            continue
                        split_line=cline.strip().split()
                        if schema.group('def_type') == "timeperiod" and \
                                split_line[0] not in  ("alias", "timeperiod_name"):
                            #handle whole line words lines, ej : "february 10  00:00-24:00"
                            #key=> "february 10 00:00-24:00"  ,val=WholeLineDefinition()
                            val=WholeLineDefinition()
                            key=" ".join(split_line)
                        else:    
                            key = cline.strip().split()[0]
                            val = " ".join(cline.strip().split()[1:])
                        instance.update({key:val})
                    
                    if self._cache.has_key(schema.group('def_type')):
                        self._cache[schema.group('def_type')].append(instance)
                    else:
                        self._cache[schema.group('def_type')] = [instance] 

    def _get_includes(self, path):
        '''Returns a set with the all cfg files that should be read.'''

        #Relativize the path to reflect the fs on the importing machine. 
        relative_path = "/".join(self.main_file.strip("/").split("/")[:-1])
        path = "/" + path.replace(self.nagios_etc_root, relative_path, 1)
        logger.debug('Looking for includes in: %s' % path)

        if os.path.isfile(path):
            return set([path])
        else:
            all=set()
            for root, sF, files in os.walk(path):
                all = all | set( map(lambda x: os.path.join(root,x),  
                             filter(lambda y: y.endswith(".cfg"),files)))
            return all

    def parse(self, cfgfile):
        '''Loads all the config to the cache, and tries to sort the hashable dicts in the order
        they should be inserted.'''

        cfgfile = os.path.join(settings.DJAGIOS_IMP_DIR, cfgfile)
        self.read_file(cfgfile, main=True)
        for eachfile in self._configs:
            self.read_file(eachfile)

        def dep_position(item, deps):
            #find the position of the dependedy
            if item.get('use'):
                for (pos, dep) in enumerate(deps):
                    if ( dep.get('name') == item.get('use') or \
                         dep.get('service_name') == item.get('use') or \
                         dep.get('host_name') == item.get('use')):
                        return pos
                raise RuntimeError("Could't find a template for %s" % item) 
            else:
                #Not dependent
                return None

        def solve(deps):
            #Cheap topological sort.
            while True:
                moved=0
                for (pos, item) in enumerate(deps):
                    dep_pos = dep_position(item, deps)
                    if dep_pos and dep_pos > pos:
                        logger.debug('moving item %s to %s' % (pos - moved, dep_pos+1 ))
                        deps.insert(dep_pos + 1 , deps.pop(pos - moved))
                        moved += 1
                        break
                if moved == 0:
                    break
            return deps
            

        #Sort the templates.
        for key in self._cache.keys():
            if key != 'nagioscfg':
                logger.info('Solving dependencies for %s %s definitions...' % (len(self._cache[key]), key)) 
                root=solve( filter( lambda x: True if x.get('register', '1') == '0' else False, self._cache[key]))
                rest=filter(lambda x: True if x.get('register', '1') == '1' else False, self._cache[key])
                self._cache[key] = solve(root + rest)
                
    def dumps(self, obj):
        '''For debugging.'''
        return dumps(obj, cls=DjagiosEncoder, indent=4)

    def load_to_db(self, filename, server_name, replace=None):
        '''This is the main importing loop, we're going to loop over the cache
        translate the dict and feed the models with that data.'''

        if replace:
            self.nagios_etc_root=replace.rstrip("/")

        self.server_name=server_name
        logger.info('Loading nagios cfg to memory..')
        self.parse(filename)

        for model_name in settings.DJAGIOS_IMPORT_OBJECTS: 
            logger.info('Saving %s to database...' % model_name )
            self._translate_and_load(model_name)

    def _translate_and_load(self, model_name):
        '''Load to db from cache: 
        1 translate the cache dict into a Transform object via self.translate_dict()
        2 save the the data from the fields key in the transform object
        3 save the fk relations from the Transform object fk key
        4 save the m2m relations from the Transform object m2m key
        '''
        relateds={}

        for obj in self._cache[model_name.lower()]:
            translated=self.translate_dict(obj, model_name)
            if model_name == "NagiosCfg":
                translated.add_field({'server_name': self.server_name})
            #Relations will be added later.
            NewModel=getattr(models, model_name)
            logger.debug('About to get/create with %s' % translated['fields'])
            new_obj, cted = NewModel.objects.get_or_create(**translated['fields'])
            
            for field, rel in translated['fk'].iteritems():
                logger.debug('Adding fk to %s with id %s' % (model_name, new_obj.pk))
                new_obj.__setattr__(field, rel)
                new_obj.save()
            for mgr in translated['m2m'].keys():
                logger.debug('Adding %s m2m objects through "%s" manager to %s with id %s' % \
                            (len(translated['m2m']), mgr, model_name, new_obj.pk) )
                getattr(new_obj, mgr).add(*translated['m2m'][mgr])
                new_obj.save()


        logger.info('Cached %s objects have been saved' % model_name)


    def translate_dict(self, dict_object, classname):
        '''Twicks a Hashable dict into a one suitable for feeding a model.
    
        Custom fields transformations should be defined in the model as classmethods, if the 
        definition block is expected to have "whole line definitions", transform_WLD,
        should be defined, else for custom & bizarre transformationis a method that parses 
        the value should be defined in the model: transform_fieldname(dict).
        This method should handle most of the work: nullboolean,m2m and foreignkey fields. 
        '''
        DjagiosModel = getattr(models, classname)
        #we'll store relations here.
        resp_dict = models.Transform()

        for field in dict_object.keys():
            if field not in DjagiosModel._meta.get_all_field_names():
                #try to fetch by object type
                if isinstance(dict_object[field], WholeLineDefinition):
                    transform_f = getattr(DjagiosModel, "transform_WLD", None)
                    if transform_f is not None:
                        resp_dict=transform_f(dict_object)
                        #we break 'couse we allready ran transform_WLD, and it is dict-wide.
                        break

        for field in DjagiosModel._meta.get_all_field_names():
            #try to get a custom transform
            transform = getattr(DjagiosModel._meta, "transform_"+field, None)
            if transform is not None and field in dict_object.keys():
                #Field transformations get a tuple of k,v pair and return a Transform dict.
                transformed_dict=transform((field,dict_object[field],))
                for each_key in transformed_dict.iteriitems():
                    resp_dict.add_field(transformed_dict[each_key], key=each_key)

            elif field in dict_object.keys():
                #Nullboolean twicking
                if isinstance(DjagiosModel._meta.get_field(field), NullBooleanField):
                    resp_dict.add_field({field:bool(int(dict_object[field]))})

                #ForeignKey & ManyToManyField twicking
                elif isinstance(DjagiosModel._meta.get_field(field), (ForeignKey, ManyToManyField)):
                    rel_cls_name=DjagiosModel._meta.get_field(field).rel.to().__class__.__name__
                    RelCls=getattr(models, rel_cls_name)
                    if isinstance (DjagiosModel._meta.get_field(field), ForeignKey):
                        resp_dict.add_field({field: RelCls.get(dict_object[field])}, key='fk')
                    else:
                        resp_dict.add_field({field:RelCls.get_all(dict_object[field])}, key='m2m')
                    
                #Default assignment
                else:
                    resp_dict.add_field({field:dict_object[field]}) 

        return resp_dict
