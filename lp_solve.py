#!/usr/bin/env python3

import collections
import dataclasses
import json
import math
import subprocess
import sys

resource_scores = {
	"Desc_OreIron_C": 70_380,
	"Desc_OreCopper_C": 28_860,
	"Desc_Stone_C": 52_860,
	"Desc_Coal_C": 30_900,
	"Desc_OreGold_C": 11_040,
	"Desc_LiquidOil_C": 11_700,
	"Desc_RawQuartz_C": 10_500,
	"Desc_Sulfur_C": 6_840,
	"Desc_OreBauxite_C": 9_780,
	"Desc_OreUranium_C": 2_100,
	"Desc_NitrogenGas_C": 12_000,
}

building_scores = {
	"Desc_AssemblerMk1_C": 1,
	"Desc_Beam_C": 1,
	"Desc_Beam_Connector_C": 1,
	"Desc_Beam_Connector_Double_C": 1,
	"Desc_Beam_Painted_C": 1,
	"Desc_Beam_Support_C": 1,
	"Desc_Blender_C": 1,
	"Desc_CatwalkCross_C": 1,
	"Desc_CatwalkRamp_C": 1,
	"Desc_CatwalkStairs_C": 1,
	"Desc_CatwalkStraight_C": 1,
	"Desc_CatwalkT_C": 1,
	"Desc_CatwalkTurn_C": 1,
	"Desc_CeilingLight_C": 1,
	"Desc_Concrete_Barrier_01_C": 1,
	"Desc_ConstructorMk1_C": 1,
	"Desc_ConveyorAttachmentMerger_C": 1,
	"Desc_ConveyorAttachmentSplitterProgrammable_C": 1,
	"Desc_ConveyorAttachmentSplitterSmart_C": 1,
	"Desc_ConveyorAttachmentSplitter_C": 1,
	"Desc_ConveyorBeltMk1_C": 1,
	"Desc_ConveyorBeltMk2_C": 1,
	"Desc_ConveyorBeltMk3_C": 1,
	"Desc_ConveyorBeltMk4_C": 1,
	"Desc_ConveyorBeltMk5_C": 1,
	"Desc_ConveyorLiftMk1_C": 1,
	"Desc_ConveyorLiftMk2_C": 1,
	"Desc_ConveyorLiftMk3_C": 1,
	"Desc_ConveyorLiftMk4_C": 1,
	"Desc_ConveyorLiftMk5_C": 1,
	"Desc_ConveyorPoleStackable_C": 1,
	"Desc_ConveyorPoleWall_C": 1,
	"Desc_ConveyorPole_C": 1,
	"Desc_CyberWagon_C": 1,
	"Desc_DroneStation_C": 1,
	"Desc_DroneTransport_C": 1,
	"Desc_Explorer_C": 1,
	"Desc_Fence_01_C": 1,
	"Desc_Flat_Frame_01_C": 1,
	"Desc_FloodlightPole_C": 1,
	"Desc_FloodlightWall_C": 1,
	"Desc_FoundationGlass_01_C": 1,
	"Desc_FoundationPassthrough_Hypertube_C": 1,
	"Desc_FoundationPassthrough_Lift_C": 1,
	"Desc_FoundationPassthrough_Pipe_C": 1,
	"Desc_Foundation_8x1_01_C": 1,
	"Desc_Foundation_8x2_01_C": 1,
	"Desc_Foundation_8x4_01_C": 1,
	"Desc_Foundation_Asphalt_8x1_C": 1,
	"Desc_Foundation_Asphalt_8x2_C": 1,
	"Desc_Foundation_Asphalt_8x4_C": 1,
	"Desc_Foundation_ConcretePolished_8x1_C": 1,
	"Desc_Foundation_ConcretePolished_8x2_2_C": 1,
	"Desc_Foundation_ConcretePolished_8x4_C": 1,
	"Desc_Foundation_Concrete_8x1_C": 1,
	"Desc_Foundation_Concrete_8x2_C": 1,
	"Desc_Foundation_Concrete_8x4_C": 1,
	"Desc_Foundation_Frame_01_C": 1,
	"Desc_Foundation_Metal_8x1_C": 1,
	"Desc_Foundation_Metal_8x2_C": 1,
	"Desc_Foundation_Metal_8x4_C": 1,
	"Desc_FoundryMk1_C": 1,
	"Desc_FrackingExtractor_C": 1,
	"Desc_FrackingSmasher_C": 1,
	"Desc_FreightWagon_C": 1,
	"Desc_Gate_Automated_8x4_C": 1,
	"Desc_GeneratorBiomass_C": 1,
	"Desc_GeneratorCoal_C": 1,
	"Desc_GeneratorFuel_C": 1,
	"Desc_GeneratorGeoThermal_C": 1,
	"Desc_GeneratorNuclear_C": 1,
	"Desc_HadronCollider_C": 1,
	"Desc_HyperPoleStackable_C": 1,
	"Desc_HyperTubeWallHole_C": 1,
	"Desc_HyperTubeWallSupport_C": 1,
	"Desc_IndustrialTank_C": 1,
	"Desc_InvertedRamp_Asphalt_8x1_C": 1,
	"Desc_InvertedRamp_Asphalt_8x2_C": 1,
	"Desc_InvertedRamp_Asphalt_8x4_C": 1,
	"Desc_InvertedRamp_Concrete_8x1_C": 1,
	"Desc_InvertedRamp_Concrete_8x2_C": 1,
	"Desc_InvertedRamp_Concrete_8x4_C": 1,
	"Desc_InvertedRamp_DCorner_Asphalt_8x1_C": 1,
	"Desc_InvertedRamp_DCorner_Asphalt_8x2_C": 1,
	"Desc_InvertedRamp_DCorner_Asphalt_8x4_C": 1,
	"Desc_InvertedRamp_DCorner_Concrete_8x1_C": 1,
	"Desc_InvertedRamp_DCorner_Concrete_8x2_C": 1,
	"Desc_InvertedRamp_DCorner_Concrete_8x4_C": 1,
	"Desc_InvertedRamp_DCorner_Metal_8x1_C": 1,
	"Desc_InvertedRamp_DCorner_Metal_8x2_C": 1,
	"Desc_InvertedRamp_DCorner_Metal_8x4_C": 1,
	"Desc_InvertedRamp_DCorner_Polished_8x1_C": 1,
	"Desc_InvertedRamp_DCorner_Polished_8x2_C": 1,
	"Desc_InvertedRamp_DCorner_Polished_8x4_C": 1,
	"Desc_InvertedRamp_Metal_8x1_C": 1,
	"Desc_InvertedRamp_Metal_8x2_C": 1,
	"Desc_InvertedRamp_Metal_8x4_C": 1,
	"Desc_InvertedRamp_Polished_8x1_C": 1,
	"Desc_InvertedRamp_Polished_8x2_C": 1,
	"Desc_InvertedRamp_Polished_8x4_C": 1,
	"Desc_InvertedRamp_UCorner_Asphalt_8x1_C": 1,
	"Desc_InvertedRamp_UCorner_Asphalt_8x2_C": 1,
	"Desc_InvertedRamp_UCorner_Asphalt_8x4_C": 1,
	"Desc_InvertedRamp_UCorner_Concrete_8x1_C": 1,
	"Desc_InvertedRamp_UCorner_Concrete_8x2_C": 1,
	"Desc_InvertedRamp_UCorner_Concrete_8x4_C": 1,
	"Desc_InvertedRamp_UCorner_Metal_8x1_C": 1,
	"Desc_InvertedRamp_UCorner_Metal_8x2_C": 1,
	"Desc_InvertedRamp_UCorner_Metal_8x4_C": 1,
	"Desc_InvertedRamp_UCorner_Polished_8x1_C": 1,
	"Desc_InvertedRamp_UCorner_Polished_8x2_C": 1,
	"Desc_InvertedRamp_UCorner_Polished_8x4_C": 1,
	"Desc_JumpPadAdjustable_C": 1,
	"Desc_Ladder_C": 1,
	"Desc_LandingPad_C": 1,
	"Desc_LightsControlPanel_C": 1,
	"Desc_Locomotive_C": 1,
	"Desc_LookoutTower_C": 1,
	"Desc_Mam_C": 1,
	"Desc_ManufacturerMk1_C": 1,
	"Desc_MinerMk1_C": 1,
	"Desc_MinerMk2_C": 1,
	"Desc_MinerMk3_C": 1,
	"Desc_OilPump_C": 1,
	"Desc_OilRefinery_C": 1,
	"Desc_Packager_C": 1,
	"Desc_PillarBase_C": 1,
	"Desc_PillarBase_Small_C": 1,
	"Desc_PillarMiddle_C": 1,
	"Desc_PillarMiddle_Concrete_C": 1,
	"Desc_PillarMiddle_Frame_C": 1,
	"Desc_PillarTop_C": 1,
	"Desc_Pillar_Small_Concrete_C": 1,
	"Desc_Pillar_Small_Frame_C": 1,
	"Desc_Pillar_Small_Metal_C": 1,
	"Desc_PipeHyperStart_C": 1,
	"Desc_PipeHyperSupport_C": 1,
	"Desc_PipeHyper_C": 1,
	"Desc_PipeStorageTank_C": 1,
	"Desc_PipeSupportStackable_C": 1,
	"Desc_PipelineJunction_Cross_C": 1,
	"Desc_PipelineMK2_C": 1,
	"Desc_PipelinePumpMk2_C": 1,
	"Desc_PipelinePump_C": 1,
	"Desc_PipelineSupportWallHole_C": 1,
	"Desc_PipelineSupportWall_C": 1,
	"Desc_PipelineSupport_C": 1,
	"Desc_Pipeline_C": 1,
	"Desc_PowerLine_C": 1,
	"Desc_PowerPoleMk1_C": 1,
	"Desc_PowerPoleMk2_C": 1,
	"Desc_PowerPoleMk3_C": 1,
	"Desc_PowerPoleWallDoubleMk2_C": 1,
	"Desc_PowerPoleWallDoubleMk3_C": 1,
	"Desc_PowerPoleWallDouble_C": 1,
	"Desc_PowerPoleWallMk2_C": 1,
	"Desc_PowerPoleWallMk3_C": 1,
	"Desc_PowerPoleWall_C": 1,
	"Desc_PowerStorageMk1_C": 1,
	"Desc_PowerSwitch_C": 1,
	"Desc_QuarterPipeCorner_01_C": 1,
	"Desc_QuarterPipeCorner_02_C": 1,
	"Desc_QuarterPipeCorner_03_C": 1,
	"Desc_QuarterPipeCorner_04_C": 1,
	"Desc_QuarterPipe_02_C": 1,
	"Desc_QuarterPipe_C": 1,
	"Desc_RadarTower_C": 1,
	"Desc_Railing_01_C": 1,
	"Desc_RailroadBlockSignal_C": 1,
	"Desc_RailroadPathSignal_C": 1,
	"Desc_RailroadTrack_C": 1,
	"Desc_RampDouble_8x1_C": 1,
	"Desc_RampDouble_Asphalt_8x1_C": 1,
	"Desc_RampDouble_Asphalt_8x2_C": 1,
	"Desc_RampDouble_Asphalt_8x4_C": 1,
	"Desc_RampDouble_C": 1,
	"Desc_RampDouble_Concrete_8x1_C": 1,
	"Desc_RampDouble_Concrete_8x2_C": 1,
	"Desc_RampDouble_Concrete_8x4_C": 1,
	"Desc_RampDouble_Metal_8x1_C": 1,
	"Desc_RampDouble_Metal_8x2_C": 1,
	"Desc_RampDouble_Metal_8x4_C": 1,
	"Desc_RampDouble_Polished_8x1_C": 1,
	"Desc_RampDouble_Polished_8x2_C": 1,
	"Desc_RampDouble_Polished_8x4_C": 1,
	"Desc_RampInverted_8x1_C": 1,
	"Desc_RampInverted_8x1_Corner_01_C": 1,
	"Desc_RampInverted_8x1_Corner_02_C": 1,
	"Desc_RampInverted_8x2_01_C": 1,
	"Desc_RampInverted_8x2_Corner_01_C": 1,
	"Desc_RampInverted_8x2_Corner_02_C": 1,
	"Desc_RampInverted_8x4_Corner_01_C": 1,
	"Desc_RampInverted_8x4_Corner_02_C": 1,
	"Desc_Ramp_8x1_01_C": 1,
	"Desc_Ramp_8x2_01_C": 1,
	"Desc_Ramp_8x4_01_C": 1,
	"Desc_Ramp_8x4_Inverted_01_C": 1,
	"Desc_Ramp_8x8x8_C": 1,
	"Desc_Ramp_Asphalt_8x1_C": 1,
	"Desc_Ramp_Asphalt_8x2_C": 1,
	"Desc_Ramp_Asphalt_8x4_C": 1,
	"Desc_Ramp_Concrete_8x1_C": 1,
	"Desc_Ramp_Concrete_8x2_C": 1,
	"Desc_Ramp_Concrete_8x4_C": 1,
	"Desc_Ramp_Diagonal_8x1_01_C": 1,
	"Desc_Ramp_Diagonal_8x1_02_C": 1,
	"Desc_Ramp_Diagonal_8x2_01_C": 1,
	"Desc_Ramp_Diagonal_8x2_02_C": 1,
	"Desc_Ramp_Diagonal_8x4_01_C": 1,
	"Desc_Ramp_Diagonal_8x4_02_C": 1,
	"Desc_Ramp_DownCorner_Asphalt_8x1_C": 1,
	"Desc_Ramp_DownCorner_Asphalt_8x2_C": 1,
	"Desc_Ramp_DownCorner_Asphalt_8x4_C": 1,
	"Desc_Ramp_DownCorner_Concrete_8x1_C": 1,
	"Desc_Ramp_DownCorner_Concrete_8x2_C": 1,
	"Desc_Ramp_DownCorner_Concrete_8x4_C": 1,
	"Desc_Ramp_DownCorner_Metal_8x1_C": 1,
	"Desc_Ramp_DownCorner_Metal_8x2_C": 1,
	"Desc_Ramp_DownCorner_Metal_8x4_C": 1,
	"Desc_Ramp_DownCorner_Polished_8x1_C": 1,
	"Desc_Ramp_DownCorner_Polished_8x2_C": 1,
	"Desc_Ramp_DownCorner_Polished_8x4_C": 1,
	"Desc_Ramp_Frame_01_C": 1,
	"Desc_Ramp_Frame_Inverted_01_C": 1,
	"Desc_Ramp_Metal_8x1_C": 1,
	"Desc_Ramp_Metal_8x2_C": 1,
	"Desc_Ramp_Metal_8x4_C": 1,
	"Desc_Ramp_Polished_8x1_C": 1,
	"Desc_Ramp_Polished_8x2_C": 1,
	"Desc_Ramp_Polished_8x4_C": 1,
	"Desc_Ramp_UpCorner_Asphalt_8x1_C": 1,
	"Desc_Ramp_UpCorner_Asphalt_8x2_C": 1,
	"Desc_Ramp_UpCorner_Asphalt_8x4_C": 1,
	"Desc_Ramp_UpCorner_Concrete_8x1_C": 1,
	"Desc_Ramp_UpCorner_Concrete_8x2_C": 1,
	"Desc_Ramp_UpCorner_Concrete_8x4_C": 1,
	"Desc_Ramp_UpCorner_Metal_8x1_C": 1,
	"Desc_Ramp_UpCorner_Metal_8x2_C": 1,
	"Desc_Ramp_UpCorner_Metal_8x4_C": 1,
	"Desc_Ramp_UpCorner_Polished_8x1_C": 1,
	"Desc_Ramp_UpCorner_Polished_8x2_C": 1,
	"Desc_Ramp_UpCorner_Polished_8x4_C": 1,
	"Desc_ResourceSinkShop_C": 1,
	"Desc_ResourceSink_C": 1,
	"Desc_Roof_A_01_C": 1,
	"Desc_Roof_A_02_C": 1,
	"Desc_Roof_A_03_C": 1,
	"Desc_Roof_A_04_C": 1,
	"Desc_Roof_Orange_01_C": 1,
	"Desc_Roof_Orange_02_C": 1,
	"Desc_Roof_Orange_03_C": 1,
	"Desc_Roof_Orange_04_C": 1,
	"Desc_Roof_Tar_01_C": 1,
	"Desc_Roof_Tar_02_C": 1,
	"Desc_Roof_Tar_03_C": 1,
	"Desc_Roof_Tar_04_C": 1,
	"Desc_Roof_Window_01_C": 1,
	"Desc_Roof_Window_02_C": 1,
	"Desc_Roof_Window_03_C": 1,
	"Desc_Roof_Window_04_C": 1,
	"Desc_SmelterMk1_C": 1,
	"Desc_SpaceElevator_C": 1,
	"Desc_Stairs_Left_01_C": 1,
	"Desc_Stairs_Right_01_C": 1,
	"Desc_StandaloneWidgetSign_Huge_C": 1,
	"Desc_StandaloneWidgetSign_Large_C": 1,
	"Desc_StandaloneWidgetSign_Medium_C": 1,
	"Desc_StandaloneWidgetSign_Portrait_C": 1,
	"Desc_StandaloneWidgetSign_SmallVeryWide_C": 1,
	"Desc_StandaloneWidgetSign_SmallWide_C": 1,
	"Desc_StandaloneWidgetSign_Small_C": 1,
	"Desc_StandaloneWidgetSign_Square_C": 1,
	"Desc_StandaloneWidgetSign_Square_Small_C": 1,
	"Desc_StandaloneWidgetSign_Square_Tiny_C": 1,
	"Desc_SteelWall_8x1_C": 1,
	"Desc_SteelWall_8x4_C": 1,
	"Desc_SteelWall_8x4_Gate_01_C": 1,
	"Desc_SteelWall_8x4_Window_01_C": 1,
	"Desc_SteelWall_8x4_Window_02_C": 1,
	"Desc_SteelWall_8x4_Window_03_C": 1,
	"Desc_SteelWall_8x4_Window_04_C": 1,
	"Desc_SteelWall_FlipTris_8x1_C": 1,
	"Desc_SteelWall_FlipTris_8x2_C": 1,
	"Desc_SteelWall_FlipTris_8x4_C": 1,
	"Desc_SteelWall_FlipTris_8x8_C": 1,
	"Desc_SteelWall_Tris_8x1_C": 1,
	"Desc_SteelWall_Tris_8x2_C": 1,
	"Desc_SteelWall_Tris_8x4_C": 1,
	"Desc_SteelWall_Tris_8x8_C": 1,
	"Desc_StorageContainerMk1_C": 1,
	"Desc_StorageContainerMk2_C": 1,
	"Desc_StorageHazard_C": 1,
	"Desc_StorageMedkit_C": 1,
	"Desc_StoragePlayer_C": 1,
	"Desc_StreetLight_C": 1,
	"Desc_Tractor_C": 1,
	"Desc_TradingPost_C": 1,
	"Desc_TrainDockingStationLiquid_C": 1,
	"Desc_TrainDockingStation_C": 1,
	"Desc_TrainPlatformEmpty_02_C": 1,
	"Desc_TrainPlatformEmpty_C": 1,
	"Desc_TrainStation_C": 1,
	"Desc_TruckStation_C": 1,
	"Desc_Truck_C": 1,
	"Desc_Valve_C": 1,
	"Desc_WalkwayCross_C": 1,
	"Desc_WalkwayRamp_C": 1,
	"Desc_WalkwayStraight_C": 1,
	"Desc_WalkwayT_C": 1,
	"Desc_WalkwayTurn_C": 1,
	"Desc_WallSet_Steel_Angular_8x4_C": 1,
	"Desc_WallSet_Steel_Angular_8x8_C": 1,
	"Desc_Wall_8x4_01_C": 1,
	"Desc_Wall_8x4_02_C": 1,
	"Desc_Wall_Concrete_8x1_C": 1,
	"Desc_Wall_Concrete_8x4_C": 1,
	"Desc_Wall_Concrete_8x4_ConveyorHole_01_C": 1,
	"Desc_Wall_Concrete_8x4_ConveyorHole_02_C": 1,
	"Desc_Wall_Concrete_8x4_ConveyorHole_03_C": 1,
	"Desc_Wall_Concrete_8x4_Corner_01_C": 1,
	"Desc_Wall_Concrete_8x4_Window_01_C": 1,
	"Desc_Wall_Concrete_8x4_Window_02_C": 1,
	"Desc_Wall_Concrete_8x4_Window_03_C": 1,
	"Desc_Wall_Concrete_8x4_Window_04_C": 1,
	"Desc_Wall_Concrete_8x8_Corner_01_C": 1,
	"Desc_Wall_Concrete_Angular_8x4_C": 1,
	"Desc_Wall_Concrete_Angular_8x8_C": 1,
	"Desc_Wall_Concrete_CDoor_8x4_C": 1,
	"Desc_Wall_Concrete_FlipTris_8x1_C": 1,
	"Desc_Wall_Concrete_FlipTris_8x2_C": 1,
	"Desc_Wall_Concrete_FlipTris_8x4_C": 1,
	"Desc_Wall_Concrete_FlipTris_8x8_C": 1,
	"Desc_Wall_Concrete_Gate_8x4_C": 1,
	"Desc_Wall_Concrete_SDoor_8x4_C": 1,
	"Desc_Wall_Concrete_Tris_8x1_C": 1,
	"Desc_Wall_Concrete_Tris_8x2_C": 1,
	"Desc_Wall_Concrete_Tris_8x4_C": 1,
	"Desc_Wall_Concrete_Tris_8x8_C": 1,
	"Desc_Wall_Conveyor_8x4_01_C": 1,
	"Desc_Wall_Conveyor_8x4_01_Steel_C": 1,
	"Desc_Wall_Conveyor_8x4_02_C": 1,
	"Desc_Wall_Conveyor_8x4_02_Steel_C": 1,
	"Desc_Wall_Conveyor_8x4_03_C": 1,
	"Desc_Wall_Conveyor_8x4_03_Steel_C": 1,
	"Desc_Wall_Conveyor_8x4_04_C": 1,
	"Desc_Wall_Conveyor_8x4_04_Steel_C": 1,
	"Desc_Wall_Door_8x4_01_C": 1,
	"Desc_Wall_Door_8x4_01_Steel_C": 1,
	"Desc_Wall_Door_8x4_03_C": 1,
	"Desc_Wall_Door_8x4_03_Steel_C": 1,
	"Desc_Wall_Frame_01_C": 1,
	"Desc_Wall_Gate_8x4_01_C": 1,
	"Desc_Wall_Orange_8x1_C": 1,
	"Desc_Wall_Orange_8x4_Corner_01_C": 1,
	"Desc_Wall_Orange_8x8_Corner_01_C": 1,
	"Desc_Wall_Orange_Angular_8x4_C": 1,
	"Desc_Wall_Orange_Angular_8x8_C": 1,
	"Desc_Wall_Orange_FlipTris_8x1_C": 1,
	"Desc_Wall_Orange_FlipTris_8x2_C": 1,
	"Desc_Wall_Orange_FlipTris_8x4_C": 1,
	"Desc_Wall_Orange_FlipTris_8x8_C": 1,
	"Desc_Wall_Orange_Tris_8x1_C": 1,
	"Desc_Wall_Orange_Tris_8x2_C": 1,
	"Desc_Wall_Orange_Tris_8x4_C": 1,
	"Desc_Wall_Orange_Tris_8x8_C": 1,
	"Desc_Wall_Steel_8x4_Corner_01_C": 1,
	"Desc_Wall_Steel_8x8_Corner_01_C": 1,
	"Desc_Wall_Window_8x4_01_C": 1,
	"Desc_Wall_Window_8x4_02_C": 1,
	"Desc_Wall_Window_8x4_03_C": 1,
	"Desc_Wall_Window_8x4_04_C": 1,
	"Desc_Wall_Window_Thin_8x4_01_C": 1,
	"Desc_Wall_Window_Thin_8x4_02_C": 1,
	"Desc_WaterPump_C": 1,
	"Desc_WorkBench_C": 1,
	"Desc_Workshop_C": 1,
}

