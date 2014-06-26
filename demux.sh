if [ -z "$(md5sum reads/CAGRF5704/BJP-277-A_D10GVACXX_NoIndex_L002_R1.fastq.gz | grep e3a3769a21df23593f1d959cd9783dd5)" ]
then
	echo "File md5sum isn't e3a3769a21df23593f1d959cd9783dd5"
fi
mkdir out2
pigz -dcp3 reads/CAGRF5704/BJP-277-A_D10GVACXX_NoIndex_L002_R1.fastq.gz  |python demux.py /dev/stdin out2/%s.fq
time python sort_leftovers.py out2/NOBCD.fq >rebarcoded.fq
