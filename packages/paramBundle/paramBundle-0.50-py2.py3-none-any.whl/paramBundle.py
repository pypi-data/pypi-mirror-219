#!/usr/bin/python
# -*- coding: utf-8 -*-

# ParamBundle - Copyright & Contact Notice
##############################################
# Created by Dominik Niedenzu                #      
# Copyright (C) 2023 Dominik Niedenzu        #
#     All Rights Reserved                    #
#                                            #
#           Contact:                         #
#      pyadaaah@blackward.de                 #         
#      www.blackward.de                      #         
##############################################

# ParamBundle - Version & Modification Notice
#################################################
# Based on ParamBundle Version 0.50             #
# Modified by --- (date: ---)                   #
#################################################

# ParamBundle - License
#######################################################################################################################
# Use and redistribution in source and binary forms, without or with modification,                                    #
# are permitted (free of charge) provided that the following conditions are met (including the disclaimer):           #
#                                                                                                                     #
# 1. Redistributions of source code must retain the above copyright & contact notice and                              #
#    this license text (including the permission notice, this list of conditions and the following disclaimer).       #
#                                                                                                                     #
#    a) If said source code is redistributed unmodified, the belonging file name must be paramBundle.py and           #
#       said file must retain the above version & modification notice too.                                            #
#                                                                                                                     #
#    b) Whereas if said source code is redistributed modified (this includes redistributions of                       #
#       substantial portions of the source code), the belonging file name(s) must be paramBundle_modified*.py         #
#       (where the asterisk stands for an arbitrary intermediate string) and said files                               #
#       must contain the above version & modification notice too - updated with the name(s) of the change             #
#       maker(s) as well as the date(s) of the modification(s).                                                       #
#                                                                                                                     #
# 2. Redistributions in binary form must reproduce the above copyright & contact notice and                           #
#    this license text (including the permission notice, this list of conditions and the following disclaimer).       #
#    They must also reproduce a version & modification notice similar to the one above - in the                       #
#    sense of 1. a) resp. b).                                                                                         #
#                                                                                                                     #
# 3. Neither the name "Dominik Niedenzu", nor the name resp. trademark "Blackward", nor the names of authors resp.    #
#    contributors resp. change makers may be used to endorse or promote products derived from this software without   #
#    specific prior written permission.                                                                               #
#                                                                                                                     #
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO   # 
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.                            #
#                                                                                                                     #
# IN NO EVENT SHALL DOMINIK NIEDENZU OR AUTHORS OR CONTRIBUTORS OR CHANGE MAKERS BE LIABLE FOR ANY CLAIM, ANY         # 
# (DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY OR CONSEQUENTIAL) DAMAGE OR ANY OTHER LIABILITY, WHETHER IN AN    #
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THIS SOFTWARE (OR PARTS OF THIS   #
# SOFTWARE) OR THE USE OR REDISTRIBUTION OR OTHER DEALINGS IN THIS SOFTWARE (OR PARTS OF THIS SOFTWARE).              #
#                                                                                                                     #
# THE USERS RESP. REDISTRIBUTORS OF THIS SOFTWARE (OR PARTS OF THIS SOFTWARE) ARE SOLELY RESPONSIBLE FOR ENSURING     #
# THAT AFOREMENTIONED CONDITIONS ALL ARE MET AND COMPLIANT WITH THE LAW IN THE RESPECTIVE JURISDICTION - BEFORE (!)   #
# THEY USE RESP. REDISTRIBUTE.                                                                                        #
#######################################################################################################################


#ParamBundle version
__version__ = 0.5
def getVersion():
    global __version__
    return __version__


#import from standard library
from argparse         import ArgumentParser as Argparse_ArgumentParser



#parameter dictionary class
class ParamBundle(dict):
      """
          !!!TBD!!!
          
          Have a look at the 'selftest()' and the 'exampleFct(...)' functions
          and their 'doc'-strings for the time being...
      """

      ### internal attributes ###
      _mandatoryParamsD  = None         #dictionary of registered mandatory parameters
      _optionalParamsD   = None         #dictionary of registered optional parameters
      _registeredParamsD = None         #union of 'self._mandatoryParamsD' and 'self._optionalParamsD'.

      #creator
      def __new__(self, *params, **paramDict):
          """ Ensures, that NO parameter is given. """
          
          #ensure, that there no parameters are provided
          assert (len(params) == 0) and (len(paramDict.keys()) == 0), \
                 "Error in ParamBundle.__new__: neither keyword nor positional arguments are allowed!"              

          #call creator of parent
          return dict.__new__(self, *params, **paramDict)


      #constructor
      def __init__(self, *params, **paramDict):
          """ Inits additional INTERNAL attributes. """

          #call constructor of parent
          dict.__init__(self, *params, **paramDict)
          
          #init additional attributes
          dict.__setattr__(self, "_mandatoryParamsD", None)
          dict.__setattr__(self, "_optionalParamsD", None)
          dict.__setattr__(self, "_registeredParamsD", None)


      #just a helper for registerMandatories and registerOptionals
      def _register(self, paramDict, typeS="registerMandatories"):
          """ 
              :param paramDict: dictionary whose keys are names and whose values are types 
              belonging to said names.
              :param typeS: either 'registerMandatories' (when called by 'self.registerMandatories') or 
              'registerOptionals' (when called from 'self.registerOptionals').
              :return: 'None'.
              
              This method is just a helper - it contains the core functionality of the methods 
              'self.registerMandatories' and 'self.registerOptionals' - which are quite similar.
              
              The method:
              
              1) ensures that all values of 'paramDict' are either of type 'type', 'None' or
              a tuple of 'types's.
              
              2) 'self._mandatoryParamsD' or 'self._optionalParamsD' (depending on 'typeS') is set 
              to a copy of 'paramDict'. 'self._registeredParamsD' is updated accordingly too.
          """
          
          ### check parameters ###
          #paramDict
          assert isinstance(paramDict, dict), \
                 "Error in ParamBundle.setRules: parameter 'paramDict' must be of type 'dict' (not %s)!" % type(paramDict)
          #typeS
          assert typeS in ("registerMandatories", "registerOptionals"),                                           \
                 "Error in ParamBundle.setRules: parameter 'typeS' must either be 'registerMandatories' or " \
                 "'registerOptionals' (not %s)!" % typeS
                 
          #paramDict - keys
          assert all([ isinstance(keyS, str) for keyS in paramDict.keys() ]), \
                 "Error in ParamBundle.%s: all keyword arguments must be of type 'str' (not %s)!" \
                                   "" % (typeS, paramDict.keys())
          
          ### paramDict - values ###
          #ensure, that all values of 'paramDict' are either of type 'type', 'None' or a tuple 'type's.
          for value in paramDict.values():
              if (type(value) != type) and (value != None):
                 #value is neither 'type' nor 'None'
                 if (isinstance(value, tuple) != True)                           or \
                    (all([ (type(typee) == type) for typee in value ]) == False)    :
                    #value is either not a 'tuple' or its elements are not all of type 'type' resp. 'None'
                    assert False, "Error in ParamBundle.%s: all keyword argument values must either be " \
                                   "of type 'type', 'None' or tuple of 'type's (not %s)!" % (typeS, paramDict.values())

          #store name <-> type tuples in the form of a dict
          if    isinstance(self._registeredParamsD, dict) == False:
                dict.__setattr__(self, "_registeredParamsD", dict())
               
          if    typeS == "registerMandatories":
                #ensure, that registering is just done once
                assert (isinstance(self._mandatoryParamsD, dict) == False), \
                    "Error in ParamBundle.registerMandatories: this already has been called before (just allowed once)!"
                       
                #register
                dict.__setattr__(self, "_mandatoryParamsD", paramDict.copy())
                self._registeredParamsD.update( self._mandatoryParamsD )
               
          elif  typeS == "registerOptionals":
                #ensure, that registering is just done once
                assert (isinstance(self._optionalParamsD, dict) == False), \
                    "Error in ParamBundle.registerOptionals: this has been called before (just allowed once)!"
                       
                #register
                dict.__setattr__(self, "_optionalParamsD", paramDict.copy())
                self._registeredParamsD.update( self._optionalParamsD )
               
          #return nothing
          return None


      #set mandatory keywords
      def registerMandatories(self, *params, **paramDict):
          """ 
              Registers all keys of 'paramDict' as allowed keys/attributes. 
              
              The belonging values must either be of type 'type', 'None' or a tuple of
              'type's. They determin, which types are allowed for the belonging
              keys/attributes.
              
              Note that registering mandatories is just allowed once!
          """
          
          ### check parameters ###
          #ensure, that there are no positional arguments
          assert len(params) == 0, "Error in ParamBundle.registerMandatories: just keyword arguments are allowed!"
          
          #register mandatories
          self._register(paramDict, typeS="registerMandatories")
          
          #return nothing
          return None


      #set optional keywords
      def registerOptionals(self, *params, **paramDict):
          """ 
              Registers all keys of 'paramDict' as allowed keys/attributes. 
              
              The belonging values must either be of type 'type', 'None' or a tuple
              'type's. They determin, which types are allowed for the belonging
              keys/attributes.
              
              Note that registering optionals is just allowed once!
          """
          
          ### check parameters ###
          #ensure, that there are no positional arguments
          assert len(params) == 0, "Error in ParamBundle.registerOptionals: just keyword arguments are allowed!"
          
          #register optionals
          self._register(paramDict, typeS="registerOptionals")
          
          #return nothing
          return None


      #set attribute
      def __setattr__(self, keyS, value):
          """ 
              Wraps 'dict.__setattr__' so that the parameters 'keyS' and 'value'
              are checked against the registered mandatories / optionals and also 
              sets the belonging item.
          """
          
          #check whether 'keyS' contains a registered key
          assert (isinstance(self._registeredParamsD, dict) and (keyS in self._registeredParamsD.keys())),   \
                 "Error in ParamBundle.__setattr__: parameter 'keyS' contains '%s' - which neither "         \
                 "is a registered mandatory nor optional yet!" % keyS
                                                   
          #check whether 'value' is of the type, registered
          assert (self._registeredParamsD[keyS] == None) or isinstance(value, self._registeredParamsD[keyS]),    \
                 "Error in ParamBundle.__setattr__: parameter 'value' must be of registered type '%s' (not %s)!" \
                 "" % (self._registeredParamsD[keyS], type(value))

          #set attribute always comes with belonging set item
          dict.__setitem__(self, keyS, value)

          #call set attribute of parent
          return dict.__setattr__(self, keyS, value)


      #set item
      def __setitem__(self, keyS, value):
          """ 
              Wraps 'dict.__setitem__' so that the parameters 'keyS' and 'value'
              are checked against the registered mandatories / optionals and also 
              sets the belonging attribute.
          """

          #set item always comes with belonging set attribute - which does the type checking!
          try:
                 self.__setattr__(keyS, value)
                 
          except Exception as ee:
                 assert False, "Error in ParamBundle.__setitem__: %s" % ee

          #call set item of parent
          return dict.__setitem__(self, keyS, value)


      #update
      def update(self, paramDict):
          """
              :param paramDict: a dictionary whose items --whose keys had been registered-- are to be used for updating 'self'.
              :return: None.
              
              Calls the 'update' method of the dictionary 'self' - but just with items, whose keys 
              have been registered before using 'self.registerMandatory' and/or 'self.registerOptional'.
          """
          
          #check parameter 'paramDict'
          assert isinstance(paramDict, dict), "Error in ParamBundle.update: parameter 'paramDict' must be of " \
                                              "type 'dict' (not %s)!" % type(paramDict)
                                              
          #ensure, something already had been registered
          assert isinstance(self._registeredParamsD, dict),                                                     \
                 "Error in ParamBundle.update: either 'self.registerMandatories(...)' or "                      \
                 "'self.registerOptionals(...)' must already have been called before calling 'self.update(...)'!"
                 
          #create dictionary with just the keys which are in both: 'paramDict' and 'self._registeredParamsD'
          intersectD = { key: value for (key, value) in paramDict.items() if key in self._registeredParamsD.keys() }
          
          #ensure, that all values of intersectD have (one of the) the registered type(s)
          assert all([ ((self._registeredParamsD[key] == None) or isinstance(value, self._registeredParamsD[key]))  \
                       for (key,value) in intersectD.items() ]),                                                    \
                 "Error in ParamBundle.update: (some) values of items '%s' have the wrong (not registered) types!"  \
                 "" % intersectD.items()
                 
          #everything seems fine - update
          retVal = dict.update(self, intersectD)
          
          #assign belonging attributes too
          for (keyS, value) in intersectD.items():
              self.__setattr__(keyS, value)
              
          #return
          return retVal


      #is complete
      def isComplete(self):
          """
              :return: returns 'True' if all mandatory parameters (already) have been 
              sucessfully set - e.g. and in particular by using 'self.update(...)';
              'False' otherwise.
          """
          
          return set( self._mandatoryParamsD.keys() ).issubset( set(self.keys()) )


### example function ###
def exampleFct(aaa, bbb, **kwargs):
    """
        :param aaa: just a dummy.
        :param bbb: just a dummy.
        :return: 'None'.
        
        An example function for using 'ParamBundle' to automatically select, 
        check (for completeness and correct types) and bundle keyword arguments
        into an instance of an enhanced dictionary class, which also and in 
        particular mirrors items to attributes and attributes to items 
        automatically.
    """
     
    try:
           ### determine the mandatory as well as the optional parameters and belonging parameter types ###
           ### and extract, check and bundle the belonging parts of 'kwargs' into 'args'.
           args = ParamBundle()
           args.registerMandatories(ccc=int, ddd=float)
           args.registerOptionals(eee=(int,float,type(None)), fff=None)
           args.update( kwargs )
           
           if args.isComplete() == False:
              print (">>>>>>>>>> MANDATORY PARAMETERS INCOMPLETE <<<<<<<<<<")
           
    except Exception as ee:
           print ("Error in exampleFct: function called with wrong arguments (%s)!" % ee)
           print ("")
           print ("")
           return None


    ### print details ###
    print ("mandatories: %s" % args._mandatoryParamsD)
    print ("optionals: %s" % args._optionalParamsD)
    
    #print all (parameter) items of args
    print ("dictionary items:")
    for (key, value) in sorted(args.items()):
        print ("%s <--> %s" % (key, value))
        
    #print all (parameter) attributes of args
    print ("class attributes:")
    for attribute_name in sorted(dir(args)):
        if (attribute_name.startswith("_") == False)                                                    and \
           (attribute_name not in ("registerMandatories", "registerOptionals", "update", "isComplete")) and \
           (attribute_name not in dir(dict))                                                                :
           print ("%s == %s" % (attribute_name, getattr(args, attribute_name)))
    print ("")
    print ("")

    #ensure, that all (parameter) items are equal to all (parameter) attributes
    for keyS in sorted(args.keys()):
        assert args[keyS] == getattr(args, keyS), "Unexpected error!"
          
    #return nothing
    return None


#self test
def selftest():
    """ 
        It is more a manual test yet. !!!TBD!!!.
    """

    #get version
    print ("----- ParamBundle Version %f -----" % getVersion())
    print ("")
    
    ### example calls ###
    print ("exampleFct(111, 222)")
    print ("====================")
    exampleFct(111, 222)
   
    print ("exampleFct(111, 222, ggg=333)")
    print ("=============================")
    exampleFct(111, 222, ggg=333)
   
    print ("exampleFct(111, 222, ccc=333)")
    print ("=============================")
    exampleFct(111, 222, ccc=333)
   
    print ("exampleFct(111, 222, ccc=333.123)")
    print ("=================================")
    exampleFct(111, 222, ccc=333.123)
   
    print ("exampleFct(111, 222, ccc=333, ddd=444)")
    print ("======================================")
    exampleFct(111, 222, ccc=333, ddd=444)
   
    print ("exampleFct(111, 222, ccc=333, ddd=444.123)")
    print ("==========================================")
    exampleFct(111, 222, ccc=333, ddd=444.123)
   
    print ("exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999)")
    print ("===================================================")
    exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999)
   
    print ("exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee=135)")
    print ("============================================================")
    exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee=135)
   
    print ("exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee=135.531)")
    print ("============================================================")
    exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee=135.531)
   
    print ("exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee=None)")
    print ("============================================================")
    exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee=None)
   
    print ("exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee='abc')")
    print ("============================================================")
    exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee='abc')
   
    print ("exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee=135, fff=1122)")
    print ("=======================================================================")
    exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee=135, fff=1122)
   
    print ("exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee=135, fff=1122.33)")
    print ("===========================================================================")
    exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee=135, fff=1122.33)
   
    print ("exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee=135, fff='aabb')")
    print ("===========================================================================")
    exampleFct(111, 222, ccc=333, ddd=444.123, ggg=999, eee=135, fff='aabb')
   
    print ("exampleFct(111, 222, ddd=444.123, ggg=999, eee=135, fff='aabb')")
    print ("===============================================================")
    exampleFct(111, 222, ddd=444.123, ggg=999, eee=135, fff='aabb')
   
    print ("exampleFct(111, 222, ccc=333, ggg=999, eee=135, fff='aabb')")
    print ("===========================================================================")
    exampleFct(111, 222, ccc=333, ggg=999, eee=135, fff='aabb')

    ### achieve 100% code coverage... ###
    wrongRouteB = False
    try:
        args = ParamBundle()
        args.registerMandatories(ccc=111)
        wrongRouteB = True # pragma: no cover

    except Exception as ee:
        assert str(ee).startswith("Error in ParamBundle.registerMandatories: all keyword argument values must either be of type 'type', 'None' or tuple of 'type's"), \
            "Unexpected error!"
    assert wrongRouteB == False, "Unexpected error!"

    args.registerMandatories(ccc=int)
    args["ccc"] = 123456
    assert args.ccc == 123456 == args["ccc"], "Unexpected error!"

    try:
        args[123] = 123
        wrongRouteB = True # pragma: no cover

    except Exception as ee:
        assert str(ee).startswith("Error in ParamBundle.__setitem__: Error in ParamBundle.__setattr__: parameter 'keyS' contains '123' - which neither is a registered mandatory nor optional yet!"), \
            "Unexpected error!"
    assert wrongRouteB == False, "Unexpected error!"



#main
if __name__ == "__main__":
   #parse command line arguments
   argParser = Argparse_ArgumentParser()
   argParser.add_argument("--test", action="store_true", help="Prints out the results of some example calls of the 'exampleFct' for testing purposes.")
   args      = argParser.parse_args()
   
   #run tests if '--test' is given in command line
   if    args.test == True:          
         selftest()

 
 
 
 