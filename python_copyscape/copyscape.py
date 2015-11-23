from __future__ import absolute_import, print_function, unicode_literals
from python_copyscape.errors import *
import requests

URL = "http://www.copyscape.com/api/"


class CopyscapeClient(object):

    def __init__(self, username, key):
        if not username:
            raise CopyscapeUsernameError('A Copyscape username must be supplied.')
        if not key:
            raise CopyscapeKeyError('A Copyscape key must be supplied.')
        self.username = username
        self.key = key
        self.api_url = URL

    # B. Functions for you to use (all accounts)

    def url_search_internet(self, url, full=0):
        return self.url_search(url, full, 'csearch')
    
    def text_search_internet(self, text, encoding, full=0):
        return self.text_search(text, encoding, full, 'csearch')
    
    def check_balance(self):
        return self.call('balance')
    
    
    # C. Functions for you to use (only accounts with private index enabled)
    
    def url_search_private(self, url, full=0):
        return self.url_search(url, full, 'psearch')
    
    def url_search_internet_and_private(self, url, full=0):
        return self.url_search(url, full, 'cpsearch')
    
    def text_search_private(self, text, encoding, full=0):
        return self.text_search(text, encoding, full, 'psearch')
    
    def text_search_internet_and_private(self, text, encoding, full=0):
        return self.text_search(text, encoding, full, 'cpsearch')
    
    def url_add_to_private(self, url, id=None):
        params={}
        params['q']=url
        if id is not None:
            params['i']=id
        
        return self.call('pindexadd', params)
    
    def text_add_to_private(self, text, encoding, title=None, id=None):
        params={}
        params['e']=encoding
        if title is not None:
            params['a']=title
        if id != None:
            params['i']=id
    
        return self.call('pindexadd', params, text)
    
    def delete_from_private(self, handle):
        params={}
        if handle is None:
            params['h'] = ''
        else: 
            params['h'] = handle
        
        return self.call('pindexdel', params)
    
    
    # D. Functions used internally
    
    def url_search(self, url, full=0, operation='csearch'):
        params={}
        params['q'] = url
        params['c'] = str(full)
        
        return self.call(operation, params)
    
    def text_search(self, text, encoding, full=0, operation='csearch'):
        params={}
        params['e']=encoding
        params['c']=str(full)
    
        return self.call(operation, params, text)
    
    def call(self, operation, params={}, postdata=None):
        urlparams={}
        urlparams['u'] = self.username
        urlparams['k'] = self.key
        urlparams['o'] = operation	
        urlparams.update(params)
        
        uri = URL + '?'
    
        request = None

        if isPython2:
            uri += urllib.urlencode(urlparams)
            if postdata is None:
                request = urllib2.Request(uri)
            else:
                request = urllib2.Request(uri, postdata.encode("UTF-8"))
        else:
            uri += urllib.parse.urlencode(urlparams)
            if postdata is None:
                request = urllib.request.Request(uri) 
            else:
                request = urllib.request.Request(uri, postdata.encode("UTF-8"))
        
        try: 
            response = None
            if isPython2:
                response = urllib2.urlopen(request)
            else:
                response = urllib.request.urlopen(request)
            res = response.read()
            return CopyscapeTree.fromstring(res)	
        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])
            
        return None

    @staticmethod
    def copyscape_title_wrap(title):
        return title+":"

    @staticmethod
    def copyscape_node_wrap(element):
        return CopyscapeClient.copyscape_node_recurse(element)

    @staticmethod
    def copyscape_node_recurse(element, depth=0):
        ret = ""
        if element is None:
            return ret
    
        ret += "\t"*depth + " " + element.tag + ": "
        if element.text is not None:
            ret += element.text.strip()
        ret += "\n"
        for child in element:
            ret += CopyscapeClient.copyscape_node_recurse(child, depth+1)
            
        return ret
