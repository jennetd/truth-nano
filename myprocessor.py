import time

import coffea.processor as processor
import hist
from coffea.analysis_tools import PackedSelection, Weights
from coffea.nanoevents import NanoAODSchema, NanoEventsFactory
from coffea.nanoevents.methods import nanoaod

NanoAODSchema.warn_missing_crossrefs = False

import pickle
import re

import awkward as ak
import numpy as np
import pandas as pd
import json

def update(events, collections):
    """Return a shallow copy of events array with some collections swapped out"""
    out = events
    for name, value in collections.items():
        out = ak.with_field(out, value, name)
    return out

# Look at ProcessorABC to see the expected methods and what they are supposed to do
class MyProcessor(processor.ProcessorABC):
    def __init__(self, isMC=False):
        ################################
        # INITIALIZE COFFEA PROCESSOR
        ################################
            
        ak.behavior.update(nanoaod.behavior)

        self.make_output = lambda: { 
            "q1pt": hist.Hist(
                hist.axis.Regular(200, 0, 1000, name="q1pt", label=r"Quark 1 $p_{T}$ [GeV]"),
                storage=hist.storage.Weight()
            ),
            "q2pt": hist.Hist(
                hist.axis.Regular(200, 0, 1000, name="q2pt", label=r"Quark 2 $p_{T}$ [GeV]"),
                storage=hist.storage.Weight()
            ),
            "vpt": hist.Hist(
                hist.axis.Regular(200, 0, 1000, name="vpt", label=r"V $p_{T}$ [GeV]"),
                storage=hist.storage.Weight()
            ),
            "detaqq": hist.Hist(
                hist.axis.Regular(200, -6, 6, name="detaqq", label=r"$\Delta\eta_{qq}$"),
                storage=hist.storage.Weight()
            ),
            "dphiqq": hist.Hist(
                hist.axis.Regular(200, -3.15, 3.15, name="dphiqq", label=r"$\Delta\phi_{qq}$"),
                storage=hist.storage.Weight()
            ),
            "mqq": hist.Hist(
                hist.axis.Regular(200, 0, 5000, name="mqq", label=r"$m_{qq}$ [GeV]"),
                storage=hist.storage.Weight()
            ),
            
            "EventCount": processor.value_accumulator(int),
        }
        
    def process(self, events):
        
        output = self.make_output()

        ##################
        # OBJECT SELECTION
        ##################

        # Nothing for now, only truth particles

        particles = events.LHEPart
        v = ak.firsts(particles[(particles.pdgId == 23) | (abs(particles.pdgId) == 24)])

        outgoing = particles[particles.status == 1]
        quarks = outgoing[outgoing.pdgId<=6]

        q1 = ak.firsts(quarks[:,0:1])
        q2 = ak.firsts(quarks[:,1:2])

        mqq = (q1+q2).mass
        detaqq = q1.eta - q2.eta
        dphiqq = q1.delta_phi(q2)

        #####################
        # EVENT SELECTION
        #####################

        # create a PackedSelection object
        # this will help us later in composing the boolean selections easily
        selection = PackedSelection()

        # Nothing for now, everything from generator

        ################
        # EVENT WEIGHTS
        ################

        # create a processor Weights object, with the same length as the number of events in the chunk
        weights = Weights(len(events))
        weights.add('genweight', events.genWeight)

        ###################
        # FILL HISTOGRAMS
        ###################
        
        #output['q1pt'].fill(q1pt=q1.pt,
        #                    weight=weights.weight()
        #                    )
        #output['q2pt'].fill(q2pt=q2.pt,
        #                    weight=weights.weight()
        #                    )
        output['vpt'].fill(vpt=v.pt,
                           weight=weights.weight()
                          )
        #output['detaqq'].fill(detaqq=detaqq,
        #                      weight=weights.weight()
        #                     )
        #output['dphiqq'].fill(dphiqq=dphiqq,
        #                      weight=weights.weight()
        #                     )
        #output['mqq'].fill(mqq=mqq,
        #                   weight=weights.weight()
        #                  )
            
        # End if no LHE weight
    
        output["EventCount"] = len(events)
    
        return output

    def postprocess(self, accumulator):
        return accumulator
