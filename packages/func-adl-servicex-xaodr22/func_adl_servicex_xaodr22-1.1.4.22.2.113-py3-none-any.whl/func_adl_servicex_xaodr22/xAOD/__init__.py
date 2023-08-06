from typing import Any, TYPE_CHECKING

class _load_me:
    """Python's type resolution system demands that types be already loaded
    when they are resolved by the type hinting system. Unfortunately,
    for us to do that for classes with circular references, this fails. In order
    to have everything loaded, we would be triggering the circular references
    during the import process.

    This loader gets around that by delay-loading the files that contain the
    classes, but also tapping into anyone that wants to load the classes.
    """

    def __init__(self, name: str):
        self._name = name
        self._loaded = None

    def __getattr__(self, __name: str) -> Any:
        if self._loaded is None:
            import importlib

            self._loaded = importlib.import_module(self._name)
        return getattr(self._loaded, __name)


# Class loads. We do this to both enable type checking and also
# get around potential circular references in the C++ data model.
if not TYPE_CHECKING:
    afpdata_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.afpdata_v1")
    afpproton_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.afpproton_v1")
    afpsihit_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.afpsihit_v2")
    afpsihitscluster_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.afpsihitscluster_v1")
    afptofhit_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.afptofhit_v1")
    afptoftrack_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.afptoftrack_v1")
    afptrack_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.afptrack_v2")
    afpvertex_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.afpvertex_v1")
    alfadata_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.alfadata_v1")
    bcmrawdata_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.bcmrawdata_v1")
    btagvertex_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.btagvertex_v1")
    btagging_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.btagging_v1")
    bunchconf_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.bunchconf_v1")
    cmmcphits_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cmmcphits_v1")
    cmmetsums_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cmmetsums_v1")
    cmmjethits_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cmmjethits_v1")
    cmxcphits_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cmxcphits_v1")
    cmxcptob_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cmxcptob_v1")
    cmxetsums_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cmxetsums_v1")
    cmxjethits_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cmxjethits_v1")
    cmxjettob_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cmxjettob_v1")
    cmxroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cmxroi_v1")
    cpmhits_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cpmhits_v1")
    cpmroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cpmroi_v1")
    cpmtobroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cpmtobroi_v1")
    cpmtower_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.cpmtower_v2")
    caloclusterbadchanneldata_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.caloclusterbadchanneldata_v1")
    calocluster_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.calocluster_v1")
    calorings_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.calorings_v1")
    calotower_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.calotower_v1")
    calovertexedclusterbase = _load_me("func_adl_servicex_xaodr22.xAOD.calovertexedclusterbase")
    calovertexedtopocluster = _load_me("func_adl_servicex_xaodr22.xAOD.calovertexedtopocluster")
    compositeparticle_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.compositeparticle_v1")
    cutbookkeeper_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.cutbookkeeper_v1")
    ditaujet_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.ditaujet_v1")
    egamma_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.egamma_v1")
    electron_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.electron_v1")
    emtauroi_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.emtauroi_v2")
    eventinfo_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.eventinfo_v1")
    forwardeventinfo_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.forwardeventinfo_v1")
    hieventshape_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.hieventshape_v2")
    iparticle = _load_me("func_adl_servicex_xaodr22.xAOD.iparticle")
    jemetsums_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.jemetsums_v2")
    jemhits_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.jemhits_v1")
    jemroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.jemroi_v1")
    jemtobroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.jemtobroi_v1")
    jetconstituent = _load_me("func_adl_servicex_xaodr22.xAOD.jetconstituent")
    jetconstituentvector = _load_me("func_adl_servicex_xaodr22.xAOD.jetconstituentvector")
    jetelement_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.jetelement_v2")
    jetroi_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.jetroi_v2")
    jet_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.jet_v1")
    klfitterresult = _load_me("func_adl_servicex_xaodr22.xAOD.klfitterresult")
    l1toporawdata_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.l1toporawdata_v1")
    l1toposimresults_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.l1toposimresults_v1")
    l2combinedmuon_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.l2combinedmuon_v1")
    l2isomuon_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.l2isomuon_v1")
    l2standalonemuon_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.l2standalonemuon_v2")
    lumiblockrange_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.lumiblockrange_v1")
    mbtsmodule_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.mbtsmodule_v1")
    missinget_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.missinget_v1")
    muonroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.muonroi_v1")
    muonsegment_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.muonsegment_v1")
    muon_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.muon_v1")
    neutralparticle_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.neutralparticle_v1")
    pfo_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.pfo_v1")
    particle_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.particle_v1")
    photon_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.photon_v1")
    pseudotopresult = _load_me("func_adl_servicex_xaodr22.xAOD.pseudotopresult")
    rodheader_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.rodheader_v2")
    ringsetconf_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.ringsetconf_v1")
    ringset_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.ringset_v1")
    sctrawhitvalidation_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.sctrawhitvalidation_v1")
    slowmuon_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.slowmuon_v1")
    systematicevent = _load_me("func_adl_servicex_xaodr22.xAOD.systematicevent")
    taujet_v3 = _load_me("func_adl_servicex_xaodr22.xAOD.taujet_v3")
    tautrack_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.tautrack_v1")
    trackcalocluster_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trackcalocluster_v1")
    trackjacobian_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trackjacobian_v1")
    trackmeasurementvalidation_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trackmeasurementvalidation_v1")
    trackmeasurement_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trackmeasurement_v1")
    trackparameters_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trackparameters_v1")
    trackparticleclusterassociation_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trackparticleclusterassociation_v1")
    trackparticle_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trackparticle_v1")
    trackstatevalidation_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trackstatevalidation_v1")
    trackstate_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trackstate_v1")
    trigbphys_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigbphys_v1")
    trigcalocluster_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigcalocluster_v1")
    trigcomposite_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigcomposite_v1")
    trigemcluster_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigemcluster_v1")
    trigelectron_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigelectron_v1")
    trighisto2d_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trighisto2d_v1")
    trigmissinget_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigmissinget_v1")
    trigpassbits_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigpassbits_v1")
    trigphoton_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigphoton_v1")
    trigrnnoutput_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.trigrnnoutput_v2")
    trigringerrings_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.trigringerrings_v2")
    trigspacepointcounts_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigspacepointcounts_v1")
    trigt2mbtsbits_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigt2mbtsbits_v1")
    trigt2zdcsignals_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigt2zdcsignals_v1")
    trigtrackcounts_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigtrackcounts_v1")
    trigvertexcounts_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trigvertexcounts_v1")
    triggermenujson_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.triggermenujson_v1")
    triggermenu_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.triggermenu_v1")
    triggertower_v2 = _load_me("func_adl_servicex_xaodr22.xAOD.triggertower_v2")
    trutheventbase_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.trutheventbase_v1")
    truthevent_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.truthevent_v1")
    truthmetadata_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.truthmetadata_v1")
    truthparticle_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.truthparticle_v1")
    truthpileupevent_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.truthpileupevent_v1")
    truthvertex_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.truthvertex_v1")
    uncalibratedmeasurement_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.uncalibratedmeasurement_v1")
    vertex_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.vertex_v1")
    zdcmodule_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.zdcmodule_v1")
    efexemroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.efexemroi_v1")
    efextauroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.efextauroi_v1")
    efextower_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.efextower_v1")
    gfexglobalroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.gfexglobalroi_v1")
    gfexjetroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.gfexjetroi_v1")
    gfextower_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.gfextower_v1")
    jfexfwdelroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.jfexfwdelroi_v1")
    jfexlrjetroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.jfexlrjetroi_v1")
    jfexmetroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.jfexmetroi_v1")
    jfexsrjetroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.jfexsrjetroi_v1")
    jfexsumetroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.jfexsumetroi_v1")
    jfextauroi_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.jfextauroi_v1")
    jfextower_v1 = _load_me("func_adl_servicex_xaodr22.xAOD.jfextower_v1")
