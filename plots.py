from collections import namedtuple
import config
from math import pi
import os
import ROOT
import style

class Sample(object):
  def __init__(self, folder, title, color, markerstyle):
    self.folder = folder
    self.title = title
    self.color = color
    self.markerstyle = markerstyle
    self.tree = ROOT.TChain("SelectedTree")
    for i in range(1, 11):
      self.tree.Add(os.path.join("rootfiles", self.folder, "cmsgrid_{}.root".format(i)))
    self.__hists = None

  def hists(self, plots):
    if self.__hists is None:
      hists = {}
      for plot in plots:
        hists[plot] = plot.hist(self.folder)
        hists[plot].SetLineColor(self.color)
        hists[plot].SetMarkerColor(self.color)
        hists[plot].SetMarkerStyle(self.markerstyle)

      length = self.tree.GetEntries()
      for i, entry in enumerate(self.tree, start=1):
        for plot, h in hists.iteritems():
          h.Fill(plot.getval(self.tree))
        if i%10000 == 0 or i == length:
          print i, "/", length

      self.__hists = hists

    return self.__hists

  def addtolegend(self, legend):
    if self.__hists is None:
      raise ValueError("need to fill hists first!")
    legend.AddEntry(self.__hists.values()[0], self.title, "lp")

samples = [
           Sample("JHUGen_VBF_m750_ZZ", "ZZ", 2, 24),
           Sample("JHUGen_VBF_m750_Zgs", "Z#gamma", ROOT.kGreen+3, 25),
           Sample("JHUGen_VBF_m750_gsgs_nodecay", "#gamma#gamma", 4, 26),
           Sample("JHUGen_VBF_m750_WW", "WW", 6, 27),
           Sample("JHUGen_HJJ_m750_gg_deltaR", "gg", ROOT.kViolet, 28),
          ]

class Plot(object):
  def __init__(self, name, title, bins, min, max, function=None):
    self.name = name
    self.title = title
    self.bins = bins
    self.min = min
    self.max = max
    self.function = function

  def hist(self, appendname):
    h = ROOT.TH1F(self.name + "_" + appendname, self.title, self.bins, self.min, self.max)
    h.SetDirectory(0)
    return h

  def getval(self, t):
    result = getattr(t, self.name)
    if self.function is not None:
      result = self.function(result)
    return result

plots = [
         Plot("GenhelcosthetaV1_VBF", "cos#theta_{1}^{VBF}", 100, -1, 1),
         Plot("GenhelcosthetaV2_VBF", "cos#theta_{2}^{VBF}", 100, -1, 1),
         Plot("Genhelphi_VBF", "#Phi^{VBF}", 100, -pi, pi),
         Plot("GenQ_V1", "q_{1}^{VBF} [GeV]", 100, 0, 1000, lambda x: x),
         Plot("GenQ_V2", "q_{2}^{VBF} [GeV]", 100, 0, 1000, lambda x: x),
        ]

def makeplots():
  hstack = {}
  for plot in plots:
    hstack[plot] = ROOT.THStack(plot.name, plot.title)

  l = style.TLegend(.6, .7, .9, .9)

  for sample in samples:
    hists = sample.hists(plots)
    for plot in plots:
      hstack[plot].Add(hists[plot])
    sample.addtolegend(l)

  c1 = ROOT.TCanvas()
  for plot in plots:
    hstack[plot].Draw("C P0 nostack")
    hstack[plot].GetXaxis().SetTitle(plot.title)
    l.Draw()
    for ext in "png eps root pdf".split():
      c1.SaveAs(os.path.join(config.maindir, "plots/VBF/{}.{}".format(plot.name, ext)))

if __name__ == "__main__":
  makeplots()
