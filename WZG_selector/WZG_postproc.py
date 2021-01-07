#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer

# from WZG_Module import * 
import WZG_Module as WZG

import argparse
import re
import optparse
import DAS_filesearch as search


parser = argparse.ArgumentParser(description='baseline selection')
parser.add_argument('-f', dest='file', default='', help='local file input')
parser.add_argument('-y', dest='year', default='2016', help='year of dataset')
parser.add_argument('-m', dest='mode', default='local', help='runmode local/condor')
parser.add_argument('-n', dest='name', default='test', help='dataset name in short, currently support' 
    '\n tZq_ll'
    '\n WZ'
    '\n TTWJetsToLNu'
    '\n ttZJets')
args = parser.parse_args()

print "mode: ", args.mode
print "year: ", args.year
print "dataset_name: ", args.name




# classify input files
if args.file == '':

    print "no local file input, use DAS file"
    dataset = ''
    if args.name == 'tZq_ll':
        if args.year == '2016': dataset = "/tZq_ll_4f_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM"
    elif args.name == 'WZ':
        if args.year == '2016': dataset = "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"
    elif args.name == 'TTWJetsToLNu':
        if args.year == '2016': dataset = "/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM"
    elif args.name == 'ttZJets':
        if args.year == '2016': dataset = "/ttZJets_13TeV_madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"
    elif args.name == 'SingleElectron':
        if args.year == '2017': dataset = "/SingleElectron/Run2017B-Nano1June2019-v1/NANOAOD"
    elif args.name == 'SingleMuon':
        if args.year == '2017': dataset = "/SingleMuon/Run2017B-Nano1June2019-v1/NANOAOD"
    else:
        print "unknown dataset name"
        sys.exit(0)


    files = []

    # condor can't use dasgoclient, so we should upload the filepath for condor run. sth. different with local run here
    if 'condor' in args.mode:
        pass

    else:
        search.getLFN(dataset, args.name+"_"+args.year)
        with open ("filepath_"+args.name+"_"+args.year+".txt","r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.rstrip('\n')
                files.append(search.getValidSite(line)+line)


    print 'from DAS input files: ',files

    p=PostProcessor(".",files,branchsel="WZG_input_branch.txt",modules=[countHistogramsProducer(),WZG.WZG_Producer()],provenance=True,outputbranchsel="WZG_output_branch.txt")
    p.run()


else:    
    files = []
    # condor can't use dasgoclient, so we should upload the filepath for condor run. sth. different with local run here
    # designed for single file here in order to run in parallel
    if 'condor' in args.mode:
        files.append(search.getValidSite(args.file) + args.file)
        print 'input files: ',files
        print 'test'

    # local specific file input, also support root://xxx    
    else:
        if not ',' in args.file:
            files.append(args.file)

        else:
            for i in args.file.split(','):
                files.append(i)

        print 'input files: ',files

    p=PostProcessor(".",files,branchsel="WZG_input_branch.txt",modules=[countHistogramsProducer(),WZG.WZG_Producer()],provenance=True,outputbranchsel="WZG_output_branch.txt")
    p.run()



print "MET_pass","\t","=","\t",WZG.MET_pass
print "muon_pass","\t","=","\t",WZG.muon_pass
print "electron_pass","\t","=","\t",WZG.electron_pass
print "photon_pass","\t","=","\t",WZG.photon_pass
print
print "none_photon_reject","\t","=","\t",WZG.none_photon_reject
print "none_lepton_reject","\t","=","\t",WZG.none_lepton_reject
print "none_2lepton_reject","\t","=","\t",WZG.none_2lepton_reject
print "different_charge_reject","\t","=","\t",WZG.different_charge_reject
print "minus_mll ","\t","=","\t",WZG.minus_mll
print "all reject",WZG.none_photon_reject+WZG.none_2lepton_reject+WZG.different_charge_reject+WZG.minus_mll+WZG.mll_reject+WZG.pt_reject+WZG.njet_reject


print "emu_pass","\t","=","\t",WZG.emu_pass
print "ee_pass","\t","=","\t",WZG.ee_pass
print "mumu_pass","\t","=","\t",WZG.mumu_pass
print "btagjet_reject","\t","=","\t",WZG.btagjet_reject
print "deltar_reject","\t","=","\t",WZG.deltar_reject
print "pt_reject","\t","=","\t",WZG.pt_reject
print "mll_reject","\t","=","\t",WZG.mll_reject
print "njet_reject","\t","=","\t",WZG.njet_reject

