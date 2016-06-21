if [ -d CMSSW_7_6_3/python ]; then exit; fi

tmpdir=$(mktemp -d)
mv CMSSW_7_6_3/src/ZZMatrixElement $tmpdir
mv CMSSW_7_6_3/.gitignore $tmpdir
rmdir -p CMSSW_7_6_3/src
scram p CMSSW CMSSW_7_6_3
mv $tmpdir/ZZMatrixElement CMSSW_7_6_3/src
mv $tmpdir/.gitignore CMSSW_7_6_3/
cd CMSSW_7_6_3/src
eval $(scram ru -sh)
scramb -j 30
cd ../..
cd CMSJHU_AnalysisMacros/JHUSpinWidthPaper_2015/LHEAnalyzer/
make all
cd ../..
echo 'NNPDFDriver.o
libmcfm_7p0.so
.gitignore' > CMSSW_7_6_3/src/ZZMatrixElement/MELA/data/slc6_amd64_gcc493/.gitignore
