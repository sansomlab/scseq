import sys
import os
import re
import sqlite3

import pandas as pd
import numpy as np

from CGATCore import Experiment as E
from CGATCore import Pipeline as P

# load options from the config file
PARAMS = P.get_parameters(
    ["%s/pipeline.yml" % os.path.splitext(__file__)[0],
     "../pipeline.yml",
     "pipeline.yml"])


# ########################################################################### #
# ####################### General functions ################################# #
# ########################################################################### #

def runCuffNorm(geneset, cxb_files, labels,
                outdir, logFile,
                library_type="fr-unstranded",
                normalisation="classic-fpkm",
                standards_file=None,
                hits="total"):
    '''
    Run cuffnorm.
    '''

    total_mem = PARAMS["cufflinks_cuffnorm_total_mb_memory"]

    job_threads = PARAMS["cufflinks_cuffnorm_threads"]
    job_memory = str(int(total_mem) // int(job_threads)) + "M"

    hits_method = "--%(hits)s-hits-norm" % locals()

    if standards_file:
        norm_standards = "--norm-standards-file=%(standards_file)s" % locals()
    else:
        norm_standards = ""

    statement = ''' gtf=`mktemp -p %(local_tmpdir)s`;
                    checkpoint;
                    zcat %(geneset)s > $gtf;
                    checkpoint;
                    cuffnorm
                        --output-dir %(outdir)s
                        --num-threads=%(job_threads)s
                        --library-type %(library_type)s
                        %(hits_method)s
                        --library-norm-method %(normalisation)s
                        %(norm_standards)s
                        --labels %(labels)s
                        $gtf %(cxb_files)s > %(logFile)s;
                     checkpoint;
                     rm $gtf;
                '''
    P.run(statement)
