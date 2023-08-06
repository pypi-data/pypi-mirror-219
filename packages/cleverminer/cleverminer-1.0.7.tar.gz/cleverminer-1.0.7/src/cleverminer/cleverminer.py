import sys #line:44
import time #line:45
import copy #line:46
from time import strftime #line:48
from time import gmtime #line:49
import pandas as pd #line:51
import numpy #line:52
from pandas .api .types import CategoricalDtype #line:53
import progressbar #line:55
class cleverminer :#line:57
    version_string ="1.0.7"#line:59
    def __init__ (OOOOOO0O0OO0OO000 ,**OOOO00OO000OO00OO ):#line:61
        OOOOOO0O0OO0OO000 ._print_disclaimer ()#line:62
        OOOOOO0O0OO0OO000 .stats ={'total_cnt':0 ,'total_ver':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:71
        OOOOOO0O0OO0OO000 .options ={'max_categories':100 ,'max_rules':None ,'optimizations':True ,'automatic_data_conversions':True ,'progressbar':True ,'keep_df':False }#line:79
        OOOOOO0O0OO0OO000 .df =None #line:80
        OOOOOO0O0OO0OO000 .kwargs =None #line:81
        if len (OOOO00OO000OO00OO )>0 :#line:82
            OOOOOO0O0OO0OO000 .kwargs =OOOO00OO000OO00OO #line:83
        OOOOOO0O0OO0OO000 .verbosity ={}#line:84
        OOOOOO0O0OO0OO000 .verbosity ['debug']=False #line:85
        OOOOOO0O0OO0OO000 .verbosity ['print_rules']=False #line:86
        OOOOOO0O0OO0OO000 .verbosity ['print_hashes']=True #line:87
        OOOOOO0O0OO0OO000 .verbosity ['last_hash_time']=0 #line:88
        OOOOOO0O0OO0OO000 .verbosity ['hint']=False #line:89
        if "opts"in OOOO00OO000OO00OO :#line:90
            OOOOOO0O0OO0OO000 ._set_opts (OOOO00OO000OO00OO .get ("opts"))#line:91
        if "opts"in OOOO00OO000OO00OO :#line:92
            if "verbose"in OOOO00OO000OO00OO .get ('opts'):#line:93
                OO00O00O0OO00000O =OOOO00OO000OO00OO .get ('opts').get ('verbose')#line:94
                if OO00O00O0OO00000O .upper ()=='FULL':#line:95
                    OOOOOO0O0OO0OO000 .verbosity ['debug']=True #line:96
                    OOOOOO0O0OO0OO000 .verbosity ['print_rules']=True #line:97
                    OOOOOO0O0OO0OO000 .verbosity ['print_hashes']=False #line:98
                    OOOOOO0O0OO0OO000 .verbosity ['hint']=True #line:99
                    OOOOOO0O0OO0OO000 .options ['progressbar']=False #line:100
                elif OO00O00O0OO00000O .upper ()=='RULES':#line:101
                    OOOOOO0O0OO0OO000 .verbosity ['debug']=False #line:102
                    OOOOOO0O0OO0OO000 .verbosity ['print_rules']=True #line:103
                    OOOOOO0O0OO0OO000 .verbosity ['print_hashes']=True #line:104
                    OOOOOO0O0OO0OO000 .verbosity ['hint']=True #line:105
                    OOOOOO0O0OO0OO000 .options ['progressbar']=False #line:106
                elif OO00O00O0OO00000O .upper ()=='HINT':#line:107
                    OOOOOO0O0OO0OO000 .verbosity ['debug']=False #line:108
                    OOOOOO0O0OO0OO000 .verbosity ['print_rules']=False #line:109
                    OOOOOO0O0OO0OO000 .verbosity ['print_hashes']=True #line:110
                    OOOOOO0O0OO0OO000 .verbosity ['last_hash_time']=0 #line:111
                    OOOOOO0O0OO0OO000 .verbosity ['hint']=True #line:112
                    OOOOOO0O0OO0OO000 .options ['progressbar']=False #line:113
                elif OO00O00O0OO00000O .upper ()=='DEBUG':#line:114
                    OOOOOO0O0OO0OO000 .verbosity ['debug']=True #line:115
                    OOOOOO0O0OO0OO000 .verbosity ['print_rules']=True #line:116
                    OOOOOO0O0OO0OO000 .verbosity ['print_hashes']=True #line:117
                    OOOOOO0O0OO0OO000 .verbosity ['last_hash_time']=0 #line:118
                    OOOOOO0O0OO0OO000 .verbosity ['hint']=True #line:119
                    OOOOOO0O0OO0OO000 .options ['progressbar']=False #line:120
        OOOOOO0O0OO0OO000 ._is_py310 =sys .version_info [0 ]>=4 or (sys .version_info [0 ]>=3 and sys .version_info [1 ]>=10 )#line:121
        if not (OOOOOO0O0OO0OO000 ._is_py310 ):#line:122
            print ("Warning: Python 3.10+ NOT detected. You should upgrade to Python 3.10 or greater to get better performance")#line:123
        else :#line:124
            if (OOOOOO0O0OO0OO000 .verbosity ['debug']):#line:125
                print ("Python 3.10+ detected.")#line:126
        OOOOOO0O0OO0OO000 ._initialized =False #line:127
        OOOOOO0O0OO0OO000 ._init_data ()#line:128
        OOOOOO0O0OO0OO000 ._init_task ()#line:129
        if len (OOOO00OO000OO00OO )>0 :#line:130
            if "df"in OOOO00OO000OO00OO :#line:131
                OOOOOO0O0OO0OO000 ._prep_data (OOOO00OO000OO00OO .get ("df"))#line:132
            else :#line:133
                print ("Missing dataframe. Cannot initialize.")#line:134
                OOOOOO0O0OO0OO000 ._initialized =False #line:135
                return #line:136
            O00OO000000O000OO =OOOO00OO000OO00OO .get ("proc",None )#line:137
            if not (O00OO000000O000OO ==None ):#line:138
                OOOOOO0O0OO0OO000 ._calculate (**OOOO00OO000OO00OO )#line:139
            else :#line:141
                if OOOOOO0O0OO0OO000 .verbosity ['debug']:#line:142
                    print ("INFO: just initialized")#line:143
                OO00O000OOOO0OO0O ={}#line:144
                O0OOO000OO0O0OO0O ={}#line:145
                O0OOO000OO0O0OO0O ["varname"]=OOOOOO0O0OO0OO000 .data ["varname"]#line:146
                O0OOO000OO0O0OO0O ["catnames"]=OOOOOO0O0OO0OO000 .data ["catnames"]#line:147
                OO00O000OOOO0OO0O ["datalabels"]=O0OOO000OO0O0OO0O #line:148
                OOOOOO0O0OO0OO000 .result =OO00O000OOOO0OO0O #line:149
        OOOOOO0O0OO0OO000 ._initialized =True #line:151
    def _set_opts (O0OOO0OO0OOO00000 ,O0OOOO000O00OOOO0 ):#line:153
        if "no_optimizations"in O0OOOO000O00OOOO0 :#line:154
            O0OOO0OO0OOO00000 .options ['optimizations']=not (O0OOOO000O00OOOO0 ['no_optimizations'])#line:155
            print ("No optimization will be made.")#line:156
        if "disable_progressbar"in O0OOOO000O00OOOO0 :#line:157
            O0OOO0OO0OOO00000 .options ['progressbar']=False #line:158
            print ("Progressbar will not be shown.")#line:159
        if "max_rules"in O0OOOO000O00OOOO0 :#line:160
            O0OOO0OO0OOO00000 .options ['max_rules']=O0OOOO000O00OOOO0 ['max_rules']#line:161
        if "max_categories"in O0OOOO000O00OOOO0 :#line:162
            O0OOO0OO0OOO00000 .options ['max_categories']=O0OOOO000O00OOOO0 ['max_categories']#line:163
            if O0OOO0OO0OOO00000 .verbosity ['debug']==True :#line:164
                print (f"Maximum number of categories set to {O0OOO0OO0OOO00000.options['max_categories']}")#line:165
        if "no_automatic_data_conversions"in O0OOOO000O00OOOO0 :#line:166
            O0OOO0OO0OOO00000 .options ['automatic_data_conversions']=not (O0OOOO000O00OOOO0 ['no_automatic_data_conversions'])#line:167
            print ("No automatic data conversions will be made.")#line:168
        if "keep_df"in O0OOOO000O00OOOO0 :#line:169
            O0OOO0OO0OOO00000 .options ['keep_df']=O0OOOO000O00OOOO0 ['keep_df']#line:170
    def _init_data (O0OO0O0O000OOOO00 ):#line:173
        O0OO0O0O000OOOO00 .data ={}#line:175
        O0OO0O0O000OOOO00 .data ["varname"]=[]#line:176
        O0OO0O0O000OOOO00 .data ["catnames"]=[]#line:177
        O0OO0O0O000OOOO00 .data ["vtypes"]=[]#line:178
        O0OO0O0O000OOOO00 .data ["dm"]=[]#line:179
        O0OO0O0O000OOOO00 .data ["rows_count"]=int (0 )#line:180
        O0OO0O0O000OOOO00 .data ["data_prepared"]=0 #line:181
    def _init_task (OO0O0OO0000O00000 ):#line:183
        if "opts"in OO0O0OO0000O00000 .kwargs :#line:185
            OO0O0OO0000O00000 ._set_opts (OO0O0OO0000O00000 .kwargs .get ("opts"))#line:186
        OO0O0OO0000O00000 .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'trace_cedent_asindata':[],'traces':[],'generated_string':'','rule':{},'filter_value':int (0 )}#line:196
        OO0O0OO0000O00000 .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:200
        OO0O0OO0000O00000 .rulelist =[]#line:201
        OO0O0OO0000O00000 .stats ['total_cnt']=0 #line:203
        OO0O0OO0000O00000 .stats ['total_valid']=0 #line:204
        OO0O0OO0000O00000 .stats ['control_number']=0 #line:205
        OO0O0OO0000O00000 .result ={}#line:206
        OO0O0OO0000O00000 ._opt_base =None #line:207
        OO0O0OO0000O00000 ._opt_relbase =None #line:208
        OO0O0OO0000O00000 ._opt_base1 =None #line:209
        OO0O0OO0000O00000 ._opt_relbase1 =None #line:210
        OO0O0OO0000O00000 ._opt_base2 =None #line:211
        OO0O0OO0000O00000 ._opt_relbase2 =None #line:212
        OO0O0OO000OOO0O00 =None #line:213
        if not (OO0O0OO0000O00000 .kwargs ==None ):#line:214
            OO0O0OO000OOO0O00 =OO0O0OO0000O00000 .kwargs .get ("quantifiers",None )#line:215
            if not (OO0O0OO000OOO0O00 ==None ):#line:216
                for OOOO00O00O0OOOO00 in OO0O0OO000OOO0O00 .keys ():#line:217
                    if OOOO00O00O0OOOO00 .upper ()=='BASE':#line:218
                        OO0O0OO0000O00000 ._opt_base =OO0O0OO000OOO0O00 .get (OOOO00O00O0OOOO00 )#line:219
                    if OOOO00O00O0OOOO00 .upper ()=='RELBASE':#line:220
                        OO0O0OO0000O00000 ._opt_relbase =OO0O0OO000OOO0O00 .get (OOOO00O00O0OOOO00 )#line:221
                    if (OOOO00O00O0OOOO00 .upper ()=='FRSTBASE')|(OOOO00O00O0OOOO00 .upper ()=='BASE1'):#line:222
                        OO0O0OO0000O00000 ._opt_base1 =OO0O0OO000OOO0O00 .get (OOOO00O00O0OOOO00 )#line:223
                    if (OOOO00O00O0OOOO00 .upper ()=='SCNDBASE')|(OOOO00O00O0OOOO00 .upper ()=='BASE2'):#line:224
                        OO0O0OO0000O00000 ._opt_base2 =OO0O0OO000OOO0O00 .get (OOOO00O00O0OOOO00 )#line:225
                    if (OOOO00O00O0OOOO00 .upper ()=='FRSTRELBASE')|(OOOO00O00O0OOOO00 .upper ()=='RELBASE1'):#line:226
                        OO0O0OO0000O00000 ._opt_relbase1 =OO0O0OO000OOO0O00 .get (OOOO00O00O0OOOO00 )#line:227
                    if (OOOO00O00O0OOOO00 .upper ()=='SCNDRELBASE')|(OOOO00O00O0OOOO00 .upper ()=='RELBASE2'):#line:228
                        OO0O0OO0000O00000 ._opt_relbase2 =OO0O0OO000OOO0O00 .get (OOOO00O00O0OOOO00 )#line:229
            else :#line:230
                print ("Warning: no quantifiers found. Optimization will not take place (1)")#line:231
        else :#line:232
            print ("Warning: no quantifiers found. Optimization will not take place (2)")#line:233
    def mine (OO00OO0OOOO000OO0 ,**OOOO0O0OO0O000OOO ):#line:236
        if not (OO00OO0OOOO000OO0 ._initialized ):#line:237
            print ("Class NOT INITIALIZED. Please call constructor with dataframe first")#line:238
            return #line:239
        OO00OO0OOOO000OO0 .kwargs =None #line:240
        if len (OOOO0O0OO0O000OOO )>0 :#line:241
            OO00OO0OOOO000OO0 .kwargs =OOOO0O0OO0O000OOO #line:242
        OO00OO0OOOO000OO0 ._init_task ()#line:243
        if len (OOOO0O0OO0O000OOO )>0 :#line:244
            OO00000O00O000O00 =OOOO0O0OO0O000OOO .get ("proc",None )#line:245
            if not (OO00000O00O000O00 ==None ):#line:246
                OO00OO0OOOO000OO0 ._calc_all (**OOOO0O0OO0O000OOO )#line:247
            else :#line:248
                print ("Rule mining procedure missing")#line:249
    def _get_ver (OOOO0OOOOO00O00O0 ):#line:252
        return OOOO0OOOOO00O00O0 .version_string #line:253
    def _print_disclaimer (O0O0OO00O000O000O ):#line:255
        print (f"Cleverminer version {O0O0OO00O000O000O._get_ver()}.")#line:257
    def _automatic_data_conversions (OOOOOOOO00OO000OO ,O000OOOOO000O0OOO ):#line:263
        print ("Automatically reordering numeric categories ...")#line:264
        for OOO0O0O000OO0O000 in range (len (O000OOOOO000O0OOO .columns )):#line:265
            if OOOOOOOO00OO000OO .verbosity ['debug']:#line:266
                print (f"#{OOO0O0O000OO0O000}: {O000OOOOO000O0OOO.columns[OOO0O0O000OO0O000]} : {O000OOOOO000O0OOO.dtypes[OOO0O0O000OO0O000]}.")#line:267
            try :#line:268
                O000OOOOO000O0OOO [O000OOOOO000O0OOO .columns [OOO0O0O000OO0O000 ]]=O000OOOOO000O0OOO [O000OOOOO000O0OOO .columns [OOO0O0O000OO0O000 ]].astype (str ).astype (float )#line:269
                if OOOOOOOO00OO000OO .verbosity ['debug']:#line:270
                    print (f"CONVERTED TO FLOATS #{OOO0O0O000OO0O000}: {O000OOOOO000O0OOO.columns[OOO0O0O000OO0O000]} : {O000OOOOO000O0OOO.dtypes[OOO0O0O000OO0O000]}.")#line:271
                O00O00O00000OOO00 =pd .unique (O000OOOOO000O0OOO [O000OOOOO000O0OOO .columns [OOO0O0O000OO0O000 ]])#line:272
                OOO0OO00OOO0O0000 =True #line:273
                for OOO00O0O0OOO0O00O in O00O00O00000OOO00 :#line:274
                    if OOO00O0O0OOO0O00O %1 !=0 :#line:275
                        OOO0OO00OOO0O0000 =False #line:276
                if OOO0OO00OOO0O0000 :#line:277
                    O000OOOOO000O0OOO [O000OOOOO000O0OOO .columns [OOO0O0O000OO0O000 ]]=O000OOOOO000O0OOO [O000OOOOO000O0OOO .columns [OOO0O0O000OO0O000 ]].astype (int )#line:278
                    if OOOOOOOO00OO000OO .verbosity ['debug']:#line:279
                        print (f"CONVERTED TO INT #{OOO0O0O000OO0O000}: {O000OOOOO000O0OOO.columns[OOO0O0O000OO0O000]} : {O000OOOOO000O0OOO.dtypes[OOO0O0O000OO0O000]}.")#line:280
                O000O000OOOO0O0OO =pd .unique (O000OOOOO000O0OOO [O000OOOOO000O0OOO .columns [OOO0O0O000OO0O000 ]])#line:281
                O000O00OO0O00O000 =CategoricalDtype (categories =O000O000OOOO0O0OO .sort (),ordered =True )#line:282
                O000OOOOO000O0OOO [O000OOOOO000O0OOO .columns [OOO0O0O000OO0O000 ]]=O000OOOOO000O0OOO [O000OOOOO000O0OOO .columns [OOO0O0O000OO0O000 ]].astype (O000O00OO0O00O000 )#line:283
                if OOOOOOOO00OO000OO .verbosity ['debug']:#line:284
                    print (f"CONVERTED TO CATEGORY #{OOO0O0O000OO0O000}: {O000OOOOO000O0OOO.columns[OOO0O0O000OO0O000]} : {O000OOOOO000O0OOO.dtypes[OOO0O0O000OO0O000]}.")#line:285
            except :#line:287
                if OOOOOOOO00OO000OO .verbosity ['debug']:#line:288
                    print ("...cannot be converted to int")#line:289
        print ("Automatically reordering numeric categories ...done")#line:290
    def _prep_data (O0O0OO0OOOO000OO0 ,OOO0O0000O0O0000O ):#line:292
        print ("Starting data preparation ...")#line:293
        O0O0OO0OOOO000OO0 ._init_data ()#line:294
        O0O0OO0OOOO000OO0 .stats ['start_prep_time']=time .time ()#line:295
        if O0O0OO0OOOO000OO0 .options ['automatic_data_conversions']:#line:296
            O0O0OO0OOOO000OO0 ._automatic_data_conversions (OOO0O0000O0O0000O )#line:297
        O0O0OO0OOOO000OO0 .data ["rows_count"]=OOO0O0000O0O0000O .shape [0 ]#line:298
        for O0OO0000O0O00O0O0 in OOO0O0000O0O0000O .select_dtypes (exclude =['category']).columns :#line:299
            OOO0O0000O0O0000O [O0OO0000O0O00O0O0 ]=OOO0O0000O0O0000O [O0OO0000O0O00O0O0 ].apply (str )#line:300
        try :#line:301
            O0O00O00O00OO0O0O =pd .DataFrame .from_records ([(OO00000O00000OO00 ,OOO0O0000O0O0000O [OO00000O00000OO00 ].nunique ())for OO00000O00000OO00 in OOO0O0000O0O0000O .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:303
        except :#line:304
            print ("Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.")#line:305
            O0OOOOOOOOO000O00 =""#line:306
            try :#line:307
                for O0OO0000O0O00O0O0 in OOO0O0000O0O0000O .columns :#line:308
                    O0OOOOOOOOO000O00 =O0OO0000O0O00O0O0 #line:309
                    print (f"...column {O0OO0000O0O00O0O0} has {int(OOO0O0000O0O0000O[O0OO0000O0O00O0O0].nunique())} values")#line:310
            except :#line:311
                print (f"... detected : column {O0OOOOOOOOO000O00} has unsupported type: {type(OOO0O0000O0O0000O[O0OO0000O0O00O0O0])}.")#line:312
                exit (1 )#line:313
            print (f"Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.")#line:314
            exit (1 )#line:315
        if O0O0OO0OOOO000OO0 .verbosity ['hint']:#line:318
            print ("Quick profile of input data: unique value counts are:")#line:319
            print (O0O00O00O00OO0O0O )#line:320
            for O0OO0000O0O00O0O0 in OOO0O0000O0O0000O .columns :#line:321
                if OOO0O0000O0O0000O [O0OO0000O0O00O0O0 ].nunique ()<O0O0OO0OOOO000OO0 .options ['max_categories']:#line:322
                    OOO0O0000O0O0000O [O0OO0000O0O00O0O0 ]=OOO0O0000O0O0000O [O0OO0000O0O00O0O0 ].astype ('category')#line:323
                else :#line:324
                    print (f"WARNING: attribute {O0OO0000O0O00O0O0} has more than {O0O0OO0OOOO000OO0.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:325
                    del OOO0O0000O0O0000O [O0OO0000O0O00O0O0 ]#line:326
        for O0OO0000O0O00O0O0 in OOO0O0000O0O0000O .columns :#line:328
            if OOO0O0000O0O0000O [O0OO0000O0O00O0O0 ].nunique ()>O0O0OO0OOOO000OO0 .options ['max_categories']:#line:329
                print (f"WARNING: attribute {O0OO0000O0O00O0O0} has more than {O0O0OO0OOOO000OO0.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:330
                del OOO0O0000O0O0000O [O0OO0000O0O00O0O0 ]#line:331
        if O0O0OO0OOOO000OO0 .options ['keep_df']:#line:332
            if O0O0OO0OOOO000OO0 .verbosity ['debug']:#line:333
                print ("Keeping df.")#line:334
            O0O0OO0OOOO000OO0 .df =OOO0O0000O0O0000O #line:335
        print ("Encoding columns into bit-form...")#line:336
        OOO0OOOO000OO0OO0 =0 #line:337
        OO0O0O0O000O0OOOO =0 #line:338
        for OO000O0000OO0000O in OOO0O0000O0O0000O :#line:339
            if O0O0OO0OOOO000OO0 .verbosity ['debug']:#line:341
                print ('Column: '+OO000O0000OO0000O )#line:342
            O0O0OO0OOOO000OO0 .data ["varname"].append (OO000O0000OO0000O )#line:343
            O0OOO0O0OOOOO0OOO =pd .get_dummies (OOO0O0000O0O0000O [OO000O0000OO0000O ])#line:344
            O00OO0OO000O00OOO =0 #line:345
            if (OOO0O0000O0O0000O .dtypes [OO000O0000OO0000O ].name =='category'):#line:346
                O00OO0OO000O00OOO =1 #line:347
            O0O0OO0OOOO000OO0 .data ["vtypes"].append (O00OO0OO000O00OOO )#line:348
            OO0O00OO00OO0O0O0 =0 #line:351
            OOOO0O0OOO0OOO000 =[]#line:352
            O00O0OO00O000O0OO =[]#line:353
            for O000OO0OOO00O000O in O0OOO0O0OOOOO0OOO :#line:355
                if O0O0OO0OOOO000OO0 .verbosity ['debug']:#line:357
                    print ('....category : '+str (O000OO0OOO00O000O )+" @ "+str (time .time ()))#line:358
                OOOO0O0OOO0OOO000 .append (O000OO0OOO00O000O )#line:359
                O00O0O0O000OOO00O =int (0 )#line:360
                O000OOOO00O00000O =O0OOO0O0OOOOO0OOO [O000OO0OOO00O000O ].values #line:361
                O0OOOO0O00O0OOOOO =numpy .packbits (O000OOOO00O00000O ,bitorder ='little')#line:363
                O00O0O0O000OOO00O =int .from_bytes (O0OOOO0O00O0OOOOO ,byteorder ='little')#line:364
                O00O0OO00O000O0OO .append (O00O0O0O000OOO00O )#line:365
                OO0O00OO00OO0O0O0 +=1 #line:383
                OO0O0O0O000O0OOOO +=1 #line:384
            O0O0OO0OOOO000OO0 .data ["catnames"].append (OOOO0O0OOO0OOO000 )#line:386
            O0O0OO0OOOO000OO0 .data ["dm"].append (O00O0OO00O000O0OO )#line:387
        print ("Encoding columns into bit-form...done")#line:389
        if O0O0OO0OOOO000OO0 .verbosity ['hint']:#line:390
            print (f"List of attributes for analysis is: {O0O0OO0OOOO000OO0.data['varname']}")#line:391
            print (f"List of category names for individual attributes is : {O0O0OO0OOOO000OO0.data['catnames']}")#line:392
        if O0O0OO0OOOO000OO0 .verbosity ['debug']:#line:393
            print (f"List of vtypes is (all should be 1) : {O0O0OO0OOOO000OO0.data['vtypes']}")#line:394
        O0O0OO0OOOO000OO0 .data ["data_prepared"]=1 #line:396
        print ("Data preparation finished.")#line:397
        if O0O0OO0OOOO000OO0 .verbosity ['debug']:#line:398
            print ('Number of variables : '+str (len (O0O0OO0OOOO000OO0 .data ["dm"])))#line:399
            print ('Total number of categories in all variables : '+str (OO0O0O0O000O0OOOO ))#line:400
        O0O0OO0OOOO000OO0 .stats ['end_prep_time']=time .time ()#line:401
        if O0O0OO0OOOO000OO0 .verbosity ['debug']:#line:402
            print ('Time needed for data preparation : ',str (O0O0OO0OOOO000OO0 .stats ['end_prep_time']-O0O0OO0OOOO000OO0 .stats ['start_prep_time']))#line:403
    def _bitcount (O0OO000O000OOOO0O ,OOOOO00OO0O0OO000 ):#line:405
        O0OOO0OO00OOOO0O0 =None #line:406
        if (O0OO000O000OOOO0O ._is_py310 ):#line:407
            O0OOO0OO00OOOO0O0 =OOOOO00OO0O0OO000 .bit_count ()#line:408
        else :#line:409
            O0OOO0OO00OOOO0O0 =bin (OOOOO00OO0O0OO000 ).count ("1")#line:410
        return O0OOO0OO00OOOO0O0 #line:411
    def _verifyCF (OOOO00O0O00O0OO00 ,_O00OO0O0O00O0OOOO ):#line:414
        O0O0OOO0OOO0OO0OO =OOOO00O0O00O0OO00 ._bitcount (_O00OO0O0O00O0OOOO )#line:415
        OO00O00OOO00O0000 =[]#line:416
        O0O00OO0OOO000O00 =[]#line:417
        O00OOOOOOOOOOOO00 =0 #line:418
        OOOO0OOO00O0OO000 =0 #line:419
        O0OO0000OOOO0O000 =0 #line:420
        OO000OOO0OOO00O0O =0 #line:421
        O00000OOO0000O0O0 =0 #line:422
        OO00O00OOO0O00O00 =0 #line:423
        O0O0O00OO00O0000O =0 #line:424
        O00O00O00OO00OOO0 =0 #line:425
        OOO00OOO0O000OO0O =0 #line:426
        OOOOOO0O00OOO00OO =None #line:427
        O00O0000O00OO00OO =None #line:428
        O00OOOOOO0O0OO0OO =None #line:429
        if ('min_step_size'in OOOO00O0O00O0OO00 .quantifiers ):#line:430
            OOOOOO0O00OOO00OO =OOOO00O0O00O0OO00 .quantifiers .get ('min_step_size')#line:431
        if ('min_rel_step_size'in OOOO00O0O00O0OO00 .quantifiers ):#line:432
            O00O0000O00OO00OO =OOOO00O0O00O0OO00 .quantifiers .get ('min_rel_step_size')#line:433
            if O00O0000O00OO00OO >=1 and O00O0000O00OO00OO <100 :#line:434
                O00O0000O00OO00OO =O00O0000O00OO00OO /100 #line:435
        OO0O0000000OOO000 =0 #line:436
        OOO0OOOOOOOO00OOO =0 #line:437
        O000000000000O000 =[]#line:438
        if ('aad_weights'in OOOO00O0O00O0OO00 .quantifiers ):#line:439
            OO0O0000000OOO000 =1 #line:440
            OO00OO0OOOO0OOO00 =[]#line:441
            O000000000000O000 =OOOO00O0O00O0OO00 .quantifiers .get ('aad_weights')#line:442
        OO0O0O0000O0OO0OO =OOOO00O0O00O0OO00 .data ["dm"][OOOO00O0O00O0OO00 .data ["varname"].index (OOOO00O0O00O0OO00 .kwargs .get ('target'))]#line:443
        def OOOOOOOOOOO00O0OO (OO0O0000OOOOOOO00 ,O0O0OO0000O00OO00 ):#line:444
            OOO00OO0O000O0OOO =True #line:445
            if (OO0O0000OOOOOOO00 >O0O0OO0000O00OO00 ):#line:446
                if not (OOOOOO0O00OOO00OO is None or OO0O0000OOOOOOO00 >=O0O0OO0000O00OO00 +OOOOOO0O00OOO00OO ):#line:447
                    OOO00OO0O000O0OOO =False #line:448
                if not (O00O0000O00OO00OO is None or OO0O0000OOOOOOO00 >=O0O0OO0000O00OO00 *(1 +O00O0000O00OO00OO )):#line:449
                    OOO00OO0O000O0OOO =False #line:450
            if (OO0O0000OOOOOOO00 <O0O0OO0000O00OO00 ):#line:451
                if not (OOOOOO0O00OOO00OO is None or OO0O0000OOOOOOO00 <=O0O0OO0000O00OO00 -OOOOOO0O00OOO00OO ):#line:452
                    OOO00OO0O000O0OOO =False #line:453
                if not (O00O0000O00OO00OO is None or OO0O0000OOOOOOO00 <=O0O0OO0000O00OO00 *(1 -O00O0000O00OO00OO )):#line:454
                    OOO00OO0O000O0OOO =False #line:455
            return OOO00OO0O000O0OOO #line:456
        for O0OO0O00OO0000OO0 in range (len (OO0O0O0000O0OO0OO )):#line:457
            OOOO0OOO00O0OO000 =O00OOOOOOOOOOOO00 #line:459
            O00OOOOOOOOOOOO00 =OOOO00O0O00O0OO00 ._bitcount (_O00OO0O0O00O0OOOO &OO0O0O0000O0OO0OO [O0OO0O00OO0000OO0 ])#line:460
            OO00O00OOO00O0000 .append (O00OOOOOOOOOOOO00 )#line:461
            if O0OO0O00OO0000OO0 >0 :#line:462
                if (O00OOOOOOOOOOOO00 >OOOO0OOO00O0OO000 ):#line:463
                    if (O0OO0000OOOO0O000 ==1 )and (OOOOOOOOOOO00O0OO (O00OOOOOOOOOOOO00 ,OOOO0OOO00O0OO000 )):#line:464
                        O00O00O00OO00OOO0 +=1 #line:465
                    else :#line:466
                        if OOOOOOOOOOO00O0OO (O00OOOOOOOOOOOO00 ,OOOO0OOO00O0OO000 ):#line:467
                            O00O00O00OO00OOO0 =1 #line:468
                        else :#line:469
                            O00O00O00OO00OOO0 =0 #line:470
                    if O00O00O00OO00OOO0 >OO000OOO0OOO00O0O :#line:471
                        OO000OOO0OOO00O0O =O00O00O00OO00OOO0 #line:472
                    O0OO0000OOOO0O000 =1 #line:473
                    if OOOOOOOOOOO00O0OO (O00OOOOOOOOOOOO00 ,OOOO0OOO00O0OO000 ):#line:474
                        OO00O00OOO0O00O00 +=1 #line:475
                if (O00OOOOOOOOOOOO00 <OOOO0OOO00O0OO000 ):#line:476
                    if (O0OO0000OOOO0O000 ==-1 )and (OOOOOOOOOOO00O0OO (O00OOOOOOOOOOOO00 ,OOOO0OOO00O0OO000 )):#line:477
                        OOO00OOO0O000OO0O +=1 #line:478
                    else :#line:479
                        if OOOOOOOOOOO00O0OO (O00OOOOOOOOOOOO00 ,OOOO0OOO00O0OO000 ):#line:480
                            OOO00OOO0O000OO0O =1 #line:481
                        else :#line:482
                            OOO00OOO0O000OO0O =0 #line:483
                    if OOO00OOO0O000OO0O >O00000OOO0000O0O0 :#line:484
                        O00000OOO0000O0O0 =OOO00OOO0O000OO0O #line:485
                    O0OO0000OOOO0O000 =-1 #line:486
                    if OOOOOOOOOOO00O0OO (O00OOOOOOOOOOOO00 ,OOOO0OOO00O0OO000 ):#line:487
                        O0O0O00OO00O0000O +=1 #line:488
                if (O00OOOOOOOOOOOO00 ==OOOO0OOO00O0OO000 ):#line:489
                    O0OO0000OOOO0O000 =0 #line:490
                    OOO00OOO0O000OO0O =0 #line:491
                    O00O00O00OO00OOO0 =0 #line:492
            if (OO0O0000000OOO000 ):#line:494
                OOO0OO0000O0O0OO0 =OOOO00O0O00O0OO00 ._bitcount (OO0O0O0000O0OO0OO [O0OO0O00OO0000OO0 ])#line:495
                OO00OO0OOOO0OOO00 .append (OOO0OO0000O0O0OO0 )#line:496
        if (OO0O0000000OOO000 &sum (OO00O00OOO00O0000 )>0 ):#line:498
            for O0OO0O00OO0000OO0 in range (len (OO0O0O0000O0OO0OO )):#line:499
                if OO00OO0OOOO0OOO00 [O0OO0O00OO0000OO0 ]>0 :#line:500
                    if OO00O00OOO00O0000 [O0OO0O00OO0000OO0 ]/sum (OO00O00OOO00O0000 )>OO00OO0OOOO0OOO00 [O0OO0O00OO0000OO0 ]/sum (OO00OO0OOOO0OOO00 ):#line:502
                        OOO0OOOOOOOO00OOO +=O000000000000O000 [O0OO0O00OO0000OO0 ]*((OO00O00OOO00O0000 [O0OO0O00OO0000OO0 ]/sum (OO00O00OOO00O0000 ))/(OO00OO0OOOO0OOO00 [O0OO0O00OO0000OO0 ]/sum (OO00OO0OOOO0OOO00 ))-1 )#line:503
        OOO00O0OO0000OO00 =True #line:506
        for O0O0OO0O00OOOOO0O in OOOO00O0O00O0OO00 .quantifiers .keys ():#line:507
            if O0O0OO0O00OOOOO0O .upper ()=='BASE':#line:508
                OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )<=O0O0OOO0OOO0OO0OO )#line:509
            if O0O0OO0O00OOOOO0O .upper ()=='RELBASE':#line:510
                OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )<=O0O0OOO0OOO0OO0OO *1.0 /OOOO00O0O00O0OO00 .data ["rows_count"])#line:511
            if O0O0OO0O00OOOOO0O .upper ()=='S_UP':#line:512
                OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )<=OO000OOO0OOO00O0O )#line:513
            if O0O0OO0O00OOOOO0O .upper ()=='S_DOWN':#line:514
                OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )<=O00000OOO0000O0O0 )#line:515
            if O0O0OO0O00OOOOO0O .upper ()=='S_ANY_UP':#line:516
                OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )<=OO000OOO0OOO00O0O )#line:517
            if O0O0OO0O00OOOOO0O .upper ()=='S_ANY_DOWN':#line:518
                OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )<=O00000OOO0000O0O0 )#line:519
            if O0O0OO0O00OOOOO0O .upper ()=='MAX':#line:520
                OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )<=max (OO00O00OOO00O0000 ))#line:521
            if O0O0OO0O00OOOOO0O .upper ()=='MIN':#line:522
                OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )<=min (OO00O00OOO00O0000 ))#line:523
            if O0O0OO0O00OOOOO0O .upper ()=='RELMAX':#line:524
                if sum (OO00O00OOO00O0000 )>0 :#line:525
                    OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )<=max (OO00O00OOO00O0000 )*1.0 /sum (OO00O00OOO00O0000 ))#line:526
                else :#line:527
                    OOO00O0OO0000OO00 =False #line:528
            if O0O0OO0O00OOOOO0O .upper ()=='RELMAX_LEQ':#line:529
                if sum (OO00O00OOO00O0000 )>0 :#line:530
                    OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )>=max (OO00O00OOO00O0000 )*1.0 /sum (OO00O00OOO00O0000 ))#line:531
                else :#line:532
                    OOO00O0OO0000OO00 =False #line:533
            if O0O0OO0O00OOOOO0O .upper ()=='RELMIN':#line:534
                if sum (OO00O00OOO00O0000 )>0 :#line:535
                    OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )<=min (OO00O00OOO00O0000 )*1.0 /sum (OO00O00OOO00O0000 ))#line:536
                else :#line:537
                    OOO00O0OO0000OO00 =False #line:538
            if O0O0OO0O00OOOOO0O .upper ()=='RELMIN_LEQ':#line:539
                if sum (OO00O00OOO00O0000 )>0 :#line:540
                    OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )>=min (OO00O00OOO00O0000 )*1.0 /sum (OO00O00OOO00O0000 ))#line:541
                else :#line:542
                    OOO00O0OO0000OO00 =False #line:543
            if O0O0OO0O00OOOOO0O .upper ()=='AAD':#line:544
                OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )<=OOO0OOOOOOOO00OOO )#line:545
            if O0O0OO0O00OOOOO0O .upper ()=='RELRANGE_LEQ':#line:547
                OOO0000OO000000OO =OOOO00O0O00O0OO00 .quantifiers .get (O0O0OO0O00OOOOO0O )#line:548
                if OOO0000OO000000OO >=1 and OOO0000OO000000OO <100 :#line:549
                    OOO0000OO000000OO =OOO0000OO000000OO *1.0 /100 #line:550
                OO00OOOO0OOO0000O =min (OO00O00OOO00O0000 )*1.0 /sum (OO00O00OOO00O0000 )#line:551
                O0OO0OO00O00O0O0O =max (OO00O00OOO00O0000 )*1.0 /sum (OO00O00OOO00O0000 )#line:552
                OOO00O0OO0000OO00 =OOO00O0OO0000OO00 and (OOO0000OO000000OO >=O0OO0OO00O00O0O0O -OO00OOOO0OOO0000O )#line:553
        O000O0OO00OO00OOO ={}#line:554
        if OOO00O0OO0000OO00 ==True :#line:555
            OOOO00O0O00O0OO00 .stats ['total_valid']+=1 #line:557
            O000O0OO00OO00OOO ["base"]=O0O0OOO0OOO0OO0OO #line:558
            O000O0OO00OO00OOO ["rel_base"]=O0O0OOO0OOO0OO0OO *1.0 /OOOO00O0O00O0OO00 .data ["rows_count"]#line:559
            O000O0OO00OO00OOO ["s_up"]=OO000OOO0OOO00O0O #line:560
            O000O0OO00OO00OOO ["s_down"]=O00000OOO0000O0O0 #line:561
            O000O0OO00OO00OOO ["s_any_up"]=OO00O00OOO0O00O00 #line:562
            O000O0OO00OO00OOO ["s_any_down"]=O0O0O00OO00O0000O #line:563
            O000O0OO00OO00OOO ["max"]=max (OO00O00OOO00O0000 )#line:564
            O000O0OO00OO00OOO ["min"]=min (OO00O00OOO00O0000 )#line:565
            if sum (OO00O00OOO00O0000 )>0 :#line:568
                O000O0OO00OO00OOO ["rel_max"]=max (OO00O00OOO00O0000 )*1.0 /sum (OO00O00OOO00O0000 )#line:569
                O000O0OO00OO00OOO ["rel_min"]=min (OO00O00OOO00O0000 )*1.0 /sum (OO00O00OOO00O0000 )#line:570
            else :#line:571
                O000O0OO00OO00OOO ["rel_max"]=0 #line:572
                O000O0OO00OO00OOO ["rel_min"]=0 #line:573
            O000O0OO00OO00OOO ["hist"]=OO00O00OOO00O0000 #line:574
            if OO0O0000000OOO000 :#line:575
                O000O0OO00OO00OOO ["aad"]=OOO0OOOOOOOO00OOO #line:576
                O000O0OO00OO00OOO ["hist_full"]=OO00OO0OOOO0OOO00 #line:577
                O000O0OO00OO00OOO ["rel_hist"]=[O0O000O0OOOO0OO0O /sum (OO00O00OOO00O0000 )for O0O000O0OOOO0OO0O in OO00O00OOO00O0000 ]#line:578
                O000O0OO00OO00OOO ["rel_hist_full"]=[O0O0OOO0O000O00OO /sum (OO00OO0OOOO0OOO00 )for O0O0OOO0O000O00OO in OO00OO0OOOO0OOO00 ]#line:579
        return OOO00O0OO0000OO00 ,O000O0OO00OO00OOO #line:581
    def _verifyUIC (OO0OOOOOOO000OOO0 ,_OOO0O00OOO0O00O0O ):#line:583
        O00O0OO00000O0O0O ={}#line:584
        OO0O0OOO0000OOOOO =0 #line:585
        for OOO000OOO0O00O00O in OO0OOOOOOO000OOO0 .task_actinfo ['cedents']:#line:586
            O00O0OO00000O0O0O [OOO000OOO0O00O00O ['cedent_type']]=OOO000OOO0O00O00O ['filter_value']#line:588
            OO0O0OOO0000OOOOO =OO0O0OOO0000OOOOO +1 #line:589
        O00O0O0O0O0000OO0 =OO0OOOOOOO000OOO0 ._bitcount (_OOO0O00OOO0O00O0O )#line:591
        OO0O0O000O00OO00O =[]#line:592
        O00000O0OO0OO0O00 =0 #line:593
        OOOO0O00O00000OOO =0 #line:594
        OO0OO0000OO0OOO0O =0 #line:595
        OO00OO00OOO0O0OO0 =[]#line:596
        O00O0O0OOO0OOOO00 =[]#line:597
        if ('aad_weights'in OO0OOOOOOO000OOO0 .quantifiers ):#line:598
            OO00OO00OOO0O0OO0 =OO0OOOOOOO000OOO0 .quantifiers .get ('aad_weights')#line:599
            OOOO0O00O00000OOO =1 #line:600
        O000O000OO00O0O0O =OO0OOOOOOO000OOO0 .data ["dm"][OO0OOOOOOO000OOO0 .data ["varname"].index (OO0OOOOOOO000OOO0 .kwargs .get ('target'))]#line:601
        for O0000OOOOO0O0O0O0 in range (len (O000O000OO00O0O0O )):#line:602
            OO0000O000000OO0O =O00000O0OO0OO0O00 #line:604
            O00000O0OO0OO0O00 =OO0OOOOOOO000OOO0 ._bitcount (_OOO0O00OOO0O00O0O &O000O000OO00O0O0O [O0000OOOOO0O0O0O0 ])#line:605
            OO0O0O000O00OO00O .append (O00000O0OO0OO0O00 )#line:606
            OOO0OO0OOOOOOO0O0 =OO0OOOOOOO000OOO0 ._bitcount (O00O0OO00000O0O0O ['cond']&O000O000OO00O0O0O [O0000OOOOO0O0O0O0 ])#line:609
            O00O0O0OOO0OOOO00 .append (OOO0OO0OOOOOOO0O0 )#line:610
        if (OOOO0O00O00000OOO &sum (OO0O0O000O00OO00O )>0 ):#line:612
            for O0000OOOOO0O0O0O0 in range (len (O000O000OO00O0O0O )):#line:613
                if O00O0O0OOO0OOOO00 [O0000OOOOO0O0O0O0 ]>0 :#line:614
                    if OO0O0O000O00OO00O [O0000OOOOO0O0O0O0 ]/sum (OO0O0O000O00OO00O )>O00O0O0OOO0OOOO00 [O0000OOOOO0O0O0O0 ]/sum (O00O0O0OOO0OOOO00 ):#line:616
                        OO0OO0000OO0OOO0O +=OO00OO00OOO0O0OO0 [O0000OOOOO0O0O0O0 ]*((OO0O0O000O00OO00O [O0000OOOOO0O0O0O0 ]/sum (OO0O0O000O00OO00O ))/(O00O0O0OOO0OOOO00 [O0000OOOOO0O0O0O0 ]/sum (O00O0O0OOO0OOOO00 ))-1 )#line:617
        O0000OO00O0O0O000 =True #line:620
        for OOOOO00000OOOO0OO in OO0OOOOOOO000OOO0 .quantifiers .keys ():#line:621
            if OOOOO00000OOOO0OO .upper ()=='BASE':#line:622
                O0000OO00O0O0O000 =O0000OO00O0O0O000 and (OO0OOOOOOO000OOO0 .quantifiers .get (OOOOO00000OOOO0OO )<=O00O0O0O0O0000OO0 )#line:623
            if OOOOO00000OOOO0OO .upper ()=='RELBASE':#line:624
                O0000OO00O0O0O000 =O0000OO00O0O0O000 and (OO0OOOOOOO000OOO0 .quantifiers .get (OOOOO00000OOOO0OO )<=O00O0O0O0O0000OO0 *1.0 /OO0OOOOOOO000OOO0 .data ["rows_count"])#line:625
            if OOOOO00000OOOO0OO .upper ()=='AAD_SCORE':#line:626
                O0000OO00O0O0O000 =O0000OO00O0O0O000 and (OO0OOOOOOO000OOO0 .quantifiers .get (OOOOO00000OOOO0OO )<=OO0OO0000OO0OOO0O )#line:627
        OOOO0OOOOOOOOO00O ={}#line:629
        if O0000OO00O0O0O000 ==True :#line:630
            OO0OOOOOOO000OOO0 .stats ['total_valid']+=1 #line:632
            OOOO0OOOOOOOOO00O ["base"]=O00O0O0O0O0000OO0 #line:633
            OOOO0OOOOOOOOO00O ["rel_base"]=O00O0O0O0O0000OO0 *1.0 /OO0OOOOOOO000OOO0 .data ["rows_count"]#line:634
            OOOO0OOOOOOOOO00O ["hist"]=OO0O0O000O00OO00O #line:635
            OOOO0OOOOOOOOO00O ["aad_score"]=OO0OO0000OO0OOO0O #line:637
            OOOO0OOOOOOOOO00O ["hist_cond"]=O00O0O0OOO0OOOO00 #line:638
            OOOO0OOOOOOOOO00O ["rel_hist"]=[O0OO00OO0OOOOOOO0 /sum (OO0O0O000O00OO00O )for O0OO00OO0OOOOOOO0 in OO0O0O000O00OO00O ]#line:639
            OOOO0OOOOOOOOO00O ["rel_hist_cond"]=[O00O0OOO0000O0OO0 /sum (O00O0O0OOO0OOOO00 )for O00O0OOO0000O0OO0 in O00O0O0OOO0OOOO00 ]#line:640
        return O0000OO00O0O0O000 ,OOOO0OOOOOOOOO00O #line:642
    def _verify4ft (OO0O000O00O0OOOO0 ,_O0O0000OO0O00O0O0 ):#line:644
        O0O0OOO0000O0OOO0 ={}#line:645
        O000O0O00OOOOO00O =0 #line:646
        for O00OOO0O0OOO0O000 in OO0O000O00O0OOOO0 .task_actinfo ['cedents']:#line:647
            O0O0OOO0000O0OOO0 [O00OOO0O0OOO0O000 ['cedent_type']]=O00OOO0O0OOO0O000 ['filter_value']#line:649
            O000O0O00OOOOO00O =O000O0O00OOOOO00O +1 #line:650
        O0O0000O0OOO0O0O0 =OO0O000O00O0OOOO0 ._bitcount (O0O0OOO0000O0OOO0 ['ante']&O0O0OOO0000O0OOO0 ['succ']&O0O0OOO0000O0OOO0 ['cond'])#line:652
        OOOO000OOOO0OO0OO =None #line:653
        OOOO000OOOO0OO0OO =0 #line:654
        if O0O0000O0OOO0O0O0 >0 :#line:663
            OOOO000OOOO0OO0OO =OO0O000O00O0OOOO0 ._bitcount (O0O0OOO0000O0OOO0 ['ante']&O0O0OOO0000O0OOO0 ['succ']&O0O0OOO0000O0OOO0 ['cond'])*1.0 /OO0O000O00O0OOOO0 ._bitcount (O0O0OOO0000O0OOO0 ['ante']&O0O0OOO0000O0OOO0 ['cond'])#line:664
        OO000OO0O0O0OO0O0 =1 <<OO0O000O00O0OOOO0 .data ["rows_count"]#line:666
        OOOOOO000000O0OO0 =OO0O000O00O0OOOO0 ._bitcount (O0O0OOO0000O0OOO0 ['ante']&O0O0OOO0000O0OOO0 ['succ']&O0O0OOO0000O0OOO0 ['cond'])#line:667
        OOOOO0OOOO0O0O00O =OO0O000O00O0OOOO0 ._bitcount (O0O0OOO0000O0OOO0 ['ante']&~(OO000OO0O0O0OO0O0 |O0O0OOO0000O0OOO0 ['succ'])&O0O0OOO0000O0OOO0 ['cond'])#line:668
        O00OOO0O0OOO0O000 =OO0O000O00O0OOOO0 ._bitcount (~(OO000OO0O0O0OO0O0 |O0O0OOO0000O0OOO0 ['ante'])&O0O0OOO0000O0OOO0 ['succ']&O0O0OOO0000O0OOO0 ['cond'])#line:669
        OO0O00OO000O0000O =OO0O000O00O0OOOO0 ._bitcount (~(OO000OO0O0O0OO0O0 |O0O0OOO0000O0OOO0 ['ante'])&~(OO000OO0O0O0OO0O0 |O0O0OOO0000O0OOO0 ['succ'])&O0O0OOO0000O0OOO0 ['cond'])#line:670
        OOOOO00O0OO00O000 =0 #line:671
        if (OOOOOO000000O0OO0 +OOOOO0OOOO0O0O00O )*(OOOOOO000000O0OO0 +O00OOO0O0OOO0O000 )>0 :#line:672
            OOOOO00O0OO00O000 =OOOOOO000000O0OO0 *(OOOOOO000000O0OO0 +OOOOO0OOOO0O0O00O +O00OOO0O0OOO0O000 +OO0O00OO000O0000O )/(OOOOOO000000O0OO0 +OOOOO0OOOO0O0O00O )/(OOOOOO000000O0OO0 +O00OOO0O0OOO0O000 )-1 #line:673
        else :#line:674
            OOOOO00O0OO00O000 =None #line:675
        O00O0000000000O00 =0 #line:676
        if (OOOOOO000000O0OO0 +OOOOO0OOOO0O0O00O )*(OOOOOO000000O0OO0 +O00OOO0O0OOO0O000 )>0 :#line:677
            O00O0000000000O00 =1 -OOOOOO000000O0OO0 *(OOOOOO000000O0OO0 +OOOOO0OOOO0O0O00O +O00OOO0O0OOO0O000 +OO0O00OO000O0000O )/(OOOOOO000000O0OO0 +OOOOO0OOOO0O0O00O )/(OOOOOO000000O0OO0 +O00OOO0O0OOO0O000 )#line:678
        else :#line:679
            O00O0000000000O00 =None #line:680
        O00000000O000OOOO =True #line:681
        for O0OOOOO00O00O0000 in OO0O000O00O0OOOO0 .quantifiers .keys ():#line:682
            if O0OOOOO00O00O0000 .upper ()=='BASE':#line:683
                O00000000O000OOOO =O00000000O000OOOO and (OO0O000O00O0OOOO0 .quantifiers .get (O0OOOOO00O00O0000 )<=O0O0000O0OOO0O0O0 )#line:684
            if O0OOOOO00O00O0000 .upper ()=='RELBASE':#line:685
                O00000000O000OOOO =O00000000O000OOOO and (OO0O000O00O0OOOO0 .quantifiers .get (O0OOOOO00O00O0000 )<=O0O0000O0OOO0O0O0 *1.0 /OO0O000O00O0OOOO0 .data ["rows_count"])#line:686
            if (O0OOOOO00O00O0000 .upper ()=='PIM')or (O0OOOOO00O00O0000 .upper ()=='CONF'):#line:687
                O00000000O000OOOO =O00000000O000OOOO and (OO0O000O00O0OOOO0 .quantifiers .get (O0OOOOO00O00O0000 )<=OOOO000OOOO0OO0OO )#line:688
            if O0OOOOO00O00O0000 .upper ()=='AAD':#line:689
                if OOOOO00O0OO00O000 !=None :#line:690
                    O00000000O000OOOO =O00000000O000OOOO and (OO0O000O00O0OOOO0 .quantifiers .get (O0OOOOO00O00O0000 )<=OOOOO00O0OO00O000 )#line:691
                else :#line:692
                    O00000000O000OOOO =False #line:693
            if O0OOOOO00O00O0000 .upper ()=='BAD':#line:694
                if O00O0000000000O00 !=None :#line:695
                    O00000000O000OOOO =O00000000O000OOOO and (OO0O000O00O0OOOO0 .quantifiers .get (O0OOOOO00O00O0000 )<=O00O0000000000O00 )#line:696
                else :#line:697
                    O00000000O000OOOO =False #line:698
            O0OOO0OO0O00O0000 ={}#line:699
        if O00000000O000OOOO ==True :#line:700
            OO0O000O00O0OOOO0 .stats ['total_valid']+=1 #line:702
            O0OOO0OO0O00O0000 ["base"]=O0O0000O0OOO0O0O0 #line:703
            O0OOO0OO0O00O0000 ["rel_base"]=O0O0000O0OOO0O0O0 *1.0 /OO0O000O00O0OOOO0 .data ["rows_count"]#line:704
            O0OOO0OO0O00O0000 ["conf"]=OOOO000OOOO0OO0OO #line:705
            O0OOO0OO0O00O0000 ["aad"]=OOOOO00O0OO00O000 #line:706
            O0OOO0OO0O00O0000 ["bad"]=O00O0000000000O00 #line:707
            O0OOO0OO0O00O0000 ["fourfold"]=[OOOOOO000000O0OO0 ,OOOOO0OOOO0O0O00O ,O00OOO0O0OOO0O000 ,OO0O00OO000O0000O ]#line:708
        return O00000000O000OOOO ,O0OOO0OO0O00O0000 #line:712
    def _verifysd4ft (O00OOOO0O0OOOO00O ,_OO0OOO00O000OO0OO ):#line:714
        O0OO00000000OO00O ={}#line:715
        OO000O0O0O00O0000 =0 #line:716
        for OOO000O0OOO00O0OO in O00OOOO0O0OOOO00O .task_actinfo ['cedents']:#line:717
            O0OO00000000OO00O [OOO000O0OOO00O0OO ['cedent_type']]=OOO000O0OOO00O0OO ['filter_value']#line:719
            OO000O0O0O00O0000 =OO000O0O0O00O0000 +1 #line:720
        OOOO0O0OOOO000OO0 =O00OOOO0O0OOOO00O ._bitcount (O0OO00000000OO00O ['ante']&O0OO00000000OO00O ['succ']&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['frst'])#line:722
        O00OO0O000OOO0O00 =O00OOOO0O0OOOO00O ._bitcount (O0OO00000000OO00O ['ante']&O0OO00000000OO00O ['succ']&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['scnd'])#line:723
        OO00OOO0OO00OOOO0 =None #line:724
        OOO0OO0O0O00OO00O =0 #line:725
        O0OO00O00O0OOO0O0 =0 #line:726
        if OOOO0O0OOOO000OO0 >0 :#line:735
            OOO0OO0O0O00OO00O =O00OOOO0O0OOOO00O ._bitcount (O0OO00000000OO00O ['ante']&O0OO00000000OO00O ['succ']&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['frst'])*1.0 /O00OOOO0O0OOOO00O ._bitcount (O0OO00000000OO00O ['ante']&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['frst'])#line:736
        if O00OO0O000OOO0O00 >0 :#line:737
            O0OO00O00O0OOO0O0 =O00OOOO0O0OOOO00O ._bitcount (O0OO00000000OO00O ['ante']&O0OO00000000OO00O ['succ']&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['scnd'])*1.0 /O00OOOO0O0OOOO00O ._bitcount (O0OO00000000OO00O ['ante']&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['scnd'])#line:738
        OOO00O00O0O0O00OO =1 <<O00OOOO0O0OOOO00O .data ["rows_count"]#line:740
        OO000OOO0OO00OO00 =O00OOOO0O0OOOO00O ._bitcount (O0OO00000000OO00O ['ante']&O0OO00000000OO00O ['succ']&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['frst'])#line:741
        OO0OO0OO000OOOO0O =O00OOOO0O0OOOO00O ._bitcount (O0OO00000000OO00O ['ante']&~(OOO00O00O0O0O00OO |O0OO00000000OO00O ['succ'])&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['frst'])#line:742
        O0OO0OO00O000OO0O =O00OOOO0O0OOOO00O ._bitcount (~(OOO00O00O0O0O00OO |O0OO00000000OO00O ['ante'])&O0OO00000000OO00O ['succ']&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['frst'])#line:743
        OO00O0O000OO000OO =O00OOOO0O0OOOO00O ._bitcount (~(OOO00O00O0O0O00OO |O0OO00000000OO00O ['ante'])&~(OOO00O00O0O0O00OO |O0OO00000000OO00O ['succ'])&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['frst'])#line:744
        O00000OOO00O000O0 =O00OOOO0O0OOOO00O ._bitcount (O0OO00000000OO00O ['ante']&O0OO00000000OO00O ['succ']&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['scnd'])#line:745
        O00O0000000O0OO00 =O00OOOO0O0OOOO00O ._bitcount (O0OO00000000OO00O ['ante']&~(OOO00O00O0O0O00OO |O0OO00000000OO00O ['succ'])&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['scnd'])#line:746
        O0OO0OOO000O0O0OO =O00OOOO0O0OOOO00O ._bitcount (~(OOO00O00O0O0O00OO |O0OO00000000OO00O ['ante'])&O0OO00000000OO00O ['succ']&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['scnd'])#line:747
        O0OOO0OO0OO0OOO0O =O00OOOO0O0OOOO00O ._bitcount (~(OOO00O00O0O0O00OO |O0OO00000000OO00O ['ante'])&~(OOO00O00O0O0O00OO |O0OO00000000OO00O ['succ'])&O0OO00000000OO00O ['cond']&O0OO00000000OO00O ['scnd'])#line:748
        OOOOOO0000OO0OOO0 =True #line:749
        for OO00OO0O0O0OO0OOO in O00OOOO0O0OOOO00O .quantifiers .keys ():#line:750
            if (OO00OO0O0O0OO0OOO .upper ()=='FRSTBASE')|(OO00OO0O0O0OO0OOO .upper ()=='BASE1'):#line:751
                OOOOOO0000OO0OOO0 =OOOOOO0000OO0OOO0 and (O00OOOO0O0OOOO00O .quantifiers .get (OO00OO0O0O0OO0OOO )<=OOOO0O0OOOO000OO0 )#line:752
            if (OO00OO0O0O0OO0OOO .upper ()=='SCNDBASE')|(OO00OO0O0O0OO0OOO .upper ()=='BASE2'):#line:753
                OOOOOO0000OO0OOO0 =OOOOOO0000OO0OOO0 and (O00OOOO0O0OOOO00O .quantifiers .get (OO00OO0O0O0OO0OOO )<=O00OO0O000OOO0O00 )#line:754
            if (OO00OO0O0O0OO0OOO .upper ()=='FRSTRELBASE')|(OO00OO0O0O0OO0OOO .upper ()=='RELBASE1'):#line:755
                OOOOOO0000OO0OOO0 =OOOOOO0000OO0OOO0 and (O00OOOO0O0OOOO00O .quantifiers .get (OO00OO0O0O0OO0OOO )<=OOOO0O0OOOO000OO0 *1.0 /O00OOOO0O0OOOO00O .data ["rows_count"])#line:756
            if (OO00OO0O0O0OO0OOO .upper ()=='SCNDRELBASE')|(OO00OO0O0O0OO0OOO .upper ()=='RELBASE2'):#line:757
                OOOOOO0000OO0OOO0 =OOOOOO0000OO0OOO0 and (O00OOOO0O0OOOO00O .quantifiers .get (OO00OO0O0O0OO0OOO )<=O00OO0O000OOO0O00 *1.0 /O00OOOO0O0OOOO00O .data ["rows_count"])#line:758
            if (OO00OO0O0O0OO0OOO .upper ()=='FRSTPIM')|(OO00OO0O0O0OO0OOO .upper ()=='PIM1')|(OO00OO0O0O0OO0OOO .upper ()=='FRSTCONF')|(OO00OO0O0O0OO0OOO .upper ()=='CONF1'):#line:759
                OOOOOO0000OO0OOO0 =OOOOOO0000OO0OOO0 and (O00OOOO0O0OOOO00O .quantifiers .get (OO00OO0O0O0OO0OOO )<=OOO0OO0O0O00OO00O )#line:760
            if (OO00OO0O0O0OO0OOO .upper ()=='SCNDPIM')|(OO00OO0O0O0OO0OOO .upper ()=='PIM2')|(OO00OO0O0O0OO0OOO .upper ()=='SCNDCONF')|(OO00OO0O0O0OO0OOO .upper ()=='CONF2'):#line:761
                OOOOOO0000OO0OOO0 =OOOOOO0000OO0OOO0 and (O00OOOO0O0OOOO00O .quantifiers .get (OO00OO0O0O0OO0OOO )<=O0OO00O00O0OOO0O0 )#line:762
            if (OO00OO0O0O0OO0OOO .upper ()=='DELTAPIM')|(OO00OO0O0O0OO0OOO .upper ()=='DELTACONF'):#line:763
                OOOOOO0000OO0OOO0 =OOOOOO0000OO0OOO0 and (O00OOOO0O0OOOO00O .quantifiers .get (OO00OO0O0O0OO0OOO )<=OOO0OO0O0O00OO00O -O0OO00O00O0OOO0O0 )#line:764
            if (OO00OO0O0O0OO0OOO .upper ()=='RATIOPIM')|(OO00OO0O0O0OO0OOO .upper ()=='RATIOCONF'):#line:767
                if (O0OO00O00O0OOO0O0 >0 ):#line:768
                    OOOOOO0000OO0OOO0 =OOOOOO0000OO0OOO0 and (O00OOOO0O0OOOO00O .quantifiers .get (OO00OO0O0O0OO0OOO )<=OOO0OO0O0O00OO00O *1.0 /O0OO00O00O0OOO0O0 )#line:769
                else :#line:770
                    OOOOOO0000OO0OOO0 =False #line:771
            if (OO00OO0O0O0OO0OOO .upper ()=='RATIOPIM_LEQ')|(OO00OO0O0O0OO0OOO .upper ()=='RATIOCONF_LEQ'):#line:772
                if (O0OO00O00O0OOO0O0 >0 ):#line:773
                    OOOOOO0000OO0OOO0 =OOOOOO0000OO0OOO0 and (O00OOOO0O0OOOO00O .quantifiers .get (OO00OO0O0O0OO0OOO )>=OOO0OO0O0O00OO00O *1.0 /O0OO00O00O0OOO0O0 )#line:774
                else :#line:775
                    OOOOOO0000OO0OOO0 =False #line:776
        OO0000000O0O00O00 ={}#line:777
        if OOOOOO0000OO0OOO0 ==True :#line:778
            O00OOOO0O0OOOO00O .stats ['total_valid']+=1 #line:780
            OO0000000O0O00O00 ["base1"]=OOOO0O0OOOO000OO0 #line:781
            OO0000000O0O00O00 ["base2"]=O00OO0O000OOO0O00 #line:782
            OO0000000O0O00O00 ["rel_base1"]=OOOO0O0OOOO000OO0 *1.0 /O00OOOO0O0OOOO00O .data ["rows_count"]#line:783
            OO0000000O0O00O00 ["rel_base2"]=O00OO0O000OOO0O00 *1.0 /O00OOOO0O0OOOO00O .data ["rows_count"]#line:784
            OO0000000O0O00O00 ["conf1"]=OOO0OO0O0O00OO00O #line:785
            OO0000000O0O00O00 ["conf2"]=O0OO00O00O0OOO0O0 #line:786
            OO0000000O0O00O00 ["deltaconf"]=OOO0OO0O0O00OO00O -O0OO00O00O0OOO0O0 #line:787
            if (O0OO00O00O0OOO0O0 >0 ):#line:788
                OO0000000O0O00O00 ["ratioconf"]=OOO0OO0O0O00OO00O *1.0 /O0OO00O00O0OOO0O0 #line:789
            else :#line:790
                OO0000000O0O00O00 ["ratioconf"]=None #line:791
            OO0000000O0O00O00 ["fourfold1"]=[OO000OOO0OO00OO00 ,OO0OO0OO000OOOO0O ,O0OO0OO00O000OO0O ,OO00O0O000OO000OO ]#line:792
            OO0000000O0O00O00 ["fourfold2"]=[O00000OOO00O000O0 ,O00O0000000O0OO00 ,O0OO0OOO000O0O0OO ,O0OOO0OO0OO0OOO0O ]#line:793
        return OOOOOO0000OO0OOO0 ,OO0000000O0O00O00 #line:797
    def _verifynewact4ft (O0000OO0O00O00O00 ,_O0O0O000O0OOO0O0O ):#line:799
        OO0O00O00O00OOOO0 ={}#line:800
        for OO00OOOOO0O0000OO in O0000OO0O00O00O00 .task_actinfo ['cedents']:#line:801
            OO0O00O00O00OOOO0 [OO00OOOOO0O0000OO ['cedent_type']]=OO00OOOOO0O0000OO ['filter_value']#line:803
        OO0O0O000OO000000 =O0000OO0O00O00O00 ._bitcount (OO0O00O00O00OOOO0 ['ante']&OO0O00O00O00OOOO0 ['succ']&OO0O00O00O00OOOO0 ['cond'])#line:805
        OO0OOOO0OO0O0OOO0 =O0000OO0O00O00O00 ._bitcount (OO0O00O00O00OOOO0 ['ante']&OO0O00O00O00OOOO0 ['succ']&OO0O00O00O00OOOO0 ['cond']&OO0O00O00O00OOOO0 ['antv']&OO0O00O00O00OOOO0 ['sucv'])#line:806
        O0OOOO0OO0O0OO000 =None #line:807
        OO00OOOOO0OOO0OO0 =0 #line:808
        O0O00OOO00O000OOO =0 #line:809
        if OO0O0O000OO000000 >0 :#line:818
            OO00OOOOO0OOO0OO0 =O0000OO0O00O00O00 ._bitcount (OO0O00O00O00OOOO0 ['ante']&OO0O00O00O00OOOO0 ['succ']&OO0O00O00O00OOOO0 ['cond'])*1.0 /O0000OO0O00O00O00 ._bitcount (OO0O00O00O00OOOO0 ['ante']&OO0O00O00O00OOOO0 ['cond'])#line:819
        if OO0OOOO0OO0O0OOO0 >0 :#line:820
            O0O00OOO00O000OOO =O0000OO0O00O00O00 ._bitcount (OO0O00O00O00OOOO0 ['ante']&OO0O00O00O00OOOO0 ['succ']&OO0O00O00O00OOOO0 ['cond']&OO0O00O00O00OOOO0 ['antv']&OO0O00O00O00OOOO0 ['sucv'])*1.0 /O0000OO0O00O00O00 ._bitcount (OO0O00O00O00OOOO0 ['ante']&OO0O00O00O00OOOO0 ['cond']&OO0O00O00O00OOOO0 ['antv'])#line:822
        OOO00OO0O00000000 =1 <<O0000OO0O00O00O00 .rows_count #line:824
        O000OOOO0O0OO0OO0 =O0000OO0O00O00O00 ._bitcount (OO0O00O00O00OOOO0 ['ante']&OO0O00O00O00OOOO0 ['succ']&OO0O00O00O00OOOO0 ['cond'])#line:825
        OOOO0O0OOOOOOOO0O =O0000OO0O00O00O00 ._bitcount (OO0O00O00O00OOOO0 ['ante']&~(OOO00OO0O00000000 |OO0O00O00O00OOOO0 ['succ'])&OO0O00O00O00OOOO0 ['cond'])#line:826
        O00O0O00O0O00O0O0 =O0000OO0O00O00O00 ._bitcount (~(OOO00OO0O00000000 |OO0O00O00O00OOOO0 ['ante'])&OO0O00O00O00OOOO0 ['succ']&OO0O00O00O00OOOO0 ['cond'])#line:827
        OOO0OO0OO000O0O00 =O0000OO0O00O00O00 ._bitcount (~(OOO00OO0O00000000 |OO0O00O00O00OOOO0 ['ante'])&~(OOO00OO0O00000000 |OO0O00O00O00OOOO0 ['succ'])&OO0O00O00O00OOOO0 ['cond'])#line:828
        O00000OOO0O0OOOO0 =O0000OO0O00O00O00 ._bitcount (OO0O00O00O00OOOO0 ['ante']&OO0O00O00O00OOOO0 ['succ']&OO0O00O00O00OOOO0 ['cond']&OO0O00O00O00OOOO0 ['antv']&OO0O00O00O00OOOO0 ['sucv'])#line:829
        O0OOO00OO0000O0OO =O0000OO0O00O00O00 ._bitcount (OO0O00O00O00OOOO0 ['ante']&~(OOO00OO0O00000000 |(OO0O00O00O00OOOO0 ['succ']&OO0O00O00O00OOOO0 ['sucv']))&OO0O00O00O00OOOO0 ['cond'])#line:830
        OOOO00O0O0O0000O0 =O0000OO0O00O00O00 ._bitcount (~(OOO00OO0O00000000 |(OO0O00O00O00OOOO0 ['ante']&OO0O00O00O00OOOO0 ['antv']))&OO0O00O00O00OOOO0 ['succ']&OO0O00O00O00OOOO0 ['cond']&OO0O00O00O00OOOO0 ['sucv'])#line:831
        OOO00O000OO00OOOO =O0000OO0O00O00O00 ._bitcount (~(OOO00OO0O00000000 |(OO0O00O00O00OOOO0 ['ante']&OO0O00O00O00OOOO0 ['antv']))&~(OOO00OO0O00000000 |(OO0O00O00O00OOOO0 ['succ']&OO0O00O00O00OOOO0 ['sucv']))&OO0O00O00O00OOOO0 ['cond'])#line:832
        OOO0OOO0OO00O0O0O =True #line:833
        for O00O00OOO0000O000 in O0000OO0O00O00O00 .quantifiers .keys ():#line:834
            if (O00O00OOO0000O000 =='PreBase')|(O00O00OOO0000O000 =='Base1'):#line:835
                OOO0OOO0OO00O0O0O =OOO0OOO0OO00O0O0O and (O0000OO0O00O00O00 .quantifiers .get (O00O00OOO0000O000 )<=OO0O0O000OO000000 )#line:836
            if (O00O00OOO0000O000 =='PostBase')|(O00O00OOO0000O000 =='Base2'):#line:837
                OOO0OOO0OO00O0O0O =OOO0OOO0OO00O0O0O and (O0000OO0O00O00O00 .quantifiers .get (O00O00OOO0000O000 )<=OO0OOOO0OO0O0OOO0 )#line:838
            if (O00O00OOO0000O000 =='PreRelBase')|(O00O00OOO0000O000 =='RelBase1'):#line:839
                OOO0OOO0OO00O0O0O =OOO0OOO0OO00O0O0O and (O0000OO0O00O00O00 .quantifiers .get (O00O00OOO0000O000 )<=OO0O0O000OO000000 *1.0 /O0000OO0O00O00O00 .data ["rows_count"])#line:840
            if (O00O00OOO0000O000 =='PostRelBase')|(O00O00OOO0000O000 =='RelBase2'):#line:841
                OOO0OOO0OO00O0O0O =OOO0OOO0OO00O0O0O and (O0000OO0O00O00O00 .quantifiers .get (O00O00OOO0000O000 )<=OO0OOOO0OO0O0OOO0 *1.0 /O0000OO0O00O00O00 .data ["rows_count"])#line:842
            if (O00O00OOO0000O000 =='Prepim')|(O00O00OOO0000O000 =='pim1')|(O00O00OOO0000O000 =='PreConf')|(O00O00OOO0000O000 =='conf1'):#line:843
                OOO0OOO0OO00O0O0O =OOO0OOO0OO00O0O0O and (O0000OO0O00O00O00 .quantifiers .get (O00O00OOO0000O000 )<=OO00OOOOO0OOO0OO0 )#line:844
            if (O00O00OOO0000O000 =='Postpim')|(O00O00OOO0000O000 =='pim2')|(O00O00OOO0000O000 =='PostConf')|(O00O00OOO0000O000 =='conf2'):#line:845
                OOO0OOO0OO00O0O0O =OOO0OOO0OO00O0O0O and (O0000OO0O00O00O00 .quantifiers .get (O00O00OOO0000O000 )<=O0O00OOO00O000OOO )#line:846
            if (O00O00OOO0000O000 =='Deltapim')|(O00O00OOO0000O000 =='DeltaConf'):#line:847
                OOO0OOO0OO00O0O0O =OOO0OOO0OO00O0O0O and (O0000OO0O00O00O00 .quantifiers .get (O00O00OOO0000O000 )<=OO00OOOOO0OOO0OO0 -O0O00OOO00O000OOO )#line:848
            if (O00O00OOO0000O000 =='Ratiopim')|(O00O00OOO0000O000 =='RatioConf'):#line:851
                if (O0O00OOO00O000OOO >0 ):#line:852
                    OOO0OOO0OO00O0O0O =OOO0OOO0OO00O0O0O and (O0000OO0O00O00O00 .quantifiers .get (O00O00OOO0000O000 )<=OO00OOOOO0OOO0OO0 *1.0 /O0O00OOO00O000OOO )#line:853
                else :#line:854
                    OOO0OOO0OO00O0O0O =False #line:855
        OOO000OO00O000OOO ={}#line:856
        if OOO0OOO0OO00O0O0O ==True :#line:857
            O0000OO0O00O00O00 .stats ['total_valid']+=1 #line:859
            OOO000OO00O000OOO ["base1"]=OO0O0O000OO000000 #line:860
            OOO000OO00O000OOO ["base2"]=OO0OOOO0OO0O0OOO0 #line:861
            OOO000OO00O000OOO ["rel_base1"]=OO0O0O000OO000000 *1.0 /O0000OO0O00O00O00 .data ["rows_count"]#line:862
            OOO000OO00O000OOO ["rel_base2"]=OO0OOOO0OO0O0OOO0 *1.0 /O0000OO0O00O00O00 .data ["rows_count"]#line:863
            OOO000OO00O000OOO ["conf1"]=OO00OOOOO0OOO0OO0 #line:864
            OOO000OO00O000OOO ["conf2"]=O0O00OOO00O000OOO #line:865
            OOO000OO00O000OOO ["deltaconf"]=OO00OOOOO0OOO0OO0 -O0O00OOO00O000OOO #line:866
            if (O0O00OOO00O000OOO >0 ):#line:867
                OOO000OO00O000OOO ["ratioconf"]=OO00OOOOO0OOO0OO0 *1.0 /O0O00OOO00O000OOO #line:868
            else :#line:869
                OOO000OO00O000OOO ["ratioconf"]=None #line:870
            OOO000OO00O000OOO ["fourfoldpre"]=[O000OOOO0O0OO0OO0 ,OOOO0O0OOOOOOOO0O ,O00O0O00O0O00O0O0 ,OOO0OO0OO000O0O00 ]#line:871
            OOO000OO00O000OOO ["fourfoldpost"]=[O00000OOO0O0OOOO0 ,O0OOO00OO0000O0OO ,OOOO00O0O0O0000O0 ,OOO00O000OO00OOOO ]#line:872
        return OOO0OOO0OO00O0O0O ,OOO000OO00O000OOO #line:874
    def _verifyact4ft (O00OO0O00000O0O00 ,_OO0OO00O00OO0O00O ):#line:876
        O0O0O00O0O00OOO0O ={}#line:877
        for O0000O0OO0OOOOO0O in O00OO0O00000O0O00 .task_actinfo ['cedents']:#line:878
            O0O0O00O0O00OOO0O [O0000O0OO0OOOOO0O ['cedent_type']]=O0000O0OO0OOOOO0O ['filter_value']#line:880
        OOO0OO00O00O0000O =O00OO0O00000O0O00 ._bitcount (O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['succ']&O0O0O00O0O00OOO0O ['cond']&O0O0O00O0O00OOO0O ['antv-']&O0O0O00O0O00OOO0O ['sucv-'])#line:882
        OO00O0O000OO0O0O0 =O00OO0O00000O0O00 ._bitcount (O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['succ']&O0O0O00O0O00OOO0O ['cond']&O0O0O00O0O00OOO0O ['antv+']&O0O0O00O0O00OOO0O ['sucv+'])#line:883
        O0O00OO0O00O00OO0 =None #line:884
        OOOO0O0O00OO0O00O =0 #line:885
        O0OOO0OO0O0O00O00 =0 #line:886
        if OOO0OO00O00O0000O >0 :#line:895
            OOOO0O0O00OO0O00O =O00OO0O00000O0O00 ._bitcount (O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['succ']&O0O0O00O0O00OOO0O ['cond']&O0O0O00O0O00OOO0O ['antv-']&O0O0O00O0O00OOO0O ['sucv-'])*1.0 /O00OO0O00000O0O00 ._bitcount (O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['cond']&O0O0O00O0O00OOO0O ['antv-'])#line:897
        if OO00O0O000OO0O0O0 >0 :#line:898
            O0OOO0OO0O0O00O00 =O00OO0O00000O0O00 ._bitcount (O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['succ']&O0O0O00O0O00OOO0O ['cond']&O0O0O00O0O00OOO0O ['antv+']&O0O0O00O0O00OOO0O ['sucv+'])*1.0 /O00OO0O00000O0O00 ._bitcount (O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['cond']&O0O0O00O0O00OOO0O ['antv+'])#line:900
        OOOO00O0OO0OO00OO =1 <<O00OO0O00000O0O00 .data ["rows_count"]#line:902
        OO00000OOOO000OO0 =O00OO0O00000O0O00 ._bitcount (O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['succ']&O0O0O00O0O00OOO0O ['cond']&O0O0O00O0O00OOO0O ['antv-']&O0O0O00O0O00OOO0O ['sucv-'])#line:903
        OOO0OOOO0O000OOOO =O00OO0O00000O0O00 ._bitcount (O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['antv-']&~(OOOO00O0OO0OO00OO |(O0O0O00O0O00OOO0O ['succ']&O0O0O00O0O00OOO0O ['sucv-']))&O0O0O00O0O00OOO0O ['cond'])#line:904
        OO000O0OO00OOOOO0 =O00OO0O00000O0O00 ._bitcount (~(OOOO00O0OO0OO00OO |(O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['antv-']))&O0O0O00O0O00OOO0O ['succ']&O0O0O00O0O00OOO0O ['cond']&O0O0O00O0O00OOO0O ['sucv-'])#line:905
        OOOOOO0O0OOO00OO0 =O00OO0O00000O0O00 ._bitcount (~(OOOO00O0OO0OO00OO |(O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['antv-']))&~(OOOO00O0OO0OO00OO |(O0O0O00O0O00OOO0O ['succ']&O0O0O00O0O00OOO0O ['sucv-']))&O0O0O00O0O00OOO0O ['cond'])#line:906
        OO0O0OO0OOOOOO0OO =O00OO0O00000O0O00 ._bitcount (O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['succ']&O0O0O00O0O00OOO0O ['cond']&O0O0O00O0O00OOO0O ['antv+']&O0O0O00O0O00OOO0O ['sucv+'])#line:907
        O0OO00000O0OO000O =O00OO0O00000O0O00 ._bitcount (O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['antv+']&~(OOOO00O0OO0OO00OO |(O0O0O00O0O00OOO0O ['succ']&O0O0O00O0O00OOO0O ['sucv+']))&O0O0O00O0O00OOO0O ['cond'])#line:908
        O0O0O00000O000O00 =O00OO0O00000O0O00 ._bitcount (~(OOOO00O0OO0OO00OO |(O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['antv+']))&O0O0O00O0O00OOO0O ['succ']&O0O0O00O0O00OOO0O ['cond']&O0O0O00O0O00OOO0O ['sucv+'])#line:909
        O0O000OO0O0OO0000 =O00OO0O00000O0O00 ._bitcount (~(OOOO00O0OO0OO00OO |(O0O0O00O0O00OOO0O ['ante']&O0O0O00O0O00OOO0O ['antv+']))&~(OOOO00O0OO0OO00OO |(O0O0O00O0O00OOO0O ['succ']&O0O0O00O0O00OOO0O ['sucv+']))&O0O0O00O0O00OOO0O ['cond'])#line:910
        O000O000000O00000 =True #line:911
        for O00O00OO00OOO0O0O in O00OO0O00000O0O00 .quantifiers .keys ():#line:912
            if (O00O00OO00OOO0O0O =='PreBase')|(O00O00OO00OOO0O0O =='Base1'):#line:913
                O000O000000O00000 =O000O000000O00000 and (O00OO0O00000O0O00 .quantifiers .get (O00O00OO00OOO0O0O )<=OOO0OO00O00O0000O )#line:914
            if (O00O00OO00OOO0O0O =='PostBase')|(O00O00OO00OOO0O0O =='Base2'):#line:915
                O000O000000O00000 =O000O000000O00000 and (O00OO0O00000O0O00 .quantifiers .get (O00O00OO00OOO0O0O )<=OO00O0O000OO0O0O0 )#line:916
            if (O00O00OO00OOO0O0O =='PreRelBase')|(O00O00OO00OOO0O0O =='RelBase1'):#line:917
                O000O000000O00000 =O000O000000O00000 and (O00OO0O00000O0O00 .quantifiers .get (O00O00OO00OOO0O0O )<=OOO0OO00O00O0000O *1.0 /O00OO0O00000O0O00 .data ["rows_count"])#line:918
            if (O00O00OO00OOO0O0O =='PostRelBase')|(O00O00OO00OOO0O0O =='RelBase2'):#line:919
                O000O000000O00000 =O000O000000O00000 and (O00OO0O00000O0O00 .quantifiers .get (O00O00OO00OOO0O0O )<=OO00O0O000OO0O0O0 *1.0 /O00OO0O00000O0O00 .data ["rows_count"])#line:920
            if (O00O00OO00OOO0O0O =='Prepim')|(O00O00OO00OOO0O0O =='pim1')|(O00O00OO00OOO0O0O =='PreConf')|(O00O00OO00OOO0O0O =='conf1'):#line:921
                O000O000000O00000 =O000O000000O00000 and (O00OO0O00000O0O00 .quantifiers .get (O00O00OO00OOO0O0O )<=OOOO0O0O00OO0O00O )#line:922
            if (O00O00OO00OOO0O0O =='Postpim')|(O00O00OO00OOO0O0O =='pim2')|(O00O00OO00OOO0O0O =='PostConf')|(O00O00OO00OOO0O0O =='conf2'):#line:923
                O000O000000O00000 =O000O000000O00000 and (O00OO0O00000O0O00 .quantifiers .get (O00O00OO00OOO0O0O )<=O0OOO0OO0O0O00O00 )#line:924
            if (O00O00OO00OOO0O0O =='Deltapim')|(O00O00OO00OOO0O0O =='DeltaConf'):#line:925
                O000O000000O00000 =O000O000000O00000 and (O00OO0O00000O0O00 .quantifiers .get (O00O00OO00OOO0O0O )<=OOOO0O0O00OO0O00O -O0OOO0OO0O0O00O00 )#line:926
            if (O00O00OO00OOO0O0O =='Ratiopim')|(O00O00OO00OOO0O0O =='RatioConf'):#line:929
                if (OOOO0O0O00OO0O00O >0 ):#line:930
                    O000O000000O00000 =O000O000000O00000 and (O00OO0O00000O0O00 .quantifiers .get (O00O00OO00OOO0O0O )<=O0OOO0OO0O0O00O00 *1.0 /OOOO0O0O00OO0O00O )#line:931
                else :#line:932
                    O000O000000O00000 =False #line:933
        O0OO0O0O0OOO0OO0O ={}#line:934
        if O000O000000O00000 ==True :#line:935
            O00OO0O00000O0O00 .stats ['total_valid']+=1 #line:937
            O0OO0O0O0OOO0OO0O ["base1"]=OOO0OO00O00O0000O #line:938
            O0OO0O0O0OOO0OO0O ["base2"]=OO00O0O000OO0O0O0 #line:939
            O0OO0O0O0OOO0OO0O ["rel_base1"]=OOO0OO00O00O0000O *1.0 /O00OO0O00000O0O00 .data ["rows_count"]#line:940
            O0OO0O0O0OOO0OO0O ["rel_base2"]=OO00O0O000OO0O0O0 *1.0 /O00OO0O00000O0O00 .data ["rows_count"]#line:941
            O0OO0O0O0OOO0OO0O ["conf1"]=OOOO0O0O00OO0O00O #line:942
            O0OO0O0O0OOO0OO0O ["conf2"]=O0OOO0OO0O0O00O00 #line:943
            O0OO0O0O0OOO0OO0O ["deltaconf"]=OOOO0O0O00OO0O00O -O0OOO0OO0O0O00O00 #line:944
            if (OOOO0O0O00OO0O00O >0 ):#line:945
                O0OO0O0O0OOO0OO0O ["ratioconf"]=O0OOO0OO0O0O00O00 *1.0 /OOOO0O0O00OO0O00O #line:946
            else :#line:947
                O0OO0O0O0OOO0OO0O ["ratioconf"]=None #line:948
            O0OO0O0O0OOO0OO0O ["fourfoldpre"]=[OO00000OOOO000OO0 ,OOO0OOOO0O000OOOO ,OO000O0OO00OOOOO0 ,OOOOOO0O0OOO00OO0 ]#line:949
            O0OO0O0O0OOO0OO0O ["fourfoldpost"]=[OO0O0OO0OOOOOO0OO ,O0OO00000O0OO000O ,O0O0O00000O000O00 ,O0O000OO0O0OO0000 ]#line:950
        return O000O000000O00000 ,O0OO0O0O0OOO0OO0O #line:952
    def _verify_opt (O0O0O0OOO0O0OOO00 ,O0O0O0OO0OOO0O0O0 ,O000000O0OO0OOO0O ):#line:954
        O0O0O0OOO0O0OOO00 .stats ['total_ver']+=1 #line:955
        OO0O00000OO0OO0OO =False #line:956
        if not (O0O0O0OO0OOO0O0O0 ['optim'].get ('only_con')):#line:959
            return False #line:960
        if not (O0O0O0OOO0O0OOO00 .options ['optimizations']):#line:963
            return False #line:965
        OO0O000O00OO00O00 ={}#line:967
        for OOO00OOO0OO00000O in O0O0O0OOO0O0OOO00 .task_actinfo ['cedents']:#line:968
            OO0O000O00OO00O00 [OOO00OOO0OO00000O ['cedent_type']]=OOO00OOO0OO00000O ['filter_value']#line:970
        O00O000O0OO0O0O00 =1 <<O0O0O0OOO0O0OOO00 .data ["rows_count"]#line:972
        OO0OOO0O0OOO0OO00 =O00O000O0OO0O0O00 -1 #line:973
        O0000O0O000O0OO00 =""#line:974
        O00OO0O00O0000OOO =0 #line:975
        if (OO0O000O00OO00O00 .get ('ante')!=None ):#line:976
            OO0OOO0O0OOO0OO00 =OO0OOO0O0OOO0OO00 &OO0O000O00OO00O00 ['ante']#line:977
        if (OO0O000O00OO00O00 .get ('succ')!=None ):#line:978
            OO0OOO0O0OOO0OO00 =OO0OOO0O0OOO0OO00 &OO0O000O00OO00O00 ['succ']#line:979
        if (OO0O000O00OO00O00 .get ('cond')!=None ):#line:980
            OO0OOO0O0OOO0OO00 =OO0OOO0O0OOO0OO00 &OO0O000O00OO00O00 ['cond']#line:981
        OOOOOO00000O0O0O0 =None #line:984
        if (O0O0O0OOO0O0OOO00 .proc =='CFMiner')|(O0O0O0OOO0O0OOO00 .proc =='4ftMiner')|(O0O0O0OOO0O0OOO00 .proc =='UICMiner'):#line:1009
            O0O0OOOO00OO00OOO =O0O0O0OOO0O0OOO00 ._bitcount (OO0OOO0O0OOO0OO00 )#line:1010
            if not (O0O0O0OOO0O0OOO00 ._opt_base ==None ):#line:1011
                if not (O0O0O0OOO0O0OOO00 ._opt_base <=O0O0OOOO00OO00OOO ):#line:1012
                    OO0O00000OO0OO0OO =True #line:1013
            if not (O0O0O0OOO0O0OOO00 ._opt_relbase ==None ):#line:1015
                if not (O0O0O0OOO0O0OOO00 ._opt_relbase <=O0O0OOOO00OO00OOO *1.0 /O0O0O0OOO0O0OOO00 .data ["rows_count"]):#line:1016
                    OO0O00000OO0OO0OO =True #line:1017
        if (O0O0O0OOO0O0OOO00 .proc =='SD4ftMiner'):#line:1019
            O0O0OOOO00OO00OOO =O0O0O0OOO0O0OOO00 ._bitcount (OO0OOO0O0OOO0OO00 )#line:1020
            if (not (O0O0O0OOO0O0OOO00 ._opt_base1 ==None ))&(not (O0O0O0OOO0O0OOO00 ._opt_base2 ==None )):#line:1021
                if not (max (O0O0O0OOO0O0OOO00 ._opt_base1 ,O0O0O0OOO0O0OOO00 ._opt_base2 )<=O0O0OOOO00OO00OOO ):#line:1022
                    OO0O00000OO0OO0OO =True #line:1024
            if (not (O0O0O0OOO0O0OOO00 ._opt_relbase1 ==None ))&(not (O0O0O0OOO0O0OOO00 ._opt_relbase2 ==None )):#line:1025
                if not (max (O0O0O0OOO0O0OOO00 ._opt_relbase1 ,O0O0O0OOO0O0OOO00 ._opt_relbase2 )<=O0O0OOOO00OO00OOO *1.0 /O0O0O0OOO0O0OOO00 .data ["rows_count"]):#line:1026
                    OO0O00000OO0OO0OO =True #line:1027
        return OO0O00000OO0OO0OO #line:1029
        if O0O0O0OOO0O0OOO00 .proc =='CFMiner':#line:1032
            if (O000000O0OO0OOO0O ['cedent_type']=='cond')&(O000000O0OO0OOO0O ['defi'].get ('type')=='con'):#line:1033
                O0O0OOOO00OO00OOO =bin (OO0O000O00OO00O00 ['cond']).count ("1")#line:1034
                O0O0OOOO0OOO00O00 =True #line:1035
                for OOO0O00OOOO00OOO0 in O0O0O0OOO0O0OOO00 .quantifiers .keys ():#line:1036
                    if OOO0O00OOOO00OOO0 =='Base':#line:1037
                        O0O0OOOO0OOO00O00 =O0O0OOOO0OOO00O00 and (O0O0O0OOO0O0OOO00 .quantifiers .get (OOO0O00OOOO00OOO0 )<=O0O0OOOO00OO00OOO )#line:1038
                        if not (O0O0OOOO0OOO00O00 ):#line:1039
                            print (f"...optimization : base is {O0O0OOOO00OO00OOO} for {O000000O0OO0OOO0O['generated_string']}")#line:1040
                    if OOO0O00OOOO00OOO0 =='RelBase':#line:1041
                        O0O0OOOO0OOO00O00 =O0O0OOOO0OOO00O00 and (O0O0O0OOO0O0OOO00 .quantifiers .get (OOO0O00OOOO00OOO0 )<=O0O0OOOO00OO00OOO *1.0 /O0O0O0OOO0O0OOO00 .data ["rows_count"])#line:1042
                        if not (O0O0OOOO0OOO00O00 ):#line:1043
                            print (f"...optimization : base is {O0O0OOOO00OO00OOO} for {O000000O0OO0OOO0O['generated_string']}")#line:1044
                OO0O00000OO0OO0OO =not (O0O0OOOO0OOO00O00 )#line:1045
        elif O0O0O0OOO0O0OOO00 .proc =='4ftMiner':#line:1046
            if (O000000O0OO0OOO0O ['cedent_type']=='cond')&(O000000O0OO0OOO0O ['defi'].get ('type')=='con'):#line:1047
                O0O0OOOO00OO00OOO =bin (OO0O000O00OO00O00 ['cond']).count ("1")#line:1048
                O0O0OOOO0OOO00O00 =True #line:1049
                for OOO0O00OOOO00OOO0 in O0O0O0OOO0O0OOO00 .quantifiers .keys ():#line:1050
                    if OOO0O00OOOO00OOO0 =='Base':#line:1051
                        O0O0OOOO0OOO00O00 =O0O0OOOO0OOO00O00 and (O0O0O0OOO0O0OOO00 .quantifiers .get (OOO0O00OOOO00OOO0 )<=O0O0OOOO00OO00OOO )#line:1052
                        if not (O0O0OOOO0OOO00O00 ):#line:1053
                            print (f"...optimization : base is {O0O0OOOO00OO00OOO} for {O000000O0OO0OOO0O['generated_string']}")#line:1054
                    if OOO0O00OOOO00OOO0 =='RelBase':#line:1055
                        O0O0OOOO0OOO00O00 =O0O0OOOO0OOO00O00 and (O0O0O0OOO0O0OOO00 .quantifiers .get (OOO0O00OOOO00OOO0 )<=O0O0OOOO00OO00OOO *1.0 /O0O0O0OOO0O0OOO00 .data ["rows_count"])#line:1056
                        if not (O0O0OOOO0OOO00O00 ):#line:1057
                            print (f"...optimization : base is {O0O0OOOO00OO00OOO} for {O000000O0OO0OOO0O['generated_string']}")#line:1058
                OO0O00000OO0OO0OO =not (O0O0OOOO0OOO00O00 )#line:1059
            if (O000000O0OO0OOO0O ['cedent_type']=='ante')&(O000000O0OO0OOO0O ['defi'].get ('type')=='con'):#line:1060
                O0O0OOOO00OO00OOO =bin (OO0O000O00OO00O00 ['ante']&OO0O000O00OO00O00 ['cond']).count ("1")#line:1061
                O0O0OOOO0OOO00O00 =True #line:1062
                for OOO0O00OOOO00OOO0 in O0O0O0OOO0O0OOO00 .quantifiers .keys ():#line:1063
                    if OOO0O00OOOO00OOO0 =='Base':#line:1064
                        O0O0OOOO0OOO00O00 =O0O0OOOO0OOO00O00 and (O0O0O0OOO0O0OOO00 .quantifiers .get (OOO0O00OOOO00OOO0 )<=O0O0OOOO00OO00OOO )#line:1065
                        if not (O0O0OOOO0OOO00O00 ):#line:1066
                            print (f"...optimization : ANTE: base is {O0O0OOOO00OO00OOO} for {O000000O0OO0OOO0O['generated_string']}")#line:1067
                    if OOO0O00OOOO00OOO0 =='RelBase':#line:1068
                        O0O0OOOO0OOO00O00 =O0O0OOOO0OOO00O00 and (O0O0O0OOO0O0OOO00 .quantifiers .get (OOO0O00OOOO00OOO0 )<=O0O0OOOO00OO00OOO *1.0 /O0O0O0OOO0O0OOO00 .data ["rows_count"])#line:1069
                        if not (O0O0OOOO0OOO00O00 ):#line:1070
                            print (f"...optimization : ANTE:  base is {O0O0OOOO00OO00OOO} for {O000000O0OO0OOO0O['generated_string']}")#line:1071
                OO0O00000OO0OO0OO =not (O0O0OOOO0OOO00O00 )#line:1072
            if (O000000O0OO0OOO0O ['cedent_type']=='succ')&(O000000O0OO0OOO0O ['defi'].get ('type')=='con'):#line:1073
                O0O0OOOO00OO00OOO =bin (OO0O000O00OO00O00 ['ante']&OO0O000O00OO00O00 ['cond']&OO0O000O00OO00O00 ['succ']).count ("1")#line:1074
                OOOOOO00000O0O0O0 =0 #line:1075
                if O0O0OOOO00OO00OOO >0 :#line:1076
                    OOOOOO00000O0O0O0 =bin (OO0O000O00OO00O00 ['ante']&OO0O000O00OO00O00 ['succ']&OO0O000O00OO00O00 ['cond']).count ("1")*1.0 /bin (OO0O000O00OO00O00 ['ante']&OO0O000O00OO00O00 ['cond']).count ("1")#line:1077
                O00O000O0OO0O0O00 =1 <<O0O0O0OOO0O0OOO00 .data ["rows_count"]#line:1078
                OO0O0O000OO0000O0 =bin (OO0O000O00OO00O00 ['ante']&OO0O000O00OO00O00 ['succ']&OO0O000O00OO00O00 ['cond']).count ("1")#line:1079
                O0O00O00OOOO00000 =bin (OO0O000O00OO00O00 ['ante']&~(O00O000O0OO0O0O00 |OO0O000O00OO00O00 ['succ'])&OO0O000O00OO00O00 ['cond']).count ("1")#line:1080
                OOO00OOO0OO00000O =bin (~(O00O000O0OO0O0O00 |OO0O000O00OO00O00 ['ante'])&OO0O000O00OO00O00 ['succ']&OO0O000O00OO00O00 ['cond']).count ("1")#line:1081
                OO0OOO00O000O0O0O =bin (~(O00O000O0OO0O0O00 |OO0O000O00OO00O00 ['ante'])&~(O00O000O0OO0O0O00 |OO0O000O00OO00O00 ['succ'])&OO0O000O00OO00O00 ['cond']).count ("1")#line:1082
                O0O0OOOO0OOO00O00 =True #line:1083
                for OOO0O00OOOO00OOO0 in O0O0O0OOO0O0OOO00 .quantifiers .keys ():#line:1084
                    if OOO0O00OOOO00OOO0 =='pim':#line:1085
                        O0O0OOOO0OOO00O00 =O0O0OOOO0OOO00O00 and (O0O0O0OOO0O0OOO00 .quantifiers .get (OOO0O00OOOO00OOO0 )<=OOOOOO00000O0O0O0 )#line:1086
                    if not (O0O0OOOO0OOO00O00 ):#line:1087
                        print (f"...optimization : SUCC:  pim is {OOOOOO00000O0O0O0} for {O000000O0OO0OOO0O['generated_string']}")#line:1088
                    if OOO0O00OOOO00OOO0 =='aad':#line:1090
                        if (OO0O0O000OO0000O0 +O0O00O00OOOO00000 )*(OO0O0O000OO0000O0 +OOO00OOO0OO00000O )>0 :#line:1091
                            O0O0OOOO0OOO00O00 =O0O0OOOO0OOO00O00 and (O0O0O0OOO0O0OOO00 .quantifiers .get (OOO0O00OOOO00OOO0 )<=OO0O0O000OO0000O0 *(OO0O0O000OO0000O0 +O0O00O00OOOO00000 +OOO00OOO0OO00000O +OO0OOO00O000O0O0O )/(OO0O0O000OO0000O0 +O0O00O00OOOO00000 )/(OO0O0O000OO0000O0 +OOO00OOO0OO00000O )-1 )#line:1092
                        else :#line:1093
                            O0O0OOOO0OOO00O00 =False #line:1094
                        if not (O0O0OOOO0OOO00O00 ):#line:1095
                            OO0O000O0OOOOO0O0 =OO0O0O000OO0000O0 *(OO0O0O000OO0000O0 +O0O00O00OOOO00000 +OOO00OOO0OO00000O +OO0OOO00O000O0O0O )/(OO0O0O000OO0000O0 +O0O00O00OOOO00000 )/(OO0O0O000OO0000O0 +OOO00OOO0OO00000O )-1 #line:1096
                            print (f"...optimization : SUCC:  aad is {OO0O000O0OOOOO0O0} for {O000000O0OO0OOO0O['generated_string']}")#line:1097
                    if OOO0O00OOOO00OOO0 =='bad':#line:1098
                        if (OO0O0O000OO0000O0 +O0O00O00OOOO00000 )*(OO0O0O000OO0000O0 +OOO00OOO0OO00000O )>0 :#line:1099
                            O0O0OOOO0OOO00O00 =O0O0OOOO0OOO00O00 and (O0O0O0OOO0O0OOO00 .quantifiers .get (OOO0O00OOOO00OOO0 )<=1 -OO0O0O000OO0000O0 *(OO0O0O000OO0000O0 +O0O00O00OOOO00000 +OOO00OOO0OO00000O +OO0OOO00O000O0O0O )/(OO0O0O000OO0000O0 +O0O00O00OOOO00000 )/(OO0O0O000OO0000O0 +OOO00OOO0OO00000O ))#line:1100
                        else :#line:1101
                            O0O0OOOO0OOO00O00 =False #line:1102
                        if not (O0O0OOOO0OOO00O00 ):#line:1103
                            OOO0OO000OOOOOO00 =1 -OO0O0O000OO0000O0 *(OO0O0O000OO0000O0 +O0O00O00OOOO00000 +OOO00OOO0OO00000O +OO0OOO00O000O0O0O )/(OO0O0O000OO0000O0 +O0O00O00OOOO00000 )/(OO0O0O000OO0000O0 +OOO00OOO0OO00000O )#line:1104
                            print (f"...optimization : SUCC:  bad is {OOO0OO000OOOOOO00} for {O000000O0OO0OOO0O['generated_string']}")#line:1105
                OO0O00000OO0OO0OO =not (O0O0OOOO0OOO00O00 )#line:1106
        if (OO0O00000OO0OO0OO ):#line:1107
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {O000000O0OO0OOO0O['cedent_type']}")#line:1108
        return OO0O00000OO0OO0OO #line:1109
    def _print (OOO00OO00000OOOO0 ,OO00O0OO000000O00 ,_OOO000000000OO0OO ,_O00O0O00OO000O000 ):#line:1112
        if (len (_OOO000000000OO0OO ))!=len (_O00O0O00OO000O000 ):#line:1113
            print ("DIFF IN LEN for following cedent : "+str (len (_OOO000000000OO0OO ))+" vs "+str (len (_O00O0O00OO000O000 )))#line:1114
            print ("trace cedent : "+str (_OOO000000000OO0OO )+", traces "+str (_O00O0O00OO000O000 ))#line:1115
        O00O000000O0O0000 =''#line:1116
        O0OOOOO000O0O0OO0 ={}#line:1117
        OO0OOO0OO0000O0O0 =[]#line:1118
        for O0OO0OOO0OO0OOO0O in range (len (_OOO000000000OO0OO )):#line:1119
            OO0O0OO0OOOO00OO0 =OOO00OO00000OOOO0 .data ["varname"].index (OO00O0OO000000O00 ['defi'].get ('attributes')[_OOO000000000OO0OO [O0OO0OOO0OO0OOO0O ]].get ('name'))#line:1120
            O00O000000O0O0000 =O00O000000O0O0000 +OOO00OO00000OOOO0 .data ["varname"][OO0O0OO0OOOO00OO0 ]+'('#line:1122
            OO0OOO0OO0000O0O0 .append (OO0O0OO0OOOO00OO0 )#line:1123
            OOO0OOOO0OOOO00O0 =[]#line:1124
            for OOO0O0000O00OOOOO in _O00O0O00OO000O000 [O0OO0OOO0OO0OOO0O ]:#line:1125
                O00O000000O0O0000 =O00O000000O0O0000 +str (OOO00OO00000OOOO0 .data ["catnames"][OO0O0OO0OOOO00OO0 ][OOO0O0000O00OOOOO ])+" "#line:1126
                OOO0OOOO0OOOO00O0 .append (str (OOO00OO00000OOOO0 .data ["catnames"][OO0O0OO0OOOO00OO0 ][OOO0O0000O00OOOOO ]))#line:1127
            O00O000000O0O0000 =O00O000000O0O0000 [:-1 ]+')'#line:1128
            O0OOOOO000O0O0OO0 [OOO00OO00000OOOO0 .data ["varname"][OO0O0OO0OOOO00OO0 ]]=OOO0OOOO0OOOO00O0 #line:1129
            if O0OO0OOO0OO0OOO0O +1 <len (_OOO000000000OO0OO ):#line:1130
                O00O000000O0O0000 =O00O000000O0O0000 +' & '#line:1131
        return O00O000000O0O0000 ,O0OOOOO000O0O0OO0 ,OO0OOO0OO0000O0O0 #line:1135
    def _print_hypo (OOO0O0OO0000OOO0O ,O0OOOO0O00000OOO0 ):#line:1137
        OOO0O0OO0000OOO0O .print_rule (O0OOOO0O00000OOO0 )#line:1138
    def _print_rule (O0000OOO0000O0000 ,OO00O0OO00OOOOO0O ):#line:1140
        if O0000OOO0000O0000 .verbosity ['print_rules']:#line:1141
            print ('Rules info : '+str (OO00O0OO00OOOOO0O ['params']))#line:1142
            for O00000OOO0OO0OOOO in O0000OOO0000O0000 .task_actinfo ['cedents']:#line:1143
                print (O00000OOO0OO0OOOO ['cedent_type']+' = '+O00000OOO0OO0OOOO ['generated_string'])#line:1144
    def _genvar (OO00O000O0000O0OO ,OOOO0000OO0OOOO00 ,O0O0O00OO000OOO00 ,_O0O00OOO0O00O0O0O ,_O00OOOOOO0O00OOO0 ,_OO000O0OO00000000 ,_OOOO0OO00O0O0O00O ,_OO00OOO0O00OOO0OO ,_O0OO0OOOOOO0OO000 ,_O0OOO0O000O0OOOOO ):#line:1146
        _O0OOO0000OOO00O0O =0 #line:1147
        if O0O0O00OO000OOO00 ['num_cedent']>0 :#line:1148
            _O0OOO0000OOO00O0O =(_O0OOO0O000O0OOOOO -_O0OO0OOOOOO0OO000 )/O0O0O00OO000OOO00 ['num_cedent']#line:1149
        for OOOO0O000OO0O0O0O in range (O0O0O00OO000OOO00 ['num_cedent']):#line:1150
            if len (_O0O00OOO0O00O0O0O )==0 or OOOO0O000OO0O0O0O >_O0O00OOO0O00O0O0O [-1 ]:#line:1151
                _O0O00OOO0O00O0O0O .append (OOOO0O000OO0O0O0O )#line:1152
                OO0000OOO000O0OO0 =OO00O000O0000O0OO .data ["varname"].index (O0O0O00OO000OOO00 ['defi'].get ('attributes')[OOOO0O000OO0O0O0O ].get ('name'))#line:1153
                _O00000OO0O0O000O0 =O0O0O00OO000OOO00 ['defi'].get ('attributes')[OOOO0O000OO0O0O0O ].get ('minlen')#line:1154
                _O0OO00000OO00O000 =O0O0O00OO000OOO00 ['defi'].get ('attributes')[OOOO0O000OO0O0O0O ].get ('maxlen')#line:1155
                _OOOO0OO0000OOO000 =O0O0O00OO000OOO00 ['defi'].get ('attributes')[OOOO0O000OO0O0O0O ].get ('type')#line:1156
                O0O000OOOO0O0OO0O =len (OO00O000O0000O0OO .data ["dm"][OO0000OOO000O0OO0 ])#line:1157
                _OOOOO0O0OO00O0000 =[]#line:1158
                _O00OOOOOO0O00OOO0 .append (_OOOOO0O0OO00O0000 )#line:1159
                _OO00OO00OOOO00O0O =int (0 )#line:1160
                OO00O000O0000O0OO ._gencomb (OOOO0000OO0OOOO00 ,O0O0O00OO000OOO00 ,_O0O00OOO0O00O0O0O ,_O00OOOOOO0O00OOO0 ,_OOOOO0O0OO00O0000 ,_OO000O0OO00000000 ,_OO00OO00OOOO00O0O ,O0O000OOOO0O0OO0O ,_OOOO0OO0000OOO000 ,_OOOO0OO00O0O0O00O ,_OO00OOO0O00OOO0OO ,_O00000OO0O0O000O0 ,_O0OO00000OO00O000 ,_O0OO0OOOOOO0OO000 +OOOO0O000OO0O0O0O *_O0OOO0000OOO00O0O ,_O0OO0OOOOOO0OO000 +(OOOO0O000OO0O0O0O +1 )*_O0OOO0000OOO00O0O )#line:1161
                _O00OOOOOO0O00OOO0 .pop ()#line:1162
                _O0O00OOO0O00O0O0O .pop ()#line:1163
    def _gencomb (OOOO00O000OOOO0O0 ,OOO0OOOOO00O00OOO ,OO0OO0000O00OOOOO ,_O0O0OO0OO00O00O0O ,_OO0O0O0O00O00O000 ,_O0OO00OOOOO00O000 ,_O0OO00O0OO0O0O00O ,_OO0OO00O0OOOOO0OO ,OOOO0000OO0O00O00 ,_OO0OOOOO00OO0OOO0 ,_OOOO0O0OOOO00O00O ,_O000OO00O000OO0OO ,_O000O0OO0O0O00OO0 ,_O0OOO000000O0000O ,_O0OOOOO0O00O0OOOO ,_OO00OOO0O00O0OOO0 ):#line:1165
        _OO0O0OO0O00OOOOO0 =[]#line:1166
        if _OO0OOOOO00OO0OOO0 =="subset":#line:1167
            if len (_O0OO00OOOOO00O000 )==0 :#line:1168
                _OO0O0OO0O00OOOOO0 =range (OOOO0000OO0O00O00 )#line:1169
            else :#line:1170
                _OO0O0OO0O00OOOOO0 =range (_O0OO00OOOOO00O000 [-1 ]+1 ,OOOO0000OO0O00O00 )#line:1171
        elif _OO0OOOOO00OO0OOO0 =="seq":#line:1172
            if len (_O0OO00OOOOO00O000 )==0 :#line:1173
                _OO0O0OO0O00OOOOO0 =range (OOOO0000OO0O00O00 -_O000O0OO0O0O00OO0 +1 )#line:1174
            else :#line:1175
                if _O0OO00OOOOO00O000 [-1 ]+1 ==OOOO0000OO0O00O00 :#line:1176
                    return #line:1177
                OOOOOOOOO0O0OO000 =_O0OO00OOOOO00O000 [-1 ]+1 #line:1178
                _OO0O0OO0O00OOOOO0 .append (OOOOOOOOO0O0OO000 )#line:1179
        elif _OO0OOOOO00OO0OOO0 =="lcut":#line:1180
            if len (_O0OO00OOOOO00O000 )==0 :#line:1181
                OOOOOOOOO0O0OO000 =0 ;#line:1182
            else :#line:1183
                if _O0OO00OOOOO00O000 [-1 ]+1 ==OOOO0000OO0O00O00 :#line:1184
                    return #line:1185
                OOOOOOOOO0O0OO000 =_O0OO00OOOOO00O000 [-1 ]+1 #line:1186
            _OO0O0OO0O00OOOOO0 .append (OOOOOOOOO0O0OO000 )#line:1187
        elif _OO0OOOOO00OO0OOO0 =="rcut":#line:1188
            if len (_O0OO00OOOOO00O000 )==0 :#line:1189
                OOOOOOOOO0O0OO000 =OOOO0000OO0O00O00 -1 ;#line:1190
            else :#line:1191
                if _O0OO00OOOOO00O000 [-1 ]==0 :#line:1192
                    return #line:1193
                OOOOOOOOO0O0OO000 =_O0OO00OOOOO00O000 [-1 ]-1 #line:1194
            _OO0O0OO0O00OOOOO0 .append (OOOOOOOOO0O0OO000 )#line:1196
        elif _OO0OOOOO00OO0OOO0 =="one":#line:1197
            if len (_O0OO00OOOOO00O000 )==0 :#line:1198
                OO000O000O0OO0000 =OOOO00O000OOOO0O0 .data ["varname"].index (OO0OO0000O00OOOOO ['defi'].get ('attributes')[_O0O0OO0OO00O00O0O [-1 ]].get ('name'))#line:1199
                try :#line:1200
                    OOOOOOOOO0O0OO000 =OOOO00O000OOOO0O0 .data ["catnames"][OO000O000O0OO0000 ].index (OO0OO0000O00OOOOO ['defi'].get ('attributes')[_O0O0OO0OO00O00O0O [-1 ]].get ('value'))#line:1201
                except :#line:1202
                    print (f"ERROR: attribute '{OO0OO0000O00OOOOO['defi'].get('attributes')[_O0O0OO0OO00O00O0O[-1]].get('name')}' has not value '{OO0OO0000O00OOOOO['defi'].get('attributes')[_O0O0OO0OO00O00O0O[-1]].get('value')}'")#line:1203
                    exit (1 )#line:1204
                _OO0O0OO0O00OOOOO0 .append (OOOOOOOOO0O0OO000 )#line:1205
                _O000O0OO0O0O00OO0 =1 #line:1206
                _O0OOO000000O0000O =1 #line:1207
            else :#line:1208
                print ("DEBUG: one category should not have more categories")#line:1209
                return #line:1210
        else :#line:1211
            print ("Attribute type "+_OO0OOOOO00OO0OOO0 +" not supported.")#line:1212
            return #line:1213
        if len (_OO0O0OO0O00OOOOO0 )>0 :#line:1215
            _OO0OOO00O00O0OO0O =(_OO00OOO0O00O0OOO0 -_O0OOOOO0O00O0OOOO )/len (_OO0O0OO0O00OOOOO0 )#line:1216
        else :#line:1217
            _OO0OOO00O00O0OO0O =0 #line:1218
        _O0OOOOO000O000OOO =0 #line:1220
        for O0O0OO0O00000O000 in _OO0O0OO0O00OOOOO0 :#line:1222
                _O0OO00OOOOO00O000 .append (O0O0OO0O00000O000 )#line:1224
                _OO0O0O0O00O00O000 .pop ()#line:1225
                _OO0O0O0O00O00O000 .append (_O0OO00OOOOO00O000 )#line:1226
                _O0OOO00O0000OO00O =_OO0OO00O0OOOOO0OO |OOOO00O000OOOO0O0 .data ["dm"][OOOO00O000OOOO0O0 .data ["varname"].index (OO0OO0000O00OOOOO ['defi'].get ('attributes')[_O0O0OO0OO00O00O0O [-1 ]].get ('name'))][O0O0OO0O00000O000 ]#line:1230
                _OOO00OO0O00000OO0 =1 #line:1232
                if (len (_O0O0OO0OO00O00O0O )<_OOOO0O0OOOO00O00O ):#line:1233
                    _OOO00OO0O00000OO0 =-1 #line:1234
                if (len (_OO0O0O0O00O00O000 [-1 ])<_O000O0OO0O0O00OO0 ):#line:1236
                    _OOO00OO0O00000OO0 =0 #line:1237
                _OO00OOO00O000000O =0 #line:1239
                if OO0OO0000O00OOOOO ['defi'].get ('type')=='con':#line:1240
                    _OO00OOO00O000000O =_O0OO00O0OO0O0O00O &_O0OOO00O0000OO00O #line:1241
                else :#line:1242
                    _OO00OOO00O000000O =_O0OO00O0OO0O0O00O |_O0OOO00O0000OO00O #line:1243
                OO0OO0000O00OOOOO ['trace_cedent']=_O0O0OO0OO00O00O0O #line:1244
                OO0OO0000O00OOOOO ['traces']=_OO0O0O0O00O00O000 #line:1245
                O00000O00O0OO00O0 ,O000000000OOOO00O ,OO0OO0OOO00OOO0OO =OOOO00O000OOOO0O0 ._print (OO0OO0000O00OOOOO ,_O0O0OO0OO00O00O0O ,_OO0O0O0O00O00O000 )#line:1246
                OO0OO0000O00OOOOO ['generated_string']=O00000O00O0OO00O0 #line:1247
                OO0OO0000O00OOOOO ['rule']=O000000000OOOO00O #line:1248
                OO0OO0000O00OOOOO ['filter_value']=_OO00OOO00O000000O #line:1249
                OO0OO0000O00OOOOO ['traces']=copy .deepcopy (_OO0O0O0O00O00O000 )#line:1250
                OO0OO0000O00OOOOO ['trace_cedent']=copy .deepcopy (_O0O0OO0OO00O00O0O )#line:1251
                OO0OO0000O00OOOOO ['trace_cedent_asindata']=copy .deepcopy (OO0OO0OOO00OOO0OO )#line:1252
                OOO0OOOOO00O00OOO ['cedents'].append (OO0OO0000O00OOOOO )#line:1254
                O0O0O0O00O0000OO0 =OOOO00O000OOOO0O0 ._verify_opt (OOO0OOOOO00O00OOO ,OO0OO0000O00OOOOO )#line:1255
                if not (O0O0O0O00O0000OO0 ):#line:1261
                    if _OOO00OO0O00000OO0 ==1 :#line:1262
                        if len (OOO0OOOOO00O00OOO ['cedents_to_do'])==len (OOO0OOOOO00O00OOO ['cedents']):#line:1264
                            if OOOO00O000OOOO0O0 .proc =='CFMiner':#line:1265
                                OO00O000O0000O00O ,O00OO0O00OOO0O00O =OOOO00O000OOOO0O0 ._verifyCF (_OO00OOO00O000000O )#line:1266
                            elif OOOO00O000OOOO0O0 .proc =='UICMiner':#line:1267
                                OO00O000O0000O00O ,O00OO0O00OOO0O00O =OOOO00O000OOOO0O0 ._verifyUIC (_OO00OOO00O000000O )#line:1268
                            elif OOOO00O000OOOO0O0 .proc =='4ftMiner':#line:1269
                                OO00O000O0000O00O ,O00OO0O00OOO0O00O =OOOO00O000OOOO0O0 ._verify4ft (_O0OOO00O0000OO00O )#line:1270
                            elif OOOO00O000OOOO0O0 .proc =='SD4ftMiner':#line:1271
                                OO00O000O0000O00O ,O00OO0O00OOO0O00O =OOOO00O000OOOO0O0 ._verifysd4ft (_O0OOO00O0000OO00O )#line:1272
                            elif OOOO00O000OOOO0O0 .proc =='NewAct4ftMiner':#line:1273
                                OO00O000O0000O00O ,O00OO0O00OOO0O00O =OOOO00O000OOOO0O0 ._verifynewact4ft (_O0OOO00O0000OO00O )#line:1274
                            elif OOOO00O000OOOO0O0 .proc =='Act4ftMiner':#line:1275
                                OO00O000O0000O00O ,O00OO0O00OOO0O00O =OOOO00O000OOOO0O0 ._verifyact4ft (_O0OOO00O0000OO00O )#line:1276
                            else :#line:1277
                                print ("Unsupported procedure : "+OOOO00O000OOOO0O0 .proc )#line:1278
                                exit (0 )#line:1279
                            if OO00O000O0000O00O ==True :#line:1280
                                O0OOO000OO0O0O000 ={}#line:1281
                                O0OOO000OO0O0O000 ["rule_id"]=OOOO00O000OOOO0O0 .stats ['total_valid']#line:1282
                                O0OOO000OO0O0O000 ["cedents_str"]={}#line:1283
                                O0OOO000OO0O0O000 ["cedents_struct"]={}#line:1284
                                O0OOO000OO0O0O000 ['traces']={}#line:1285
                                O0OOO000OO0O0O000 ['trace_cedent_taskorder']={}#line:1286
                                O0OOO000OO0O0O000 ['trace_cedent_dataorder']={}#line:1287
                                for O00O00OOO0000O0O0 in OOO0OOOOO00O00OOO ['cedents']:#line:1288
                                    O0OOO000OO0O0O000 ['cedents_str'][O00O00OOO0000O0O0 ['cedent_type']]=O00O00OOO0000O0O0 ['generated_string']#line:1290
                                    O0OOO000OO0O0O000 ['cedents_struct'][O00O00OOO0000O0O0 ['cedent_type']]=O00O00OOO0000O0O0 ['rule']#line:1291
                                    O0OOO000OO0O0O000 ['traces'][O00O00OOO0000O0O0 ['cedent_type']]=O00O00OOO0000O0O0 ['traces']#line:1292
                                    O0OOO000OO0O0O000 ['trace_cedent_taskorder'][O00O00OOO0000O0O0 ['cedent_type']]=O00O00OOO0000O0O0 ['trace_cedent']#line:1293
                                    O0OOO000OO0O0O000 ['trace_cedent_dataorder'][O00O00OOO0000O0O0 ['cedent_type']]=O00O00OOO0000O0O0 ['trace_cedent_asindata']#line:1294
                                O0OOO000OO0O0O000 ["params"]=O00OO0O00OOO0O00O #line:1296
                                OOOO00O000OOOO0O0 ._print_rule (O0OOO000OO0O0O000 )#line:1298
                                OOOO00O000OOOO0O0 .rulelist .append (O0OOO000OO0O0O000 )#line:1304
                            OOOO00O000OOOO0O0 .stats ['total_cnt']+=1 #line:1306
                            OOOO00O000OOOO0O0 .stats ['total_ver']+=1 #line:1307
                    if _OOO00OO0O00000OO0 >=0 :#line:1308
                        if len (OOO0OOOOO00O00OOO ['cedents_to_do'])>len (OOO0OOOOO00O00OOO ['cedents']):#line:1309
                            OOOO00O000OOOO0O0 ._start_cedent (OOO0OOOOO00O00OOO ,_O0OOOOO0O00O0OOOO +_O0OOOOO000O000OOO *_OO0OOO00O00O0OO0O ,_O0OOOOO0O00O0OOOO +(_O0OOOOO000O000OOO +0.33 )*_OO0OOO00O00O0OO0O )#line:1310
                    OOO0OOOOO00O00OOO ['cedents'].pop ()#line:1311
                    if (len (_O0O0OO0OO00O00O0O )<_O000OO00O000OO0OO ):#line:1312
                        OOOO00O000OOOO0O0 ._genvar (OOO0OOOOO00O00OOO ,OO0OO0000O00OOOOO ,_O0O0OO0OO00O00O0O ,_OO0O0O0O00O00O000 ,_OO00OOO00O000000O ,_OOOO0O0OOOO00O00O ,_O000OO00O000OO0OO ,_O0OOOOO0O00O0OOOO +(_O0OOOOO000O000OOO +0.33 )*_OO0OOO00O00O0OO0O ,_O0OOOOO0O00O0OOOO +(_O0OOOOO000O000OOO +0.66 )*_OO0OOO00O00O0OO0O )#line:1313
                else :#line:1314
                    OOO0OOOOO00O00OOO ['cedents'].pop ()#line:1315
                if len (_O0OO00OOOOO00O000 )<_O0OOO000000O0000O :#line:1316
                    OOOO00O000OOOO0O0 ._gencomb (OOO0OOOOO00O00OOO ,OO0OO0000O00OOOOO ,_O0O0OO0OO00O00O0O ,_OO0O0O0O00O00O000 ,_O0OO00OOOOO00O000 ,_O0OO00O0OO0O0O00O ,_O0OOO00O0000OO00O ,OOOO0000OO0O00O00 ,_OO0OOOOO00OO0OOO0 ,_OOOO0O0OOOO00O00O ,_O000OO00O000OO0OO ,_O000O0OO0O0O00OO0 ,_O0OOO000000O0000O ,_O0OOOOO0O00O0OOOO +_OO0OOO00O00O0OO0O *(_O0OOOOO000O000OOO +0.66 ),_O0OOOOO0O00O0OOOO +_OO0OOO00O00O0OO0O *(_O0OOOOO000O000OOO +1 ))#line:1317
                _O0OO00OOOOO00O000 .pop ()#line:1318
                _O0OOOOO000O000OOO +=1 #line:1319
                if OOOO00O000OOOO0O0 .options ['progressbar']:#line:1320
                    OOOO00O000OOOO0O0 .bar .update (min (100 ,_O0OOOOO0O00O0OOOO +_OO0OOO00O00O0OO0O *_O0OOOOO000O000OOO ))#line:1321
    def _start_cedent (OOO000OOO0OO0O00O ,OOOO0OO0O000O00O0 ,_OOO00OO0O0O00000O ,_O000O0O000O00O000 ):#line:1324
        if len (OOOO0OO0O000O00O0 ['cedents_to_do'])>len (OOOO0OO0O000O00O0 ['cedents']):#line:1325
            _O0OOO0O0OO000OO0O =[]#line:1326
            _O0O00000O00O0OO00 =[]#line:1327
            OO0O0000OO00O00O0 ={}#line:1328
            OO0O0000OO00O00O0 ['cedent_type']=OOOO0OO0O000O00O0 ['cedents_to_do'][len (OOOO0OO0O000O00O0 ['cedents'])]#line:1329
            O00O0O000000OOOO0 =OO0O0000OO00O00O0 ['cedent_type']#line:1330
            if ((O00O0O000000OOOO0 [-1 ]=='-')|(O00O0O000000OOOO0 [-1 ]=='+')):#line:1331
                O00O0O000000OOOO0 =O00O0O000000OOOO0 [:-1 ]#line:1332
            OO0O0000OO00O00O0 ['defi']=OOO000OOO0OO0O00O .kwargs .get (O00O0O000000OOOO0 )#line:1334
            if (OO0O0000OO00O00O0 ['defi']==None ):#line:1335
                print ("Error getting cedent ",OO0O0000OO00O00O0 ['cedent_type'])#line:1336
            _OO0OOOOOO00OOO0O0 =int (0 )#line:1337
            OO0O0000OO00O00O0 ['num_cedent']=len (OO0O0000OO00O00O0 ['defi'].get ('attributes'))#line:1344
            if (OO0O0000OO00O00O0 ['defi'].get ('type')=='con'):#line:1345
                _OO0OOOOOO00OOO0O0 =(1 <<OOO000OOO0OO0O00O .data ["rows_count"])-1 #line:1346
            OOO000OOO0OO0O00O ._genvar (OOOO0OO0O000O00O0 ,OO0O0000OO00O00O0 ,_O0OOO0O0OO000OO0O ,_O0O00000O00O0OO00 ,_OO0OOOOOO00OOO0O0 ,OO0O0000OO00O00O0 ['defi'].get ('minlen'),OO0O0000OO00O00O0 ['defi'].get ('maxlen'),_OOO00OO0O0O00000O ,_O000O0O000O00O000 )#line:1347
    def _calc_all (O0OO0O0OO0000O00O ,**O0O0OOO00O0OO0O00 ):#line:1350
        if "df"in O0O0OOO00O0OO0O00 :#line:1351
            O0OO0O0OO0000O00O ._prep_data (O0OO0O0OO0000O00O .kwargs .get ("df"))#line:1352
        if not (O0OO0O0OO0000O00O ._initialized ):#line:1353
            print ("ERROR: dataframe is missing and not initialized with dataframe")#line:1354
        else :#line:1355
            O0OO0O0OO0000O00O ._calculate (**O0O0OOO00O0OO0O00 )#line:1356
    def _check_cedents (OO0O0O0O00OOO00OO ,OO00OO0OOO0000OOO ,**O00O0O000OO000OO0 ):#line:1358
        O0OO0000O0000000O =True #line:1359
        if (O00O0O000OO000OO0 .get ('quantifiers',None )==None ):#line:1360
            print (f"Error: missing quantifiers.")#line:1361
            O0OO0000O0000000O =False #line:1362
            return O0OO0000O0000000O #line:1363
        if (type (O00O0O000OO000OO0 .get ('quantifiers'))!=dict ):#line:1364
            print (f"Error: quantifiers are not dictionary type.")#line:1365
            O0OO0000O0000000O =False #line:1366
            return O0OO0000O0000000O #line:1367
        for O00000OOOO0OO0O00 in OO00OO0OOO0000OOO :#line:1369
            if (O00O0O000OO000OO0 .get (O00000OOOO0OO0O00 ,None )==None ):#line:1370
                print (f"Error: cedent {O00000OOOO0OO0O00} is missing in parameters.")#line:1371
                O0OO0000O0000000O =False #line:1372
                return O0OO0000O0000000O #line:1373
            O0O00O00OOOOOO00O =O00O0O000OO000OO0 .get (O00000OOOO0OO0O00 )#line:1374
            if (O0O00O00OOOOOO00O .get ('minlen'),None )==None :#line:1375
                print (f"Error: cedent {O00000OOOO0OO0O00} has no minimal length specified.")#line:1376
                O0OO0000O0000000O =False #line:1377
                return O0OO0000O0000000O #line:1378
            if not (type (O0O00O00OOOOOO00O .get ('minlen'))is int ):#line:1379
                print (f"Error: cedent {O00000OOOO0OO0O00} has invalid type of minimal length ({type(O0O00O00OOOOOO00O.get('minlen'))}).")#line:1380
                O0OO0000O0000000O =False #line:1381
                return O0OO0000O0000000O #line:1382
            if (O0O00O00OOOOOO00O .get ('maxlen'),None )==None :#line:1383
                print (f"Error: cedent {O00000OOOO0OO0O00} has no maximal length specified.")#line:1384
                O0OO0000O0000000O =False #line:1385
                return O0OO0000O0000000O #line:1386
            if not (type (O0O00O00OOOOOO00O .get ('maxlen'))is int ):#line:1387
                print (f"Error: cedent {O00000OOOO0OO0O00} has invalid type of maximal length.")#line:1388
                O0OO0000O0000000O =False #line:1389
                return O0OO0000O0000000O #line:1390
            if (O0O00O00OOOOOO00O .get ('type'),None )==None :#line:1391
                print (f"Error: cedent {O00000OOOO0OO0O00} has no type specified.")#line:1392
                O0OO0000O0000000O =False #line:1393
                return O0OO0000O0000000O #line:1394
            if not ((O0O00O00OOOOOO00O .get ('type'))in (['con','dis'])):#line:1395
                print (f"Error: cedent {O00000OOOO0OO0O00} has invalid type. Allowed values are 'con' and 'dis'.")#line:1396
                O0OO0000O0000000O =False #line:1397
                return O0OO0000O0000000O #line:1398
            if (O0O00O00OOOOOO00O .get ('attributes'),None )==None :#line:1399
                print (f"Error: cedent {O00000OOOO0OO0O00} has no attributes specified.")#line:1400
                O0OO0000O0000000O =False #line:1401
                return O0OO0000O0000000O #line:1402
            for OO0OOO0O0OOO0OOOO in O0O00O00OOOOOO00O .get ('attributes'):#line:1403
                if (OO0OOO0O0OOO0OOOO .get ('name'),None )==None :#line:1404
                    print (f"Error: cedent {O00000OOOO0OO0O00} / attribute {OO0OOO0O0OOO0OOOO} has no 'name' attribute specified.")#line:1405
                    O0OO0000O0000000O =False #line:1406
                    return O0OO0000O0000000O #line:1407
                if not ((OO0OOO0O0OOO0OOOO .get ('name'))in OO0O0O0O00OOO00OO .data ["varname"]):#line:1408
                    print (f"Error: cedent {O00000OOOO0OO0O00} / attribute {OO0OOO0O0OOO0OOOO.get('name')} not in variable list. Please check spelling.")#line:1409
                    O0OO0000O0000000O =False #line:1410
                    return O0OO0000O0000000O #line:1411
                if (OO0OOO0O0OOO0OOOO .get ('type'),None )==None :#line:1412
                    print (f"Error: cedent {O00000OOOO0OO0O00} / attribute {OO0OOO0O0OOO0OOOO.get('name')} has no 'type' attribute specified.")#line:1413
                    O0OO0000O0000000O =False #line:1414
                    return O0OO0000O0000000O #line:1415
                if not ((OO0OOO0O0OOO0OOOO .get ('type'))in (['rcut','lcut','seq','subset','one'])):#line:1416
                    print (f"Error: cedent {O00000OOOO0OO0O00} / attribute {OO0OOO0O0OOO0OOOO.get('name')} has unsupported type {OO0OOO0O0OOO0OOOO.get('type')}. Supported types are 'subset','seq','lcut','rcut','one'.")#line:1417
                    O0OO0000O0000000O =False #line:1418
                    return O0OO0000O0000000O #line:1419
                if (OO0OOO0O0OOO0OOOO .get ('minlen'),None )==None :#line:1420
                    print (f"Error: cedent {O00000OOOO0OO0O00} / attribute {OO0OOO0O0OOO0OOOO.get('name')} has no minimal length specified.")#line:1421
                    O0OO0000O0000000O =False #line:1422
                    return O0OO0000O0000000O #line:1423
                if not (type (OO0OOO0O0OOO0OOOO .get ('minlen'))is int ):#line:1424
                    if not (OO0OOO0O0OOO0OOOO .get ('type')=='one'):#line:1425
                        print (f"Error: cedent {O00000OOOO0OO0O00} / attribute {OO0OOO0O0OOO0OOOO.get('name')} has invalid type of minimal length.")#line:1426
                        O0OO0000O0000000O =False #line:1427
                        return O0OO0000O0000000O #line:1428
                if (OO0OOO0O0OOO0OOOO .get ('maxlen'),None )==None :#line:1429
                    print (f"Error: cedent {O00000OOOO0OO0O00} / attribute {OO0OOO0O0OOO0OOOO.get('name')} has no maximal length specified.")#line:1430
                    O0OO0000O0000000O =False #line:1431
                    return O0OO0000O0000000O #line:1432
                if not (type (OO0OOO0O0OOO0OOOO .get ('maxlen'))is int ):#line:1433
                    if not (OO0OOO0O0OOO0OOOO .get ('type')=='one'):#line:1434
                        print (f"Error: cedent {O00000OOOO0OO0O00} / attribute {OO0OOO0O0OOO0OOOO.get('name')} has invalid type of maximal length.")#line:1435
                        O0OO0000O0000000O =False #line:1436
                        return O0OO0000O0000000O #line:1437
        return O0OO0000O0000000O #line:1438
    def _calculate (OOOOO0O0000000OOO ,**O00O0OOOO00O00O00 ):#line:1440
        if OOOOO0O0000000OOO .data ["data_prepared"]==0 :#line:1441
            print ("Error: data not prepared")#line:1442
            return #line:1443
        OOOOO0O0000000OOO .kwargs =O00O0OOOO00O00O00 #line:1444
        OOOOO0O0000000OOO .proc =O00O0OOOO00O00O00 .get ('proc')#line:1445
        OOOOO0O0000000OOO .quantifiers =O00O0OOOO00O00O00 .get ('quantifiers')#line:1446
        OOOOO0O0000000OOO ._init_task ()#line:1448
        OOOOO0O0000000OOO .stats ['start_proc_time']=time .time ()#line:1449
        OOOOO0O0000000OOO .task_actinfo ['cedents_to_do']=[]#line:1450
        OOOOO0O0000000OOO .task_actinfo ['cedents']=[]#line:1451
        if O00O0OOOO00O00O00 .get ("proc")=='UICMiner':#line:1454
            if not (OOOOO0O0000000OOO ._check_cedents (['ante'],**O00O0OOOO00O00O00 )):#line:1455
                return #line:1456
            _O0O0OO0O00O000000 =O00O0OOOO00O00O00 .get ("cond")#line:1458
            if _O0O0OO0O00O000000 !=None :#line:1459
                OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1460
            else :#line:1461
                OO00O0OO00000OO0O =OOOOO0O0000000OOO .cedent #line:1462
                OO00O0OO00000OO0O ['cedent_type']='cond'#line:1463
                OO00O0OO00000OO0O ['filter_value']=(1 <<OOOOO0O0000000OOO .data ["rows_count"])-1 #line:1464
                OO00O0OO00000OO0O ['generated_string']='---'#line:1465
                OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1467
                OOOOO0O0000000OOO .task_actinfo ['cedents'].append (OO00O0OO00000OO0O )#line:1468
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('ante')#line:1469
            if O00O0OOOO00O00O00 .get ('target',None )==None :#line:1470
                print ("ERROR: no succedent/target variable defined for UIC Miner")#line:1471
                return #line:1472
            if not (O00O0OOOO00O00O00 .get ('target')in OOOOO0O0000000OOO .data ["varname"]):#line:1473
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1474
                return #line:1475
            if ("aad_score"in OOOOO0O0000000OOO .quantifiers ):#line:1476
                if not ("aad_weights"in OOOOO0O0000000OOO .quantifiers ):#line:1477
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1478
                    return #line:1479
                if not (len (OOOOO0O0000000OOO .quantifiers .get ("aad_weights"))==len (OOOOO0O0000000OOO .data ["dm"][OOOOO0O0000000OOO .data ["varname"].index (OOOOO0O0000000OOO .kwargs .get ('target'))])):#line:1480
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1481
                    return #line:1482
        elif O00O0OOOO00O00O00 .get ("proc")=='CFMiner':#line:1483
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do']=['cond']#line:1484
            if O00O0OOOO00O00O00 .get ('target',None )==None :#line:1485
                print ("ERROR: no target variable defined for CF Miner")#line:1486
                return #line:1487
            if not (OOOOO0O0000000OOO ._check_cedents (['cond'],**O00O0OOOO00O00O00 )):#line:1488
                return #line:1489
            if not (O00O0OOOO00O00O00 .get ('target')in OOOOO0O0000000OOO .data ["varname"]):#line:1490
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1491
                return #line:1492
            if ("aad"in OOOOO0O0000000OOO .quantifiers ):#line:1493
                if not ("aad_weights"in OOOOO0O0000000OOO .quantifiers ):#line:1494
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1495
                    return #line:1496
                if not (len (OOOOO0O0000000OOO .quantifiers .get ("aad_weights"))==len (OOOOO0O0000000OOO .data ["dm"][OOOOO0O0000000OOO .data ["varname"].index (OOOOO0O0000000OOO .kwargs .get ('target'))])):#line:1497
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1498
                    return #line:1499
        elif O00O0OOOO00O00O00 .get ("proc")=='4ftMiner':#line:1502
            if not (OOOOO0O0000000OOO ._check_cedents (['ante','succ'],**O00O0OOOO00O00O00 )):#line:1503
                return #line:1504
            _O0O0OO0O00O000000 =O00O0OOOO00O00O00 .get ("cond")#line:1506
            if _O0O0OO0O00O000000 !=None :#line:1507
                OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1508
            else :#line:1509
                OO00O0OO00000OO0O =OOOOO0O0000000OOO .cedent #line:1510
                OO00O0OO00000OO0O ['cedent_type']='cond'#line:1511
                OO00O0OO00000OO0O ['filter_value']=(1 <<OOOOO0O0000000OOO .data ["rows_count"])-1 #line:1512
                OO00O0OO00000OO0O ['generated_string']='---'#line:1513
                OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1515
                OOOOO0O0000000OOO .task_actinfo ['cedents'].append (OO00O0OO00000OO0O )#line:1516
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('ante')#line:1520
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('succ')#line:1521
        elif O00O0OOOO00O00O00 .get ("proc")=='NewAct4ftMiner':#line:1522
            _O0O0OO0O00O000000 =O00O0OOOO00O00O00 .get ("cond")#line:1525
            if _O0O0OO0O00O000000 !=None :#line:1526
                OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1527
            else :#line:1528
                OO00O0OO00000OO0O =OOOOO0O0000000OOO .cedent #line:1529
                OO00O0OO00000OO0O ['cedent_type']='cond'#line:1530
                OO00O0OO00000OO0O ['filter_value']=(1 <<OOOOO0O0000000OOO .data ["rows_count"])-1 #line:1531
                OO00O0OO00000OO0O ['generated_string']='---'#line:1532
                print (OO00O0OO00000OO0O ['filter_value'])#line:1533
                OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1534
                OOOOO0O0000000OOO .task_actinfo ['cedents'].append (OO00O0OO00000OO0O )#line:1535
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('antv')#line:1536
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('sucv')#line:1537
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('ante')#line:1538
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('succ')#line:1539
        elif O00O0OOOO00O00O00 .get ("proc")=='Act4ftMiner':#line:1540
            _O0O0OO0O00O000000 =O00O0OOOO00O00O00 .get ("cond")#line:1543
            if _O0O0OO0O00O000000 !=None :#line:1544
                OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1545
            else :#line:1546
                OO00O0OO00000OO0O =OOOOO0O0000000OOO .cedent #line:1547
                OO00O0OO00000OO0O ['cedent_type']='cond'#line:1548
                OO00O0OO00000OO0O ['filter_value']=(1 <<OOOOO0O0000000OOO .data ["rows_count"])-1 #line:1549
                OO00O0OO00000OO0O ['generated_string']='---'#line:1550
                print (OO00O0OO00000OO0O ['filter_value'])#line:1551
                OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1552
                OOOOO0O0000000OOO .task_actinfo ['cedents'].append (OO00O0OO00000OO0O )#line:1553
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('antv-')#line:1554
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('antv+')#line:1555
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1556
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1557
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('ante')#line:1558
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('succ')#line:1559
        elif O00O0OOOO00O00O00 .get ("proc")=='SD4ftMiner':#line:1560
            if not (OOOOO0O0000000OOO ._check_cedents (['ante','succ','frst','scnd'],**O00O0OOOO00O00O00 )):#line:1563
                return #line:1564
            _O0O0OO0O00O000000 =O00O0OOOO00O00O00 .get ("cond")#line:1565
            if _O0O0OO0O00O000000 !=None :#line:1566
                OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1567
            else :#line:1568
                OO00O0OO00000OO0O =OOOOO0O0000000OOO .cedent #line:1569
                OO00O0OO00000OO0O ['cedent_type']='cond'#line:1570
                OO00O0OO00000OO0O ['filter_value']=(1 <<OOOOO0O0000000OOO .data ["rows_count"])-1 #line:1571
                OO00O0OO00000OO0O ['generated_string']='---'#line:1572
                OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1574
                OOOOO0O0000000OOO .task_actinfo ['cedents'].append (OO00O0OO00000OO0O )#line:1575
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('frst')#line:1576
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('scnd')#line:1577
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('ante')#line:1578
            OOOOO0O0000000OOO .task_actinfo ['cedents_to_do'].append ('succ')#line:1579
        else :#line:1580
            print ("Unsupported procedure")#line:1581
            return #line:1582
        print ("Will go for ",O00O0OOOO00O00O00 .get ("proc"))#line:1583
        OOOOO0O0000000OOO .task_actinfo ['optim']={}#line:1586
        OOOO0OOO0O0OOOOO0 =True #line:1587
        for OO0OO000OOO000O00 in OOOOO0O0000000OOO .task_actinfo ['cedents_to_do']:#line:1588
            try :#line:1589
                OOO0000OO000O00OO =OOOOO0O0000000OOO .kwargs .get (OO0OO000OOO000O00 )#line:1590
                if OOO0000OO000O00OO .get ('type')!='con':#line:1594
                    OOOO0OOO0O0OOOOO0 =False #line:1595
            except :#line:1597
                O0O0O000OO00O0OO0 =1 <2 #line:1598
        if OOOOO0O0000000OOO .options ['optimizations']==False :#line:1600
            OOOO0OOO0O0OOOOO0 =False #line:1601
        O0OO0O0O00OO0O0OO ={}#line:1602
        O0OO0O0O00OO0O0OO ['only_con']=OOOO0OOO0O0OOOOO0 #line:1603
        OOOOO0O0000000OOO .task_actinfo ['optim']=O0OO0O0O00OO0O0OO #line:1604
        print ("Starting to mine rules.")#line:1612
        sys .stdout .flush ()#line:1613
        time .sleep (0.01 )#line:1614
        if OOOOO0O0000000OOO .options ['progressbar']:#line:1615
            O0OOO00O0OOOOO0O0 =[progressbar .Percentage (),progressbar .Bar (),progressbar .Timer ()]#line:1616
            OOOOO0O0000000OOO .bar =progressbar .ProgressBar (widgets =O0OOO00O0OOOOO0O0 ,max_value =100 ,fd =sys .stdout ).start ()#line:1617
            OOOOO0O0000000OOO .bar .update (0 )#line:1618
        OOOOO0O0000000OOO .progress_lower =0 #line:1619
        OOOOO0O0000000OOO .progress_upper =100 #line:1620
        OOOOO0O0000000OOO ._start_cedent (OOOOO0O0000000OOO .task_actinfo ,OOOOO0O0000000OOO .progress_lower ,OOOOO0O0000000OOO .progress_upper )#line:1621
        if OOOOO0O0000000OOO .options ['progressbar']:#line:1622
            OOOOO0O0000000OOO .bar .update (100 )#line:1623
            OOOOO0O0000000OOO .bar .finish ()#line:1624
        OOOOO0O0000000OOO .stats ['end_proc_time']=time .time ()#line:1626
        print ("Done. Total verifications : "+str (OOOOO0O0000000OOO .stats ['total_cnt'])+", rules "+str (OOOOO0O0000000OOO .stats ['total_valid'])+", times: prep "+"{:.2f}".format (OOOOO0O0000000OOO .stats ['end_prep_time']-OOOOO0O0000000OOO .stats ['start_prep_time'])+"sec, processing "+"{:.2f}".format (OOOOO0O0000000OOO .stats ['end_proc_time']-OOOOO0O0000000OOO .stats ['start_proc_time'])+"sec")#line:1630
        OOOO0O0OOO00O0O00 ={}#line:1631
        O0O00O000O00OOO0O ={}#line:1632
        O0O00O000O00OOO0O ["task_type"]=O00O0OOOO00O00O00 .get ('proc')#line:1633
        O0O00O000O00OOO0O ["target"]=O00O0OOOO00O00O00 .get ('target')#line:1635
        O0O00O000O00OOO0O ["self.quantifiers"]=OOOOO0O0000000OOO .quantifiers #line:1636
        if O00O0OOOO00O00O00 .get ('cond')!=None :#line:1638
            O0O00O000O00OOO0O ['cond']=O00O0OOOO00O00O00 .get ('cond')#line:1639
        if O00O0OOOO00O00O00 .get ('ante')!=None :#line:1640
            O0O00O000O00OOO0O ['ante']=O00O0OOOO00O00O00 .get ('ante')#line:1641
        if O00O0OOOO00O00O00 .get ('succ')!=None :#line:1642
            O0O00O000O00OOO0O ['succ']=O00O0OOOO00O00O00 .get ('succ')#line:1643
        if O00O0OOOO00O00O00 .get ('opts')!=None :#line:1644
            O0O00O000O00OOO0O ['opts']=O00O0OOOO00O00O00 .get ('opts')#line:1645
        OOOO0O0OOO00O0O00 ["taskinfo"]=O0O00O000O00OOO0O #line:1646
        OO0OO00OO00000O00 ={}#line:1647
        OO0OO00OO00000O00 ["total_verifications"]=OOOOO0O0000000OOO .stats ['total_cnt']#line:1648
        OO0OO00OO00000O00 ["valid_rules"]=OOOOO0O0000000OOO .stats ['total_valid']#line:1649
        OO0OO00OO00000O00 ["total_verifications_with_opt"]=OOOOO0O0000000OOO .stats ['total_ver']#line:1650
        OO0OO00OO00000O00 ["time_prep"]=OOOOO0O0000000OOO .stats ['end_prep_time']-OOOOO0O0000000OOO .stats ['start_prep_time']#line:1651
        OO0OO00OO00000O00 ["time_processing"]=OOOOO0O0000000OOO .stats ['end_proc_time']-OOOOO0O0000000OOO .stats ['start_proc_time']#line:1652
        OO0OO00OO00000O00 ["time_total"]=OOOOO0O0000000OOO .stats ['end_prep_time']-OOOOO0O0000000OOO .stats ['start_prep_time']+OOOOO0O0000000OOO .stats ['end_proc_time']-OOOOO0O0000000OOO .stats ['start_proc_time']#line:1653
        OOOO0O0OOO00O0O00 ["summary_statistics"]=OO0OO00OO00000O00 #line:1654
        OOOO0O0OOO00O0O00 ["rules"]=OOOOO0O0000000OOO .rulelist #line:1655
        O00O00O0OOO0OOO0O ={}#line:1656
        O00O00O0OOO0OOO0O ["varname"]=OOOOO0O0000000OOO .data ["varname"]#line:1657
        O00O00O0OOO0OOO0O ["catnames"]=OOOOO0O0000000OOO .data ["catnames"]#line:1658
        OOOO0O0OOO00O0O00 ["datalabels"]=O00O00O0OOO0OOO0O #line:1659
        OOOOO0O0000000OOO .result =OOOO0O0OOO00O0O00 #line:1660
    def print_summary (O0O00O000OOOOO0O0 ):#line:1662
        print ("")#line:1663
        print ("CleverMiner task processing summary:")#line:1664
        print ("")#line:1665
        print (f"Task type : {O0O00O000OOOOO0O0.result['taskinfo']['task_type']}")#line:1666
        print (f"Number of verifications : {O0O00O000OOOOO0O0.result['summary_statistics']['total_verifications']}")#line:1667
        print (f"Number of rules : {O0O00O000OOOOO0O0.result['summary_statistics']['valid_rules']}")#line:1668
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(O0O00O000OOOOO0O0.result['summary_statistics']['time_total']))}")#line:1669
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(O0O00O000OOOOO0O0.result['summary_statistics']['time_prep']))}")#line:1671
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(O0O00O000OOOOO0O0.result['summary_statistics']['time_processing']))}")#line:1672
        print ("")#line:1673
    def print_hypolist (OO000O0OO0O000O0O ):#line:1675
        OO000O0OO0O000O0O .print_rulelist ();#line:1676
    def print_rulelist (O0OOO0O00O00OOO00 ,sortby =None ,storesorted =False ):#line:1678
        def OOO0OO0O0O0O0O000 (OO00O0O00000000O0 ):#line:1679
            OO0OO00000OO00OOO =OO00O0O00000000O0 ["params"]#line:1680
            return OO0OO00000OO00OOO .get (sortby ,0 )#line:1681
        print ("")#line:1683
        print ("List of rules:")#line:1684
        if O0OOO0O00O00OOO00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1685
            print ("RULEID BASE  CONF  AAD    Rule")#line:1686
        elif O0OOO0O00O00OOO00 .result ['taskinfo']['task_type']=="UICMiner":#line:1687
            print ("RULEID BASE  AAD_SCORE  Rule")#line:1688
        elif O0OOO0O00O00OOO00 .result ['taskinfo']['task_type']=="CFMiner":#line:1689
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:1690
        elif O0OOO0O00O00OOO00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1691
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:1692
        else :#line:1693
            print ("Unsupported task type for rulelist")#line:1694
            return #line:1695
        O00O0OO0O000OO0O0 =O0OOO0O00O00OOO00 .result ["rules"]#line:1696
        if sortby is not None :#line:1697
            O00O0OO0O000OO0O0 =sorted (O00O0OO0O000OO0O0 ,key =OOO0OO0O0O0O0O000 ,reverse =True )#line:1698
            if storesorted :#line:1699
                O0OOO0O00O00OOO00 .result ["rules"]=O00O0OO0O000OO0O0 #line:1700
        for O0OO0OOO00O0OOO0O in O00O0OO0O000OO0O0 :#line:1702
            OOO0000O00OO0OO00 ="{:6d}".format (O0OO0OOO00O0OOO0O ["rule_id"])#line:1703
            if O0OOO0O00O00OOO00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1704
                OOO0000O00OO0OO00 =OOO0000O00OO0OO00 +" "+"{:5d}".format (O0OO0OOO00O0OOO0O ["params"]["base"])+" "+"{:.3f}".format (O0OO0OOO00O0OOO0O ["params"]["conf"])+" "+"{:+.3f}".format (O0OO0OOO00O0OOO0O ["params"]["aad"])#line:1706
                OOO0000O00OO0OO00 =OOO0000O00OO0OO00 +" "+O0OO0OOO00O0OOO0O ["cedents_str"]["ante"]+" => "+O0OO0OOO00O0OOO0O ["cedents_str"]["succ"]+" | "+O0OO0OOO00O0OOO0O ["cedents_str"]["cond"]#line:1707
            elif O0OOO0O00O00OOO00 .result ['taskinfo']['task_type']=="UICMiner":#line:1708
                OOO0000O00OO0OO00 =OOO0000O00OO0OO00 +" "+"{:5d}".format (O0OO0OOO00O0OOO0O ["params"]["base"])+" "+"{:.3f}".format (O0OO0OOO00O0OOO0O ["params"]["aad_score"])#line:1709
                OOO0000O00OO0OO00 =OOO0000O00OO0OO00 +"     "+O0OO0OOO00O0OOO0O ["cedents_str"]["ante"]+" => "+O0OOO0O00O00OOO00 .result ['taskinfo']['target']+"(*) | "+O0OO0OOO00O0OOO0O ["cedents_str"]["cond"]#line:1710
            elif O0OOO0O00O00OOO00 .result ['taskinfo']['task_type']=="CFMiner":#line:1711
                OOO0000O00OO0OO00 =OOO0000O00OO0OO00 +" "+"{:5d}".format (O0OO0OOO00O0OOO0O ["params"]["base"])+" "+"{:5d}".format (O0OO0OOO00O0OOO0O ["params"]["s_up"])+" "+"{:5d}".format (O0OO0OOO00O0OOO0O ["params"]["s_down"])#line:1712
                OOO0000O00OO0OO00 =OOO0000O00OO0OO00 +" "+O0OO0OOO00O0OOO0O ["cedents_str"]["cond"]#line:1713
            elif O0OOO0O00O00OOO00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1714
                OOO0000O00OO0OO00 =OOO0000O00OO0OO00 +" "+"{:5d}".format (O0OO0OOO00O0OOO0O ["params"]["base1"])+" "+"{:5d}".format (O0OO0OOO00O0OOO0O ["params"]["base2"])+"    "+"{:.3f}".format (O0OO0OOO00O0OOO0O ["params"]["ratioconf"])+"    "+"{:+.3f}".format (O0OO0OOO00O0OOO0O ["params"]["deltaconf"])#line:1715
                OOO0000O00OO0OO00 =OOO0000O00OO0OO00 +"  "+O0OO0OOO00O0OOO0O ["cedents_str"]["ante"]+" => "+O0OO0OOO00O0OOO0O ["cedents_str"]["succ"]+" | "+O0OO0OOO00O0OOO0O ["cedents_str"]["cond"]+" : "+O0OO0OOO00O0OOO0O ["cedents_str"]["frst"]+" x "+O0OO0OOO00O0OOO0O ["cedents_str"]["scnd"]#line:1716
            print (OOO0000O00OO0OO00 )#line:1718
        print ("")#line:1719
    def print_hypo (O00O0O00O0O00OOOO ,O0OOOOOO000O00O00 ):#line:1721
        O00O0O00O0O00OOOO .print_rule (O0OOOOOO000O00O00 )#line:1722
    def print_rule (OO0O0O0O0000O0OOO ,O0OOOOOO0OOOOOO00 ):#line:1725
        print ("")#line:1726
        if (O0OOOOOO0OOOOOO00 <=len (OO0O0O0O0000O0OOO .result ["rules"])):#line:1727
            if OO0O0O0O0000O0OOO .result ['taskinfo']['task_type']=="4ftMiner":#line:1728
                print ("")#line:1729
                O00O00OO0OO000000 =OO0O0O0O0000O0OOO .result ["rules"][O0OOOOOO0OOOOOO00 -1 ]#line:1730
                print (f"Rule id : {O00O00OO0OO000000['rule_id']}")#line:1731
                print ("")#line:1732
                print (f"Base : {'{:5d}'.format(O00O00OO0OO000000['params']['base'])}  Relative base : {'{:.3f}'.format(O00O00OO0OO000000['params']['rel_base'])}  CONF : {'{:.3f}'.format(O00O00OO0OO000000['params']['conf'])}  AAD : {'{:+.3f}'.format(O00O00OO0OO000000['params']['aad'])}  BAD : {'{:+.3f}'.format(O00O00OO0OO000000['params']['bad'])}")#line:1733
                print ("")#line:1734
                print ("Cedents:")#line:1735
                print (f"  antecedent : {O00O00OO0OO000000['cedents_str']['ante']}")#line:1736
                print (f"  succcedent : {O00O00OO0OO000000['cedents_str']['succ']}")#line:1737
                print (f"  condition  : {O00O00OO0OO000000['cedents_str']['cond']}")#line:1738
                print ("")#line:1739
                print ("Fourfold table")#line:1740
                print (f"    |  S  |  ¬S |")#line:1741
                print (f"----|-----|-----|")#line:1742
                print (f" A  |{'{:5d}'.format(O00O00OO0OO000000['params']['fourfold'][0])}|{'{:5d}'.format(O00O00OO0OO000000['params']['fourfold'][1])}|")#line:1743
                print (f"----|-----|-----|")#line:1744
                print (f"¬A  |{'{:5d}'.format(O00O00OO0OO000000['params']['fourfold'][2])}|{'{:5d}'.format(O00O00OO0OO000000['params']['fourfold'][3])}|")#line:1745
                print (f"----|-----|-----|")#line:1746
            elif OO0O0O0O0000O0OOO .result ['taskinfo']['task_type']=="CFMiner":#line:1747
                print ("")#line:1748
                O00O00OO0OO000000 =OO0O0O0O0000O0OOO .result ["rules"][O0OOOOOO0OOOOOO00 -1 ]#line:1749
                print (f"Rule id : {O00O00OO0OO000000['rule_id']}")#line:1750
                print ("")#line:1751
                OO0O000OOOOOOOOO0 =""#line:1752
                if ('aad'in O00O00OO0OO000000 ['params']):#line:1753
                    OO0O000OOOOOOOOO0 ="aad : "+str (O00O00OO0OO000000 ['params']['aad'])#line:1754
                print (f"Base : {'{:5d}'.format(O00O00OO0OO000000['params']['base'])}  Relative base : {'{:.3f}'.format(O00O00OO0OO000000['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(O00O00OO0OO000000['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(O00O00OO0OO000000['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(O00O00OO0OO000000['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(O00O00OO0OO000000['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(O00O00OO0OO000000['params']['max'])}  Histogram minimum : {'{:5d}'.format(O00O00OO0OO000000['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(O00O00OO0OO000000['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(O00O00OO0OO000000['params']['rel_min'])} {OO0O000OOOOOOOOO0}")#line:1756
                print ("")#line:1757
                print (f"Condition  : {O00O00OO0OO000000['cedents_str']['cond']}")#line:1758
                print ("")#line:1759
                O0OOO0O00O0O0000O =OO0O0O0O0000O0OOO .get_category_names (OO0O0O0O0000O0OOO .result ["taskinfo"]["target"])#line:1760
                print (f"Categories in target variable  {O0OOO0O00O0O0000O}")#line:1761
                print (f"Histogram                      {O00O00OO0OO000000['params']['hist']}")#line:1762
                if ('aad'in O00O00OO0OO000000 ['params']):#line:1763
                    print (f"Histogram on full set          {O00O00OO0OO000000['params']['hist_full']}")#line:1764
                    print (f"Relative histogram             {O00O00OO0OO000000['params']['rel_hist']}")#line:1765
                    print (f"Relative histogram on full set {O00O00OO0OO000000['params']['rel_hist_full']}")#line:1766
            elif OO0O0O0O0000O0OOO .result ['taskinfo']['task_type']=="UICMiner":#line:1767
                print ("")#line:1768
                O00O00OO0OO000000 =OO0O0O0O0000O0OOO .result ["rules"][O0OOOOOO0OOOOOO00 -1 ]#line:1769
                print (f"Rule id : {O00O00OO0OO000000['rule_id']}")#line:1770
                print ("")#line:1771
                OO0O000OOOOOOOOO0 =""#line:1772
                if ('aad_score'in O00O00OO0OO000000 ['params']):#line:1773
                    OO0O000OOOOOOOOO0 ="aad score : "+str (O00O00OO0OO000000 ['params']['aad_score'])#line:1774
                print (f"Base : {'{:5d}'.format(O00O00OO0OO000000['params']['base'])}  Relative base : {'{:.3f}'.format(O00O00OO0OO000000['params']['rel_base'])}   {OO0O000OOOOOOOOO0}")#line:1776
                print ("")#line:1777
                print (f"Condition  : {O00O00OO0OO000000['cedents_str']['cond']}")#line:1778
                print (f"Antecedent : {O00O00OO0OO000000['cedents_str']['ante']}")#line:1779
                print ("")#line:1780
                print (f"Histogram                                        {O00O00OO0OO000000['params']['hist']}")#line:1781
                if ('aad_score'in O00O00OO0OO000000 ['params']):#line:1782
                    print (f"Histogram on full set with condition             {O00O00OO0OO000000['params']['hist_cond']}")#line:1783
                    print (f"Relative histogram                               {O00O00OO0OO000000['params']['rel_hist']}")#line:1784
                    print (f"Relative histogram on full set with condition    {O00O00OO0OO000000['params']['rel_hist_cond']}")#line:1785
                OO0O0OO000OO000O0 =OO0O0O0O0000O0OOO .result ['datalabels']['catnames'][OO0O0O0O0000O0OOO .result ['datalabels']['varname'].index (OO0O0O0O0000O0OOO .result ['taskinfo']['target'])]#line:1786
                print (" ")#line:1788
                print ("Interpretation:")#line:1789
                for OOO0OO00OOOOO0OO0 in range (len (OO0O0OO000OO000O0 )):#line:1790
                  O000O0O00000000OO =0 #line:1791
                  if O00O00OO0OO000000 ['params']['rel_hist'][OOO0OO00OOOOO0OO0 ]>0 :#line:1792
                      O000O0O00000000OO =O00O00OO0OO000000 ['params']['rel_hist'][OOO0OO00OOOOO0OO0 ]/O00O00OO0OO000000 ['params']['rel_hist_cond'][OOO0OO00OOOOO0OO0 ]#line:1793
                  O0O00O00O00OOOO0O =''#line:1794
                  if not (O00O00OO0OO000000 ['cedents_str']['cond']=='---'):#line:1795
                      O0O00O00O00OOOO0O ="For "+O00O00OO0OO000000 ['cedents_str']['cond']+": "#line:1796
                  print (f"    {O0O00O00O00OOOO0O}{OO0O0O0O0000O0OOO.result['taskinfo']['target']}({OO0O0OO000OO000O0[OOO0OO00OOOOO0OO0]}) has occurence {'{:.1%}'.format(O00O00OO0OO000000['params']['rel_hist_cond'][OOO0OO00OOOOO0OO0])}, with antecedent it has occurence {'{:.1%}'.format(O00O00OO0OO000000['params']['rel_hist'][OOO0OO00OOOOO0OO0])}, that is {'{:.3f}'.format(O000O0O00000000OO)} times more.")#line:1798
            elif OO0O0O0O0000O0OOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1799
                print ("")#line:1800
                O00O00OO0OO000000 =OO0O0O0O0000O0OOO .result ["rules"][O0OOOOOO0OOOOOO00 -1 ]#line:1801
                print (f"Rule id : {O00O00OO0OO000000['rule_id']}")#line:1802
                print ("")#line:1803
                print (f"Base1 : {'{:5d}'.format(O00O00OO0OO000000['params']['base1'])} Base2 : {'{:5d}'.format(O00O00OO0OO000000['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(O00O00OO0OO000000['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(O00O00OO0OO000000['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(O00O00OO0OO000000['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(O00O00OO0OO000000['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(O00O00OO0OO000000['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(O00O00OO0OO000000['params']['ratioconf'])}")#line:1804
                print ("")#line:1805
                print ("Cedents:")#line:1806
                print (f"  antecedent : {O00O00OO0OO000000['cedents_str']['ante']}")#line:1807
                print (f"  succcedent : {O00O00OO0OO000000['cedents_str']['succ']}")#line:1808
                print (f"  condition  : {O00O00OO0OO000000['cedents_str']['cond']}")#line:1809
                print (f"  first set  : {O00O00OO0OO000000['cedents_str']['frst']}")#line:1810
                print (f"  second set : {O00O00OO0OO000000['cedents_str']['scnd']}")#line:1811
                print ("")#line:1812
                print ("Fourfold tables:")#line:1813
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:1814
                print (f"----|-----|-----|  ----|-----|-----| ")#line:1815
                print (f" A  |{'{:5d}'.format(O00O00OO0OO000000['params']['fourfold1'][0])}|{'{:5d}'.format(O00O00OO0OO000000['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(O00O00OO0OO000000['params']['fourfold2'][0])}|{'{:5d}'.format(O00O00OO0OO000000['params']['fourfold2'][1])}|")#line:1816
                print (f"----|-----|-----|  ----|-----|-----|")#line:1817
                print (f"¬A  |{'{:5d}'.format(O00O00OO0OO000000['params']['fourfold1'][2])}|{'{:5d}'.format(O00O00OO0OO000000['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(O00O00OO0OO000000['params']['fourfold2'][2])}|{'{:5d}'.format(O00O00OO0OO000000['params']['fourfold2'][3])}|")#line:1818
                print (f"----|-----|-----|  ----|-----|-----|")#line:1819
            else :#line:1820
                print ("Unsupported task type for rule details")#line:1821
            print ("")#line:1825
        else :#line:1826
            print ("No such rule.")#line:1827
    def get_rulecount (O0OO0OO0000O00O0O ):#line:1829
        return len (O0OO0OO0000O00O0O .result ["rules"])#line:1830
    def get_fourfold (O000OO000O0O0O0OO ,O00000O0OO000OO00 ,order =0 ):#line:1832
        if (O00000O0OO000OO00 <=len (O000OO000O0O0O0OO .result ["rules"])):#line:1834
            if O000OO000O0O0O0OO .result ['taskinfo']['task_type']=="4ftMiner":#line:1835
                O00OOO0000OO00O0O =O000OO000O0O0O0OO .result ["rules"][O00000O0OO000OO00 -1 ]#line:1836
                return O00OOO0000OO00O0O ['params']['fourfold']#line:1837
            elif O000OO000O0O0O0OO .result ['taskinfo']['task_type']=="CFMiner":#line:1838
                print ("Error: fourfold for CFMiner is not defined")#line:1839
                return None #line:1840
            elif O000OO000O0O0O0OO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1841
                O00OOO0000OO00O0O =O000OO000O0O0O0OO .result ["rules"][O00000O0OO000OO00 -1 ]#line:1842
                if order ==1 :#line:1843
                    return O00OOO0000OO00O0O ['params']['fourfold1']#line:1844
                if order ==2 :#line:1845
                    return O00OOO0000OO00O0O ['params']['fourfold2']#line:1846
                print ("Error: for SD4ft-Miner, you need to provide order of fourfold table in order= parameter (valid values are 1,2).")#line:1847
                return None #line:1848
            else :#line:1849
                print ("Unsupported task type for rule details")#line:1850
        else :#line:1851
            print ("No such rule.")#line:1852
    def get_hist (OO000OOOO0O00O000 ,OO0O0O0OO00O0O0O0 ):#line:1854
        if (OO0O0O0OO00O0O0O0 <=len (OO000OOOO0O00O000 .result ["rules"])):#line:1856
            if OO000OOOO0O00O000 .result ['taskinfo']['task_type']=="CFMiner":#line:1857
                O0OOOOOOOO0O0OO0O =OO000OOOO0O00O000 .result ["rules"][OO0O0O0OO00O0O0O0 -1 ]#line:1858
                return O0OOOOOOOO0O0OO0O ['params']['hist']#line:1859
            elif OO000OOOO0O00O000 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1860
                print ("Error: SD4ft-Miner has no histogram")#line:1861
                return None #line:1862
            elif OO000OOOO0O00O000 .result ['taskinfo']['task_type']=="4ftMiner":#line:1863
                print ("Error: 4ft-Miner has no histogram")#line:1864
                return None #line:1865
            else :#line:1866
                print ("Unsupported task type for rule details")#line:1867
        else :#line:1868
            print ("No such rule.")#line:1869
    def get_hist_cond (O00OO0000OOOOOO0O ,OOOO00O00OOO0OOOO ):#line:1872
        if (OOOO00O00OOO0OOOO <=len (O00OO0000OOOOOO0O .result ["rules"])):#line:1874
            if O00OO0000OOOOOO0O .result ['taskinfo']['task_type']=="UICMiner":#line:1875
                OO0O00OO00O0OOO0O =O00OO0000OOOOOO0O .result ["rules"][OOOO00O00OOO0OOOO -1 ]#line:1876
                return OO0O00OO00O0OOO0O ['params']['hist_cond']#line:1877
            elif O00OO0000OOOOOO0O .result ['taskinfo']['task_type']=="CFMiner":#line:1878
                OO0O00OO00O0OOO0O =O00OO0000OOOOOO0O .result ["rules"][OOOO00O00OOO0OOOO -1 ]#line:1879
                return OO0O00OO00O0OOO0O ['params']['hist']#line:1880
            elif O00OO0000OOOOOO0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1881
                print ("Error: SD4ft-Miner has no histogram")#line:1882
                return None #line:1883
            elif O00OO0000OOOOOO0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1884
                print ("Error: 4ft-Miner has no histogram")#line:1885
                return None #line:1886
            else :#line:1887
                print ("Unsupported task type for rule details")#line:1888
        else :#line:1889
            print ("No such rule.")#line:1890
    def get_quantifiers (OOO00O00OOOO0OOOO ,OOO000O0OO00O0OO0 ,order =0 ):#line:1892
        if (OOO000O0OO00O0OO0 <=len (OOO00O00OOOO0OOOO .result ["rules"])):#line:1894
            O00O00O00000O00OO =OOO00O00OOOO0OOOO .result ["rules"][OOO000O0OO00O0OO0 -1 ]#line:1895
            if OOO00O00OOOO0OOOO .result ['taskinfo']['task_type']=="4ftMiner":#line:1896
                return O00O00O00000O00OO ['params']#line:1897
            elif OOO00O00OOOO0OOOO .result ['taskinfo']['task_type']=="CFMiner":#line:1898
                return O00O00O00000O00OO ['params']#line:1899
            elif OOO00O00OOOO0OOOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1900
                return O00O00O00000O00OO ['params']#line:1901
            else :#line:1902
                print ("Unsupported task type for rule details")#line:1903
        else :#line:1904
            print ("No such rule.")#line:1905
    def get_varlist (OO0OOOOOOO0O0O00O ):#line:1907
        return OO0OOOOOOO0O0O00O .result ["datalabels"]["varname"]#line:1908
    def get_category_names (O000000OO0OO0O0OO ,varname =None ,varindex =None ):#line:1910
        OOO00O00OOOO0000O =0 #line:1911
        if varindex is not None :#line:1912
            if OOO00O00OOOO0000O >=0 &OOO00O00OOOO0000O <len (O000000OO0OO0O0OO .get_varlist ()):#line:1913
                OOO00O00OOOO0000O =varindex #line:1914
            else :#line:1915
                print ("Error: no such variable.")#line:1916
                return #line:1917
        if (varname is not None ):#line:1918
            O00O00OO00OOO0000 =O000000OO0OO0O0OO .get_varlist ()#line:1919
            OOO00O00OOOO0000O =O00O00OO00OOO0000 .index (varname )#line:1920
            if OOO00O00OOOO0000O ==-1 |OOO00O00OOOO0000O <0 |OOO00O00OOOO0000O >=len (O000000OO0OO0O0OO .get_varlist ()):#line:1921
                print ("Error: no such variable.")#line:1922
                return #line:1923
        return O000000OO0OO0O0OO .result ["datalabels"]["catnames"][OOO00O00OOOO0000O ]#line:1924
    def print_data_definition (O0OOO0000OO0OOO0O ):#line:1926
        O000OOO0OO00OO000 =O0OOO0000OO0OOO0O .get_varlist ()#line:1927
        for OO00OOOOOO0O00OO0 in O000OOO0OO00OO000 :#line:1928
            OO00OOOOOOO00OOO0 =O0OOO0000OO0OOO0O .get_category_names (OO00OOOOOO0O00OO0 )#line:1929
            OOO00OO0OOOO0OO00 =""#line:1930
            for O0OO0O0OO00O00O00 in OO00OOOOOOO00OOO0 :#line:1931
                OOO00OO0OOOO0OO00 =OOO00OO0OOOO0OO00 +str (O0OO0O0OO00O00O00 )+" "#line:1932
            OOO00OO0OOOO0OO00 =OOO00OO0OOOO0OO00 [:-1 ]#line:1933
            print (f"Variable {OO00OOOOOO0O00OO0} has {len(O000OOO0OO00OO000)} categories: {OOO00OO0OOOO0OO00}")#line:1934
