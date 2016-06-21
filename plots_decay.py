import contextlib
import errno
import os
import ROOT
import tempfile

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

@contextlib.contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
with cd("CMSJHU_AnalysisMacros/MCProductionValidation"):
    ROOT.gROOT.Macro("loadLib.C")
ROOT.gROOT.LoadMacro("angularDistributions_spin0_ggH.cc+")

#void angularDistributions_spin0_ggH(string cinput, double g1Re=1, double g2Re=0, double g4Re=0, double g1L1Re=0, double g2Im=0,
#                                    double g4Im=0, double g1L1Im=0, int nbins=80, double mPOLE = 125., int useTaus=0,
#                                    vector<string> morecinputs = vector<string>())

class AngularDistributions(object):
    validdecaymodes = ["ZZ4l", "WW2l2nu", "ZG2l", "GG"]
    def __init__(self, folder, decaymode, plotsdir, g1=1, g2=0, g4=0, g1L1=0, nbins=80, mPOLE=750., useTaus=False):
        self.files = [os.path.join(folder, file) for file in os.listdir(folder)]
        self.decaymode = decaymode
        assert self.decaymode in self.validdecaymodes
        self.plotsdir = plotsdir
        if os.path.exists(plotsdir) and os.listdir(plotsdir):
            return
        mkdir_p(plotsdir)
        open(os.path.join(plotsdir, "index.php"), "w")
        self.g1 = g1
        self.g2 = g2
        self.g4 = g4
        self.g1L1 = g1L1
        self.nbins = nbins
        self.mPOLE = mPOLE
        self.useTaus = useTaus

#    def __enter__(self):
        self.tmpdir = tempfile.mkdtemp()
        self.cinput = os.path.join(self.tmpdir, "{}.root".format(decaymode))
        os.symlink(os.path.abspath(self.files[0]), self.cinput)
        os.symlink(os.path.abspath(plotsdir), os.path.join(self.tmpdir, "Validation"))

        self.morecinputs = ROOT.std.vector(ROOT.std.string)()
        for f in self.files[1:]:
            self.morecinputs.push_back(f)

        self.args = self.cinput, self.g1.real, self.g2.real, self.g4.real, self.g1L1.real, self.g2.imag, self.g4.imag, self.g1L1.imag, self.nbins, self.mPOLE, self.useTaus, self.morecinputs

        self.incontextmanager = True

#    def __call__(self):
#        if not self.incontextmanager:
#            raise RuntimeError("Can only call AngularDistributions within context manager!")
        ROOT.angularDistributions_spin0_ggH(*self.args)

#    def __exit__(self):
#        self.incontextmanager = False


#ggH 0+
AngularDistributions("rootfiles/JHUGen_ggH_m750_ZZ", "ZZ4l", "plots/decay/ZZ", g1=0, g2=1)
AngularDistributions("rootfiles/JHUGen_ggH_m750_WW", "WW2l2nu", "plots/decay/WW", g1=0, g2=1)
AngularDistributions("rootfiles/JHUGen_ggH_m750_gg", "GG", "plots/decay/gammagamma", g1=0, g2=1)
AngularDistributions("rootfiles/JHUGen_ggH_m750_Zg", "ZG2l", "plots/decay/Zgamma", g1=0, g2=1)
