#!/bin/sh

if [[ "${OCL_ICD_VENDORS_RESET:-}" = "1" ]] ; then
    unset OCL_ICD_VENDORS_RESET
    unset OCL_ICD_VENDORS
elif [ -n "$OCL_ICD_VENDORS_SAVED" ] ; then
    export OCL_ICD_VENDORS=${OCL_ICD_VENDORS_SAVED}
    unset OCL_ICD_VENDORS_SAVED
fi
if [[ "${OCL_ICD_FILENAMES_RESET:-}" = "1" ]] ; then
    unset OCL_ICD_FILENAMES_RESET
    unset OCL_ICD_FILENAMES
elif [ -n "$OCL_ICD_FILENAMES_SAVED" ] ; then
    export OCL_ICD_FILENAMES=${OCL_ICD_FILENAMES_SAVED}
    unset OCL_ICD_FILENAMES_SAVED
fi

