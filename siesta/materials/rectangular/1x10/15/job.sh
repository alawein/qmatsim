#!/bin/bash

# Job name
#SBATCH --job-name=SIESTA-MoS2-Monolayer-GGA-T-rectangular-1x10-15%

#SBATCH --account=co_msedcc

#SBATCH --partition=savio3

#SBATCH --qos=savio_lowprio

# Wall clock limit
#SBATCH --time=3-00:00:00

# Number of nodes, taks, and CPUs
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=32

# Output data
#SBATCH --output=co-%x-%j.out
#SBATCH --error=eco-%x-%j.err

# Feedback for job 
#SBATCH --mail-type=FAIL,REQUEUE,END
# Optional notification address: configure --mail-user in a local submission wrapper.

# Specify the job is eligible to requeue
#SBATCH --requeue

# Append the standard output/error of the requeued job to the same standard out/error files from the previously terminated job
#SBATCH --open-mode=append

# Enable globstar and aliases expansion


shopt -s globstar
shopt -s expand_aliases

find . -name 'co-*' -mmin +0.1 -exec rm {} \;
find . -name 'eco-*' -mmin +0.1 -exec rm {} \;

rm -f ./*~
rm -f ./*#

conda activate siesta-env

# Variables
systemLabel=MoS2
SOCCond=T
RelaxCond=T
StaticCond=T
BandsCond=T
LDOSCond=T
homedir="${QMATSIM_WORKSPACE_ROOT:?Set QMATSIM_WORKSPACE_ROOT}/siesta/materials/MoS2/Monolayer/rectangular/1x10/15/"

if [ "$SOCCond" = "T" ]; then
    scratchFolder="${QMATSIM_SCRATCH_ROOT:?Set QMATSIM_SCRATCH_ROOT}/MoS2/Monolayer/GGA-SOC/rectangular/1x10/15/"
    potdir="${QMATSIM_PSEUDOPOTENTIAL_ROOT:?Set QMATSIM_PSEUDOPOTENTIAL_ROOT}/GGA-SOC/"
else
    scratchFolder="${QMATSIM_SCRATCH_ROOT:?Set QMATSIM_SCRATCH_ROOT}/MoS2/Monolayer/GGA/rectangular/1x10/15/"
    potdir="${QMATSIM_PSEUDOPOTENTIAL_ROOT:?Set QMATSIM_PSEUDOPOTENTIAL_ROOT}/GGA/"
fi

# Scratch folder structure
mkdir -p ${scratchFolder}/1-Relaxation ${scratchFolder}/2-Static ${scratchFolder}/3-Bands ${scratchFolder}/LDOS ${scratchFolder}/FILES


cd ${scratchFolder}

cp ${homedir}/* FILES
sed -i 's/-vector/cell-vector/g' FILES/*.fdf

######################## RELAXATION ########################
if [ "$RelaxCond" = "T" ]; then
    cd 1-Relaxation

    find . -name 'co-*' -mmin +0.1 -exec rm {} \;
    find . -name 'eco-*' -mmin +0.1 -exec rm {} \;
    find . -name 'log-*' -mmin +0.1 -exec rm {} \;
    find . -type f ! \( -name 'MoS2.CG' -o -name 'MoS2.DM' -o -name 'MoS2.STRUCT_OUT' -o -name "*.psf" -o -name "*.psml" -o -name "*.sh" -o -name "MoS2.STRUCT_IN" -o -name "1-Relaxation.fdf" \) -delete

    cp ../FILES/* .
    
    cp MoS2.STRUCT_OUT MoS2.STRUCT_IN

    siesta 1-Relaxation.fdf > siesta.out

    echo "RELAXATION RUN DONE!" > completed.relaxCompleted

    cd ..
fi

wait

######################## STATIC ########################
if [ "$StaticCond" = "T" ]; then
    cd 2-Static

    find . -name 'co-*' -mmin +0.1 -exec rm {} \;
    find . -name 'eco-*' -mmin +0.1 -exec rm {} \;
    find . -name 'log-*' -mmin +0.1 -exec rm {} \;    

    cp ../FILES/* .
    
    cp ../1-Relaxation/MoS2.STRUCT_OUT ../1-Relaxation/MoS2.STRUCT_NEXT_ITER ../1-Relaxation/MoS2.CG ../1-Relaxation/MoS2.DM .
    cp MoS2.STRUCT_OUT MoS2.STRUCT_IN
    
    siesta 2-Static.fdf > siesta.out

    echo "STATIC RUN DONE!" > completed.staticCompleted

    cd ..
fi

######################## BANDS ########################
if [ "$BandsCond" = "T" ]; then
    cd 3-Bands

    find . -name 'co-*' -mmin +0.1 -exec rm {} \;
    find . -name 'eco-*' -mmin +0.1 -exec rm {} \;
    find . -name 'log-*' -mmin +0.1 -exec rm {} \;

    cp ../FILES/* .

    cp ../1-Relaxation/MoS2.STRUCT_OUT ../1-Relaxation/MoS2.STRUCT_NEXT_ITER ../1-Relaxation/MoS2.CG ../1-Relaxation/MoS2.DM .
    cp MoS2.STRUCT_OUT MoS2.STRUCT_IN
    

    siesta 3-Bands.fdf > siesta.out
    
    echo "BANDS RUN DONE!" > completed.bandsCompleted

    cd ..
fi

######################## LDOS ########################
if [ "$LDOSCond" = "T" ]; then
    cd LDOS

    find . -name 'co-*' -mmin +0.1 -exec rm {} \;
    find . -name 'eco-*' -mmin +0.1 -exec rm {} \;
    find . -name 'log-*' -mmin +0.1 -exec rm {} \;

    cp ../FILES/* .
    
    cp ../1-Relaxation/MoS2.STRUCT_OUT ../1-Relaxation/MoS2.STRUCT_NEXT_ITER ../1-Relaxation/MoS2.CG ../2-Static/MoS2.DM .
    cp MoS2.STRUCT_OUT MoS2.STRUCT_IN
    
    # If needed, add additional commands here

    cd ..
fi
