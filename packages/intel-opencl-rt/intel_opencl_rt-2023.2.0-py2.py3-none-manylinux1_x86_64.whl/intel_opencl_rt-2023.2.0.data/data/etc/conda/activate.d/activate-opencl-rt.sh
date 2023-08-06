#!/bin/bash

if [ "${OCL_ICD_VENDORS:-}" = "" ] ; then
    export OCL_ICD_VENDORS_RESET=1
else
    export OCL_ICD_VENDORS_SAVED=${OCL_ICD_VENDORS}
fi
if [ "${OCL_ICD_FILENAMES:-}" = "" ] ; then
    export OCL_ICD_FILENAMES_RESET=1
else
    export OCL_ICD_FILENAMES_SAVED=${OCL_ICD_FILENAMES}
fi
export OCL_ICD_VENDORS=${CONDA_PREFIX}/etc/OpenCL/vendors
unset OCL_ICD_FILENAMES
