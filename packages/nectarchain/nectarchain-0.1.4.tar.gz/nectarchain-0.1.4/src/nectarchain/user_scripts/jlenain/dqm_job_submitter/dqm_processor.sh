#!/bin/env bash
#
# Time-stamp: "2023-05-30 12:05:14 jlenain"


function usage ()
{
    echo "Usage: `basename $0` -r <run number>"
}

function help ()
{
    usage
    cat <<EOF

This script launches a data quality monitoring processing of a given NectarCAM run.

OPTIONS:
     -h                       This help message.
     -r <RUN NUMBER>          NectarCAM run number to be processed.
EOF
}

# Get options
while getopts ":hr:" option; do
   case $option in
      h) # display help
          help
	  exit;;
      r) # Enter a run number
         runnb=$OPTARG;;
     \?) # Invalid option
         usage
	 exit 1;;
   esac
done
shift $((OPTIND-1))

if [ -z $runnb ]; then
    usage
    exit 1
fi

WRAPPER="singularity_wrapper.sh"
CONTAINER="oras://ghcr.io/cta-observatory/nectarchain:latest"
OUTDIR=NectarCAM_DQM_Run${runnb}
DIRAC_OUTDIR=/vo.cta.in2p3.fr/user/j/jlenain/nectarcam/dqm

function exit_script() {
    return_code=$1

    # Some cleanup before leaving:
    # [ -d $CONTAINER ] && rm -rf $CONTAINER
    # [ -f $CONTAINER ] && rm -f $CONTAINER
    [ -d $OUTDIR ] && rm -rf $OUTDIR
    [ -f ${OUTDIR}.tar.gz ] && rm -f ${OUTDIR}.tar.gz
    [ -d ${OUTDIR} ] && rm -rf ${OUTDIR}
    [ -f $WRAPPER ] && rm -f $WRAPPER

    exit $return_code
}

# Halim's DQM code needs to use a specific output directory:
export NECTARDIR=$PWD/$OUTDIR
[ ! -d $NECTARDIR ] && mkdir -p $NECTARDIR || exit_script $?
# mv nectarcam*.sqlite NectarCAM.Run*.fits.fz $NECTARDIR/.

LISTRUNS=""
for run in $PWD/NectarCAM.Run${runnb}.*.fits.fz; do
    LISTRUNS="$LISTRUNS $(basename $run)"
done

# Create a wrapper BASH script with cleaned environment, see https://redmine.cta-observatory.org/issues/51483
cat > $WRAPPER <<EOF
#!/bin/env bash
echo "Cleaning environment \$CLEANED_ENV" 
[ -z "\$CLEANED_ENV" ] && exec /bin/env -i CLEANED_ENV="Done" HOME=\${HOME} SHELL=/bin/bash /bin/bash -l "\$0" "\$@" 


# Some environment variables related to python, to be passed to container, be it for old Singularity version or recent Apptainer ones:
export SINGULARITYENV_MPLCONFIGDIR=/tmp
export SINGULARITYENV_NUMBA_CACHE_DIR=/tmp
export SINGULARITYENV_NECTARDIR=$NECTARDIR

export APPTAINERENV_MPLCONFIGDIR=/tmp
export APPTAINERENV_NUMBA_CACHE_DIR=/tmp
export APPTAINERENV_NECTARDIR=$NECTARDIR

# Handle Singularity or Apptainer case:
if command -v singularity &> /dev/null; then
    CALLER=singularity
elif command -v apptainer &> /dev/null; then
    CALLER=apptainer
else
    echo "It seems neither Singularity nor Apptainer are available from here"
    exit 1
fi

echo
echo "Running" 
# Instantiate the nectarchain Singularity image, run our DQM example run within it:
cmd="\$CALLER exec --home $PWD $CONTAINER /opt/conda/envs/nectarchain/bin/python /opt/cta/nectarchain/src/nectarchain/dqm/start_calib.py $PWD $NECTARDIR -i $LISTRUNS"
echo \$cmd
eval \$cmd
EOF

chmod u+x $WRAPPER || exit_script $?
./${WRAPPER} || exit_script $?


# Archive the output directory and push it on DIRAC before leaving the job:
tar zcf ${OUTDIR}.tar.gz ${OUTDIR}/ || exit_script $?
dirac-dms-add-file ${DIRAC_OUTDIR}/${OUTDIR}.tar.gz ${OUTDIR}.tar.gz LPNHE-USER || exit_script $?

exit_script 0
