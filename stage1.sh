set -e
set -u

# MAD_PATH=$(realpath `dirname $0`)
MAD_PATH=M-MAD
system=$1
lp=$2
start=$3
version=$4


python3 $MAD_PATH/code/stage1.py \
    -i $MAD_PATH/data/input.${lp}.${system}_v2.txt \
    -o $MAD_PATH/data/output_${lp}_${system}_${version} \
    -lp $lp \
    -k  ##OPENAI KEY## \
    -s $start