else:
    from . import afpdata_v1
    from . import afpproton_v1
    from . import afpsihit_v2
    from . import afpsihitscluster_v1
    from . import afptofhit_v1
    from . import afptoftrack_v1
    from . import afptrack_v2
    from . import afpvertex_v1
    from . import alfadata_v1
    from . import bcmrawdata_v1
    from . import btagvertex_v1
    from . import btagging_v1
    from . import bunchconf_v1
    from . import cmmcphits_v1
    from . import cmmetsums_v1
    from . import cmmjethits_v1
    from . import cmxcphits_v1
    from . import cmxcptob_v1
    from . import cmxetsums_v1
    from . import cmxjethits_v1
    from . import cmxjettob_v1
    from . import cmxroi_v1
    from . import cpmhits_v1
    from . import cpmroi_v1
    from . import cpmtobroi_v1
    from . import cpmtower_v2
    from . import caloclusterbadchanneldata_v1
    from . import calocluster_v1
    from . import calorings_v1
    from . import calotower_v1
    from . import calovertexedclusterbase
    from . import calovertexedtopocluster
    from . import compositeparticle_v1
    from . import cutbookkeeper_v1
    from . import ditaujet_v1
    from . import egamma_v1
    from . import electron_v1
    from . import emtauroi_v2
    from . import eventinfo_v1
    from . import forwardeventinfo_v1
    from . import hieventshape_v2
    from . import iparticle
    from . import jemetsums_v2
    from . import jemhits_v1
    from . import jemroi_v1
    from . import jemtobroi_v1
    from . import jetconstituent
    from . import jetconstituentvector
    from . import jetelement_v2
    from . import jetroi_v2
    from . import jet_v1
    from . import klfitterresult
    from . import l1toporawdata_v1
    from . import l1toposimresults_v1
    from . import l2combinedmuon_v1
    from . import l2isomuon_v1
    from . import l2standalonemuon_v2
    from . import lumiblockrange_v1
    from . import mbtsmodule_v1
    from . import missinget_v1
    from . import muonroi_v1
    from . import muonsegment_v1
    from . import muon_v1
    from . import neutralparticle_v1
    from . import pfo_v1
    from . import particle_v1
    from . import photon_v1
    from . import pseudotopresult
    from . import rodheader_v2
    from . import ringsetconf_v1
    from . import ringset_v1
    from . import sctrawhitvalidation_v1
    from . import slowmuon_v1
    from . import systematicevent
    from . import taujet_v3
    from . import tautrack_v1
    from . import trackcalocluster_v1
    from . import trackjacobian_v1
    from . import trackmeasurementvalidation_v1
    from . import trackmeasurement_v1
    from . import trackparameters_v1
    from . import trackparticleclusterassociation_v1
    from . import trackparticle_v1
    from . import trackstatevalidation_v1
    from . import trackstate_v1
    from . import trigbphys_v1
    from . import trigcalocluster_v1
    from . import trigcomposite_v1
    from . import trigemcluster_v1
    from . import trigelectron_v1
    from . import trighisto2d_v1
    from . import trigmissinget_v1
    from . import trigpassbits_v1
    from . import trigphoton_v1
    from . import trigrnnoutput_v2
    from . import trigringerrings_v2
    from . import trigspacepointcounts_v1
    from . import trigt2mbtsbits_v1
    from . import trigt2zdcsignals_v1
    from . import trigtrackcounts_v1
    from . import trigvertexcounts_v1
    from . import triggermenujson_v1
    from . import triggermenu_v1
    from . import triggertower_v2
    from . import trutheventbase_v1
    from . import truthevent_v1
    from . import truthmetadata_v1
    from . import truthparticle_v1
    from . import truthpileupevent_v1
    from . import truthvertex_v1
    from . import uncalibratedmeasurement_v1
    from . import vertex_v1
    from . import zdcmodule_v1
    from . import efexemroi_v1
    from . import efextauroi_v1
    from . import efextower_v1
    from . import gfexglobalroi_v1
    from . import gfexjetroi_v1
    from . import gfextower_v1
    from . import jfexfwdelroi_v1
    from . import jfexlrjetroi_v1
    from . import jfexmetroi_v1
    from . import jfexsrjetroi_v1
    from . import jfexsumetroi_v1
    from . import jfextauroi_v1
    from . import jfextower_v1

# Include sub-namespace items
from . import TruthParticle_v1
from . import EventInfo_v1
from . import TruthEvent_v1