target_items = {
	"Desc_ResourceSinkCoupon_C": 10_000_000
}

only_in_machines = True


def main():
	with open("data/data.json") as infile:
		obj = json.loads(infile.read())
		assert set(obj["resources"].keys()) == {*resource_scores, "Desc_Water_C"}
		assert obj["resources"].keys() <= obj["items"].keys()
		assert obj["buildings"].keys().isdisjoint(obj["items"].keys())
	buildings = scan_buildings(obj)
	lp_solver = subprocess.Popen(["lp_solve", "-s6"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
	stdin = lp_solver.stdin
	stdin.write(f"min: {build_resource_score(obj)} + {build_building_score(obj, buildings)};\n")
	stdin.write(build_resources())
	stdin.write(build_recipes(obj))
	stdin.write(build_target())
	stdin.write(build_buildings(obj, buildings))
	stdin.write(build_declarations(buildings))
	lp_solver.stdin.close()
	lp_solver.wait()

	output = lp_solver.stdout.read().split("\n")
	if "Actual values of the variables:" not in output:
		sys.exit("Error occured. Original output:\n" + "\n".join(output))

	resources = {}
	recipes = {}
	items = {}
	buildings = {}
	max_name_length = 8
	for line in output[output.index("Actual values of the variables:")+1:-1]:
		columns = list(filter(None, line.split(" ")))
		assert len(columns) == 2
		variable = columns[0]
		value = float(columns[1])
		if variable.startswith("itm#"):
			assert variable[4:] in obj["items"]
			if value != 0:
				items[variable[4:]] = value
			max_name_length = max(max_name_length, len(obj["items"][variable[4:]]["name"]))
		elif "@" in variable and value != 0:
			recipe_name, building_name = variable.split("@")
			buildings.setdefault(building_name, 0)
			buildings[building_name] += math.ceil(value)
			max_name_length = max(max_name_length, len(obj["buildings"][building_name]["name"]))
		elif variable.startswith("Recipe_") and value != 0:
			assert variable in obj["recipes"]
			recipes[variable] = value
		elif variable.startswith("res#") and value != 0:
			assert variable[4:] in obj["resources"]
			resources[variable[4:]] = value
		elif value != 0:
			print("WARN: Unknown variable: " + variable, file=sys.stderr)

	sorted_recipes = sort_recipes(recipes, obj)

	print("Resources:\n")
	for resource_name, value in resources.items():
		assert resource_name in obj["resources"]
		item = obj["items"][resource_name]
		print(f"  {item['name']:{max_name_length}}  :  {value:13,.2f}")

	print("\nFactories:\n")
	for recipe_name, value in sorted_recipes.items():
		recipe = obj["recipes"][recipe_name]
		building = obj["buildings"][recipe["producedIn"][0]]
		print(f"  {recipe['name']} ({math.ceil(value)} x)")
		print(f"    Building {building['name']}")
		print(f"    Input")
		for ingredient in recipe["ingredients"]:
			name = obj["items"][ingredient["item"]]["name"]
			rate = 60 * ingredient["amount"] / recipe["time"]
			print(f"      {name:{max_name_length}} {value * rate:13,.2f} (at most {math.floor(780 / rate):3} factories per belt)")
		print(f"    Output")
		for product in recipe["products"]:
			name = obj["items"][product["item"]]["name"]
			rate = 60 * product["amount"] / recipe["time"]
			print(f"      {name:{max_name_length}} {value * rate:13,.2f} (at most {math.floor(780 / rate):3} factories per belt)")
		print()

	print("Buildings:\n")
	for building_name, value in buildings.items():
		assert building_name in obj["buildings"]
		print(f"  {obj['buildings'][building_name]['name']:{max_name_length}}  :  {value:4}")

	print("\nOverall Output:\n")
	for item_name, value in items.items():
		assert item_name in obj["items"]
		item = obj["items"][item_name]
		print(f"  {item['name']:{max_name_length}}  :  {value:13,.2f}")


def scan_buildings(obj):
	buildings = {}
	for recipe_name, recipe in obj["recipes"].items():
		if only_in_machines and not recipe["inMachine"]:
			continue  # Skip recipes which cannot be build in machines
		assert len(recipe["producedIn"]) == 1
		for building in recipe["producedIn"]:
			assert building in obj["buildings"]
			buildings[f"{recipe_name}@{building}"] = (recipe_name, building)
	return buildings


def build_resource_score(obj):
	assert 0 not in resource_scores.values(), "math.lcm returns 0 when one value is 0"
	multiplicator = math.lcm(*resource_scores.values())
	result = ""
	for resource_name in obj["resources"]:
		score = 1 if resource_name == "Desc_Water_C" else (multiplicator // resource_scores[resource_name])
		result += str(score) + " res#" + resource_name + " + "
	return result[:-3]


def build_building_score(obj, buildings):
	building_score = ""
	for building_name, (_, original_name) in buildings.items():
		assert original_name in obj["buildings"]
		building_score += str(building_scores[original_name]) + " " + building_name + " + "
	return building_score[:-3]


def build_resources():
	result = "\n// resources\n"
	for resource_name, limit in resource_scores.items():
		result += f"res#{resource_name} <= {limit};\n"
	return result


def build_recipes(obj):
	@dataclasses.dataclass(frozen=True)
	class Recipe:
		name: str
		rate: float

	def join(sep, recipes):
		terms = []
		for recipe in recipes:
			terms.append(f"{sep}{recipe.rate} {recipe.name}")
		return " ".join(terms) if terms else "0"

	produced_by = {}
	consumed_by = {}

	for recipe_name, recipe in obj["recipes"].items():
		if only_in_machines and not recipe["inMachine"]:
			continue  # Skip recipes which cannot be build in machines
		if recipe_name == "Recipe_SinkPoint_Desc_ResourceSinkCoupon_C":
			continue  # Skip "broken" recipe
		for product in recipe["products"]:
			recipes = produced_by.setdefault(product["item"], list())
			recipes.append(Recipe(recipe_name, 60 * product["amount"] / recipe["time"]))
		for ingredient in recipe["ingredients"]:
			recipes = consumed_by.setdefault(ingredient["item"], list())
			recipes.append(Recipe(recipe_name, 60 * ingredient["amount"] / recipe["time"]))

	result = "\n// items\n"
	for item in consumed_by.keys() | produced_by.keys() | resource_scores.keys():
		assert item in obj["items"]
		assert item not in obj["buildings"]
		production = join('+', produced_by.get(item, list()))
		consumption = join('-', consumed_by.get(item, list()))
		if item in resource_scores:
			result += f"itm#{item} = res#{item} {production} {consumption};\n"
		else:
			result += f"itm#{item} = {production} {consumption};\n"

	return result


def build_buildings(obj, buildings):
	result = "\n// buildings\n"
	for building_name, (recipe_name, _) in buildings.items():
		assert recipe_name in obj["recipes"]
		result += f"{building_name} >= {recipe_name};\n"
	return result


def build_target():
	result = "\n// targets\n"
	for item, amount in target_items.items():
		result += f"itm#{item} >= {str(amount)};\n"
	return result


def build_declarations(buildings):
	result = "\n// declarations\n"
	result += f"int {', '.join(buildings.keys())};\n"
	return result


def sort_recipes(recipes, obj):
	out = collections.OrderedDict()
	seen = set()
	recipes_by_product = {}
	for recipe_name in recipes.keys():
		for product in obj["recipes"][recipe_name]["products"]:
			recipes_by_product.setdefault(product["item"], list()).append(recipe_name)

	def add_recursively(recipe_name):
		if recipe_name in seen:
			return  # Avoid endless recursion
		seen.add(recipe_name)
		for ingredient in obj["recipes"][recipe_name]["ingredients"]:
			for ingredient_recipe_name in recipes_by_product.get(ingredient["item"], []):
				add_recursively(ingredient_recipe_name)
		out[recipe_name] = recipes[recipe_name]

	for recipe_name in recipes.keys():
		add_recursively(recipe_name)
	return out


if __name__ == '__main__':
	main()
