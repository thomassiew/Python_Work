#! /usr/bin/env python
#coding=utf-8

import gc
gc.enable()
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import traceback
import path
import time
import bz2
import lxml
import lxml.etree
import base64
import types
import psutil

class autoprop(type):
	def __init__(cls, name, bases, dict):
		super(autoprop, cls).__init__(name, bases, dict)
	def __new__(cls,name, bases, dict):
		sf=super(autoprop, cls).__new__(cls,name, bases, dict)
		ps=set()
		for key in dict.keys():
			if len(key)<5:
				continue
			for x in ["get_","set_","del_"]:
				if key.lower().startswith(x):
					ps.add(key[4:])
					break
		for x in ps:
			fget = getattr(sf, "get_%s" % x, None)
			fset = getattr(sf, "set_%s" % x, None)
			fdel = getattr(sf, "del_%s" % x, None)
			fget, fset, fdel
			setattr(sf,x,property(fget, fset, fdel))
		return sf
	def __getattribute__(self,name):
		return super(autoprop, self).__getattribute__(name)
class functionclass(object):
	'''
	function class wraper for normal funtion
	Foo() => Foo._new_()+Foo.__call__()
	'''
	__metaclass__ = autoprop
	def __init__(self,fname):
		'''
		constructor class
		'''
		self._fname=fname
	def __call__(self,*arg,**kwd):
		args=[]
		for a in arg:
			if isinstance(a,node):
				rt=a._obj
			else:
				rt=a
			args.append(rt)
		kwds={}
		for k,v in kwd.iteritems():
			if isinstance(v,node):
				rt=v._obj
			else:
				rt=v
			kwds[k]=v
		result=self._fname(*args,**kwds)
		result=node.__convert__(result)
		return result
