#!/usr/bin/env python3

import json
import math
import subprocess
import sys

resource_scores = {
	"Desc_OreIron_C": 70380,
	"Desc_OreCopper_C": 28860,
	"Desc_Stone_C": 52860,
	"Desc_Coal_C": 30900,
	"Desc_OreGold_C": 11040,
	"Desc_LiquidOil_C": 11700,
	"Desc_RawQuartz_C": 10500,
	"Desc_Sulfur_C": 6840,
	"Desc_OreBauxite_C": 9780,
	"Desc_OreUranium_C": 2100,
	"Desc_NitrogenGas_C": 12000
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
	"Desc_ResourceSinkCoupon_C": 1000000000
}

only_in_machines = True

def main(argv):
	with open("data/data.json") as infile:
		obj = json.loads(infile.read())
	lp_solver = subprocess.Popen("lp_solve", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	lp_solver.stdin.write(("min: score;\nscore = resource_score + building_score;\n").encode("utf-8"))
	resource_score = "resource_score = "
	multiplicator = math.lcm(*resource_scores.values())
	for resource_name in resource_scores:
		lp_solver.stdin.write((resource_name + " <= " + str(resource_scores[resource_name]) + ";\n").encode("utf-8"))
	resource_scores["Desc_Water_C"] = multiplicator
	for resource_name in obj["resources"]:
		resource_score += str(multiplicator // resource_scores[resource_name]) + " * " + resource_name + " + "
	lp_solver.stdin.write((resource_score[:-3] + ";\n").encode("utf-8"))
	building_score = "building_score = "
	for building_name in obj["buildings"]:
		building_score += str(building_scores[building_name]) + " * " + building_name + " + "
	lp_solver.stdin.write((building_score[:-3] + ";\n").encode("utf-8"))
	resources = {}
	products = {}
	produced_in = {}
	for recipe_name in obj["recipes"]:
		recipe = obj["recipes"][recipe_name]
		for ingredient in recipe["ingredients"]:
			if ingredient["item"] not in resources:
				resources[ingredient["item"]] = []
		for product in recipe["products"]:
			if product["item"] not in products:
				products[product["item"]] = []
			if product["item"] not in produced_in:
				produced_in[product["item"]] = []
			produced_in[product["item"]].append(recipe_name)
		if only_in_machines and recipe["inMachine"] == False:
			continue
		for ingredient in recipe["ingredients"]:
			resources[ingredient["item"]].append([ingredient["amount"] / recipe["time"] * 60, recipe["className"]])
		for product in recipe["products"]:
			products[product["item"]].append([product["amount"] / recipe["time"] * 60, recipe["className"]])
	for resource_name in resources:
		if len(resources[resource_name]) > 0:
			text = " + ".join([str(1 / item[0]) + " * " + item[1] for item in resources[resource_name]])
		else:
			text = "0"
		lp_solver.stdin.write((resource_name + " >= " + text + ";\n").encode("utf-8"))
	for product_name in products:
		if len(products[product_name]) > 0:
			text = " + ".join([str(item[0]) + " * " + item[1] for item in products[product_name]])
		else:
			text = "0"
		lp_solver.stdin.write((product_name + " <= " + text + ";\n").encode("utf-8"))
		lp_solver.stdin.write((product_name + " >= " + "0" + ";\n").encode("utf-8"))
	for item in target_items:
		lp_solver.stdin.write((item + " >= " + str(target_items[item]) + ";\n").encode("utf-8"))
	declarations = set(list(resources.keys()) + list(products.keys()) + list(obj["recipes"].keys()))
	if only_in_machines:
		for decl in declarations.copy():
			if decl in obj["recipes"] and obj["recipes"][decl]["inMachine"] == False:
				declarations.remove(decl)
	#lp_solver.stdin.write(("int " + ", ".join(declarations) + ";\n").encode("utf-8"))
	lp_solver.stdin.close()
	lp_solver.wait()
	output = lp_solver.stdout.read().decode("utf-8").split("\n")
	if "Actual values of the variables:" not in output:
		print("Error occured. Original output:")
		print("\n".join(output))
		return
	result = []
	for line in output[output.index("Actual values of the variables:")+1:-1]:
		if not line.endswith(" 0"):
			result.append(list(filter(None, line.split(" "))))
	used_keys = set([item[0] for item in result])
	for i in range(len(result)):
		if result[i][0].startswith("Recipe_"):
			if result[i][0] in obj["recipes"]:
				result[i][1] = str(float(result[i][1]) * obj["recipes"][result[i][0]]["time"])
				result[i].append("using")
				ingredients = []
				for ingredient in obj["recipes"][result[i][0]]["ingredients"]:
					ingredients += [str(ingredient["amount"] * float(result[i][1])), ingredient["item"], "and"]
				result[i] += ingredients[:-1]
			else:
				result[i][1] += " (unknown time)"
		elif result[i][0].startswith("Desc_"):
			if result[i][0] in produced_in:
				result[i].append("produced in")
				result[i] += [item for item in produced_in[result[i][0]] if item in used_keys]
	print("\n".join([" ".join(line) for line in result]))
	print("main items:")
	print("\n".join([" ".join(line) for line in result if line[0].startswith("Recipe_SinkPoint_")]))
	print("inputs:")
	print("\n".join([" ".join(line) for line in result if line[0] in obj["resources"]]))

if __name__ == '__main__':
	main(sys.argv)
