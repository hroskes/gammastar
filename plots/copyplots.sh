rm $(find . -name index.php)
rsync -az --exclude copyplots.sh ./ hroskes@lxplus.cern.ch:www/JHUGen/gammastar