class node(object):
	__metaclass__ = autoprop
	def __init__(self,xmlobj=None,encoding='utf-8',parser=lxml.etree.XMLParser(recover=True)):
		self.__obj=None
		self._filetimestamp=None
		self._file=None
		self._parser=parser
		self._encoding=encoding
		self._xmlobj=xmlobj
		self._types=[ty for ty in dir(types) if not ty.startswith('_')]
		self._cfgfile=None
		self._pidfile=None
	@staticmethod
	def cfgfile(pth=None,ext='.xml'):
		if pth:
			localpath = path.path(pth)
		else:
			localpath = path.path(sys.argv[0])
		tmp=localpath.abspath().stripext() + ext
		if not tmp.exists():
			tmp.write_bytes("""<root>
  <item key="Pid check">True</item>
  <item key="Exit Error">Exit With Error!</item>
  <item key="Exit">Done!</item>
</root>
""")
		result=node(tmp)
		result._cfgfile = tmp
		return result
	def pidfilecheck(self,pth=None,ext='.pid'):
		if pth:
			localpath = path.path(pth)
		else:
			localpath = path.path(sys.argv[0])
		tmp = localpath.abspath().stripext() + ext
		if tmp.exists():
			rpid = tmp.bytes().strip()
			pid='%s'%(os.getpid())
			if pid==rpid:
				result=True
			else:
				if psutil.pid_exists(int(rpid)):
					result=False
				else:
					tmp.write_bytes(pid)
					result=True
		else:
			pid=os.getpid()
			tmp.write_bytes('%s'%(pid))
			result=True
		self._pid=tmp
		return result
	def get_pidfile(self):
		return self._pid
	def set_cfg(self,dt):
		self._cfgfile=dt
	def get_cfg(self):
		return self._cfgfile
	@staticmethod
	def __convert__(obj):
		if isinstance(obj,list):
			rt=map(lambda x: node.__convert__(x),obj)
		elif isinstance(obj,tuple):
			rt=tuple(map(lambda x: node.__convert__(x),obj))
		elif isinstance(obj,set):
			rt=set(map(lambda x: node.__convert__(x),obj))
		elif isinstance(obj,dict):
			rt={}
			for x,y in obj.iteritems():
				rt[x]=node.__convert__(y)
			#if isinstance(obj,tuple):
			#	rt=tuple(rt)
		else:
			try:
				rt=node(obj)
				rt._obj
			except:
				#print sys.exc_info()
				rt=obj
		return rt
	def __getattr__(self,name,default=None):
		if hasattr(self._obj,name):
			result=getattr(self._obj,name,default)
		elif hasattr(self._tree,name):
			result=getattr(self._tree,name,default)
		else:
			try:
				result=self(name)
			except:
				result=getattr(self._obj,name,default)
				#result = getattr(self, name, default)
		#if isinstance(result,node):
		#	return result
		#else:
		#	return node(result)
		if isinstance(result,node):
			return result
		if callable(result):
			result=functionclass(result)
		return result
	def get_value(self):
		return self.text
	def get__obj(self):
		if self.__obj is None:
			if isinstance(self._xmlobj,lxml.etree._ElementTree):
				self.__tree=self._xmlobj
				self.__obj=self.__tree.getroot()
			elif isinstance(self._xmlobj,lxml.etree._Element):
				self.__tree=None
				self.__obj=self._xmlobj
			elif hasattr(self._xmlobj,'read'):
				self.__tree=lxml.etree.parse(self._xmlobj,self._parser)
				self.__obj=self.__tree.getroot()
				self._file=self._xmlobj.name
				self._filetimestamp=path.path(self._xmlobj.name).mtime
			elif isinstance(self._xmlobj,(basestring,types.StringTypes)):
				if os.path.exists(self._xmlobj):
					if self._xmlobj.lower().endswith('.bzx'):
						self.__tree=lxml.etree.parse(bz2.BZ2File(self._xmlobj,'rb'),self._parser)
						self.__obj=self.__tree.getroot()
					else:
						self.__obj=lxml.etree.parse(self._xmlobj,self._parser).getroot()
						self._file=self._xmlobj
						self._filetimestamp = path.path(self._file).mtime
				else:
					try:
						self.__obj=lxml.etree.fromstring(self._xmlobj,self._parser)
						self.__tree=self.__obj.getroottree()
					except:
						#print "Object [", self._xmlobj,"] Type [", type(self._xmlobj),"]"
						#print self._xmlobj
						#print traceback.format_exc()
						raise Exception
			else:
				try:
					if hasattr(self._xmlobj,'__str__'):
						self.__obj=lxml.etree.fromstring(str(self._xmlobj,self._parser))
					else:
						self.__obj=lxml.etree.fromstring(unicode(self._xmlobj,self._parser))
					self.__tree=None
				except:
					#print "Object [", self._xmlobj,"] Type [", type(self._xmlobj),"]"
					raise Exception
		else:
			if self._file:
				timestamp=path.path(self._file).mtime
				if self._filetimestamp<timestamp:
					self._filetimestamp=timestamp
					self.__tree = lxml.etree.parse(self._file, self._parser)
					self.__obj = self.__tree.getroot()
		#if isinstance(self.__obj,lxml.etree._ElementTree):
		#	self.__obj=self.__obj.getroot()
		return self.__obj
	def get__tree(self):
		return self.__obj.getroottree()
	def __dir__(self):
		return dir(self._obj)+self.__dict__.keys()
	def __repr__(self):
		return "[csc{%s%s%s}csc]"%(os.linesep,self,os.linesep)
	def get_dict(self):
		tmp={}
		for x in self('*'):
			#nd=node(x)
			tmp[x.tag]=x
		return tmp
	def get_Xpath(self):
		rt=self.getroottree()
		pt=rt.getpath(self._obj)
		return pt
	def get__path(self):
		grt=self.getroottree()
		pt=grt.getpath(self._obj)
		del grt
		return pt
	def get__parent(self):
		return self.getparent()
	def get__previous(self):
		return self.getprevious()
	def __call__(self,*arg,**kwd):
		tmp=[]
		for a in arg:
			try:
				value=self._obj.xpath(a)
			except:
				print traceback.format_exc()
				xpth=lxml.etree.ETXPath(a)
				value=xpth(self._obj)
			if isinstance(value,(tuple,list)):
				tmp+=map(lambda x: node(x),value)
			else:
				tmp+=[node(value),]
		if not tmp:
			tmp=None
		if len(tmp)==1:
			tmp=tmp[0]
		return tmp
	def get_xml(self):
		return str(self)
	def get_xmls(self):
		if isinstance(self._obj,lxml.etree._Element):
			return lxml.etree.tostring(self._obj,pretty_print=True,xml_declaration=True,encoding=self._encoding)
		else:
			return lxml.etree.tostring(str(self._obj),pretty_print=True,xml_declaration=True,encoding=self._encoding)
	def __str__(self):
		if isinstance(self._obj,lxml.etree._Element):
			return lxml.etree.tostring(self._obj,pretty_print=True,xml_declaration=False,encoding=self._encoding)
		else:
			return lxml.etree.tostring(self._obj,pretty_print=True,xml_declaration=False,encoding=self._encoding)
	def __getslice__(self,i,j):
		return node.__convert__(self._obj[i:j])
	def __getitem__(self,name):
		return node.__convert__(self(name))
	def __mul__(self,name):
		return self.get(name,None)
	def __mod__(self,name):
		return self.get(name,None)
	def __add__(self,b):
		return node.__convert__(lxml.etree.SubElement(self._obj,b))
	def write(self,filen,pretty_print=True,xml_declaration=True,**kwd):
		if not kwd.has_key('encoding'):
			kwd['encoding']=self._encoding
		#try:
		self._tree.write(filen,pretty_print=pretty_print,xml_declaration=xml_declaration,**kwd)
		#except:
		#	self._obj.write(*arg,**kwd)
	def set_attr(self,data):
		if isinstance(data,dict):
			for x,y in data.iteritems():
				self.set(x,y)
		elif isinstance(data,(list,tuple)):
			self.set(data[0],data[1])
		else:
			self.set(data[0],data[1])
	def get_attr(self):
		return self.attrib
	def get_text(self):
		if self.attr.get('encoding'):
			value=base64.decodestring(self._obj.text)
		else:
			value=self._obj.text
		if self.tag in self._types:
			value=getattr(types,self.tag)(value)
		return value
	def __getitem__(self,name):
		if isinstance(name,basestring):
			return self.attrib[name]
		else:
			return self.obj[name]
	def __setitem__(self,name,vars):
		if not isinstance(vars,basestring):
			self.attrib[name]=unicode(vars)
		else:
			self.attrib[name]=vars
	def set_text(self,data):
		try:
			self._obj.text=data
		except:
			value=base64.encodestring(data)
			setattr(self._obj,'text',value)
			self._obj.set('encoding','base64')
	def set_cdata(self,data):
		try:
			self._obj.text=lxml.etree.CDATA(data)
		except:
			value=base64.encodestring(data)
			setattr(self._obj,'text',value)
			self._obj.set('encoding','base64')
if __name__=="__main__":
	#et=lxml.etree.Element('root')
	#print dir(et)
	nd=node('<root><a haha="1">haha<b haha="g">gg</b><c>ff</c></a></root>')
	#nd=node('haha.xml')
	#print nd("/root/a","//b")
	#aa=nd("//a")
	#print aa[0]*"haha"
	#a=aa[0]
	#abc=a+"abc"
	#print abc.xml
	#abc.text="asdasdasdsd"
	#(a+'nm').text='adsdasds'
	#abc.attr={"df":'123456'}
	#print nd.xml
	#print a['nm']
	print nd._obj
	print nd._tree
	print nd.getroot()

