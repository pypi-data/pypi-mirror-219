from ecoengine.objects.SystemConfig import SystemConfig
from ecoengine.objects.SimulationRun import SimulationRun
import numpy as np
from ecoengine.objects.Building import Building
from ecoengine.constants.Constants import *
from ecoengine.objects.systemConfigUtils import mixVolume, hrToMinList, getPeakIndices, checkHeatHours

class MultiPass(SystemConfig):
    def __init__(self, storageT_F, defrostFactor, percentUseable, compRuntime_hr, aquaFract, building,
                 doLoadShift = False, loadShiftPercent = 1, loadShiftSchedule = None, loadUpHours = None, aquaFractLoadUp = None, 
                 aquaFractShed = None, loadUpT_F = None, systemModel = None, numHeatPumps = None, PVol_G_atStorageT = None, PCap_kBTUhr = None):
        # set static aquastat fractions, ignore inputs
        aquaFract = 0.15
        aquaFractLoadUp = 0.15
        aquaFractShed = 0.3
        
        super().__init__(storageT_F, defrostFactor, percentUseable, compRuntime_hr, aquaFract, building, doLoadShift, 
                loadShiftPercent, loadShiftSchedule, loadUpHours, aquaFractLoadUp, aquaFractShed, loadUpT_F, systemModel, 
                numHeatPumps, PVol_G_atStorageT, PCap_kBTUhr)
        
        # Set inlet water temperature equal to average(hot storage temperature, city water temperature) 
        # self.inletWaterT_F = (building.incomingT_F + self.storageT_F) / 2.0

    # def getInitializedSimulation(self, building : Building, initPV=None, initST=None, minuteIntervals = 1, nDays = 3):
    #     simRun = super().getInitializedSimulation(building, initPV, initST, minuteIntervals, nDays)
    #     return simRun

    def runOneSystemStep(self, simRun : SimulationRun, i, minuteIntervals = 1, oat = None):
        incomingWater_T = (simRun.getIncomingWaterT(i) + self.storageT_F) / 2.0
        if not (oat is None or self.perfMap is None):
            # set primary system capacity based on outdoor ait temp and incoming water temp 
            self.setCapacity(oat = oat, incomingWater_T = incomingWater_T)
            simRun.addHWGen((1000 * self.PCap_kBTUhr / rhoCp / (simRun.building.supplyT_F - incomingWater_T) \
               * self.defrostFactor)/(60/minuteIntervals))
        mixedDHW = mixVolume(simRun.hwDemand[i], simRun.mixedStorT_F, incomingWater_T, simRun.building.supplyT_F) 
        mixedGHW = mixVolume(simRun.hwGenRate, simRun.mixedStorT_F, incomingWater_T, simRun.building.supplyT_F)
        # Account for recirculation losses
        recircLoss_G = (simRun.building.recirc_loss / (rhoCp * (simRun.building.supplyT_F - simRun.getIncomingWaterT(i)))) / (60/minuteIntervals)

        simRun.pheating, simRun.pV[i], simRun.pGen[i], simRun.pRun[i] = self.runOnePrimaryStep(pheating = simRun.pheating, 
                                                                                               V0 = simRun.V0, 
                                                                                               Vtrig = simRun.Vtrig[i], 
                                                                                               Vcurr = simRun.pV[i-1], 
                                                                                               hw_out = mixedDHW + recircLoss_G, 
                                                                                               hw_in = mixedGHW, 
                                                                                               Vtrig_previous = simRun.Vtrig[i-1],
                                                                                               minuteIntervals = minuteIntervals)