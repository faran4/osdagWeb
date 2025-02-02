"""
Started on 1st November, 2019.

@author: Kumari Anjali Jatav

Module: Beam-Beam Cover Plate Bolted Connection

Reference:
            1) IS 800: 2007 General construction in steel - Code of practice (Third revision)
            2) Design of Steel Structures by N. Subramanian
            3) IS 1367 (Part3):2002 - TECHNICAL SUPPLY CONDITIONS FOR THREADED STEEL FASTENERS

"""

from api.osdag.moment_connection import MomentConnection
from api.osdag.component import *
from api.osdag.Common import *
from api.osdag.load import Load
from api.osdag.reportGenerator_latex import CreateLatex
from api.osdag.Report_functions import *
import logging
import math

logger = logging.getLogger(__name__) 

class BeamCoverPlate(MomentConnection):

    def __init__(self):
        super(BeamCoverPlate, self).__init__()
        self.design_status = False

    def generate_stl(beam_cover):
        """
        Generate and save the STL file.
        """
        stl_dir = os.path.join(settings.MEDIA_ROOT)
        os.makedirs(stl_dir, exist_ok=True)  # Ensure directory exists
        stl_path = os.path.join(stl_dir, "beam_cover_plate.stl")

        # Example STL generation (Replace with actual Osdag STL export)
        with open(stl_path, "w") as f:
            f.write("Generated STL file for Beam Cover Plate")

        return stl_path
    
    def generate_design_report(beam_cover):
        """
        Generates the design report PDF using PyLaTeX.
        """
        report_dir = os.path.join(settings.MEDIA_ROOT)
        os.makedirs(report_dir, exist_ok=True)  # Ensure directory exists
        report_path = os.path.join(report_dir, "design_report.pdf")

        doc = CreateLatex()
        doc.save_latex(beam_cover, {}, {}, report_path, "", "", "", "Beam Cover Plate Bolted")

        return report_path

    def set_osdaglogger(key):

        """
        Function to set Logger for Tension Module
        """

        # @author Arsil Zunzunia
        global logger
        logger = logging.getLogger('Osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if key is not None:
            handler = OurLog(key)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def out_bolt_bearing(self):

        bolt_type = self[0]
        if bolt_type != TYP_BEARING:
            return True
        else:
            return False

    def preference_type(self):

        pref_type = self[0]
        if pref_type == VALUES_FLANGEPLATE_PREFERENCES[0] :
            return True
        else:
            return False

    def set_input_values(self, design_dictionary):
        super().set_input_values(design_dictionary)

        self.module = design_dictionary.get("Module", "Moment Connection")  # Default value
        self.preference = design_dictionary.get("FlangePlatePreferences", {})  # Empty dict as default
        self.material = design_dictionary.get("Material", "Steel")  # Default material

        self.section = Beam(designation=design_dictionary[KEY_SECSIZE],
                              material_grade=design_dictionary[KEY_SEC_MATERIAL])
        
        self.web_bolt = Bolt(grade=design_dictionary[KEY_GRD], 
                             diameter=design_dictionary[KEY_D],
                             bolt_type=design_dictionary[KEY_TYP])
                            #  bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                            #  edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                            #  mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
                            #  corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES],
                            #  bolt_tensioning=design_dictionary[KEY_DP_BOLT_TYPE])


        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], 
                         diameter=design_dictionary[KEY_D],
                             bolt_type=design_dictionary[KEY_TYP]),
                        #      bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                        #      edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                        #      mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
                        #      corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES],
                        #  bolt_tensioning=design_dictionary[KEY_DP_BOLT_TYPE])
        self.flange_bolt = Bolt(grade=design_dictionary[KEY_GRD], 
                                diameter=design_dictionary[KEY_D],
                                bolt_type=design_dictionary[KEY_TYP]),
                                # bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                                # edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                                # mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
                                # corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES],
                                # bolt_tensioning=design_dictionary[KEY_DP_BOLT_TYPE])

        self.flange_plate = Plate(thickness=design_dictionary.get(KEY_FLANGEPLATE_THICKNESS, 6),
                                  material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL],
                                  gap=design_dictionary.get(KEY_DP_DETAILING_GAP, 3)
                                )


        self.web_plate = Plate(thickness=design_dictionary.get(KEY_WEBPLATE_THICKNESS, None),
                               material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL]),
                            #    gap=design_dictionary[KEY_DP_DETAILING_GAP])

        # self.flange_check_thk =[]
        # self.web_check_thk = []
        # self.previous_thk_flange =[]
        # self.previous_thk_web =[]
        self.member_capacity_status = False
        self.initial_pt_thk_status = False
        self.initial_pt_thk_status_web = False
        self.webheight_status = False
        self.select_bolt_dia_status = False
        self.get_plate_details_status = False
        self.flange_check_axial_status = False
        self.flange_plate_check_status = False
        self.web_axial_check_status = False
        self.web_plate_axial_check_status = False
        self.web_shear_plate_check_status = False
        self.member_capacity()
        #self.hard_values(self)
    def hard_values(self):
        # Select Selection  WPB 240* 240 * 60.3 (inside Ouside)- material E 250 fe 450A bearing
        #flange bolt
        self.load.moment = 8.318420#kN
        self.factored_axial_load= 481.745#KN
        self.load.shear_force =111.906 # kN
        self.flange_bolt.bolt_type = "Bearing Bolt"
        # self.flange_bolt.bolt_hole_type = bolt_hole_type
        # self.flange_bolt.edge_type = edge_type
        # self.flange_bolt.mu_f = float(mu_f)
        self.flange_bolt.connecting_plates_tk = None

        self.flange_bolt.bolt_grade_provided = 3.6
        self.flange_bolt.bolt_diameter_provided = 24
        self.flange_bolt.dia_hole =26
        # self.flange_bolt.bolt_shear_capacity = 56580.32638058333
        # self.flange_bolt.bolt_bearing_capacity = 118287.48484848486
        # self.flange_bolt.bolt_capacity = 56580.32638058333




        # web bolt
        self.web_bolt.bolt_type = "Bearing Bolt"
        # self.web_bolt.bolt_hole_type = bolt_hole_type
        # self.web_bolt.edge_type = edge_type
        # self.web_bolt.mu_f = float(mu_f)
        self.web_bolt.connecting_plates_tk = None

        self.web_bolt.bolt_grade_provided = 3.6
        self.web_bolt.bolt_diameter_provided = 24
        self.web_bolt.dia_hole = 26
        # self.web_bolt.bolt_shear_capacity = 56580.32638058333
        # self.web_bolt.bolt_bearing_capacity = 69923.63636363638
        # self.web_bolt.bolt_capacity = 69923.63636363638
        # self.web_bolt.min_edge_dist_round = 33
        # self.web_bolt.min_end_dist_round = 33
        # self.web_bolt.min_gauge_round = 50
        #anjali jatav
        # self.web_bolt.min_pitch_round = 50

        # self.web_bolt.max_edge_dist_round = 150
        # self.web_bolt.max_end_dist_round = 150
        # self.web_bolt.max_spacing_round = 300.0

        # self.web_bolt.bolt_shank_area = 0.0
        # self.web_bolt.bolt_net_area = 0.0



        #flange plate
        self.flange_plate.thickness_provided =6
        self.flange_plate.height = 240
        self.flange_plate.length= 310
        self.flange_plate.bolt_line = 4
        self.flange_plate.bolts_one_line =2
        self.flange_plate.bolts_required= 8
        # self.flange_plate.bolt_capacity_red = 56580.32638058333
        # self.flange_plate.bolt_force = 29359.584393928224
        # self.flange_plate.moment_demand= 0
        self.flange_plate.pitch_provided = 60
        self.flange_plate.gauge_provided = 0.0
        self.flange_plate.edge_dist_provided = 45
        self.flange_plate.end_dist_provided= 45

        # web plate
        self.web_plate.thickness_provided = 8
        self.web_plate.height =200
        self.web_plate.length =310
        self.web_plate.bolt_line = 4
        self.web_plate.bolts_one_line = 2
        self.web_plate.bolts_required = 8
        self.web_plate.pitch_provided = 60
        self.web_plate.gauge_provided = 110
        self.web_plate.edge_dist_provided = 45
        self.web_plate.end_dist_provided = 45
        #  Inner Flange plate
        self.flange_plate.thickness_provided = 6
        self.flange_plate.Innerheight = 114.15
        self.flange_plate.Innerlength =310
        self.flange_plate.gap = 10
        self.web_plate.gap = 10

        self.flange_plate.midgauge = 101.7
        self.web_plate.midpitch = 100
        self.flange_plate.midpitch=100
        # self.web_plate.moment_capacity = 0
        self.design_status = True

    def member_capacity(self):
        """
        Calculates:
        - Axial Capacity [Ref: Cl.10.7 IS 800:2007]
        - Shear Capacity [Ref: Cl.8.4 IS 800:2007]
        - Moment Capacity [Ref: Cl.10.7 IS 800:2007]

        Returns: Design Status (Safe/Unsafe)
        """
        self.member_capacity_status = False  # Default design status

        # Prevent crash if section is not assigned
        if not hasattr(self, "section") or self.section is None:
            logger.error("No section data found. Ensure beam section is initialized.")
            return

        gamma_m0 = 1.1

        # Axial Capacity (N)
        if hasattr(self.section, "area") and hasattr(self.section, "fy"):
            self.axial_capacity = round((self.section.area * self.section.fy) / gamma_m0, 2)
        else:
            self.axial_capacity = 0  # Default to zero if missing

        # Shear Capacity (N)
        if hasattr(self.section, "depth") and hasattr(self.section, "flange_thickness") and hasattr(self.section, "web_thickness"):
            self.shear_capacity1 = round(
                ((self.section.depth - (2 * self.section.flange_thickness)) *
                self.section.web_thickness * self.section.fy * 0.6) /
                (math.sqrt(3) * gamma_m0), 2
            )
        else:
            self.shear_capacity1 = 0  # Default to zero if missing

        # Section Modulus Calculations (Preventing Errors)
        self.Z_p = getattr(self.section, "plast_sec_mod_z", 0)
        self.Z_e = getattr(self.section, "elast_sec_mod_z", 0)

        if hasattr(self.section, "web_thickness") and hasattr(self.section, "depth") and hasattr(self.section, "flange_thickness"):
            self.Z_wp = round(((self.section.web_thickness * (self.section.depth - 2 * self.section.flange_thickness) ** 2) / 4), 2)
            self.Z_we = round(((self.section.web_thickness * (self.section.depth - 2 * self.section.flange_thickness) ** 2) / 6), 2)
        else:
            self.Z_wp = 0
            self.Z_we = 0

        # Assign Section Class
        self.class_of_section = int(max(self.Z_wp, self.Z_we))

        # Compute Moment Capacity
        if hasattr(self.section, "plastic_moment_capacty"):
            self.section.plastic_moment_capacity(beta_b=1, Z_p=self.Z_p, fy=self.section.fy)
            self.Pmc = self.section.plastic_moment_capacity  # Plastic Moment Capacity
        else:
            self.Pmc = 0  # Default to zero

        if hasattr(self.section, "moment_d_deformation_criteria"):
            self.section.moment_d_deformation_criteria(fy=self.section.fy, Z_e=self.Z_e)
            self.Mdc = self.section.moment_d_def_criteria  # Deformation Moment Capacity
        else:
            self.Mdc = 0

        self.section.moment_capacity = round(min(self.Pmc, self.Mdc), 2)

        # Interaction Ratios
        self.IR_axial = round(self.load.axial_force * 1000 / max(self.axial_capacity, 1), 4)  # Avoid division by zero
        self.IR_shear = round(self.load.shear_force * 1000 / max(self.shear_capacity1, 1), 4)
        self.IR_moment = round(self.load.moment * 1000000 / max(self.section.moment_capacity, 1), 4)
        self.sum_IR = round(self.IR_axial + self.IR_moment, 4)

        # Check Design Safety
        if self.IR_axial > 1:
            logger.error(f"Axial load exceeds capacity: {self.IR_axial} > 1.0")
            self.member_capacity_status = False
            return

        if self.IR_shear > 1:
            logger.error(f"Shear load exceeds capacity: {self.IR_shear} > 1.0")
            self.member_capacity_status = False
            return

        if self.IR_moment > 1:
            logger.error(f"Bending moment exceeds capacity: {self.IR_moment} > 1.0")
            self.member_capacity_status = False
            return

        # If All Checks Pass, Design is Safe
        self.member_capacity_status = True
        logger.info("Beam cover plate design is safe.")

        return

         #############################################################

    def initial_pt_thk(self, previous_thk_flange= None,previous_thk_web = None):

        ############################### WEB MENBER CAPACITY CHECK ############################
        ###### # capacity Check for web in axial = yielding

        if (previous_thk_flange) == None:
            pass
        else:
            # for i in previous_thk_flange:
            if previous_thk_flange in self.flange_plate.thickness:
                self.flange_plate.thickness.remove(previous_thk_flange)
            else:
                pass

        if (previous_thk_web) == None:
            pass
        else:
            if previous_thk_web in self.web_plate.thickness:
                self.web_plate.thickness.remove(previous_thk_web)
            else:
                pass


        #
        # if (previous_thk_flange) == None:
        #     pass
        # else:
        #     for i in previous_thk_flange:
        #         if i in self.flange_plate.thickness:
        #             self.flange_plate.thickness.remove(i)
        #         else:
        #             pass
        #
        # if (previous_thk_web) == None:
        #     pass
        # else:
        #     for i in previous_thk_web:
        #         if i in self.web_plate.thickness:
        #             self.web_plate.thickness.remove(i)
        #         else:
        #             pass
        print("thickness_previous_list_flange", previous_thk_flange)
        print("thickness_previous_list_web",previous_thk_web)
        print("thicknesslist",self.web_plate.thickness)
        print("thicknesslist", self.flange_plate.thickness)
        self.initial_pt_thk_status = False
        self.initial_pt_thk_status_web =False
        A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
        self.section.tension_yielding_capacity_web = self.tension_member_design_due_to_yielding_of_gross_section(A_v=A_v_web,fy=self.section.fy)
        if self.section.tension_yielding_capacity_web> self.axial_force_w:

        ################################# FLANGE MEMBER CAPACITY CHECK##############################
            A_v_flange = self.section.flange_thickness * self.section.flange_width
            self.section.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(A_v=A_v_flange,fy=self.section.fy)
            if self.section.tension_yielding_capacity > self.flange_force:
                self.web_plate_thickness_possible = [i for i in self.web_plate.thickness if i >= (self.section.web_thickness / 2)]
                if self.preference == "Outside":
                    self.flange_plate_thickness_possible = [i for i in self.flange_plate.thickness if i >= self.section.flange_thickness]
                else:
                    self.flange_plate_thickness_possible = [i for i in self.flange_plate.thickness if i >= (self.section.flange_thickness / 2)]
                if len(self.flange_plate_thickness_possible) == 0:
                    logger.error(" : The flange plate thickness is less than the flange thickness of the section.")
                    logger.warning(" : The flange plate thickness should be greater than the thickness of the flange of the section, i.e. {} mm."
                                   .format( self.section.flange_thickness))
                    self.initial_pt_thk_status =False
                    self.design_status = False
                else:
                    self.flange_plate.thickness_provided = self.min_thick_based_on_area(self, tk=self.section.flange_thickness,
                                                                                        width=self.section.flange_width,
                                                                                        list_of_pt_tk=self.flange_plate_thickness_possible,
                                                                                        t_w=self.section.web_thickness,
                                                                                        r_1=self.section.root_radius,
                                                                                        D=self.section.depth,
                                                                                        preference=self.preference)
                    self.flange_plate.connect_to_database_to_get_fy_fu(self.flange_plate.material,self.flange_plate.thickness_provided)
                    if self.flange_plate.thickness_provided != 0:
                        if self.preference =="Outside":
                            if self.outerwidth < 50:
                                logger.error(" : The outer height of the flange plate is less than 50 mm.")
                                logger.info(" : Select a wider section.")
                                self.initial_pt_thk_status = False
                                self.design_status = False

                            else:
                                if self.flange_plate_crs_sec_area < (self.flange_crs_sec_area  * 1.05):
                                    logger.error(" : The area of the flange plate is less than the area of the flange.")
                                    logger.warning(" : The area of the flange plate should be greater than 1.05 times the area of the flange, i.e. "
                                                   "{} mm2.".format(round(self.Ap, 2)))
                                    logger.info(" : Increase the thickness of the plate.")
                                    self.initial_pt_thk_status = False
                                    self.design_status = False
                                else:
                                    self.initial_pt_thk_status = True
                                    pass
                        else:
                            if self.outerwidth < 50 or self.innerwidth < 50:
                                logger.error(" : The height of the flange plates is less than 50 mm.")
                                logger.info(" : Select a wider section.")
                                self.initial_pt_thk_status = False
                                self.design_status = False
                            else:
                                if self.flange_plate_crs_sec_area < (self.flange_crs_sec_area * 1.05):
                                    logger.error(" : The area of flange plates is less than the area of the flange.")
                                    logger.warning(" : The area of flange plates should be greater than 1.05 times the area of the flange, i.e. {} "
                                                   "mm2.".format(round(self.Ap, 2)))
                                    logger.info(" : Increase the thickness of the flange plate.")
                                    self.initial_pt_thk_status = False
                                    self.design_status = False
                                else:
                                    self.initial_pt_thk_status = True
                                    pass
                    else:
                        self.initial_pt_thk_status = False
                        self.design_status = False
                        logger.error(" : Provided flange plate thickness is not sufficient.")

                self.initial_pt_thk_status_web = False
                # self.webheight_status = False
                if len(self.web_plate_thickness_possible) == 0:
                    logger.error(" : The web plate thickness is less than the web thickness of the section.")
                    logger.warning(" : The web plate thickness should be greater than the thickness of web of the section, i.e. {} mm."
                                   .format(  self.section.web_thickness))
                    self.initial_pt_thk_status_web = False
                    self.design_status = False
                else:

                    self.web_plate.thickness_provided = self.min_thick_based_on_area(self,
                                                                                     tk=self.section.flange_thickness,
                                                                                     width=self.section.flange_width,
                                                                                     list_of_pt_tk=self.web_plate_thickness_possible,
                                                                                     t_w=self.section.web_thickness,
                                                                                     r_1=self.section.root_radius, D=self.section.depth,
                                                                                     preference=None,fp_thk =self.flange_plate.thickness_provided )
                    self.web_plate.connect_to_database_to_get_fy_fu(self.web_plate.material,
                                                                       self.web_plate.thickness_provided)
                    if self.web_plate.thickness_provided != 0:
                        if self.preference == "Outside":
                            if self.webplatewidth < self.min_web_plate_height:
                                self.webheight_status = False
                                self.design_status = False
                                logger.error(" : Web plate error!")
                                logger.warning(" : The height of the web plate ({} mm) is less than the minimum depth of the plate, i.e. {} mm"
                                               .format(self.webplatewidth, self.min_web_plate_height))
                                logger.warning("Try a deeper section")
                            else:
                                self.webheight_status = True
                                if self.web_plate_crs_sec_area < (self.web_crs_area * 1.05):
                                    logger.error(" : Area of web plates is less than the area of the web.")
                                    logger.warning(" : Area of web plates should be greater than 1.05 times the area of the web, i.e. {} mm2."
                                                   .format(round(self.Wp, 2)))
                                    logger.info(" : Increase the thickness of the web plate.")
                                    self.initial_pt_thk_status_web = False
                                    self.design_status = False
                                else:
                                    self.initial_pt_thk_status_web = True
                                    # self.webheight_status = True
                                    pass
                        else:
                            if self.webplatewidth < self.min_web_plate_height:
                                self.webheight_status = False
                                self.design_status = False
                                logger.error(" : Inner plate error!")
                                logger.warning(" : Decrease the thickness of the inner flange plate or try a wider/deeper section.")

                            else:
                                self.webheight_status = True
                                if self.web_plate_crs_sec_area < (self.web_crs_area * 1.05):
                                    logger.error(" : Area of web plates is less than the area of the web.")
                                    logger.warning(" : Area of web plates should be greater than 1.05 times the area of the web, i.e. {} mm2."
                                                   .format(round(self.Wp, 2)))
                                    logger.info(" : Increase the thickness of the web plate.")
                                    self.initial_pt_thk_status_web = False
                                    self.design_status = False
                                else:
                                    self.initial_pt_thk_status_web = True
                                    pass
                    else:
                        self.initial_pt_thk_status_web = False
                        logger.error(" : Provided flange plate thickness is not sufficient.")

                if len(self.flange_plate_thickness_possible) == 0:
                    if len(self.flange_plate.thickness) >= 2:
                        self.max_thick_f = max(self.flange_plate.thickness)
                    else:
                        self.max_thick_f = self.flange_plate.thickness[0]
                else:
                    # if self.flange_plate.thickness_provided ==0:
                    #     if len(self.flange_plate.thickness) >= 2:
                    #         self.max_thick_f = max(self.flange_plate.thickness)
                    #     else:
                    #         self.max_thick_f = self.flange_plate.thickness[0]
                    # else:
                    self.max_thick_f = self.flange_plate.thickness_provided

                if len(self.web_plate_thickness_possible) == 0:
                    if len(self.web_plate.thickness) >= 2:
                        self.max_thick_w = max(self.web_plate.thickness)
                    else:
                        self.max_thick_w = self.web_plate.thickness[0]
                else:
                    # if self.web_plate.thickness_provided == 0:
                    #     if len(self.web_plate.thickness) >= 2:
                    #         self.max_thick_w = max(self.web_plate.thickness)
                    #     else:
                    #         self.max_thick_w = self.web_plate.thickness[0]
                    # else:
                    self.max_thick_w = self.web_plate.thickness_provided

                if self.initial_pt_thk_status == True and self.initial_pt_thk_status_web == True and self.webheight_status == True:
                    self.design_status = True
                    self.select_bolt_dia(self)
                else:
                    self.initial_pt_thk_status = False and self.initial_pt_thk_status_web == False and  self.webheight_status == False
                    self.design_status = False
                    # logger.warning(" : Plate is not possible")
                    logger.error(" : Design is unsafe. \n ")
                    logger.info(" :=========End Of design===========")

            else:
                self.initial_pt_thk_status = False
                self.design_status = False
                logger.warning(" : The tension capacity of the flange is less than the required flange force {} kN."
                               .format(round(self.flange_force/1000, 2)))
                logger.info(" : Select a larger beam section or decrease the applied load.")
                logger.error(" : Design is unsafe. \n ")
                logger.info(" :=========End Of design===========")
        else:
            self.initial_pt_thk_status_web = False
            self.design_status = False
            logger.warning( " : The tension capacity of the web is less than the required axial force, i.e. {} kN."
                            .format(round(self.axial_force_w/1000, 2)))
            logger.info(" : Select a larger beam section or decrease the applied axial load.")
            logger.error(" : Design is unsafe. \n ")
            logger.info(" :=========End Of design===========")

    def select_bolt_dia(self):

        self.select_bolt_dia_status = False
        self.min_plate_height = self.section.flange_width
        self.max_plate_height = self.section.flange_width

        axial_force_f =  self.factored_axial_load  * self.section.flange_width * \
                         self.section.flange_thickness / (self.section.area )

        self.flange_force = ((( self.moment_flange) / (self.section.depth - self.section.flange_thickness)) +(axial_force_f))
        self.res_force = math.sqrt((self.fact_shear_load)** 2 + ( self.factored_axial_load ) ** 2) #N
        bolts_required_previous_1 = 2
        bolts_required_previous_2 = 2
        bolt_diameter_previous = self.bolt.bolt_diameter[-1]

        self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]
        count_1 = 0
        count_2 = 0
        bolts_one_line = 1
        ###### for flange plate thickness####
        self.bolt_conn_plates_t_fu_fy = []
        if self.preference == "Outside":
            self.bolt_conn_plates_t_fu_fy.append((self.flange_plate.thickness_provided, self.flange_plate.fu, self.flange_plate.fy))
            self.bolt_conn_plates_t_fu_fy.append(
                (self.section.flange_thickness, self.section.fu, self.section.fy))
        else:
            self.bolt_conn_plates_t_fu_fy.append(
                (2*self.flange_plate.thickness_provided, self.flange_plate.fu, self.flange_plate.fy))
            self.bolt_conn_plates_t_fu_fy.append(
                (self.section.flange_thickness, self.section.fu, self.section.fy))

        ##### for web plate thickness######
        self.bolt_conn_plates_web_t_fu_fy = []
        self.bolt_conn_plates_web_t_fu_fy.append(
            ( 2*self.web_plate.thickness_provided, self.web_plate.fu, self.web_plate.fy))
        self.bolt_conn_plates_web_t_fu_fy.append(
            (self.section.web_thickness, self.section.fu, self.section.fy))

        # TO GET BOLT BEARING CAPACITY CORRESPONDING TO PLATE THICKNESS
        # FOR FLANGE
        if self.preference == "Outside":
            self.t_sum1 = self.flange_plate.thickness_provided + self.section.flange_thickness
        else:
            self.t_sum1 = (2 * self.flange_plate.thickness_provided) + self.section.flange_thickness

        # FOR WEB
        self.t_sum2 = (2 * self.web_plate.thickness_provided) + self.section.web_thickness
        self.t_sum_max = max(self.t_sum1,self.t_sum2)
        self.large_grip_status = False
        self.bolt.bolt_diameter_possible = []
        for d in self.bolt.bolt_diameter:
            if 8 * d >= self.t_sum_max:
                self.bolt.bolt_diameter_possible.append(d)
            else:
                pass

        print("bolt dia ", d, " mm  available bolt list ",
              self.bolt.bolt_diameter_possible, " mm")

        if len(self.bolt.bolt_diameter_possible) ==0:
            self.large_grip_status = False
            self.design_status = False
            logger.error(" : The thickness of the connected plates should not be greater than 8 times the bolt diameter.")
            logger.error(" : Design is unsafe. \n ")
            logger.info(" :=========End Of design===========")

        else:
            self.large_grip_status = True
            bolt_design_status_1 = False
            bolt_design_status_2= False
            for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter_possible):

                self.flange_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                            conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)
                print(self.flange_bolt.min_edge_dist, self.flange_bolt.edge_type)

                if self.preference == "Outside":
                    self.flange_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                             bolt_grade_provided=self.bolt.bolt_grade_provided,
                                                             conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                                             n_planes=1)
                else:
                    self.flange_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                             bolt_grade_provided=self.bolt.bolt_grade_provided,
                                                             conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                                             n_planes=2)

                self.web_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                            conn_plates_t_fu_fy= self.bolt_conn_plates_web_t_fu_fy)

                self.web_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                         bolt_grade_provided=self.bolt.bolt_grade_provided,
                                                         conn_plates_t_fu_fy= self.bolt_conn_plates_web_t_fu_fy,
                                                         n_planes=2)

                self.flange_plate.get_flange_plate_details(bolt_dia=self.flange_bolt.bolt_diameter_provided,
                                                        flange_plate_h_min=self.min_plate_height,
                                                        flange_plate_h_max=self.max_plate_height,
                                                        bolt_capacity=self.flange_bolt.bolt_capacity,
                                                        min_edge_dist=self.flange_bolt.min_edge_dist_round,
                                                        min_gauge=self.flange_bolt.min_gauge_round,
                                                        max_spacing=self.flange_bolt.max_spacing_round,
                                                        max_edge_dist=self.flange_bolt.max_edge_dist_round,
                                                        axial_load=self.flange_force, gap=self.flange_plate.gap/2,
                                                        web_thickness =self.section.web_thickness,
                                                        root_radius= self.section.root_radius,joint = "half")
                # if self.preference == "Outside":
                #     plate_quantity = 1
                # else:
                #     plate_quantity = 2
                # self.flange_plate.length_grip_bolt_cap_red(plate_quantity=plate_quantity,
                #                                            parent_tk =self.section.flange_thickness,
                #                                            plate_tk=self.flange_plate.thickness_provided,
                #                                            diameter = self.flange_bolt.bolt_diameter_provided,
                #                                            bolt_capacity = self.flange_plate.bolt_capacity_red,
                #                                            vres = self.flange_plate.bolt_force)


                self.min_web_plate_height = round(self.section.min_plate_height() ,2)
                if self.preference == "Outside":
                    self.max_web_plate_height = self.section.max_plate_height()
                else:
                    self.max_web_plate_height = self.section.depth - 2 * self.section.flange_thickness - (2 * self.webclearance)

                self.axial_force_w = ((self.section.depth - (2 * self.section.flange_thickness)) *
                                      self.section.web_thickness *
                                      self.factored_axial_load) / (self.section.area )

                self.web_plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                                     web_plate_h_min=self.min_web_plate_height,
                                                     web_plate_h_max=self.max_web_plate_height,
                                                     bolt_capacity=self.web_bolt.bolt_capacity,
                                                     min_edge_dist=self.web_bolt.min_edge_dist_round,
                                                     min_gauge=self.web_bolt.min_gauge_round,
                                                     max_spacing=self.web_bolt.max_spacing_round,
                                                     max_edge_dist=self.web_bolt.max_edge_dist_round
                                                     ,shear_load=self.fact_shear_load ,
                                                     axial_load=self.axial_force_w,
                                                     web_moment = self.moment_web,
                                                     gap=(self.web_plate.gap/2), shear_ecc=True,joint = "half")
                # plate_quantity =2
                # self.web_plate.length_grip_bolt_cap_red(plate_quantity=plate_quantity,
                #                                         parent_tk=self.section.web_thickness,
                #                                         plate_tk=self.web_plate.thickness_provided,
                #                                         diameter=self.web_bolt.bolt_diameter_provided,
                #                                         bolt_capacity=self.web_plate.bolt_capacity_red,
                #                                         vres=self.web_plate.bolt_force)

                if self.flange_plate.design_status is True and self.web_plate.design_status is True:
                    if self.flange_plate.bolts_required > bolts_required_previous_1 and count_1 >= 1:
                        self.bolt.bolt_diameter_provided = bolt_diameter_previous
                        self.flange_plate.bolts_required = bolts_required_previous_1
                        self.flange_plate.bolt_force = bolt_force_previous_1
                        bolt_design_status_1 = self.flange_plate.design_status
                        break
                    bolts_required_previous_1 = self.flange_plate.bolts_required
                    bolt_diameter_previous = self.bolt.bolt_diameter_provided
                    bolt_force_previous_1 = self.flange_plate.bolt_force
                    count_1 += 1
                    bolt_design_status_1 = self.flange_plate.design_status

                    if self.web_plate.bolts_required > bolts_required_previous_2 and count_2 >= 1:
                        self.bolt.bolt_diameter_provided = bolt_diameter_previous
                        self.web_plate.bolts_required = bolts_required_previous_2
                        self.web_plate.bolt_force = bolt_force_previous_2
                        bolt_design_status_2 = self.web_plate.design_status
                        break
                    bolts_required_previous_2 = self.web_plate.bolts_required
                    bolt_diameter_previous = self.bolt.bolt_diameter_provided
                    bolt_force_previous_2 = self.web_plate.bolt_force
                    count_2 += 1
                    bolt_design_status_2 = self.web_plate.design_status

            bolt_capacity_req = self.bolt.bolt_capacity

            if (self.flange_plate.design_status == False and bolt_design_status_1 != True ) or (self.web_plate.design_status == False and bolt_design_status_2 != True ):
                self.design_status = False
            else:
                self.bolt.bolt_diameter_provided = bolt_diameter_previous
                self.flange_plate.bolts_required = bolts_required_previous_1
                self.flange_plate.bolt_force = bolt_force_previous_1
                self.web_plate.bolts_required = bolts_required_previous_2
                self.web_plate.bolt_force = bolt_force_previous_2

            if bolt_design_status_1 is True and bolt_design_status_2 is True  :
                self.flange_plate.spacing_status =True
                self.web_plate.spacing_status = True
                self.design_status = True
                self.select_bolt_dia_status = True
                self.get_bolt_grade(self)
            else:
                if self.flange_plate.spacing_status  == False:
                    logger.error(" : Bolted connection is not possible at the flange due to the spacing requirements.")
                if self.web_plate.spacing_status == False:
                    logger.error(" : Bolt connection is not possible at the web due to the spacing requirements.")
                self.design_status = False
                logger.error(" : Bolted design is not possible.")
                logger.error(" : Design is unsafe. \n ")
                logger.info(" :=========End Of design===========")
            # else:
            #     self.large_grip_status = False
            #     self.design_status = False
            #     logger.error(" : Connected plate thickness should not be greater than 8 times diameter")
            #     logger.error(" : Design is not safe. \n ")
            #     logger.info(" :=========End Of design===========")
    def get_bolt_grade(self):
        print(self.design_status, "Getting bolt grade")
        bolt_grade_previous = self.bolt.bolt_grade[-1]
        self.select_bolt_dia_status = False
        grade_status = False
        for self.bolt.bolt_grade_provided in reversed(self.bolt.bolt_grade):
            count = 1
            self.flange_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                           conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)

            if self.preference == "Outside":
                self.flange_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                         bolt_grade_provided=self.bolt.bolt_grade_provided,
                                                         conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                                         n_planes=1)
            else:
                self.flange_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                         bolt_grade_provided=self.bolt.bolt_grade_provided,
                                                         conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                                         n_planes=2)

            self.web_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                        conn_plates_t_fu_fy=self.bolt_conn_plates_web_t_fu_fy)

            self.web_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                  bolt_grade_provided=self.bolt.bolt_grade_provided,
                                                  conn_plates_t_fu_fy=self.bolt_conn_plates_web_t_fu_fy,
                                                  n_planes=2)

            print(self.bolt.bolt_grade_provided, self.bolt.bolt_capacity, self.flange_plate.bolt_force)

            bolt_capacity_reduced_flange = self.flange_plate.get_bolt_red(self.flange_plate.bolts_one_line,
                                                                          self.flange_plate.gauge_provided,self.web_plate.bolt_line,self.web_plate.pitch_provided,
                                                                          self.flange_bolt.bolt_capacity,
                                                                          self.bolt.bolt_diameter_provided)
            bolt_capacity_reduced_web = self.web_plate.get_bolt_red(self.web_plate.bolts_one_line,
                                                                    self.web_plate.gauge_provided,self.web_plate.bolt_line,self.web_plate.pitch_provided,
                                                                    self.web_bolt.bolt_capacity,
                                                                    self.bolt.bolt_diameter_provided)
            if ( bolt_capacity_reduced_flange < self.flange_plate.bolt_force) and  (bolt_capacity_reduced_web  < self.web_plate.bolt_force) and (count >= 1):
                self.bolt.bolt_grade_provided = bolt_grade_previous
                grade_status = True
                break
            bolt_grade_previous = self.bolt.bolt_grade_provided
            grade_status = True
            count += 1

        if grade_status == False:
            self.select_bolt_dia_status = False
            self.design_status = False

        else:
            self.bolt.bolt_grade_provided = bolt_grade_previous
            self.select_bolt_dia_status = True
            self.get_plate_details(self)


    def get_plate_details(self):
        self.get_plate_details_status = False
        self.min_plate_height = self.section.flange_width
        self.max_plate_height = self.section.flange_width

        axial_force_f = self.factored_axial_load * self.section.flange_width * \
                        self.section.flange_thickness / (self.section.area)

        self.flange_force = (((self.moment_flange) / (self.section.depth - self.section.flange_thickness)) +
                             (axial_force_f))
        self.flange_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                       conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)

        if self.preference == "Outside":
            self.flange_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                     bolt_grade_provided=self.bolt.bolt_grade_provided,
                                                     conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                                     n_planes=1)
        else:
            self.flange_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                     bolt_grade_provided=self.bolt.bolt_grade_provided,
                                                     conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                                     n_planes=2)

        self.web_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    conn_plates_t_fu_fy=self.bolt_conn_plates_web_t_fu_fy)

        self.web_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_web_t_fu_fy,
                                              n_planes=2)

        self.flange_plate.get_flange_plate_details(bolt_dia=self.flange_bolt.bolt_diameter_provided,
                                                   flange_plate_h_min=self.min_plate_height,
                                                   flange_plate_h_max=self.max_plate_height,
                                                   bolt_capacity=self.flange_bolt.bolt_capacity,
                                                   min_edge_dist=self.flange_bolt.min_edge_dist_round,
                                                   min_gauge=self.flange_bolt.min_gauge_round,
                                                   max_spacing=self.flange_bolt.max_spacing_round,
                                                   max_edge_dist=self.flange_bolt.max_edge_dist_round,
                                                   axial_load=self.flange_force,gap=self.flange_plate.gap/2,
                                                   web_thickness=self.section.web_thickness,
                                                   root_radius=self.section.root_radius,joint = "half")

        self.min_web_plate_height = round(self.section.min_plate_height() ,2)
        if self.preference == "Outside":
            self.max_web_plate_height = self.section.max_plate_height()
        else:
            self.max_web_plate_height = self.section.depth - 2 * self.section.flange_thickness - (2 * self.webclearance)
        axial_force_w = ((self.section.depth - (2 * self.section.flange_thickness)) *
                         self.section.web_thickness * self.factored_axial_load) / (
                         self.section.area)
        if self.preference =="Outside + Inside":
            self.flange_plate.Innerheight = round_down(((self.section.flange_width - self.section.web_thickness - (self.section.root_radius * 2)) / 2), 5)
        else:
            self.flange_plate.Innerheight =0

        self.web_plate.get_web_plate_details(bolt_dia=self.web_bolt.bolt_diameter_provided,
                                             web_plate_h_min=self.min_web_plate_height,
                                             web_plate_h_max=self.max_web_plate_height,
                                             bolt_capacity=self.web_bolt.bolt_capacity,
                                             min_edge_dist=self.web_bolt.min_edge_dist_round,
                                             min_gauge=self.web_bolt.min_gauge_round,
                                             max_spacing=self.web_bolt.max_spacing_round,
                                             max_edge_dist=self.web_bolt.max_edge_dist_round
                                             , shear_load=self.fact_shear_load, axial_load=self.axial_force_w,web_moment = self.moment_web,

                                             gap=(self.web_plate.gap/2), shear_ecc=True,joint = "half")




        # if self.web_plate.thickness_provided > (self.flange_plate.edge_dist_provided / 2 + self.section.root_radius):
        #     logger.error("erertetre")
        #     self.design_status = False
        # else:
        #     self.design_status = True
        # possible_inner_plate = self.section.flange_width / 2 - self.section.web_thickness / 2 - self.section.root_radius
        # self.flange_plate.edge_dist_provided = (possible_inner_plate- (self.flange_plate.gauge_provided *
        #                                                                ((self.flange_plate.bolts_one_line/2) -1)))/2
        #
        # self.web_spacing_status = True
        if self.flange_plate.design_status is False or self.web_plate.design_status is False :
            self.design_status = False
            self.get_plate_details_status = False
            logger.error(" : Bolted connection is not possible.")
            logger.error(" : Design is unsafe. \n ")
            logger.info(" :=========End Of design===========")
        else:
            if self.preference == "Outside":
                self.design_status = True
                self.get_plate_details_status = True
                self.flange_check_axial(self)

            else:
                self.max_possible_tk = int(self.flange_plate.edge_dist_provided / 2 + self.section.root_radius)
                if self.web_plate.thickness_provided >= (
                        self.flange_plate.edge_dist_provided / 2 + self.section.root_radius):
                    self.design_status = False
                    logger.error(" : The maximum allowable web plate thickness exceeded.")
                    logger.warning(
                        " : The maximum web plate thickness should not be greater than {} mm, to avoid fouling between the plates.".format(
                            self.max_possible_tk))
                    logger.error(" : Design is unsafe. \n ")
                    logger.info(" :=========End Of design===========")
                else:
                    self.design_status = True
                    self.get_plate_details_status = True
                    self.flange_check_axial(self)

            # self.max_possible_tk = int(self.flange_plate.edge_dist_provided / 2 + self.section.root_radius)
            # if self.web_plate.thickness_provided >= (self.flange_plate.edge_dist_provided / 2 + self.section.root_radius):
            #     self.design_status = False
            #     logger.error(" : Maximum web plate thickness exceeded. ")
            #     logger.warning(" : Maximum possible web plate thickness should not be greater than {} mm, to avoid fouling between plates" .format(self.max_possible_tk))
            #     logger.error(" : Design is not safe. \n ")
            #     logger.info(" :=========End Of design===========")
            # else:
            #     self.design_status = True
            #     self.get_plate_details_status = True
            #     self.flange_check_axial(self)


        ################################################################
        ##################################################################
    def flange_check_axial(self):
        ###### # capacity Check for flange = min(block, yielding, rupture)
        #### Block shear capacity of  flange ### #todo comment out
        self.flange_check_axial_status = False
        axial_force_f = self.factored_axial_load * self.section.flange_width * self.section.flange_thickness / (
                        self.section.area)
        self.flange_force = (((self.moment_flange) / (self.section.depth - self.section.flange_thickness)) + (
                            axial_force_f))

        A_vn_flange = (self.section.flange_width - self.flange_plate.bolts_one_line * self.flange_bolt.dia_hole) * \
                      self.section.flange_thickness
        A_v_flange = self.section.flange_thickness * self.flange_plate.height

        self.section.tension_yielding_capacity= self.tension_member_design_due_to_yielding_of_gross_section(
                                                A_v=A_v_flange,
                                                fy=self.section.fy)

        self.section.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
                                                A_vn=A_vn_flange,
                                                fu=self.section.fu)
        #  Block shear strength for flange
        design_status_block_shear = False
        edge_dist = self.flange_plate.edge_dist_provided
        end_dist = self.flange_plate.end_dist_provided
        gauge = self.flange_plate.gauge_provided
        pitch = self.flange_plate.pitch_provided

        while design_status_block_shear == False:

            Avg = 2 * (end_dist + (self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided) \
                       * self.section.flange_thickness
            Avn = 2 * (self.flange_plate.end_dist_provided + (self.flange_plate.bolt_line - 1) *
                       self.flange_plate.pitch_provided - (self.flange_plate.bolt_line - 0.5) *
                       self.flange_bolt.dia_hole) * self.section.flange_thickness
            Atg = 2 * (( self.flange_plate.bolts_one_line / 2 - 1) * self.flange_plate.gauge_provided +
                       self.flange_plate.edge_dist_provided) * self.section.flange_thickness

            Atn = 2 * ((self.flange_plate.bolts_one_line / 2 - 1) * self.flange_plate.gauge_provided -
                       ((self.flange_plate.bolts_one_line / 2 - 0.5) * self.flange_bolt.dia_hole) +
                       self.flange_plate.edge_dist_provided) * \
                       self.section.flange_thickness

            self.section.block_shear_capacity = self.block_shear_strength_section(A_vg=Avg, A_vn=Avn, A_tg=Atg,
                                                                                  A_tn=Atn,
                                                                                  f_u=self.section.fu,
                                                                                  f_y=self.section.fy)

            if self.section.block_shear_capacity <  self.flange_force:
                if self.flange_bolt.max_spacing_round >= pitch + 5 and self.flange_bolt.max_end_dist_round >= end_dist + 5:  # increase thickness todo
                    if self.flange_plate.bolt_line == 1:
                        end_dist += 5
                    else:
                        pitch += 5
                else:
                    break
            else:
                design_status_block_shear = True
                break

            if design_status_block_shear is True:
                break
        if design_status_block_shear is True:
            self.section.tension_capacity_flange = min(self.section.tension_yielding_capacity, self.section.tension_rupture_capacity,
                                                       self.section.block_shear_capacity)
            if self.section.tension_capacity_flange  < self.flange_force:
                self.design_status = False
                self.flange_check_axial_status = False
                logger.warning(": The tension capacity of the flange is less than the required flange force, i.e. {} kN."
                               .format(  round(self.flange_force/1000 ,2)))
                logger.info(": Select a larger beam section or decrease the applied load(s).")
                logger.error(" : Design is not safe. \n ")
                logger.info(" :=========End Of design===========")
            else:
                self.flange_check_axial_status = True
                self.design_status = True
                self.flange_plate_check(self)
        else:
            self.flange_check_axial_status = False
            self.design_status = False
            logger.warning(": The block shear capacity of the flange is less than the required flange force, i.e. {} kN."
                           .format( round(self.flange_force/1000 ,2)))
            logger.info(": Select a larger beam section or decrease the applied load(s)")
            logger.error(" : Design is unsafe. \n ")
            logger.info(" :=========End Of design===========")

    def flange_plate_check(self):
        # capacity Check for flange_outside_plate =min(block, yielding, rupture)
        ####Capacity of flange cover plate for bolted Outside #
        self.flange_plate_check_status =False
        self.axial_force_f = self.factored_axial_load * self.section.flange_width * self.section.flange_thickness / (self.section.area)
        self.flange_force = (((self.moment_flange) / (self.section.depth - self.section.flange_thickness)) + self.axial_force_f)

        if self.preference == "Outside":
            #  Block shear strength for outside flange plate
            design_status_block_shear = False
            # available_flange_thickness = list([x for x in self.flange_plate.thickness if (self.flange_plate.thickness_provided <= x)])
            # for self.flange_plate.thickness_provided in available_flange_thickness:

            edge_dist = self.flange_plate.edge_dist_provided
            end_dist = self.flange_plate.end_dist_provided
            gauge = self.flange_plate.gauge_provided
            pitch = self.flange_plate.pitch_provided

            A_vn_flange = (self.section.flange_width - self.flange_plate.bolts_one_line * self.flange_bolt.dia_hole) * \
                          self.flange_plate.thickness_provided
            A_v_flange = self.flange_plate.thickness_provided * self.flange_plate.height
            self.flange_plate.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
                                                            A_v=A_v_flange,
                                                            fy=self.flange_plate.fy)

            self.flange_plate.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
                                                            A_vn=A_vn_flange,
                                                            fu=self.flange_plate.fu)

            #### Block shear capacity of flange plate ###
            while design_status_block_shear == False:
##################################################################################################################
#For C shape Block shear in Axial
##################################################################################################################
                # Avg = 2 * (self.flange_plate.end_dist_provided + (self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided) * self.flange_plate.thickness_provided
                # Avn = 2 * (self.flange_plate.end_dist_provided + (self.flange_plate.bolt_line - 1)
                #            * self.flange_plate.pitch_provided - (self.flange_plate.bolt_line - 0.5) *
                #            self.flange_bolt.dia_hole) *  self.flange_plate.thickness_provided
                # Atg = 2 * ((((self.flange_plate.bolts_one_line / 2 - 1) * self.flange_plate.gauge_provided) + (
                #             self.flange_plate.edge_dist_provided + self.section.root_radius + self.section.web_thickness / 2))
                #            * self.flange_plate.thickness_provided)
                # Atn = 2 * (((((self.flange_plate.bolts_one_line / 2 - 1) * self.flange_plate.gauge_provided) - (
                #          self.flange_plate.bolts_one_line / 2 - 0.5) * self.flange_bolt.dia_hole)) + (
                #          self.flange_plate.edge_dist_provided + self.section.root_radius + self.section.web_thickness / 2)) \
                #          * self.flange_plate.thickness_provided
#
##################################################################################################################
#For Double L shape Block shear in Axial
##################################################################################################################

                Avg = 2 * (end_dist + (self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided) \
                      * self.flange_plate.thickness_provided
                Avn = 2 * (self.flange_plate.end_dist_provided + (self.flange_plate.bolt_line - 1) *
                           self.flange_plate.pitch_provided - (self.flange_plate.bolt_line - 0.5) *
                           self.flange_bolt.dia_hole) * self.flange_plate.thickness_provided
                Atg = 2 * ((self.flange_plate.bolts_one_line / 2 - 1) * self.flange_plate.gauge_provided +
                           self.flange_plate.edge_dist_provided) * self.flange_plate.thickness_provided

                Atn = 2 * ((self.flange_plate.bolts_one_line / 2 - 1) * self.flange_plate.gauge_provided -
                           ((self.flange_plate.bolts_one_line / 2 - 0.5) * self.flange_bolt.dia_hole) +
                           self.flange_plate.edge_dist_provided) * \
                      self.flange_plate.thickness_provided

                self.flange_plate.block_shear_capacity = self.block_shear_strength_plate(A_vg=Avg, A_vn=Avn,
                                                                                         A_tg=Atg,
                                                                                         A_tn=Atn,
                                                                                         f_u=self.flange_plate.fu,
                                                                                         f_y=self.flange_plate.fy)
                if self.flange_plate.block_shear_capacity < self.flange_force :
                    if self.flange_bolt.max_spacing_round >= pitch + 5 and self.flange_bolt.max_end_dist_round >= end_dist + 5:  # increase thickness todo
                        if self.flange_plate.bolt_line == 1:
                            end_dist += 5
                        else:
                            pitch += 5
                    else:
                        break
                else:
                    design_status_block_shear = True
                    break
            # if design_status_block_shear is True:
            #     break

            if design_status_block_shear is True:
                self.flange_plate.tension_capacity_flange_plate= min(self.flange_plate.tension_yielding_capacity,
                                                    self.flange_plate.tension_rupture_capacity,
                                                    self.flange_plate.block_shear_capacity)

                if self.flange_plate.tension_capacity_flange_plate < self.flange_force:
                    if len(self.flange_plate.thickness) >= 2:
                        thk_f = self.flange_plate.thickness_provided
                        self.initial_pt_thk(self, previous_thk_flange=  thk_f)
                    else:
                        self.flange_plate_check_status = False
                        self.design_status = False
                        logger.warning(": The tension capacity of the flange plate is less than the required flange force, i.e. {} kN."
                                       .format( round(self.flange_force/1000 ,2)))
                        logger.info(": Increase the thickness of the flange plate or decrease the applied load(s)")
                        logger.error(" : Design is unsafe. \n ")
                        logger.info(" :=========End Of design===========")
                else:
                    self.flange_plate_check_status =True
                    self.design_status = True
                    self.web_axial_check(self)
            else:
                self.flange_plate_check_status = False
                self.design_status = False
                logger.warning(": The block shear capacity of the flange plate is less than the required flange force, i.e. {} kN."
                               .format(round(self.flange_force/1000 ,2)))
                logger.info(": Increase the thickness of the flange plate or decrease the applied load(s).")
                logger.error(" : Design is unsafe. \n ")
                logger.info(" :=========End Of design===========")

        else:
            # capacity Check for flange_outsite_plate =min(block, yielding, rupture)
            #  Block shear strength for outside + inside flange plate
            # OUTSIDE-inside

            design_status_block_shear = False
            # available_flange_thickness = list([x for x in self.flange_plate.thickness if ((self.flange_plate.thickness_provided) <= x)])
            # for self.flange_plate.thickness_provided in available_flange_thickness:

            edge_dist = self.flange_plate.edge_dist_provided
            end_dist = self.flange_plate.end_dist_provided
            gauge = self.flange_plate.gauge_provided
            pitch = self.flange_plate.pitch_provided

            #  yielding,rupture  for  inside flange plate
            # self.flange_plate.Innerheight = round_down(self.section.flange_width - self.section.web_thickness - (self.section.root_radius * 2)) / 2),5)
            flange_plate_height_outside = self.flange_plate.height
            self.flange_plate.Innerlength = self.flange_plate.length

            A_vn_flange = (((2 * self.flange_plate.Innerheight ) + self.section.flange_width) - (self.flange_plate.bolts_one_line * self.flange_bolt.dia_hole)) * self.flange_plate.thickness_provided
            A_v_flange = ((2 *self.flange_plate.Innerheight ) + self.section.flange_width) * self.flange_plate.thickness_provided
            self.flange_plate.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
                A_v=A_v_flange,
                fy=self.flange_plate.fy)

            self.flange_plate.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
                A_vn=A_vn_flange,
                fu=self.flange_plate.fu)
            #### Block shear capacity of flange plate ###

            while design_status_block_shear == False:
                ##################################################################################################################
                # For Double U shape Block shear in Axial
                ##################################################################################################################
                # Avg = 2 * (self.flange_plate.end_dist_provided + (
                #         self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided) * self.flange_plate.thickness_provided
                # Avn = 2 * (self.flange_plate.end_dist_provided + (
                #         self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided - (
                #                    self.flange_plate.bolt_line - 0.5) * self.flange_bolt.dia_hole) * \
                #       self.flange_plate.thickness_provided
                # Atg = 2*((((self.flange_plate.bolts_one_line/2 - 1) * self.flange_plate.gauge_provided) + (self.flange_plate.edge_dist_provided +self.section.root_radius + self.section.web_thickness/2))
                #      * self.flange_plate.thickness_provided) #
                # Atn =  2*(((((self.flange_plate.bolts_one_line/2 - 1) * self.flange_plate.gauge_provided) - (
                #         self.flange_plate.bolts_one_line/2 - 0.5) * self.flange_bolt.dia_hole)) +
                #           (self.flange_plate.edge_dist_provided +self.section.root_radius + self.section.web_thickness/2)) * self.flange_plate.thickness_provided

                ##################################################################################################################
                # For Double L shape Block shear in Axial
                ##################################################################################################################

                Avg = 2 * (end_dist + (self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided) \
                      * self.flange_plate.thickness_provided
                Avn = 2 * (self.flange_plate.end_dist_provided + (self.flange_plate.bolt_line - 1) *
                           self.flange_plate.pitch_provided - (self.flange_plate.bolt_line - 0.5) *
                           self.flange_bolt.dia_hole) * self.flange_plate.thickness_provided
                Atg = 2 * ((self.flange_plate.bolts_one_line / 2 - 1) * self.flange_plate.gauge_provided +
                           self.flange_plate.edge_dist_provided) * self.flange_plate.thickness_provided

                Atn = 2 * ((self.flange_plate.bolts_one_line / 2 - 1) * self.flange_plate.gauge_provided -
                           ((self.flange_plate.bolts_one_line / 2 - 0.5) * self.flange_bolt.dia_hole) +
                           self.flange_plate.edge_dist_provided) * \
                      self.flange_plate.thickness_provided

                self.flange_plate_block_shear_capactity_outside = self.block_shear_strength_plate(A_vg=Avg, A_vn=Avn,
                                                                                             A_tg=Atg,
                                                                                             A_tn=Atn,
                                                                                             f_u=self.flange_plate.fu,
                                                                                             f_y=self.flange_plate.fy)

                #  Block shear strength for inside flange plate under AXIAL
                Avg = 2 * (self.flange_plate.end_dist_provided + (
                        self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided) \
                      * self.flange_plate.thickness_provided
                Avn = 2 * (self.flange_plate.end_dist_provided + (
                        self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided - (
                                   self.flange_plate.bolt_line - 0.5) * self.flange_bolt.dia_hole) * \
                      self.flange_plate.thickness_provided

                Atg = 2 * ((self.flange_plate.bolts_one_line/2  - 1) * self.flange_plate.gauge_provided + self.flange_plate.edge_dist_provided )* \
                      self.flange_plate.thickness_provided
                # todo add in DDCl and diagram
                Atn = 2 * ((self.flange_plate.bolts_one_line/2  - 1) *
                           self.flange_plate.gauge_provided - ((self.flange_plate.bolts_one_line/2  - 0.5) * self.flange_bolt.dia_hole)+ self.flange_plate.edge_dist_provided )* \
                      self.flange_plate.thickness_provided
                # todo add in DDCl
                self.flange_plate_block_shear_capacity_inside = self.block_shear_strength_plate(A_vg=Avg, A_vn=Avn,
                                                                                           A_tg=Atg,
                                                                                           A_tn=Atn,
                                                                                           f_u=self.flange_plate.fu,
                                                                                           f_y=self.flange_plate.fy)
                self.flange_plate.block_shear_capacity = self.flange_plate_block_shear_capactity_outside + self.flange_plate_block_shear_capacity_inside

                if self.flange_plate.block_shear_capacity <  self.flange_force :
                    if self.flange_bolt.max_spacing_round >= pitch + 5 and self.flange_bolt.max_end_dist_round >= end_dist + 5:  # increase thickness todo
                        if self.flange_plate.bolt_line == 1:
                            end_dist += 5
                        else:
                            pitch += 5
                    else:
                        break
                else:
                    design_status_block_shear = True
                    break
            # if design_status_block_shear is True:
            #     break

            if design_status_block_shear is True:
                self.flange_plate.tension_capacity_flange_plate = min(self.flange_plate.tension_yielding_capacity,
                                                    self.flange_plate.tension_rupture_capacity,
                                                    self.flange_plate.block_shear_capacity)
                print ("flange_force",self.flange_force)
                print(self.flange_plate.tension_capacity_flange_plate, "tension_capacity_flange_plate")
                if  self.flange_plate.tension_capacity_flange_plate < self.flange_force:
                    # self.flange_plate_check_status = False
                    if len(self.flange_plate.thickness) >= 2:
                        thk_f = self.flange_plate.thickness_provided
                        self.initial_pt_thk(self, previous_thk_flange= thk_f)
                    else:
                        self.flange_plate_check_status = False
                        self.design_status = False
                        logger.warning(": The tension capacity of the flange plate is less than the required flange force, i.e. {} kN."
                                       .format( round(self.flange_force/1000 ,2)))
                        logger.info(": Increase the thickness of the flange plate or decrease the applied load(s).")
                        logger.error(" : Design is unsafe. \n ")
                        logger.info(" :=========End Of design===========")
                else:
                    self.flange_plate_check_status = True
                    self.design_status = True
                    self.web_axial_check(self)
            else:
                self.flange_plate_check_status = False
                self.design_status = False
                logger.warning(": The block shear capacity of the flange plate is less than the required flange force, i.e. {} kN."
                               .format(round(self.flange_force/1000 ,2)))
                logger.info(": Increase the thickness of the flange plate or decrease the applied load(s).")
                logger.error(" : Design is unsafe. \n ")
                logger.info(" :=========End Of design===========")

        ######################################################################### ##
                    # Design of web splice plate

    ################################ CAPACITY CHECK FOR WEB #####################################################################################

    def web_axial_check(self):
        self.web_axial_check_status = False
        self.axial_force_w = ((self.section.depth - (2 * self.section.flange_thickness)) * self.section.web_thickness *  self.factored_axial_load ) / (self.section.area )

        ###### # capacity Check for web in axial = min(block, yielding, rupture)
        A_vn_web =  (( self.section.depth - (2 * self.section.flange_thickness) - (self.web_plate.bolts_one_line * self.web_bolt.dia_hole))) \
                   * self.section.web_thickness
        A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
        self.section.tension_yielding_capacity_web = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_web, fy=self.section.fy)
        self.section.tension_rupture_capacity_web = self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_vn_web, fu=self.section.fu)

        design_status_block_shear = False
        edge_dist = self.web_plate.edge_dist_provided
        end_dist = self.web_plate.end_dist_provided
        gauge = self.web_plate.gauge_provided
        pitch = self.web_plate.pitch_provided

        #### Block shear capacity of web in axial ###
        while design_status_block_shear == False:
            Avg = 2 * ((self.web_plate.bolt_line - 1) * pitch + end_dist) * \
                  self.section.web_thickness
            Avn = 2 * ((self.web_plate.bolt_line - 1) * pitch - (
                    self.web_plate.bolt_line - 0.5) * self.web_bolt.dia_hole + end_dist) * \
                  self.section.web_thickness
            Atg = (self.web_plate.edge_dist_provided + (
                    self.web_plate.bolts_one_line - 1) * gauge) * self.section.web_thickness
            Atn = (self.web_plate.edge_dist_provided + (
                    self.web_plate.bolts_one_line - 1) * gauge - (
                           self.web_plate.bolts_one_line - 1) * self.web_bolt.dia_hole) * self.section.web_thickness

            self.section.block_shear_capacity_web = self.block_shear_strength_section(A_vg=Avg, A_vn=Avn, A_tg=Atg,
                                                                                    A_tn=Atn,
                                                                                    f_u=self.section.fu,
                                                                                    f_y=self.section.fy)

            if self.section.block_shear_capacity_web <  self.axial_force_w :
                if self.web_bolt.max_spacing_round >= pitch + 5 and self.web_bolt.max_end_dist_round >= end_dist + 5:  # increase thickness todo
                    if self.web_plate.bolt_line == 1:
                        end_dist += 5
                    else:
                        pitch += 5
                else:
                    break
            else:
                design_status_block_shear = True
                break
        if design_status_block_shear == True:
            self.section.tension_capacity_web = min(self.section.tension_yielding_capacity_web, self.section.tension_rupture_capacity_web,
                                             self.section.block_shear_capacity_web)

            self.axial_force_w = ((self.section.depth - (2 * self.section.flange_thickness)) * self.section.web_thickness *  self.factored_axial_load ) / (self.section.area )
            if self.section.tension_capacity_web < self.axial_force_w:
                self.web_axial_check_status = False
                self.design_status = False
                logger.warning(" : The tension capacity of the web is less than the required axial force, i.e. {} kN."
                               .format(round(self.axial_force_w/1000 ,2)))
                logger.info(" : Select a larger beam section or decrease the applied axial load(s).")
                logger.error(" : Design is unsafe. \n ")
                logger.info(" :=========End Of design===========")
            else:
                self.web_axial_check_status =True
                self.design_status = True
                self.web_plate_axial_check(self)
        else:
            self.web_axial_check_status = False
            self.design_status = False
            logger.warning(" : The block shear capacity of the web is less than the required axial force, i.e. {} kN.".format(round(self.axial_force_w/1000 ,2)))
            logger.info(" : Select a larger beam section or decrease the applied axial load.")
            logger.error(" : Design is unsafe. \n ")
            logger.info(" :=========End Of design===========")

#         ###### # capacity Check for web plate in axial = min(block, yielding, rupture)
    def web_plate_axial_check(self):
        self.web_plate_axial_check_status = False
        self.axial_force_w = ((self.section.depth - (2 * self.section.flange_thickness))
                              * self.section.web_thickness * self.factored_axial_load) / (
                              self.section.area)

        A_vn_web = 2*(self.web_plate.height - (self.web_plate.bolts_one_line * self.web_bolt.dia_hole)) \
                   * self.web_plate.thickness_provided
        A_v_web = 2*self.web_plate.height * self.web_plate.thickness_provided
        self.web_plate.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
                                                    A_v=A_v_web, fy=self.web_plate.fy)
        self.web_plate.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
                                                    A_vn=A_vn_web, fu=self.web_plate.fu)
        design_status_block_shear = False
        # available_web_thickness = list([x for x in self.web_plate.thickness if ((self.web_plate.thickness_provided) <= x)])
        # for self.web_plate.thickness_provided in available_web_thickness:
        edge_dist = self.web_plate.edge_dist_provided
        end_dist = self.web_plate.end_dist_provided
        gauge = self.web_plate.gauge_provided
        pitch = self.web_plate.pitch_provided
        # print(1)

        #### Block shear capacity of web plate in axial ###

        while design_status_block_shear == False:
            Avg = 2 * ((self.web_plate.bolt_line - 1) * pitch + end_dist) * \
                  self.web_plate.thickness_provided
            Avn = 2 * ((self.web_plate.bolt_line - 1) * pitch - ((
                    self.web_plate.bolt_line - 0.5) * self.web_bolt.dia_hole) + end_dist) * \
                  self.web_plate.thickness_provided
            Atg = (self.web_plate.edge_dist_provided + (
                    self.web_plate.bolts_one_line - 1) * gauge) * self.web_plate.thickness_provided
            Atn = (self.web_plate.edge_dist_provided + (
                    self.web_plate.bolts_one_line - 1) * gauge - (
                           self.web_plate.bolts_one_line - 1) * self.web_bolt.dia_hole) * self.web_plate.thickness_provided

            self.web_plate.block_shear_capacity = self.block_shear_strength_section(A_vg=Avg, A_vn=Avn, A_tg=Atg,
                                                                                    A_tn=Atn,
                                                                                    f_u=self.web_plate.fu,
                                                                                    f_y=self.web_plate.fy)
            print("block_shear_strength_section",self.web_plate.block_shear_capacity )
            self.web_plate.block_shear_capacity = 2 * self.web_plate.block_shear_capacity
            if self.web_plate.block_shear_capacity < self.axial_force_w:
                if self.web_bolt.max_spacing_round >= pitch + 5 and self.web_bolt.max_end_dist_round >= end_dist + 5:  # increase thickness todo
                    if self.web_plate.bolt_line == 1:
                        end_dist += 5
                    else:
                        pitch += 5

                else:
                    break

            else:
                design_status_block_shear = True
                break

        # if design_status_block_shear == True:
        #     break
        if design_status_block_shear == True:

            self.web_plate.tension_capacity_web_plate = min( self.web_plate.tension_yielding_capacity ,
                                                             self.web_plate.tension_rupture_capacity,
                                                             self.web_plate.block_shear_capacity)
            if self.web_plate.tension_capacity_web_plate < self.axial_force_w:
                # self.web_plate_axial_check_status = False
                if len(self.web_plate.thickness) >= 2:
                    thk = self.web_plate.thickness_provided
                    self.initial_pt_thk(self, previous_thk_web=thk)
                else:
                    self.web_plate_axial_check_status = False
                    self.design_status = False
                    logger.warning(": The tension capacity of the web plate is less than the required axial force, i.e. {} kN."
                                   .format(round(self.axial_force_w/1000 ,2)))
                    logger.info(": Increase the thickness of the web plate or decrease the applied axial load.")
                    logger.error(" : Design is unsafe. \n ")
                    logger.info(" :=========End Of design===========")
            else:
                self.web_plate_axial_check_status = True
                self.design_status = True
                self.web_shear_plate_check(self)
        else:
            self.web_plate_axial_check_status = False
            self.design_status = False
            logger.warning(": The block shear capacity of the web plate is less than the required axial force, i.e. {} kN.".format( round(self.axial_force_w/1000 ,2)))
            logger.info(" : Increase the thickness of the web plate or decrease the applied axial load.")
            logger.error(" : Design is unsafe. \n ")
            logger.info(" :=========End Of design===========")
    def web_shear_plate_check(self):
        ###### # capacity Check for web plate  in shear = min(block, yielding, rupture)
        self.web_shear_plate_check_status = False
        self.shear_yielding_status = False
        A_vn_web = 2 * (self.web_plate.height - (self.web_plate.bolts_one_line * self.web_bolt.dia_hole)) * \
                   self.web_plate.thickness_provided
        A_v_web = 2 * self.web_plate.height * self.web_plate.thickness_provided
        self.web_plate.shear_yielding_capacity = round(0.6*self.shear_yielding(
            A_v=A_v_web, fy=self.web_plate.fy),2)
        if  self.web_plate.shear_yielding_capacity < self.fact_shear_load:
            # self.web_shear_plate_check_status = False
            if len(self.web_plate.thickness) >= 2:
                thk = self.web_plate.thickness_provided
                self.initial_pt_thk(self, previous_thk_web=thk)
            else:
                self.web_shear_plate_check_status = False
                self.design_status = False
                logger.warning(": The shear capacity of the web plate is less than the required factored shear load, i.e. {} kN.".format(
                    round(self.fact_shear_load / 1000, 2)))
                logger.info(": Increase the thickness of the web plate or decrease the applied shear load.")
                logger.error(" : Design is unsafe. \n ")
                logger.info(" :=========End Of design===========")
        else:
            self.shear_yielding_status = True
            self.design_status = True

        self.web_plate.shear_rupture_capacity = self.shear_rupture_(
            A_vn=A_vn_web, fu=self.web_plate.fu)
        design_status_block_shear = False
        # available_web_thickness = list([x for x in self.web_plate.thickness if ((self.web_plate.thickness_provided) <= x)])
        # for self.web_plate.thickness_provided in available_web_thickness:  #
        edge_dist = self.web_plate.edge_dist_provided
        end_dist = self.web_plate.end_dist_provided
        gauge = self.web_plate.gauge_provided
        pitch = self.web_plate.pitch_provided

        #### Block shear capacity of web plate ###

        while design_status_block_shear == False:
            Atg = (((self.web_plate.bolt_line - 1) * self.web_plate.pitch_provided) + self.web_plate.end_dist_provided) * self.web_plate.thickness_provided
            Atn = (((self.web_plate.bolt_line - 1) * self.web_plate.pitch_provided) - ((
                        self.web_plate.bolt_line - 0.5) * self.web_bolt.dia_hole) + self.web_plate.end_dist_provided) * self.web_plate.thickness_provided
            Avg = (self.web_plate.edge_dist_provided + (
                        self.web_plate.bolts_one_line - 1) * self.web_plate.gauge_provided) * self.web_plate.thickness_provided
            Avn = ((((self.web_plate.bolts_one_line - 1)* self.web_plate.gauge_provided)
                    +self.web_plate.edge_dist_provided)- ((self.web_plate.bolts_one_line - 0.5)
                                                          * self.web_bolt.dia_hole)) *self.web_plate.thickness_provided

            self.web_plate.block_shear_capacity_shear = self.block_shear_strength_section(A_vg=Avg, A_vn=Avn, A_tg=Atg,
                                                                                    A_tn=Atn,
                                                                                    f_u=self.web_plate.fu,
                                                                                    f_y=self.web_plate.fy)
            self.web_plate.block_shear_capacity_shear = 2 * self.web_plate.block_shear_capacity_shear
            if self.web_plate.block_shear_capacity_shear < self.fact_shear_load:
                if self.web_bolt.max_spacing_round >= pitch + 5 and self.web_bolt.max_end_dist_round >= end_dist + 5:  # increase thickness todo
                    if self.web_plate.bolt_line == 1:
                        end_dist += 5
                    else:
                        pitch += 5
                else:
                    break
            else:
                design_status_block_shear = True
                break
        # if design_status_block_shear is True:
        #     break

        if design_status_block_shear is True:
            self.web_plate.shear_capacity_web_plate = round(min(self.web_plate.shear_yielding_capacity,
                                                          self.web_plate.shear_rupture_capacity,
                                                          self.web_plate.block_shear_capacity_shear),2)
            # self.allowable_web_shear_cap = round(0.6 *self.web_plate.shear_capacity_web_plate,2)
            if self.web_plate.shear_capacity_web_plate  < self.fact_shear_load:
                # self.web_shear_plate_check_status = False
                if len(self.web_plate.thickness) >= 2:
                    thk = self.web_plate.thickness_provided
                    self.initial_pt_thk(self, previous_thk_web=thk)
                else:
                    self.web_shear_plate_check_status = False
                    self.design_status = False
                    logger.warning(": The shear capacity of the web plate is less than the required factored shear load, i.e. {} kN."
                                   .format(round(self.fact_shear_load/1000, 2)))
                    logger.info(": Increase the thickness of the web plate or decrease the applied shear load.")
                    logger.error(" : Design is unsafe. \n ")
                    logger.info(" :=========End Of design===========")
            else:
                self.web_shear_plate_check_status = True
                self.design_status = True
                logger.info(": Overall bolted cover plate splice connection design is safe \n")
                logger.info(" :=========End Of design===========")
        else:
            self.web_shear_plate_check_status = False
            self.design_status = False
            logger.warning(" : The block shear capacity of the web plate is less than the required factored shear load, i.e. {} kN."
                           .format( round(self.fact_shear_load/1000 ,2)))
            logger.info(" : Increase the thickness of the web plate or decrease the applied shear load.")
            logger.error(" : Design is unsafe. \n ")
            logger.info(" :=========End Of design===========")

        ####todo comment out

        self.flange_plate.length = self.flange_plate.length * 2
        self.web_plate.length = self.web_plate.length * 2
        # self.web_plate.height = 110
        self.flange_plate.bolt_line = 2 * self.flange_plate.bolt_line
        self.flange_plate.bolts_one_line = self.flange_plate.bolts_one_line
        self.flange_plate.bolts_required = self.flange_plate.bolt_line *self.flange_plate.bolts_one_line
        self.flange_plate.midgauge = 2*(self.flange_plate.edge_dist_provided + self.section.root_radius) + \
                                     self.section.web_thickness
        self.web_plate.midpitch = (2*self.web_plate.end_dist_provided) +self.web_plate.gap
        self.flange_plate.midpitch = (2 * self.flange_plate.end_dist_provided) + self.flange_plate.gap


        self.web_plate.bolts_one_line =  self.web_plate.bolts_one_line
        self.web_plate.bolt_line = 2 * self.web_plate.bolt_line
        self.web_plate.bolts_required = self.web_plate.bolt_line * self.web_plate.bolts_one_line
        self.flange_plate.Innerlength = self.flange_plate.length

        self.min_plate_length = (((self.flange_plate.bolt_line / 2 - 1) * self.flange_bolt.min_pitch) +
                                 (2*self.flange_bolt.min_end_dist) + (self.flange_plate.gap/2))
        print("self.min_plate_length",self.min_plate_length)
        if self.preference =="Outside":
            self.flange_out_plate_tk = self.flange_plate.thickness_provided
            self.flange_in_plate_tk =0.0
        else :
            self.flange_in_plate_tk = self.flange_plate.thickness_provided
            self.flange_out_plate_tk = self.flange_plate.thickness_provided


        if self.preference =="Outside":
            self.plate_out_len = self.flange_plate.length
            self.plate_in_len = 0.0
        else:
            self.plate_out_len = self.flange_plate.length
            self.plate_in_len = self.flange_plate.Innerlength

        # print("anjali", self.anjali)
        print(self.section)
        print(self.load)
        print(self.flange_bolt)
        print(self.flange_plate)
        print(self.web_bolt)
        print(self.web_plate)
        print(self.web_plate.thickness_provided)
        print(self.flange_plate.thickness_provided)
        #print(design_status)
        print(self.flange_plate.length )
        print(self.web_plate.length )
        print(self.flange_plate.bolts_required )
        print(self.web_plate.bolts_required )
        print("bolt dia",self.flange_bolt.bolt_diameter_provided)
        print("flange_plate.Innerlength", self.flange_plate.Innerlength)
        print("flange_plate.Innerheight", self.flange_plate.Innerheight)
        print("flange_plate.gap", self.flange_plate.gap)
        print(self.web_plate.length)
        print("webplategap", self.web_plate.gap)

        print( "self.flange_plate.midgauge" , self.flange_plate.midgauge)
        print( "self.web_plate.midpitch" ,self.web_plate.midpitch)
        print( "self.flange_plate.midpitch" ,  self.flange_plate.midpitch)

        # if self.design_status == True:
        #
        #     logger.info(": Overall bolted cover plate splice connection design is safe \n")
        #     logger.info(" :=========End Of design===========")
        # else:
        #     logger.error(": Design is not safe \n ")
        #     logger.info(" :=========End Of design===========")
################################ Design Report #####################################################################################

 ################################ CAPACITY CHECK Functions#####################################################################################

    @staticmethod
    def block_shear_strength_plate(A_vg, A_vn, A_tg, A_tn, f_u, f_y):  # for flange plate
        """Calculate the block shear strength of bolted connections as per cl. 6.4.1

        Args:
            A_vg: Minimum gross area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_vn: Minimum net area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_tg: Minimum gross area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            A_tn: Minimum net area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            f_u: Ultimate stress of the plate material in MPa (float)
            f_y: Yield stress of the plate material in MPa (float)

        Return:
            block shear strength of bolted connection in N (float)

        Note:
            Reference:
            IS 800:2007, cl. 6.4.1

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = A_vg * f_y / (math.sqrt(3) * gamma_m0) + 0.9 * A_tn * f_u / gamma_m1
        T_db2 = 0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1) + A_tg * f_y / gamma_m0
        Tdb = min(T_db1, T_db2)
        Tdb = round(Tdb , 3)
        return Tdb

        # Function for block shear capacity calculation

    @staticmethod
    def block_shear_strength_section(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        """Calculate the block shear strength of bolted connections as per cl. 6.4.1

        Args:
            A_vg: Minimum gross area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_vn: Minimum net area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_tg: Minimum gross area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            A_tn: Minimum net area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            f_u: Ultimate stress of the plate material in MPa (float)
            f_y: Yield stress of the plate material in MPa (float)

        Return:
            block shear strength of bolted connection in N (float)

        Note:
            Reference:
            IS 800:2007, cl. 6.4.1

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = A_vg * f_y / (math.sqrt(3) * gamma_m0) + 0.9 * A_tn * f_u / gamma_m1
        T_db2 = 0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1) + A_tg * f_y / gamma_m0
        Tdb = min(T_db1, T_db2)
        Tdb = round(Tdb , 2)
        return Tdb
        # cl 6.2 Design Strength Due to Yielding of Gross Section

    @staticmethod
    def tension_member_design_due_to_yielding_of_gross_section(A_v, fy):
        '''
             Args:
                 A_v (float) Area under shear
                 Beam_fy (float) Yield stress of Beam material
             Returns:
                 Capacity of Beam web in shear yielding
             '''
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        # A_v = height * thickness
        tdg = (A_v * fy) / (gamma_m0 )
        return tdg

    @staticmethod
    def tension_member_design_due_to_rupture_of_critical_section(A_vn, fu):
        '''
               Args:
                   A_vn (float) Net area under shear
                   Beam_fu (float) Ultimate stress of Beam material
               Returns:
                   Capacity of beam web in shear rupture
               '''

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        # A_vn = (height- bolts_one_line * dia_hole) * thickness
        T_dn = 0.9 * A_vn * fu / (gamma_m1)
        return T_dn

    @staticmethod
    def shear_yielding(A_v,fy):
        '''
        Args:
            length (float) length of member in direction of shear load
            thickness(float) thickness of member resisting shear
            beam_fy (float) Yeild stress of section material
        Returns:
            Capacity of section in shear yeiding
        '''

        # A_v = length * thickness
        gamma_m0 = 1.1
        # print(length, thickness, fy, gamma_m0)
        # V_p = (0.6 * A_v * fy) / (math.sqrt(3) * gamma_m0 * 1000)  # kN
        V_p = (A_v * fy) / (math.sqrt(3) * gamma_m0 )  # N
        return V_p

    @staticmethod
    def shear_rupture_(A_vn, fu):
        '''
               Args:
                   A_vn (float) Net area under shear
                   Beam_fu (float) Ultimate stress of Beam material
               Returns:
                   Capacity of beam web in shear rupture
               '''

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        # A_vn = (height- bolts_one_line * dia_hole) * thickness
        T_dn = 0.75 * A_vn * fu / (math.sqrt(3) *gamma_m1)
        return T_dn
    #
    # def web_force(column_d, column_f_t, column_t_w, axial_force, column_area):
    #     """
    #     Args:
    #        c_d: Overall depth of the column section in mm (float)
    #        column_f_t: Thickness of flange in mm (float)
    #        column_t_w: Thickness of flange in mm (float)
    #        axial_force: Factored axial force in kN (float)
    #
    #     Returns:
    #         Force in flange in kN (float)
    #     """
    #     axial_force_w = int(
    #         ((column_d - 2 * (column_f_t)) * column_t_w * axial_force ) / column_area)   # N
    #     return round(axial_force_w)

    @staticmethod
    def limiting_width_thk_ratio(column_f_t, column_t_w, D, column_b, column_fy, factored_axial_force,
                                 column_area, compression_element, section):
        column_d = D - (2 * column_f_t)
        epsilon = float(math.sqrt(250 / column_fy))
        axial_force_w = int(
            ((D - 2 * (column_f_t)) * column_t_w * factored_axial_force) / (column_area))  # N

        des_comp_stress_web = column_fy
        des_comp_stress_section = column_fy
        avg_axial_comp_stress = axial_force_w / ((D - 2 * column_f_t) * column_t_w)
        r1 = avg_axial_comp_stress / des_comp_stress_web
        r2 = avg_axial_comp_stress / des_comp_stress_section
        a = column_b / column_f_t
        # column_d = D - 2(column_f_t)
        # compression_element=["External","Internal","Web of an I-H" ,"box section" ]
        # section=["rolled","welded","compression due to bending","generally", "Axial compression" ]
        # section = "rolled"
        if compression_element == "External" or compression_element == "Internal":
            if section == "Rolled":
                if column_b * 0.5 / column_f_t <= 9.4 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 10.5 * epsilon:
                    class_of_section1 = "compact"
                # elif column_b * 0.5 / column_f_t <= 15.7 * epsilon:
                #     class_of_section1 = "semi-compact"
                else:
                      class_of_section1 = "semi-compact"
            elif section == "welded":
                if column_b * 0.5 / column_f_t <= 8.4 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 9.4 * epsilon:
                    class_of_section1 = "compact"
                # elif column_b * 0.5 / column_f_t <= 13.6 * epsilon:
                    # class_of_section1 = "semi-compact"
                else:
                    class_of_section1 = "semi-compact"
                # else:
                #     print('fail')
            elif section == "compression due to bending":
                if column_b * 0.5 / column_f_t <= 29.3 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 33.5 * epsilon:
                    class_of_section1 = "compact"
                # elif column_b * 0.5 / column_f_t <= 42 * epsilon:
                    # class_of_section1 = "semi-compact"
                else:
                      class_of_section1 = "semi-compact"
                # else:
                #     print('fail')
            # else:
            #     pass

        elif compression_element == "Web of an I-H" or compression_element == "box section":
            if section == "generally":
                if r1 < 0:
                    if column_d / column_t_w <= max((84 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "plastic"
                    elif column_d / column_t_w <= (max(105 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "compact"
                    else:
                        class_of_section1 = "semi-compact"
                    # else:
                    #     print('fail')
                    # print("class_of_section3", class_of_section)
                elif r1 > 0:
                    if column_d / column_t_w <= max((84 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "plastic"
                    elif column_d / column_t_w <= max((105 * epsilon / (1 + (r1 * 1.5))), (
                            42 * epsilon)):
                        class_of_section1 = "compact"
                    else:
                        class_of_section1 = "semi-compact"

            elif section == "Axial compression":
                if column_d / column_t_w <= (42 * epsilon):
                    class_of_section1 = "semi-compact"
                else:
                    class_of_section1 = "N/A"

        print("class_of_section", class_of_section1)
        if class_of_section1 == "plastic":
            class_of_section1 = 1
        elif class_of_section1 == "compact":
            class_of_section1 = 2
        elif class_of_section1 == "semi-compact":
            class_of_section1 = 3
        # else:
        #     print('fail')
        print("class_of_section2", class_of_section1)
        print("class_of_section1", class_of_section1)
        return class_of_section1

    def min_thick_based_on_area(self, tk, width, list_of_pt_tk, t_w, r_1, D,
                                preference=None,fp_thk =None):
        """

        Args:
            tk: flange thickness
            width: flange width
            list_of_pt_tk: list of plate thickness greater than the section thickness
            t_w: web thickness
            r_1: root radius
            D: depth of the section
            fp_thk: flange thickness provided

            area of flange plate should be greater than 1.05 times area of flange [Ref: cl.8.6.3.2 IS 800:2007]
            minimum outside flange plate width = 50 mm
            minimum inside flange plate width = 50 mm
            webclearance = (max (self.section.root_radius, fp_thk)) +25 for depth > 600 mm
                         = (max (self.section.root_radius, fp_thk)) +10 for depth < 600 mm
        Returns:

        """

        self.flange_crs_sec_area = tk * width
        self.Ap = self.flange_crs_sec_area * 1.05
        # self.design_status = True
        for y in list_of_pt_tk:
            if preference != None:
                if preference == "Outside":
                    self.outerwidth = width
                    if self.outerwidth < 50:
                        thickness = y
                        self.initial_pt_thk_status = False
                        self.design_status = False
                    else:
                        pass
                    self.flange_plate_crs_sec_area = y * width

                    if self.flange_plate_crs_sec_area >= self.flange_crs_sec_area * 1.05:
                        thickness = y
                        break
                    else:
                        thickness = y
                        self.initial_pt_thk_status = False
                        self.design_status = False

                elif preference == "Outside + Inside":
                    self.outerwidth = width
                    self.innerwidth = (width - t_w - (2 * r_1)) / 2
                    if self.outerwidth < 50:
                        self.design_status = False
                        self.initial_pt_thk_status = False
                    else:
                        if self.innerwidth < 50:
                            self.initial_pt_thk_status = False
                            # self.design_status =False
                            self.design_status = False
                            thickness = y
                        else:
                            self.flange_plate_crs_sec_area = (self.outerwidth + (2*self.innerwidth)) * y
                            if self.flange_plate_crs_sec_area >= self.flange_crs_sec_area * 1.05:
                                thickness = y
                                break
                            else:
                                thickness = y
                                self.initial_pt_thk_status = False
                                self.design_status = False

            else:
                if self.section.depth > 600.00:
                    self.webclearance = (max (self.section.root_radius, fp_thk)) +25
                else:
                    self.webclearance = (max(self.section.root_radius, fp_thk)) + 10
                self.webheight_status =False
                self.min_web_plate_height = round(self.section.min_plate_height(),2)
                self.webwidth = round(D - (2 * tk) , 2)
                self.web_crs_area = t_w * self.webwidth
                self.Wp = self.web_crs_area * 1.05

                if self.preference =="Outside":
                    self.webplatewidth = round(D - (2 * tk) - (2 * self.section.root_radius) ,2)
                    if self.webplatewidth < self.min_web_plate_height:
                        thickness = y
                        self.webheight_status = False
                        self.design_status = False
                    else:
                        self.webheight_status = True
                        self.web_plate_crs_sec_area = 2 *  self.min_web_plate_height * y
                        if self.web_plate_crs_sec_area >= self.web_crs_area * 1.05:
                            thickness = y
                            break
                        else:
                            thickness = y
                            self.design_status = False

                else:
                    self.webplatewidth = round(D - (2 * tk) - (2 * self.webclearance),2)
                    if self.webplatewidth < self.min_web_plate_height:
                        thickness = y
                        self.webheight_status = False
                        self.design_status = False
                    else:
                        self.webheight_status = True
                        self.web_plate_crs_sec_area = 2 *  self.min_web_plate_height * y
                        if self.web_plate_crs_sec_area  >= self.web_crs_area * 1.05:
                            thickness = y
                            break
                        else:
                            thickness = y
                            self.webheight_status = False
                            self.design_status = False
        return thickness


    # def call_3DModel(self,ui,bgcolor):
    #     # Call to calculate/create the BB Cover Plate Bolted CAD model
    #     # status = self.resultObj['Bolt']['status']
    #     # if status is True:
    #     #     self.createBBCoverPlateBoltedCAD()
    #     #     self.ui.btn3D.setChecked(Qt.Checked)
    #     if ui.btn3D.isChecked():
    #         ui.chkBxBeam.setChecked(Qt.Unchecked)
    #         ui.chkBxFinplate.setChecked(Qt.Unchecked)
    #         ui.mytabWidget.setCurrentIndex(0)
    #
    #     # Call to display the BB Cover Plate Bolted CAD model
    #     #     ui.Commondisplay_3DModel("Model", bgcolor)  # "gradient_bg")
    #     ui.commLogicObj.display_3DModel("Model",bgcolor)
    #
    #     # else:
    #     #     self.display.EraseAll()
    #
    # def call_3DBeam(self, ui, bgcolor):
    #     # status = self.resultObj['Bolt']['status']
    #     # if status is True:
    #     #     self.ui.chkBx_beamSec1.setChecked(Qt.Checked)
    #     if ui.chkBxBeam.isChecked():
    #         ui.btn3D.setChecked(Qt.Unchecked)
    #         ui.chkBxBeam.setChecked(Qt.Unchecked)
    #         ui.mytabWidget.setCurrentIndex(0)
    #     # self.display_3DModel("Beam", bgcolor)
    #     ui.commLogicObj.display_3DModel("Beam",bgcolor)
    #
    #
    # def call_3DConnector(self, ui, bgcolor):
    #     # status = self.resultObj['Bolt']['status']
    #     # if status is True:
    #     #     self.ui.chkBx_extndPlate.setChecked(Qt.Checked)
    #     if ui.chkBxFinplate.isChecked():
    #         ui.btn3D.setChecked(Qt.Unchecked)
    #         ui.chkBxBeam.setChecked(Qt.Unchecked)
    #         ui.mytabWidget.setCurrentIndex(0)
    #     # self.display_3DModel("Connector", bgcolor)
    #     ui.commLogicObj.display_3DModel("Connector", bgcolor)

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t2 = ('Beam', self.call_3DBeam)
        components.append(t2)

        t4 = ('Cover Plate', self.call_3DPlate)
        components.append(t4)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Cover Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Connector", bgcolor)
###########################################################################
    def results_to_test(self):
        # test_in_list = {KEY_MODULE : self.module,
        #                 KEY_MAIN_MODULE:  self.mainmodule,
        #                 KEY_DISP_SEC_PROFILE: "ISection",
        #                 KEY_DISP_BEAMSEC: self.section.designation,
        #                 KEY_DISP_FLANGESPLATE_PREFERENCES: self.preference,
        #                 KEY_MATERIAL : self.section.material,
        #                 KEY_SEC_FU: self.section.fu,
        #                 KEY_SEC_FY : self.section.fy,
        #                 KEY_D  : self.bolt.bolt_diameter,
        #                 KEY_GRD : self.bolt.bolt_grade,
        #                 KEY_TYP : self.bolt.bolt_type,
        #                 KEY_FLANGEPLATE_THICKNESS:  self.flange_plate.thickness,
        #                 KEY_WEBPLATE_THICKNESS: self.web_plate.thickness,
        #                 KEY_DP_BOLT_HOLE_TYPE : self.bolt.bolt_hole_type,
        #                 KEY_DP_BOLT_SLIP_FACTOR : self.bolt.mu_f,
        #                 KEY_DP_DETAILING_EDGE_TYPE : self.bolt.edge_type,
        #                 KEY_DP_DETAILING_GAP : self.flange_plate.gap,
        #                 KEY_DP_DETAILING_CORROSIVE_INFLUENCES : self.bolt.corrosive_influences}
        if self.bolt.bolt_type == TYP_BEARING:
            flange_bolt_bearing_cap_disp = round(self.flange_bolt.bolt_bearing_capacity / 1000, 2)
            web_bolt_bearing_cap_disp = round(self.web_bolt.bolt_bearing_capacity/1000,2)
        else:
            flange_bolt_bearing_cap_disp = 'N/A'
            web_bolt_bearing_cap_disp = 'N/A'

        test_out_list = {#applied loads
                        KEY_DISP_APPLIED_AXIAL_FORCE :round(self.factored_axial_load / 1000, 2),
                        KEY_DISP_APPLIED_SHEAR_LOAD :round(self.fact_shear_load / 1000, 2),
                        KEY_DISP_APPLIED_MOMENT_LOAD :round(self.load_moment / 1000000, 2),
                        # Diameter and grade
                        KEY_OUT_D_PROVIDED: self.bolt.bolt_diameter_provided,
                        KEY_OUT_GRD_PROVIDED: self.bolt.bolt_grade_provided,
                        # webplate dimensions
                        KEY_WEB_PLATE_HEIGHT: self.web_plate.height,
                        KEY_WEB_PLATE_LENGTH: self.web_plate.length,
                        KEY_OUT_WEBPLATE_THICKNESS: self.web_plate.thickness_provided,
                        # Web spacing
                        KEY_WEB_PITCH: self.web_plate.pitch_provided,
                        KEY_ENDDIST_W: self.web_plate.end_dist_provided,
                        KEY_WEB_GAUGE: self.web_plate.gauge_provided,
                        KEY_EDGEDIST_W: self.web_plate.edge_dist_provided,

                        # def web_bolt_capacity(self, flag):
                        KEY_WEB_BOLT_LINE: (self.web_plate.bolt_line),
                        KEY_WEB_BOLTS_ONE_LINE: (self.web_plate.bolts_one_line),
                        KEY_WEB_BOLTS_REQ: (self.web_plate.bolts_required),
                        'WebBolt.ShearCapacity': round(self.web_bolt.bolt_shear_capacity / 1000, 2),
                        'WebBolt.BearingCapacity': web_bolt_bearing_cap_disp,
                        'WebBolt.Capacity': round(self.web_plate.bolt_capacity_red / 1000, 2),
                        'WebBolt.Force': round(self.web_plate.bolt_force / 1000, 2),

                        # flange plate_outer
                        KEY_FLANGE_PLATE_HEIGHT: self.flange_plate.height,
                        KEY_FLANGE_PLATE_LENGTH: self.plate_out_len,
                        KEY_OUT_FLANGESPLATE_THICKNESS: self.flange_out_plate_tk,
                        # flange plate_inner
                        KEY_INNERFLANGE_PLATE_HEIGHT: self.flange_plate.Innerheight,
                        KEY_INNERFLANGE_PLATE_LENGTH: self.plate_in_len,
                        KEY_INNERFLANGEPLATE_THICKNESS: self.flange_in_plate_tk,
                        #Flange spacing
                        KEY_FLANGE_PITCH : self.flange_plate.pitch_provided,
                        KEY_ENDDIST_FLANGE :self.flange_plate.end_dist_provided,
                        KEY_FLANGE_PLATE_GAUGE: self.flange_plate.gauge_provided,
                        KEY_EDGEDIST_FLANGE : self.flange_plate.edge_dist_provided,
                        # def flange_bolt_capacity
                        KEY_FLANGE_BOLT_LINE: (self.flange_plate.bolt_line),
                        KEY_FLANGE_BOLTS_ONE_LINE: (self.flange_plate.bolts_one_line),
                        KEY_FLANGE_BOLTS_REQ: (self.flange_plate.bolts_required),
                        'FlangeBolt.ShearCapacity': round(self.flange_bolt.bolt_shear_capacity / 1000, 2),
                        'FlangeBolt.BearingCapacity': flange_bolt_bearing_cap_disp,
                        'FlangeBolt.Capacity': round(self.flange_plate.bolt_capacity_red / 1000, 2),

                        'FlangeBolt.Force': round(self.flange_plate.bolt_force / 1000, 2),

                        # def flangecapacity(self, flag):
                        KEY_TENSIONYIELDINGCAP_FLANGE : round(self.section.tension_yielding_capacity / 1000, 2),
                        KEY_TENSIONRUPTURECAP_FLANGE :round(self.section.tension_rupture_capacity / 1000,2),
                        KEY_BLOCKSHEARCAP_FLANGE :round(self.section.block_shear_capacity / 1000, 2),
                        KEY_FLANGE_TEN_CAPACITY:round(self.section.tension_capacity_flange / 1000, 2),
                        # flange plate capacities
                        KEY_TENSIONYIELDINGCAP_FLANGE_PLATE :round(self.flange_plate.tension_yielding_capacity / 1000,2),
                        KEY_TENSIONRUPTURECAP_FLANGE_PLATE :round(self.flange_plate.tension_rupture_capacity / 1000,   2),
                        KEY_BLOCKSHEARCAP_FLANGE_PLATE  : round(self.flange_plate.block_shear_capacity / 1000, 2),
                        KEY_FLANGE_PLATE_TEN_CAP : round(self.flange_plate.tension_capacity_flange_plate / 1000, 2),

                        # def webcapacity(self, flag):
                        KEY_TENSIONYIELDINGCAP_WEB : round( self.section.tension_yielding_capacity_web / 1000, 2),
                        KEY_TENSIONRUPTURECAP_WEB :round(self.section.tension_rupture_capacity_web / 1000,2),
                        KEY_TENSIONBLOCK_WEB : round(self.section.block_shear_capacity_web / 1000, 2),
                        KEY_WEB_TEN_CAPACITY:round(self.section.tension_capacity_web / 1000, 2),
                        #web plate capac in axial
                        KEY_TEN_YIELDCAPACITY_WEB_PLATE :   round(self.web_plate.tension_yielding_capacity / 1000,2),
                        KEY_TENSION_RUPTURECAPACITY_WEB_PLATE :round(self.web_plate.tension_rupture_capacity / 1000, 2),
                        KEY_TENSION_BLOCKSHEARCAPACITY_WEB_PLATE : round(self.web_plate.block_shear_capacity / 1000, 2),
                        KEY_WEB_PLATE_CAPACITY: round(self.web_plate.tension_capacity_web_plate / 1000, 2),
                        #shear
                        KEY_SHEARYIELDINGCAP_WEB_PLATE : round(self.web_plate.shear_yielding_capacity / 1000, 2),
                        KEY_SHEARRUPTURECAP_WEB_PLATE :round(self.web_plate.shear_rupture_capacity / 1000, 2),
                        KEY_BLOCKSHEARCAP_WEB_PLATE :round(self.web_plate.block_shear_capacity_shear / 1000, 2),
                        KEY_WEBPLATE_SHEAR_CAPACITY_PLATE:round(self.web_plate.shear_capacity_web_plate / 1000, 2),
                        KEY_WEB_PLATE_MOM_DEMAND:round(self.web_plate.moment_demand / 1000000, 2),
                        # def member_capacityoutput(self, flag):
                        KEY_MEMBER_MOM_CAPACITY: round(self.section.moment_capacity / 1000000, 2),
                        KEY_MEMBER_SHEAR_CAPACITY:round(self.shear_capacity1 / 1000, 2),
                        KEY_MEMBER_AXIALCAPACITY:round(self.axial_capacity / 1000, 2),
                        KEY_OUT_DISP_PLASTIC_MOMENT_CAPACITY  :round(self.Pmc / 1000000, 2),
                        KEY_OUT_DISP_MOMENT_D_DEFORMATION :round(self.Mdc / 1000000, 2)}
        return test_out_list

    ################################ Design Report #####################################################################################

    def save_design(self, popup_summary):
        # bolt_list = str(*self.bolt.bolt_diameter, sep=", ")

        if self.section.flange_slope == 90:
            image = "Parallel_Beam"
        else:
            image = "Slope_Beam"
        self.report_supporting = {KEY_DISP_SEC_PROFILE: image,
                                  KEY_DISP_BEAMSEC_REPORT: self.section.designation,
                                  KEY_DISP_MATERIAL: self.section.material,
                                  KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.section.fu,
                                  KEY_DISP_YIELD_STRENGTH_REPORT: self.section.fy,
                                  KEY_REPORT_MASS: self.section.mass,
                                  KEY_REPORT_AREA: round(self.section.area, 2),
                                  KEY_REPORT_DEPTH: self.section.depth,
                                  KEY_REPORT_WIDTH: self.section.flange_width,
                                  KEY_REPORT_WEB_THK: self.section.web_thickness,
                                  KEY_REPORT_FLANGE_THK: self.section.flange_thickness,
                                  KEY_DISP_FLANGE_S_REPORT: self.section.flange_slope,
                                  KEY_REPORT_R1: self.section.root_radius,
                                  KEY_REPORT_R2: self.section.toe_radius,
                                  KEY_REPORT_IZ: round(self.section.mom_inertia_z * 1e-4, 2),
                                  KEY_REPORT_IY: round(self.section.mom_inertia_y * 1e-4, 2),
                                  KEY_REPORT_RZ: round(self.section.rad_of_gy_z * 1e-1, 2),
                                  KEY_REPORT_RY: round(self.section.rad_of_gy_y * 1e-1, 2),
                                  KEY_REPORT_ZEZ: round(self.section.elast_sec_mod_z * 1e-3, 2),
                                  KEY_REPORT_ZEY: round(self.section.elast_sec_mod_y * 1e-3, 2),
                                  KEY_REPORT_ZPZ: round(self.section.plast_sec_mod_z * 1e-3, 2),
                                  KEY_REPORT_ZPY: round(self.section.plast_sec_mod_y * 1e-3, 2)}

        self.report_input = \
            {KEY_MODULE: self.module,
             KEY_MAIN_MODULE: self.mainmodule,
             # KEY_CONN: self.connectivity,
             KEY_DISP_MOMENT: self.load.moment,
             KEY_DISP_SHEAR: self.load.shear_force,
             KEY_DISP_AXIAL: self.load.axial_force,

             "Beam Section - Mechanical Properties": "TITLE",
             "Section Details": self.report_supporting,

             "Bolt Details - Input and Design Preference": "TITLE",
             # KEY_DISP_FLANGESPLATE_PREFERENCES: self.preference,
             KEY_DISP_D: str([int(d) for d in self.bolt.bolt_diameter]),
             KEY_DISP_GRD: str(self.bolt.bolt_grade),
             KEY_DISP_TYP: self.bolt.bolt_type,
             KEY_DISP_DP_BOLT_HOLE_TYPE: self.bolt.bolt_hole_type,
             KEY_DISP_DP_BOLT_SLIP_FACTOR_REPORT: self.bolt.mu_f,
             KEY_DISP_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
             KEY_DISP_DP_DETAILING_GAP_BEAM: self.flange_plate.gap,
             KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES_BEAM: self.bolt.corrosive_influences,

             "Plate Details - Input and Design Preference": "TITLE",
             KEY_DISP_FLANGESPLATE_PREFERENCES: self.preference,
             KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.flange_plate.fu,
             KEY_DISP_YIELD_STRENGTH_REPORT: self.flange_plate.fy,
             KEY_DISP_MATERIAL: self.flange_plate.material,
             KEY_DISP_FLANGESPLATE_THICKNESS: str(self.flange_plate.thickness),
             KEY_DISP_WEBPLATE_THICKNESS: str([int(d) for d in self.web_plate.thickness]),
             }
        self.report_check = []

        #####Outer plate#####

        h = self.section.depth - (2 * self.section.flange_thickness)
        self.Pmc = self.section.plastic_moment_capactiy
        self.Mdc = self.section.moment_d_def_criteria
        t1 = ('SubSection', 'Member Capacity', '|p{4cm}|p{3.5cm}|p{6.5cm}|p{1.5cm}|')
        self.report_check.append(t1)
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']

        t1=(SECTION_CLASSIFICATION,"", cl_3_7_2_section_classification(class_of_section=self.class_of_section), "")
        self.report_check.append(t1)

        t1 = (KEY_OUT_DISP_AXIAL_CAPACITY, display_prov(self.load.axial_force, "P_x"),
              cl_6_2_tension_yield_capacity_member(l=None, t=None, f_y=self.section.fy, gamma=gamma_m0,
                                                   T_dg=round(self.axial_capacity / 1000, 2), multiple =None,
                                                   area=round(self.section.area, 2)), '')
        self.report_check.append(t1)

        # self.shear_capacity1 = round(((self.section.depth - (2 * self.section.flange_thickness)) *
        #                               self.section.web_thickness * self.section.fy) / (math.sqrt(3) * gamma_m0), 2)

        t1 = (KEY_OUT_DISP_SHEAR_CAPACITY, '', cl_8_4_shear_yielding_capacity_member(h=h, t=self.section.web_thickness, f_y=self.section.fy, gamma_m0=gamma_m0,
                                                                                     V_dg=round(self.shear_capacity1 / 1000 / 0.6, 2)), '')
        self.report_check.append(t1)

        initial_shear_capacity = round(self.shear_capacity1 / 1000 / 0.6, 2)
        reduced_shear_capacity = round(self.shear_capacity1 / 1000, 2)
        t1 = (KEY_DISP_ALLOW_SHEAR, display_prov(self.load.shear_force, "V_y"),
              allow_shear_capacity(initial_shear_capacity, reduced_shear_capacity),
              get_pass_fail(self.load.shear_force, reduced_shear_capacity, relation="lesser"))
        self.report_check.append(t1)

        t1 = (KEY_OUT_DISP_PLASTIC_MOMENT_CAPACITY, '', cl_8_2_1_2_plastic_moment_capacity_member(beta_b=round(self.beta_b, 2),
                                                                                                  Z_p=round(self.Z_p,2), f_y=self.section.fy,
                                                                                                  gamma_m0=gamma_m0,
                                                                                                  Pmc=round(self.Pmc / 1000000, 2)), '')
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_MOMENT_D_DEFORMATION, '', cl_8_2_1_2_deformation_moment_capacity_member(fy=self.section.fy,
                                                                                                   Z_e=round(self.section.elast_sec_mod_z,2),
                                                                                                   Mdc=round(self.Mdc / 1000000, 2)),
              '')
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_MOMENT_CAPACITY, display_prov(self.load.moment, "M_z"), cl_8_2_moment_capacity_member(Pmc=round(self.Pmc / 1000000, 2),
                                                                                                               Mdc=round(self.Mdc / 1000000, 2),
                                                                                                               M_c=round(self.section.moment_capacity / 1000000, 2)),
              '')
        self.report_check.append(t1)
        t1 = ('SubSection', 'Load Consideration', '|p{3cm}|p{6cm}|p{5.2cm}|p{1.5cm}|')
        self.report_check.append(t1)
        #####INTERACTION RATIO#######

        t1 = (KEY_INTERACTION_RATIO, '', ir_sum_bb_cc(Al = self.load.axial_force, M = self.load.moment,
                                                      A_c = round(self.axial_capacity/1000,2),
                                                      M_c =round(self.section.moment_capacity/1000000,2),
                                                      IR_axial =self.IR_axial,IR_moment =self.IR_moment,sum_IR =self.sum_IR), '')
        self.report_check.append(t1)
        #############################
        #### Min load Required ###############
        t2 =(MIN_LOADS_REQUIRED,min_loads_required(conn="beam_beam") , min_loads_provided(min_ac= round(self.min_axial_load / 1000, 2),
                                                                          min_mc=round(self.load_moment_min / 1000000, 2),
                                                                          conn = "beam_beam"),'')
        self.report_check.append(t2)

        #############################
        t1 = (KEY_DISP_APPLIED_AXIAL_FORCE,display_prov(self.load.axial_force, "P_x"),
              prov_axial_load(axial_input=self.load.axial_force,min_ac=round(self.min_axial_load / 1000, 2),
                              app_axial_load=round(self.factored_axial_load / 1000, 2),axial_capacity=round(self.axial_capacity/1000,2)),'' )

        self.report_check.append(t1)
        V_dy = round(self.shear_capacity1 / 0.6 / 1000, 2)
        t1 = (KEY_DISP_APPLIED_SHEAR_LOAD,display_prov(self.load.shear_force, "V_y"),
              prov_shear_load(shear_input=self.load.shear_force,min_sc=round(self.shear_load1 / 1000, 2),
                              app_shear_load=round(self.fact_shear_load / 1000, 2),shear_capacity_1=V_dy),"")
        self.report_check.append(t1)
        t1 = (KEY_DISP_APPLIED_MOMENT_LOAD,display_prov(self.load.moment, "M_z"),
              prov_moment_load(moment_input=self.load.moment,min_mc=round(self.load_moment_min / 1000000, 2),
                               app_moment_load=round(self.load_moment / 1000000, 2),moment_capacity=round(self.section.moment_capacity / 1000000, 2),
                               moment_capacity_supporting=0.0),"")

        self.report_check.append(t1)
        t23 = (KEY_OUT_DISP_FORCES_WEB, '', forces_in_web(Au=round(self.factored_axial_load / 1000, 2),
                                                          T=self.section.flange_thickness,
                                                          A=round(self.section.area, 2),
                                                          t=self.section.web_thickness, D=self.section.depth,
                                                          Zw=round(self.Z_w,2), Mu=round(self.load_moment / 1000000, 2),
                                                          Z=round(self.section.plast_sec_mod_z,2),
                                                          Mw=round(self.moment_web / 1000000, 2),
                                                          Aw=round(self.axial_force_w / 1000, 2)), '')
        self.report_check.append(t23)
        t23 = (KEY_OUT_DISP_FORCES_FLANGE, '', forces_in_flange(Au=round(self.factored_axial_load / 1000, 2),
                                                                B=self.section.flange_width,
                                                                T=self.section.flange_thickness,
                                                                A=round(self.section.area, 2),
                                                                D=self.section.depth,
                                                                Mu=round(self.load_moment / 1000000, 2),
                                                                Mw=round(self.moment_web / 1000000, 2),
                                                                Mf=round(self.moment_flange / 1000000, 2),
                                                                Af=round(self.axial_force_f / 1000, 2),
                                                                ff=round(self.flange_force / 1000, 2), ), '')
        self.report_check.append(t23)
        if self.design_status == False:
            if self.member_capacity_status == True:
                t2 = ('SubSection', 'Initial Member Check', '|p{3cm}|p{4.5cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t2)
                t1 = (KEY_DISP_TENSIONYIELDINGCAP_FLANGE, display_prov(round(self.flange_force / 1000, 2), "F_f"),
                      cl_6_2_tension_yield_capacity_member(self.section.flange_width,
                                                           self.section.flange_thickness,
                                                           self.section.fy, gamma_m0,
                                                           round(self.section.tension_yielding_capacity / 1000, 2), 1),
                      get_pass_fail(round(self.flange_force / 1000, 2),
                                    round(self.section.tension_yielding_capacity / 1000, 2), relation="lesser"))
                self.report_check.append(t1)
                if self.section.tension_yielding_capacity > self.flange_force:
                    webheight = round((self.section.depth - 2 * self.section.flange_thickness), 2)
                    t1 = (KEY_DISP_TENSIONYIELDINGCAP_WEB, display_prov(round(self.axial_force_w / 1000, 2), "A_w"),
                          cl_6_2_tension_yield_capacity_member(webheight,
                                                               self.section.web_thickness,
                                                               self.section.fy, gamma_m0,
                                                               round(self.section.tension_yielding_capacity_web / 1000, ), 1),
                          get_pass_fail(round(self.axial_force_w / 1000, 2),
                                        round(self.section.tension_yielding_capacity_web / 1000, 2), relation="lesser"))
                    self.report_check.append(t1)

            if self.member_capacity_status == True and (self.section.tension_yielding_capacity > self.flange_force) and (len(self.flange_plate_thickness_possible) != 0):
                t1 = ('SubSection', 'Initial Flange Plate Height Check', '|p{4.5cm}|p{2.5cm}|p{7cm}|p{1.5cm}|')
                self.report_check.append(t1)
                if self.preference == "Outside":
                    t1 = ('Flange Plate Width (mm)' , 'Bfp >= 50',
                          display_prov(round(self.outerwidth,2), "B_{fp}"),
                          get_pass_fail(50,round(self.outerwidth,2), relation="leq"))
                    self.report_check.append(t1)
                else:
                    t1 = ('Flange Plate Width (mm)' , 'Bfp >= 50',
                          display_prov(round(self.outerwidth,2), "B_{fp}"),
                          get_pass_fail(50, round(self.outerwidth,2), relation="leq"))
                    self.report_check.append(t1)

                    t1 = ('Flange Plate Inner Width (mm)', 'Bifp >= 50' ,
                          width_pt_chk_bolted(B =self.section.flange_width,t = self.section.web_thickness,r_1 =self.section.root_radius),
                         get_pass_fail(50, round(self.innerwidth,2), relation="leq"))
                    self.report_check.append(t1)


            if self.member_capacity_status == True and (self.section.tension_yielding_capacity > self.flange_force) and self.webheight_status == True:
                if self.initial_pt_thk_status == True:
                    self.thick_f = self.flange_plate.thickness_provided
                    self.thick_w = self.web_plate.thickness_provided
                else:
                    self.thick_f = self.max_thick_f
                    self.thick_w = self.max_thick_w
                t1 = ('SubSection', 'Flange Plate Thickness', '|p{2.5cm}|p{5cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                if  self.preference == "Outside":
                    t2 = (KEY_DISP_FLANGESPLATE_THICKNESS, display_prov(self.section.flange_thickness, "T"),display_prov(self.thick_f, "t_{fp}"),
                          get_pass_fail(self.section.flange_thickness, self.thick_f, relation="lesser"))
                    self.report_check.append(t2)
                    if(len(self.flange_plate_thickness_possible) != 0) and self.outerwidth >= 50:
                        t2 = (KEY_DISP_AREA_CHECK, plate_area_req(crs_area=round(self.flange_crs_sec_area,2),flange_web_area = round(self.Ap,2)),
                              flange_plate_area_prov_bolt(B=self.section.flange_width,pref = "Outside",y = self.thick_f,
                                                          outerwidth= round(self.outerwidth,2),
                                                          fp_area =round(self.flange_plate_crs_sec_area,2),
                                                          t = self.section.web_thickness,
                                                          r_1 = self.section.root_radius,),
                              get_pass_fail(self.Ap , self.flange_plate_crs_sec_area, relation="leq"))

                else:
                    t2 = (KEY_DISP_FLANGESPLATE_THICKNESS, display_prov(self.section.flange_thickness/2, "T"),
                          display_prov(self.thick_f, "t_{fp}"),get_pass_fail(self.section.flange_thickness/2,
                                                                             self.thick_f, relation="lesser"))
                    self.report_check.append(t2)
                    # flange_plate_crs_sec_area = (self.outerwidth + (2 * self.innerwidth)) * self.thick_f
                    if len(self.flange_plate_thickness_possible) != 0 and self.innerwidth >= 50 and self.outerwidth >= 50:
                        t2 = (KEY_DISP_AREA_CHECK, plate_area_req(crs_area=round(self.flange_crs_sec_area, 2),flange_web_area =round( self.Ap,2)),
                              flange_plate_area_prov_bolt(B=self.section.flange_width, pref="Outside+Inside",
                                                     y=self.thick_f,
                                                     outerwidth=round(self.outerwidth,2), fp_area=round(self.flange_plate_crs_sec_area,2),
                                                     t=self.section.web_thickness, r_1=self.section.root_radius,
                                                     innerwidth=round(self.innerwidth,2) ),get_pass_fail(self.Ap, self.flange_plate_crs_sec_area, relation="leq"))
                        self.report_check.append(t2)

            if self.member_capacity_status == True and (self.section.tension_yielding_capacity > self.flange_force) and (len(self.flange_plate_thickness_possible) != 0):
                t1 = ('SubSection', 'Initial Web Plate Height Check', '|p{3cm}|p{4.5cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                if self.preference == "Outside":

                    t1 = (
                        'Web Plate Height (mm)', min_plate_ht_req(D=self.section.depth, min_req_width=self.min_web_plate_height, r_r=self.section.root_radius,
                                                               t_f=self.section.flange_thickness),
                        web_width_chk_bolt(pref=self.preference, D=self.section.depth, tk=self.flange_plate.thickness_provided,T=self.section.flange_thickness,
                                       R_1=self.section.root_radius, webplatewidth=self.webplatewidth, webclearance=None),
                        get_pass_fail(self.min_web_plate_height, self.webplatewidth, relation="leq"))
                    self.report_check.append(t1)
                else:
                    # self.min_web_plate_height = self.section.min_plate_height()
                    t1 = ('Web Plate Height (mm)', min_plate_ht_req(D=self.section.depth, min_req_width=self.min_web_plate_height, r_r=self.section.root_radius,
                                                                 t_f=self.section.flange_thickness),
                          web_width_chk_bolt(pref=self.preference, D=self.section.depth, tk=self.flange_plate.thickness_provided,T=self.section.flange_thickness,
                                             R_1=self.section.root_radius, webplatewidth=self.webplatewidth,
                                             webclearance=self.webclearance),
                          get_pass_fail(self.min_web_plate_height, self.webplatewidth, relation="leq"))
                    self.report_check.append(t1)


            if self.member_capacity_status == True and (self.section.tension_yielding_capacity > self.flange_force) and self.webheight_status == True:

                # if (self.flange_plate_crs_sec_area >= (1.05 * self.flange_crs_sec_area)) and len(self.flange_plate_thickness_possible) != 0 and len(self.web_plate_thickness_possible) != 0 :
                t1 = ('SubSection', 'Web Plate Thickness', '|p{2.5cm}|p{5cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                t2 = (KEY_DISP_WEBPLATE_THICKNESS, display_prov(self.section.web_thickness/2, "t"),display_prov(self.thick_w, "t_{wp}"),get_pass_fail(self.section.web_thickness/2, self.thick_w, relation="lesser"))
                self.report_check.append(t2)
                if len(self.web_plate_thickness_possible) != 0 and self.webplatewidth > self.min_web_plate_height:
                    # if (self.flange_plate_crs_sec_area >= 1.05 * self.flange_crs_sec_area):
                    t2 = (KEY_DISP_AREA_CHECK, plate_area_req(crs_area=round(self.web_crs_area, 2),
                                                              flange_web_area = round( self.Wp,2)),
                          web_plate_area_prov_bolt(D=self.section.depth, y = self.thick_w,
                                                   webwidth =  self.min_web_plate_height,
                                                   wp_area =round(self.web_plate_crs_sec_area,2),T = self.section.flange_thickness, r_1 = self.section.root_radius),
                                                get_pass_fail(self.Wp, self.web_plate_crs_sec_area, relation="lesser"))
                    self.report_check.append(t2)
            if self.member_capacity_status == True and self.initial_pt_thk_status == True and self.initial_pt_thk_status_web ==True:
                t1 = ('SubSection', 'Web Spacing Check', '|p{3.0cm}|p{6.5cm}|p{5 cm}|p{1cm}|')
                self.report_check.append(t1)
                self.bolt_diameter_min = min(self.bolt.bolt_diameter)
                min_gauge =self.web_bolt.min_gauge_round
                self.d_0_min = IS800_2007.cl_10_2_1_bolt_hole_size(self.bolt_diameter_min,
                                                                   self.bolt.bolt_hole_type)
                row_limit = "Row~Limit~(r_l) = 2"
                row = 2.0
                depth_max = round(self.section.depth - (2*self.section.flange_thickness)- (2*self.webclearance) ,2)
                depth = round(2 * self.web_bolt.min_edge_dist_round + min_gauge ,2)

                t6 = (KEY_OUT_DISP_D_MIN, "", display_prov(self.bolt_diameter_min, "d"), '')
                self.report_check.append(t6)
                t2 = (DISP_MIN_GAUGE, cl_10_2_2_min_spacing(self.bolt_diameter_min), display_prov(min_gauge, "g", row_limit), "")
                self.report_check.append(t2)
                t3 = (DISP_MIN_EDGE, cl_10_2_4_2_min_edge_end_dist(self.d_0_min, self.bolt.edge_type),
                      self.web_bolt.min_edge_dist_round, "")
                self.report_check.append(t3)
                t3 = (KEY_SPACING, depth_req(self.web_bolt.min_edge_dist_round, min_gauge, row,sec ="beam"), depth_max,
                      get_pass_fail(depth, depth_max, relation="lesser"))
                self.report_check.append(t3)

                t1 = ('SubSection', 'Flange Spacing Check', '|p{3.0cm}|p{6.5cm}|p{5cm}|p{1cm}|')
                self.report_check.append(t1)
                self.bolt_diameter_min = min(self.bolt.bolt_diameter)
                min_gauge =0.0
                self.d_0_min = IS800_2007.cl_10_2_1_bolt_hole_size(self.bolt_diameter_min,
                                                                   self.bolt.bolt_hole_type)
                row_limit = "Row~Limit~(r_l) = 1"
                row = 1.0
                depth_max = round((self.section.flange_width/2) - (self.section.web_thickness/2)- self.section.root_radius ,2)
                depth = round(2 * self.flange_bolt.min_edge_dist_round ,2)

                t6 = (KEY_OUT_DISP_D_MIN, "", display_prov(self.bolt_diameter_min, "d"), '')
                self.report_check.append(t6)
                t2 = (DISP_MIN_GAUGE, cl_10_2_2_min_spacing(self.bolt_diameter_min), display_prov(min_gauge, "g", row_limit), "")
                self.report_check.append(t2)
                t3 = (DISP_MIN_EDGE, cl_10_2_4_2_min_edge_end_dist(self.d_0_min, self.bolt.edge_type),
                      self.flange_bolt.min_edge_dist_round, "")
                self.report_check.append(t3)
                t3 = (KEY_SPACING, depth_req(self.flange_bolt.min_edge_dist_round, self.flange_bolt.min_pitch_round, row,sec ="beam"), depth_max,
                      get_pass_fail(depth, depth_max, relation="leq"))
                self.report_check.append(t3)


        if self.flange_plate.spacing_status == True:
            flange_connecting_plates = [self.flange_plate.thickness_provided, self.section.flange_thickness]

            flange_bolt_shear_capacity_kn = round(self.flange_bolt.bolt_shear_capacity / 1000, 2)
            # flange_bolt_bearing_capacity_kn = round(self.flange_bolt.bolt_bearing_capacity / 1000, 2)
            flange_bolt_capacity_kn = round(self.flange_bolt.bolt_capacity / 1000, 2)
            flange_kb_disp = round(self.flange_bolt.kb, 2)
            flange_kh_disp = round(self.flange_bolt.kh, 2)
            flange_bolt_force_kn = round(self.flange_plate.bolt_force, 2)
            flange_bolt_capacity_red_kn = round(self.flange_plate.bolt_capacity_red / 1000, 2)
            if self.initial_pt_thk_status == True:
                self.thick_f = self.flange_plate.thickness_provided
                self.thick_w = self.web_plate.thickness_provided
            else:
                self.thick_f = self.max_thick_f
                self.thick_w = self.max_thick_w
            ########Inner plate#####
            innerflange_connecting_plates = [self.flange_plate.thickness_provided, self.section.flange_thickness]

            innerflange_bolt_shear_capacity_kn = round(self.flange_bolt.bolt_shear_capacity / 1000, 2)

            innerflange_bolt_capacity_kn = round(self.flange_bolt.bolt_capacity / 1000, 2)
            innerflange_kb_disp = round(self.flange_bolt.kb, 2)
            innerflange_kh_disp = round(self.flange_bolt.kh, 2)
            innerflange_bolt_force_kn = round(self.flange_plate.bolt_force, 2)
            innerflange_bolt_capacity_red_kn = round(self.flange_plate.bolt_capacity_red, 2)
            min_plate_length = (((self.flange_plate.bolt_line / 2 - 1) * self.flange_bolt.min_pitch) + (
                    2 * self.flange_bolt.min_end_dist) + (self.flange_plate.gap / 2))

            t1 = ('SubSection', 'Flange Bolt Check', '|p{3cm}|p{4.5cm}|p{6.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t6 = (KEY_OUT_DISP_D_PROVIDED, "Bolt Quantity Optimization", display_prov(self.bolt.bolt_diameter_provided, "d"), '')

            self.report_check.append(t6)

            t8 = (KEY_OUT_DISP_GRD_PROVIDED, "Bolt Grade Optimization", self.bolt.bolt_grade_provided, '')
            self.report_check.append(t8)
            t8 = (KEY_DISP_DP_BOLT_FU, "", display_prov(round(self.flange_bolt.bolt_fu, 2), "f_{ub}"), '')
            self.report_check.append(t8)

            t8 = (KEY_DISP_DP_BOLT_FY, "", display_prov(round(self.flange_bolt.bolt_fy, 2), "f_{yb}"), '')
            self.report_check.append(t8)

            t8 = (KEY_DISP_BOLT_AREA, " ", display_prov(self.flange_bolt.bolt_net_area, "A_{nb}", " Ref~IS~1367-3~(2002)"), '')
            self.report_check.append(t8)
            t8 = (KEY_DISP_BOLT_HOLE, " ", display_prov(self.flange_bolt.dia_hole, "d_0"), '')
            self.report_check.append(t8)
            if self.preference == "Outside":
                t1 = (DISP_MIN_FLANGE_PLATE_THICK, display_prov(self.section.flange_thickness, "T"),
                      display_prov(self.flange_plate.thickness_provided, "t_{fp}"),
                      get_pass_fail(self.section.flange_thickness, self.flange_plate.thickness_provided,
                                    relation="lesser"))
                self.report_check.append(t1)
            else:
                t1 = (DISP_MIN_FLANGE_PLATE_THICK, display_prov(self.section.flange_thickness / 2, "T/2"),
                      display_prov(self.flange_plate.thickness_provided, "t_{ifp}"),
                      get_pass_fail(self.section.flange_thickness / 2, self.flange_plate.thickness_provided,
                                    relation="lesser"))
                self.report_check.append(t1)
            t6 = (DISP_NUM_OF_COLUMNS, '', display_prov(self.flange_plate.bolt_line, "n_c"), '')

            self.report_check.append(t6)
            t7 = (DISP_NUM_OF_ROWS, '', display_prov(self.flange_plate.bolts_one_line, "n_r"), '')
            self.report_check.append(t7)
            t1 = (DISP_MIN_PITCH, cl_10_2_2_min_spacing(self.bolt.bolt_diameter_provided),
                  self.flange_plate.pitch_provided,
                  get_pass_fail(self.flange_bolt.min_pitch, self.flange_plate.pitch_provided, relation='leq'))
            self.report_check.append(t1)
            t1 = (DISP_MAX_PITCH, cl_10_2_3_1_max_spacing(flange_connecting_plates),
                  self.flange_plate.pitch_provided,
                  get_pass_fail(self.flange_bolt.max_spacing, self.flange_plate.pitch_provided, relation='geq'))
            self.report_check.append(t1)
            t2 = (DISP_MIN_GAUGE, cl_10_2_2_min_spacing(self.bolt.bolt_diameter_provided),
                  self.flange_plate.gauge_provided,
                  get_pass_fail(self.flange_bolt.min_gauge, self.flange_plate.gauge_provided, relation="leq"))
            self.report_check.append(t2)
            t2 = (DISP_MAX_GAUGE, cl_10_2_3_1_max_spacing(flange_connecting_plates),
                  self.flange_plate.gauge_provided,
                  get_pass_fail(self.flange_bolt.max_spacing, self.flange_plate.gauge_provided, relation="geq"))
            self.report_check.append(t2)
            t3 = (DISP_MIN_END, cl_10_2_4_2_min_edge_end_dist(self.flange_bolt.dia_hole, self.bolt.edge_type),
                  self.flange_plate.end_dist_provided,
                  get_pass_fail(self.flange_bolt.min_end_dist, self.flange_plate.end_dist_provided, relation='leq'))
            self.report_check.append(t3)
            t4 = (DISP_MAX_END, cl_10_2_4_3_max_edge_end_dist(self.bolt_conn_plates_t_fu_fy,
                                                              corrosive_influences=self.bolt.corrosive_influences,
                                                              parameter='end_dist'),
                  self.flange_plate.end_dist_provided,
                  get_pass_fail(self.flange_bolt.max_end_dist, self.flange_plate.end_dist_provided, relation='geq'))
            self.report_check.append(t4)
            t3 = (DISP_MIN_EDGE, cl_10_2_4_2_min_edge_end_dist(self.flange_bolt.dia_hole, self.bolt.edge_type),
                  self.flange_plate.edge_dist_provided,
                  get_pass_fail(self.flange_bolt.min_edge_dist, self.flange_plate.edge_dist_provided, relation='leq'))
            self.report_check.append(t3)
            t4 = (DISP_MAX_EDGE, cl_10_2_4_3_max_edge_end_dist(self.bolt_conn_plates_t_fu_fy,
                                                              corrosive_influences=self.bolt.corrosive_influences,
                                                              parameter='edge_dist'),
                  self.flange_plate.edge_dist_provided,
                  get_pass_fail(self.flange_bolt.max_edge_dist, self.flange_plate.edge_dist_provided, relation="geq"))
            self.report_check.append(t4)

            if self.preference == "Outside":
                if self.flange_bolt.bolt_type == TYP_BEARING:
                    flange_bolt_bearing_capacity_kn = round(self.flange_bolt.bolt_bearing_capacity / 1000, 2)
                    t1 = (KEY_OUT_DISP_FLANGE_BOLT_SHEAR, '', cl_10_3_3_bolt_shear_capacity(self.flange_bolt.bolt_fu, 1,
                                                                                            self.flange_bolt.bolt_net_area,
                                                                                            self.flange_bolt.gamma_mb,
                                                                                            flange_bolt_shear_capacity_kn), '')
                    self.report_check.append(t1)
                    t8 = (KEY_DISP_KB, " ", cl_10_3_4_calculate_kb(self.flange_plate.end_dist_provided, self.flange_plate.pitch_provided, self.flange_bolt.dia_hole,
                                                                   self.flange_bolt.bolt_fu, self.flange_bolt.fu_considered), '')
                    self.report_check.append(t8)
                    t2 = (KEY_OUT_DISP_FLANGE_BOLT_BEARING, '', cl_10_3_4_bolt_bearing_capacity(flange_kb_disp,
                                                                                                self.bolt.bolt_diameter_provided,
                                                                                                self.bolt_conn_plates_t_fu_fy,
                                                                                                self.flange_bolt.gamma_mb,
                                                                                                flange_bolt_bearing_capacity_kn), '')
                    self.report_check.append(t2)
                    t3 = (KEY_OUT_DISP_FLANGE_BOLT_CAPACITY, '', cl_10_3_2_bolt_capacity(flange_bolt_shear_capacity_kn,
                                                                                         flange_bolt_bearing_capacity_kn,
                                                                                         flange_bolt_capacity_kn), '')
                    self.report_check.append(t3)
                else:

                    t4 = (KEY_OUT_DISP_FLANGE_BOLT_SLIP, '', cl_10_4_3_HSFG_bolt_capacity(mu_f=self.bolt.mu_f, n_e=1,
                                                                                          K_h=flange_kh_disp,
                                                                                          fub=self.flange_bolt.bolt_fu,
                                                                                          Anb=self.flange_bolt.bolt_net_area,
                                                                                          gamma_mf=self.flange_bolt.gamma_mf,
                                                                                          capacity=flange_bolt_capacity_kn), '')
                    self.report_check.append(t4)
            else:
                if self.flange_bolt.bolt_type == TYP_BEARING:
                    innerflange_bolt_bearing_capacity_kn = round(self.flange_bolt.bolt_bearing_capacity / 1000, 2)
                    t1 = (KEY_OUT_DISP_FLANGE_BOLT_SHEAR, '', cl_10_3_3_bolt_shear_capacity(self.flange_bolt.bolt_fu, 2,
                                                                                            self.flange_bolt.bolt_net_area,
                                                                                            self.flange_bolt.gamma_mb,
                                                                                            innerflange_bolt_shear_capacity_kn), '')
                    self.report_check.append(t1)
                    t8 = (KEY_DISP_KB, " ", cl_10_3_4_calculate_kb(self.flange_plate.end_dist_provided, self.flange_plate.pitch_provided,
                                                                   self.flange_bolt.dia_hole,
                                                                   self.flange_bolt.bolt_fu, self.flange_bolt.fu_considered), '')
                    self.report_check.append(t8)
                    t2 = (KEY_OUT_DISP_FLANGE_BOLT_BEARING, '', cl_10_3_4_bolt_bearing_capacity(innerflange_kb_disp,
                                                                                                self.bolt.bolt_diameter_provided,
                                                                                                self.bolt_conn_plates_t_fu_fy,
                                                                                                self.flange_bolt.gamma_mb,
                                                                                                innerflange_bolt_bearing_capacity_kn), '')
                    self.report_check.append(t2)
                    t3 = (KEY_OUT_DISP_FLANGE_BOLT_CAPACITY, '', cl_10_3_2_bolt_capacity(innerflange_bolt_shear_capacity_kn,
                                                                                         innerflange_bolt_bearing_capacity_kn,
                                                                                         innerflange_bolt_capacity_kn), '')
                    self.report_check.append(t3)
                else:

                    t4 = (KEY_OUT_DISP_FLANGE_BOLT_SLIP, '', cl_10_4_3_HSFG_bolt_capacity(mu_f=self.bolt.mu_f, n_e=2,
                                                                                          K_h=innerflange_kh_disp,
                                                                                          fub=self.flange_bolt.bolt_fu,
                                                                                          Anb=self.flange_bolt.bolt_net_area,
                                                                                          gamma_mf=self.flange_bolt.gamma_mf,
                                                                                          capacity=innerflange_bolt_capacity_kn),
                          '')
                    self.report_check.append(t4)

            # t6 = (DISP_NUM_OF_BOLTS, get_trial_bolts(V_u=0.0, A_u=(round(self.flange_force / 1000, 2)),
            #                                          bolt_capacity=flange_bolt_capacity_kn, multiple=2,conn ="flange_web"),
            #       self.flange_plate.bolts_required, '')
            # self.report_check.append(t6)

            t10 = (KEY_OUT_LONG_JOINT, cl_10_3_3_1_long_joint_bolted_req(),
                   long_joint_bolted_beam(self.flange_plate.bolt_line, self.flange_plate.bolts_one_line,
                                          self.flange_plate.pitch_provided,
                                          self.flange_plate.gauge_provided, self.bolt.bolt_diameter_provided,
                                          flange_bolt_capacity_kn,
                                          flange_bolt_capacity_red_kn,'flange',self.flange_plate.end_dist_provided,
                                          self.flange_plate.gap,self.flange_plate.edge_dist_provided,
                                          self.section.web_thickness,self.section.root_radius,conn="beam_beam"), "")
            self.report_check.append(t10)

            t10 = (KEY_OUT_LARGE_GRIP, cl_10_3_3_2_large_grip_bolted_req(),
                   cl_10_3_3_2_large_grip_bolted_prov(self.t_sum1, self.flange_bolt.bolt_diameter_provided,
                                   self.flange_plate.beta_lj), "")
            self.report_check.append(t10)

            if self.flange_bolt.bolt_type == TYP_BEARING:
                t5 = (KEY_OUT_DISP_BOLT_CAPACITY, vres_cap_bolt_check(V_u=0.0, A_u=(round(self.flange_force / 1000, 2)),
                                                                      bolt_capacity=round(
                                                                          self.flange_plate.bolt_force / 1000, 2),
                                                                      bolt_req=self.flange_plate.bolts_required, multiple=2,
                                                                      conn="flange_web"),
                      bolt_red_capacity_prov(self.flange_plate.beta_lj,
                                             self.flange_plate.beta_lg,
                                             flange_bolt_capacity_kn,
                                             flange_bolt_capacity_red_kn,"b"),
                      get_pass_fail(round(self.flange_plate.bolt_force / 1000, 2), flange_bolt_capacity_red_kn,
                                    relation="lesser"))
                self.report_check.append(t5)
            else:
                t5 = (KEY_OUT_DISP_BOLT_CAPACITY, vres_cap_bolt_check(V_u=0.0, A_u=(round(self.flange_force / 1000, 2)),
                                                                      bolt_capacity=round(
                                                                          self.flange_plate.bolt_force / 1000, 2),
                                                                      bolt_req=self.flange_plate.bolts_required,
                                                                      multiple=2,
                                                                      conn="flange_web"),
                      bolt_red_capacity_prov(self.flange_plate.beta_lj,
                                             self.flange_plate.beta_lg,
                                             flange_bolt_capacity_kn,
                                             flange_bolt_capacity_red_kn, "f"),
                      get_pass_fail(round(self.flange_plate.bolt_force / 1000, 2), flange_bolt_capacity_red_kn,
                                    relation="lesser"))
                self.report_check.append(t5)

        if self.web_plate.spacing_status == True and self.flange_plate.spacing_status == True:

            ############web variables###
            web_connecting_plates = [self.web_plate.thickness_provided, self.section.web_thickness]
            web_bolt_shear_capacity_kn = round(self.web_bolt.bolt_shear_capacity / 1000, 2)
            # web_bolt_bearing_capacity_kn = round(self.web_bolt.bolt_bearing_capacity / 1000, 2)
            web_bolt_capacity_kn = round(self.web_bolt.bolt_capacity / 1000, 2)
            web_kb_disp = round(self.web_bolt.kb, 2)
            web_kh_disp = round(self.web_bolt.kh, 2)

            web_bolt_force_kn = round(self.web_plate.bolt_force / 1000, 2)
            web_bolt_capacity_red_kn = round(self.web_plate.bolt_capacity_red / 1000, 2)
            res_force = self.web_plate.bolt_force * self.web_plate.bolt_line * self.web_plate.bolts_one_line
            print("res_focce", res_force)

            t1 = ('SubSection', 'Web Bolt Check', '|p{2.5cm}|p{5.6cm}|p{6.4cm}|p{1.5cm}|')

            self.report_check.append(t1)
            t6 = (KEY_OUT_DISP_D_PROVIDED, "Bolt Quantity Optimization", display_prov(self.bolt.bolt_diameter_provided, "d"),
            '')
            self.report_check.append(t6)
            t8 = (KEY_OUT_DISP_GRD_PROVIDED, "Bolt Grade Optimization", self.bolt.bolt_grade_provided, '')
            self.report_check.append(t8)
            t1 = (DISP_MIN_WEB_PLATE_THICK, display_prov(self.section.web_thickness / 2, "t/2"),
                  display_prov(self.web_plate.thickness_provided, "t_{wp}"),
                  get_pass_fail(self.section.web_thickness / 2, self.web_plate.thickness_provided, relation="lesser"))
            self.report_check.append(t1)
            t6 = (DISP_NUM_OF_COLUMNS, '', display_prov(self.web_plate.bolt_line, "n_c"), '')

            self.report_check.append(t6)
            t7 = (DISP_NUM_OF_ROWS, '', display_prov(self.web_plate.bolts_one_line, "n_r"), '')
            self.report_check.append(t7)

            t1 = (DISP_MIN_PITCH, cl_10_2_2_min_spacing(self.bolt.bolt_diameter_provided),
                  self.web_plate.pitch_provided,
                  get_pass_fail(self.web_bolt.min_pitch, self.web_plate.pitch_provided, relation='leq'))
            self.report_check.append(t1)
            t1 = (DISP_MAX_PITCH, cl_10_2_3_1_max_spacing(web_connecting_plates),
                  self.web_plate.pitch_provided,
                  get_pass_fail(self.web_bolt.max_spacing, self.web_plate.pitch_provided,
                                relation='geq'))
            self.report_check.append(t1)
            t2 = (DISP_MIN_GAUGE, cl_10_2_2_min_spacing(self.bolt.bolt_diameter_provided),
                  self.web_plate.gauge_provided,
                  get_pass_fail(self.web_bolt.min_gauge, self.web_plate.gauge_provided, relation="leq"))
            self.report_check.append(t2)
            t2 = (DISP_MAX_GAUGE, cl_10_2_3_1_max_spacing(web_connecting_plates),
                  self.web_plate.gauge_provided,
                  get_pass_fail(self.flange_bolt.max_spacing, self.web_plate.gauge_provided,
                                relation="geq"))
            self.report_check.append(t2)
            t3 = (DISP_MIN_END, cl_10_2_4_2_min_edge_end_dist(self.web_bolt.dia_hole, self.bolt.edge_type),
                  self.web_plate.end_dist_provided,
                  get_pass_fail(self.web_bolt.min_end_dist, self.web_plate.end_dist_provided,
                                relation='leq'))
            self.report_check.append(t3)
            t4 = (DISP_MAX_END, cl_10_2_4_3_max_edge_end_dist(self.bolt_conn_plates_web_t_fu_fy,
                                                              corrosive_influences=self.bolt.corrosive_influences,
                                                              parameter='end_dist'),
                  self.web_plate.end_dist_provided,
                  get_pass_fail(self.web_bolt.max_end_dist, self.web_plate.end_dist_provided,
                                relation='geq'))
            self.report_check.append(t4)
            t3 = (DISP_MIN_EDGE, cl_10_2_4_2_min_edge_end_dist(self.web_bolt.dia_hole, self.bolt.edge_type),
                  self.web_plate.edge_dist_provided,
                  get_pass_fail(self.web_bolt.min_edge_dist, self.web_plate.edge_dist_provided,
                                relation='leq'))
            self.report_check.append(t3)
            t4 = (DISP_MAX_EDGE, cl_10_2_4_3_max_edge_end_dist(self.bolt_conn_plates_web_t_fu_fy,
                                                              corrosive_influences=self.bolt.corrosive_influences,
                                                              parameter='edge_dist'),
                  self.web_plate.edge_dist_provided,
                  get_pass_fail(self.web_bolt.max_edge_dist, self.web_plate.edge_dist_provided,
                                relation="geq"))
            self.report_check.append(t4)

            if self.web_bolt.bolt_type == TYP_BEARING:
                web_bolt_bearing_capacity_kn = round(self.web_bolt.bolt_bearing_capacity / 1000, 2)
                t1 = (KEY_OUT_DISP_WEB_BOLT_SHEAR, '', cl_10_3_3_bolt_shear_capacity(self.web_bolt.bolt_fu, 2,
                                                                                     self.web_bolt.bolt_net_area,
                                                                                     self.web_bolt.gamma_mb,
                                                                                     web_bolt_shear_capacity_kn), '')
                self.report_check.append(t1)
                t8 = (KEY_DISP_KB, " ", cl_10_3_4_calculate_kb(self.web_plate.end_dist_provided, self.web_plate.pitch_provided,
                                                               self.web_bolt.dia_hole,
                                                               self.web_bolt.bolt_fu, self.web_bolt.fu_considered), '')
                self.report_check.append(t8)
                t2 = (KEY_OUT_DISP_WEB_BOLT_BEARING, '', cl_10_3_4_bolt_bearing_capacity(web_kb_disp,
                                                                                         self.bolt.bolt_diameter_provided,
                                                                                         self.bolt_conn_plates_web_t_fu_fy,
                                                                                         self.web_bolt.gamma_mb,
                                                                                         web_bolt_bearing_capacity_kn), '')
                self.report_check.append(t2)
                t3 = (KEY_OUT_DISP_WEB_BOLT_CAPACITY, '', cl_10_3_2_bolt_capacity(web_bolt_shear_capacity_kn,
                                                                                  web_bolt_bearing_capacity_kn,
                                                                                  web_bolt_capacity_kn), '')
                self.report_check.append(t3)
            else:

                t4 = (KEY_OUT_DISP_WEB_BOLT_SLIP, '', cl_10_4_3_HSFG_bolt_capacity(mu_f=self.bolt.mu_f, n_e=2,
                                                                                   K_h=web_kh_disp, fub=self.web_bolt.bolt_fu,
                                                                                   Anb=self.web_bolt.bolt_net_area,
                                                                                   gamma_mf=self.web_bolt.gamma_mf,
                                                                                   capacity=web_bolt_capacity_kn), '')
                self.report_check.append(t4)

            # t5 = (DISP_NUM_OF_BOLTS, get_trial_bolts(V_u=round(self.fact_shear_load / 1000, 2),
            #                                          A_u=(round(self.axial_force_w / 1000, 2)),
            #                                          bolt_capacity=web_bolt_capacity_kn, multiple=2,conn="flange_web"),
            #       self.web_plate.bolts_required, '')
            # self.report_check.append(t5)  # todo no of bolts


            t10 = (KEY_OUT_REQ_PARA_BOLT,  parameter_req_bolt_force(bolts_one_line=self.web_plate.bolts_one_line
                                                                       , gauge=self.web_plate.gauge_provided,
                                                                       ymax=round(self.web_plate.ymax, 2),
                                                                       xmax=round(self.web_plate.xmax, 2),
                                                                       bolt_line=self.web_plate.bolt_line,
                                                                       pitch=self.web_plate.pitch_provided,
                                                                       length_avail=self.web_plate.length_avail,conn="beam_beam"),'', '')
            self.report_check.append(t10)

            t10 = (KEY_OUT_REQ_MOMENT_DEMAND_BOLT,  moment_demand_req_bolt_force(
                shear_load=round(self.fact_shear_load / 1000, 2),
                web_moment=round(self.moment_web / 1000000, 2), ecc=self.web_plate.ecc,
                moment_demand=round(self.web_plate.moment_demand / 1000000, 2)),'', '')

            self.report_check.append(t10)

            t10 = (KEY_OUT_DISP_BOLT_FORCE,  Vres_bolts(bolts_one_line=self.web_plate.bolts_one_line,
                                                      ymax=round(self.web_plate.ymax, 2),
                                                      xmax=round(self.web_plate.xmax, 2),
                                                      bolt_line=self.web_plate.bolt_line,
                                                      shear_load=round(self.fact_shear_load / 1000, 2),
                                                      axial_load=round(self.axial_force_w / 1000, 2),
                                                      moment_demand=round(self.web_plate.moment_demand / 1000000, 2),
                                                      r=round(self.web_plate.sigma_r_sq / 1000, 2),
                                                      vbv=round(self.web_plate.vbv / 1000, 2),
                                                      tmv=round(self.web_plate.tmv / 1000, 2),
                                                      tmh=round(self.web_plate.tmh / 1000, 2),
                                                      abh=round(self.web_plate.abh / 1000, 2),
                                                      vres=round(self.web_plate.bolt_force / 1000, 2),conn = "beam_beam"),'', '')
            self.report_check.append(t10)

            t10 = (KEY_OUT_LONG_JOINT, cl_10_3_3_1_long_joint_bolted_req(),
                   long_joint_bolted_beam(self.web_plate.bolt_line, self.web_plate.bolts_one_line,
                                          self.web_plate.pitch_provided,
                                          self.web_plate.gauge_provided, self.bolt.bolt_diameter_provided,
                                          web_bolt_capacity_kn,
                                          web_bolt_capacity_red_kn,'web',self.web_plate.end_dist_provided,
                                          self.flange_plate.gap,self.web_plate.edge_dist_provided,
                                          self.section.web_thickness,self.section.root_radius,conn="beam_beam"), "")
            self.report_check.append(t10)

            t10 = (KEY_OUT_LARGE_GRIP, cl_10_3_3_2_large_grip_bolted_req(),
                   cl_10_3_3_2_large_grip_bolted_prov(self.t_sum2, self.web_bolt.bolt_diameter_provided,
                                          self.web_plate.beta_lj), "")
            self.report_check.append(t10)
            if self.web_bolt.bolt_type == TYP_BEARING:
                t5 = (KEY_OUT_DISP_BOLT_CAPACITY, round(self.web_plate.bolt_force / 1000, 2),
                      bolt_red_capacity_prov(self.web_plate.beta_lj,
                                             self.web_plate.beta_lg,
                                             web_bolt_capacity_kn,
                                             web_bolt_capacity_red_kn,"b"),
                      get_pass_fail(round(self.web_plate.bolt_force / 1000, 2), web_bolt_capacity_red_kn,
                                    relation="lesser"))
                self.report_check.append(t5)
            else:
                t5 = (KEY_OUT_DISP_BOLT_CAPACITY, round(self.web_plate.bolt_force / 1000, 2),
                      bolt_red_capacity_prov(self.web_plate.beta_lj,
                                             self.web_plate.beta_lg,
                                             web_bolt_capacity_kn,
                                             web_bolt_capacity_red_kn,"f"),
                      get_pass_fail(round(self.web_plate.bolt_force / 1000, 2), web_bolt_capacity_red_kn,
                                    relation="lesser"))
                self.report_check.append(t5)
        ######Flange plate check####
        if self.select_bolt_dia_status == True:
            if self.preference == "Outside":
                t1 = ('SubSection', 'Flange Plate Dimension Check - Outside', '|p{4cm}|p{5cm}|p{5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                t1 = (DISP_MIN_FLANGE_PLATE_HEIGHT, min_flange_plate_ht_req(beam_width=self.section.flange_width,
                                                                     min_flange_plate_ht=self.min_plate_height),
                      self.flange_plate.height,
                      get_pass_fail(self.min_plate_height, self.flange_plate.height, relation="leq"))
                self.report_check.append(t1)

                min_plate_length = 2 * (((self.flange_plate.bolt_line / 2 - 1) * self.flange_bolt.min_pitch) + (
                        2 * self.flange_bolt.min_end_dist) + (self.flange_plate.gap / 2))

                t1 = (DISP_MIN_FLANGE_PLATE_LENGTH, min_flange_plate_length_req(min_pitch=self.flange_bolt.min_pitch,
                                                                         min_end_dist=self.flange_bolt.min_end_dist,
                                                                         bolt_line=self.flange_plate.bolt_line,
                                                                         min_length=min_plate_length,
                                                                         gap=self.flange_plate.gap, sec="beam"),
                      self.flange_plate.length,
                      get_pass_fail(min_plate_length, self.flange_plate.length, relation="leq"))
                self.report_check.append(t1)

                t1 = (DISP_MIN_FLANGE_PLATE_THICK, display_prov(self.section.flange_thickness, "T"),
                      display_prov(self.flange_plate.thickness_provided, "t_{fp}"),
                      get_pass_fail(self.section.flange_thickness, self.flange_plate.thickness_provided,
                                    relation="lesser"))
                self.report_check.append(t1)
                self.Recheck_flange_pt_area_o = (self.flange_plate.height) * \
                                                self.flange_plate.thickness_provided
                t2 = (KEY_DISP_AREA_CHECK, plate_area_req(crs_area=round(self.flange_crs_sec_area, 2),
                                                          flange_web_area=round(self.Ap, 2)),
                      plate_recheck_area_weld(outerwidth=self.flange_plate.height,
                                              f_tp=self.flange_plate.thickness_provided, conn="flange",
                                              pref="Outside"),
                      get_pass_fail(self.Ap, self.Recheck_flange_pt_area_o, relation="leq"))
                self.report_check.append(t2)
            else:
                t1 = ('SubSection', 'Flange Plate Dimension Check - Outside/Inside', '|p{4cm}|p{5cm}|p{5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                ####OUTER PLATE####
                t1 = (DISP_MIN_FLANGE_PLATE_HEIGHT, min_flange_plate_ht_req(beam_width=self.section.flange_width,
                                                                     min_flange_plate_ht=self.min_plate_height),
                      self.flange_plate.height,
                      get_pass_fail(self.min_plate_height, self.flange_plate.height, relation="leq"))
                self.report_check.append(t1)

                min_plate_length = 2 * (((self.flange_plate.bolt_line / 2 - 1) * self.flange_bolt.min_pitch) + (
                        2 * self.flange_bolt.min_end_dist) + (self.flange_plate.gap / 2))

                t1 = (DISP_MIN_FLANGE_PLATE_LENGTH, min_flange_plate_length_req(min_pitch=self.flange_bolt.min_pitch,
                                                                         min_end_dist=self.flange_bolt.min_end_dist,
                                                                         bolt_line=self.flange_plate.bolt_line,
                                                                         min_length=min_plate_length,
                                                                         gap=self.flange_plate.gap, sec="beam"),
                      self.flange_plate.length,
                      get_pass_fail(min_plate_length, self.flange_plate.length, relation="leq"))
                self.report_check.append(t1)
                ######INNER PLATE
                min_inner_height =int((self.section.flange_width - self.section.web_thickness - (self.section.root_radius * 2)) / 2)
                min_inner_ht_req =50
                t1 = (DISP_MIN_PLATE_INNERHEIGHT, '>=50',
                      self.flange_plate.Innerheight,
                      get_pass_fail(min_inner_ht_req, self.flange_plate.Innerheight, relation="leq"))
                self.report_check.append(t1)

                t1 = (DISP_MAX_PLATE_INNERHEIGHT, min_inner_flange_plate_ht_req(beam_width=self.section.flange_width,
                                                                                web_thickness=self.section.web_thickness,
                                                                                root_radius=self.section.root_radius,
                                                                                min_inner_flange_plate_ht=min_inner_height),
                      self.flange_plate.Innerheight, get_pass_fail(min_inner_height,
                                                                   self.flange_plate.Innerheight,
                                                                   relation="geq"))
                self.report_check.append(t1)

                min_plate_length = 2 * (((self.flange_plate.bolt_line / 2 - 1) * self.flange_bolt.min_pitch) + (
                        2 * self.flange_bolt.min_end_dist) + (self.flange_plate.gap / 2))

                t1 = (DISP_MIN_PLATE_INNERLENGTH, min_flange_plate_length_req(min_pitch=self.flange_bolt.min_pitch,
                                                                              min_end_dist=self.flange_bolt.min_end_dist,
                                                                              bolt_line=self.flange_plate.bolt_line,
                                                                              min_length=min_plate_length,
                                                                              gap=self.flange_plate.gap, sec="beam"),
                      self.flange_plate.length,
                      get_pass_fail(min_plate_length, self.flange_plate.length, relation="leq"))
                self.report_check.append(t1)

                t1 = (DISP_MIN_FLANGE_PLATE_THICK, display_prov(self.section.flange_thickness / 2, "T/2"),
                      display_prov(self.flange_plate.thickness_provided, "t_{ifp}"),
                      get_pass_fail(self.section.flange_thickness / 2, self.flange_plate.thickness_provided,
                                    relation="lesser"))
                self.report_check.append(t1)
                self.Recheck_flange_pt_area_oi = (self.flange_plate.height + (2 * self.flange_plate.Innerheight)) * \
                                                 self.flange_plate.thickness_provided
                t2 = (KEY_DISP_AREA_CHECK, plate_area_req(crs_area=round(self.flange_crs_sec_area, 2),
                                                          flange_web_area=round(self.Ap, 2)),
                      plate_recheck_area_weld(outerwidth=self.flange_plate.height,
                                              innerwidth=self.flange_plate.Innerheight,
                                              f_tp=self.flange_plate.thickness_provided, t_wp=None, conn="flange",
                                              pref="Outside+Inside"),
                      get_pass_fail(self.Ap, self.Recheck_flange_pt_area_oi, relation="leq"))
                self.report_check.append(t2)

         ################
        if self.select_bolt_dia_status == True:
            self.min_web_plate_height = round(self.section.min_plate_height(), 2)
            t1 = ('SubSection', 'Web Plate Dimension Check', '|p{4cm}|p{5cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t1 = (DISP_MIN_WEB_PLATE_HEIGHT, min_plate_ht_req(D=self.section.depth, min_req_width=self.min_web_plate_height, r_r=self.section.root_radius,
                                                              t_f=self.section.flange_thickness),
                  self.web_plate.height,
                  get_pass_fail(self.min_web_plate_height, self.web_plate.height, relation="leq"))
            self.report_check.append(t1)

            min_plate_length = 2 * (((self.web_plate.bolt_line / 2 - 1) * self.web_bolt.min_pitch) + (
                    2 * self.web_bolt.min_end_dist) + (self.flange_plate.gap / 2))

            t1 = (DISP_MIN_WEB_PLATE_LENGTH, min_flange_plate_length_req(min_pitch=self.web_bolt.min_pitch,
                                                                     min_end_dist=self.web_bolt.min_end_dist,
                                                                     bolt_line=self.web_plate.bolt_line,
                                                                     min_length=min_plate_length,
                                                                     gap=self.flange_plate.gap, sec="beam"),
                  self.web_plate.length,
                  get_pass_fail(min_plate_length, self.web_plate.length, relation="leq"))
            self.report_check.append(t1)
            t1 = (DISP_MIN_WEB_PLATE_THICK, display_prov(self.section.web_thickness / 2, "t/2"),
                  display_prov(self.web_plate.thickness_provided, "t_{wp}"),
                  get_pass_fail(self.section.web_thickness / 2, self.web_plate.thickness_provided, relation="lesser"))
            self.report_check.append(t1)
            self.Recheck_web_pt_area_o = (2 * self.web_plate.height) * \
                                         self.web_plate.thickness_provided
            t2 = (KEY_DISP_AREA_CHECK, plate_area_req(round(self.web_crs_area, 2),
                                                      flange_web_area=round(self.Wp, 2)),
                  plate_recheck_area_weld(outerwidth=self.web_plate.height, innerwidth=None,
                                          f_tp=None, t_wp=self.web_plate.thickness_provided, conn="web",
                                          pref=None),
                  get_pass_fail(self.Wp, self.Recheck_web_pt_area_o, relation="leq"))
            self.report_check.append(t2)


        ###################
        # Member Capacities
        ###################
        ### Flange Check ###
        if self.get_plate_details_status ==True:
            t1 = ('SubSection', 'Member Check', '|p{4cm}|p{3cm}|p{7cm}|p{1.5cm}|')
            self.report_check.append(t1)
            gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']

            t1 = (KEY_DISP_TENSIONYIELDINGCAP_FLANGE, '', cl_6_2_tension_yield_capacity_member(self.section.flange_width,
                                                                                               self.section.flange_thickness,
                                                                                               self.section.fy, gamma_m0,
                                                                                               round(
                                                                                 self.section.tension_yielding_capacity / 1000,
                                                                                 2)), '')
            self.report_check.append(t1)
            gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

            t1 = (KEY_DISP_TENSIONRUPTURECAP_FLANGE, '', cl_6_3_1_tension_rupture_plate(w_p=self.section.flange_width,
                                                                                        t_p=self.section.flange_thickness,
                                                                                        n_c=self.flange_plate.bolts_one_line,
                                                                                        d_o=self.flange_bolt.dia_hole,
                                                                                        fu=self.section.fu, gamma_m1=gamma_m1,
                                                                                        T_dn=round(
                                                                                         self.section.tension_rupture_capacity / 1000,
                                                                                         2)), '')

            self.report_check.append(t1)

            t6 = (
                KEY_DISP_BLOCKSHEARCAP_FLANGE, '', cl_6_4_blockshear_capacity_member(Tdb=round(self.section.block_shear_capacity / 1000, 2)), '')
            self.report_check.append(t6)

            t1 = (KEY_DISP_FLANGE_TEN_CAPACITY, display_prov(round(self.flange_force / 1000, 2), "F_f"),

                  cl_6_1_tension_capacity_member(round(self.section.tension_yielding_capacity / 1000, 2),
                                                 round(self.section.tension_rupture_capacity / 1000, 2),
                                                 round(self.section.block_shear_capacity / 1000, 2)),
                  get_pass_fail(round(self.flange_force / 1000, 2), round(self.section.tension_capacity_flange / 1000, 2),
                                relation="lesser"))
            self.report_check.append(t1)

            ### web Check ###
            gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
            # A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
            webheight = round((self.section.depth - 2 * self.section.flange_thickness),2)
            t1 = (KEY_DISP_TENSIONYIELDINGCAP_WEB, '', cl_6_2_tension_yield_capacity_member(webheight,
                                                                                            self.section.web_thickness,
                                                                                            self.section.fy, gamma_m0,
                                                                                            round(
                                                                              self.section.tension_yielding_capacity_web / 1000,
                                                                              2)), '')
            self.report_check.append(t1)
            gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

            t1 = (KEY_DISP_TENSIONRUPTURECAP_WEB, '', cl_6_3_1_tension_rupture_plate(w_p=webheight,
                                                                                     t_p=self.section.web_thickness,
                                                                                     n_c=self.web_plate.bolts_one_line,
                                                                                     d_o=self.web_bolt.dia_hole,
                                                                                     fu=self.section.fu, gamma_m1=gamma_m1,
                                                                                     T_dn=round(
                                                                                      self.section.tension_rupture_capacity_web / 1000,
                                                                                      2)), '')
            self.report_check.append(t1)

            t1 = (
                KEY_DISP_BLOCKSHEARCAP_WEB, '', cl_6_4_blockshear_capacity_member(Tdb=round(self.section.block_shear_capacity_web / 1000, 2)), '')

            self.report_check.append(t1)

            t1 = (KEY_DISP_WEB_TEN_CAPACITY, display_prov(round(self.axial_force_w / 1000, 2), "A_w"),

                  cl_6_1_tension_capacity_member(round(self.section.tension_yielding_capacity_web / 1000, 2),
                                                 round(self.section.tension_rupture_capacity_web / 1000, 2),
                                                 round(self.section.block_shear_capacity_web / 1000, 2)),
                  get_pass_fail(round(self.axial_force_w / 1000, 2), round(self.section.tension_capacity_web / 1000, 2),
                                relation="lesser"))
            self.report_check.append(t1)
        ###################
        # Flange plate Capacities check
        ###################
        if self.flange_check_axial_status == True:
            if self.preference == "Outside":

                t1 = ('SubSection', 'Flange Plate Capacity Check for Axial Load - Outside', '|p{4cm}|p{3cm}|p{7cm}|p{1.5cm}|')
                self.report_check.append(t1)
                gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']

                t1 = (KEY_DISP_TENSIONYIELDINGCAP_FLANGE_PLATE, '', cl_6_2_tension_yield_capacity_member(self.flange_plate.height,
                                                                                                         self.flange_plate.thickness_provided,
                                                                                                         self.flange_plate.fy, gamma_m0,
                                                                                                         round(
                                                                                 self.flange_plate.tension_yielding_capacity / 1000,
                                                                                 2)), '')
                self.report_check.append(t1)
                gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

                t1 = (KEY_DISP_TENSIONRUPTURECAP_FLANGE_PLATE, '', cl_6_3_1_tension_rupture_plate(w_p=self.flange_plate.height,
                                                                                                  t_p=self.flange_plate.thickness_provided,
                                                                                                  n_c=self.flange_plate.bolts_one_line,
                                                                                                  d_o=self.flange_bolt.dia_hole,
                                                                                                  fu=self.flange_plate.fu,
                                                                                                  gamma_m1=gamma_m1,
                                                                                                  T_dn=round(
                                                                                            self.flange_plate.tension_rupture_capacity / 1000,
                                                                                            2)), '')
                self.report_check.append(t1)

                t1 = (KEY_DISP_BLOCKSHEARCAP_FLANGE_PLATE, '',
                      cl_6_4_blockshear_capacity_member(Tdb=round(self.flange_plate.block_shear_capacity / 1000, 2)), '')

                self.report_check.append(t1)

                t1 = (KEY_DISP_FLANGE_PLATE_TEN_CAP, display_prov(round(self.flange_force / 1000, 2), "F_f"),
                      cl_6_1_tension_capacity_member(round(self.flange_plate.tension_yielding_capacity / 1000, 2),
                                                     round(self.flange_plate.tension_rupture_capacity / 1000, 2),
                                                     round(self.flange_plate.block_shear_capacity / 1000, 2)),
                      get_pass_fail(round(self.flange_force / 1000, 2),
                                    round(self.flange_plate.tension_capacity_flange_plate / 1000, 2),
                                    relation="lesser"))
                self.report_check.append(t1)
            else:
                t1 = (
                'SubSection', 'Flange Plate Capacity Check for Axial Load - Outside/Inside ', '|p{4cm}|p{3cm}|p{7cm}|p{1.5cm}|')
                self.report_check.append(t1)
                gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
                total_height = self.flange_plate.height + (2 * self.flange_plate.Innerheight)

                t1 = (KEY_DISP_TENSIONYIELDINGCAP_FLANGE_PLATE, '', cl_6_2_tension_yield_capacity_member(total_height,
                                                                                                         self.flange_plate.thickness_provided,
                                                                                                         self.flange_plate.fy, gamma_m0,
                                                                                                         round(
                                                                                 self.flange_plate.tension_yielding_capacity / 1000,
                                                                                 2)), '')
                self.report_check.append(t1)

                gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

                t1 = (KEY_DISP_TENSIONRUPTURECAP_FLANGE_PLATE, '', cl_6_3_1_tension_rupture_plate(w_p=total_height,
                                                                                                  t_p=self.flange_plate.thickness_provided,
                                                                                                  n_c=self.flange_plate.bolts_one_line,
                                                                                                  d_o=self.flange_bolt.dia_hole,
                                                                                                  fu=self.flange_plate.fu,
                                                                                                  gamma_m1=gamma_m1,
                                                                                                  T_dn=round(
                                                                                            self.flange_plate.tension_rupture_capacity / 1000,
                                                                                            2)), '')
                self.report_check.append(t1)

                t1 = (KEY_DISP_BLOCKSHEARCAP_FLANGE_PLATE, '',
                      cl_6_4_blockshear_capacity_member(Tdb=round(self.flange_plate.block_shear_capacity / 1000, 2)), '')

                self.report_check.append(t1)

                t1 = (KEY_DISP_FLANGE_PLATE_TEN_CAP, display_prov(round(self.flange_force / 1000, 2), "F_f"),
                      cl_6_1_tension_capacity_member(round(self.flange_plate.tension_yielding_capacity / 1000, 2),
                                                     round(self.flange_plate.tension_rupture_capacity / 1000, 2),
                                                     round(self.flange_plate.block_shear_capacity / 1000, 2)),
                      get_pass_fail(round(self.flange_force / 1000, 2),
                                    round(self.flange_plate.tension_capacity_flange_plate / 1000, 2),
                                    relation="lesser"))
                self.report_check.append(t1)

        ###################
        # Web plate Capacities check axial
        ###################
        if self.flange_plate_check_status == True and self.web_axial_check_status == True:
            t1 = ('SubSection', 'Web Plate Capacity Check for Axial Load', '|p{4cm}|p{3cm}|p{7cm}|p{1.5cm}|')
            self.report_check.append(t1)
            gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']

            t1 = (KEY_DISP_TENSION_YIELDCAPACITY_WEB_PLATE, '', cl_6_2_tension_yield_capacity_member(self.web_plate.height,
                                                                                                     self.web_plate.thickness_provided,
                                                                                                     self.web_plate.fy,
                                                                                                     gamma_m0,
                                                                                                     round(self.web_plate.tension_yielding_capacity / 1000,
                                                                             2), 2), '')

            self.report_check.append(t1)
            gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

            t1 = (KEY_DISP_TENSION_RUPTURECAPACITY_WEB_PLATE, '', cl_6_3_1_tension_rupture_plate(self.web_plate.height,
                                                                                                 self.web_plate.thickness_provided,
                                                                                                 self.web_plate.bolts_one_line,
                                                                                                 self.web_bolt.dia_hole,
                                                                                                 self.web_plate.fu, gamma_m1,
                                                                                                 round(
                                                                                        self.web_plate.tension_rupture_capacity / 1000,
                                                                                        2), 2), '')

            self.report_check.append(t1)

            t1 = (KEY_DISP_TENSION_BLOCKSHEARCAPACITY_WEB_PLATE, '',
                  cl_6_4_blockshear_capacity_member(Tdb=round(self.web_plate.block_shear_capacity / 1000, 2)), '')
            self.report_check.append(t1)

            t1 = (KEY_DISP_WEB_PLATE_CAPACITY, display_prov(round(self.axial_force_w / 1000, 2), "A_w"),
                  cl_6_1_tension_capacity_member(round(self.web_plate.tension_yielding_capacity / 1000, 2),
                                                 round(self.web_plate.tension_rupture_capacity / 1000, 2),
                                                 round(self.web_plate.block_shear_capacity / 1000, 2)),
                  get_pass_fail(round(self.axial_force_w / 1000, 2),
                                round(self.web_plate.tension_capacity_web_plate / 1000, 2),
                                relation="lesser"))
            self.report_check.append(t1)

        ###################

        # Web plate Capacities check Shear
        ###################
        if self.web_plate_axial_check_status == True:
            t1 = ('SubSection', 'Web Plate Capacity Checks for Shear Load', '|p{4cm}|p{3cm}|p{7cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t1 = (KEY_DISP_SHEARYIELDINGCAP_WEB_PLATE, '', cl_8_4_shear_yielding_capacity_member(self.web_plate.height, self.web_plate.thickness_provided,
                                                                                                 self.web_plate.fy, gamma_m0,
                                                                                                 round(self.web_plate.shear_yielding_capacity / 1000/0.6, 2), 2), '')
            self.report_check.append(t1)

            initial_shear_capacity = round(self.web_plate.shear_yielding_capacity / 1000 /0.6, 2)
            reduced_shear_capacity = round(self.web_plate.shear_yielding_capacity / 1000, 2)
            t1 = (KEY_DISP_ALLOW_SHEAR, display_prov(self.load.shear_force, "V"),
                  allow_shear_capacity(initial_shear_capacity, reduced_shear_capacity),
                  get_pass_fail(self.load.shear_force, reduced_shear_capacity, relation="lesser"))
            self.report_check.append(t1)
            if self.shear_yielding_status == True:
                t1 = (KEY_DISP_SHEARRUPTURECAP_WEB_PLATE, '', AISC_J4_shear_rupture_capacity_member(self.web_plate.height, self.web_plate.thickness_provided,
                                                                      self.web_plate.bolts_one_line ,self.web_bolt.dia_hole,
                                                                      self.web_plate.fu,
                                                                      round(self.web_plate.shear_rupture_capacity / 1000, 2),
                                                                      gamma_m1,2), '')

                self.report_check.append(t1)

            t1 = (KEY_DISP_BLOCKSHEARCAP_WEB_PLATE, '',
                  cl_6_4_blockshear_capacity_member(Tdb=round(self.web_plate.block_shear_capacity_shear / 1000, 2), stress ="shear"), '')
            self.report_check.append(t1)

            t1 = (KEY_DISP_WEBPLATE_SHEAR_CAPACITY_PLATE, '',

                  cl_8_4_shear_capacity_member(round(self.web_plate.shear_yielding_capacity / 1000, 2),
                                               round(self.web_plate.shear_rupture_capacity / 1000, 2),
                                               round(self.web_plate.block_shear_capacity_shear/ 1000, 2)),
                  get_pass_fail(round(self.fact_shear_load / 1000, 2),
                                round(self.web_plate.shear_capacity_web_plate / 1000, 2),relation="lesser"))
            self.report_check.append(t1)

            # red_shear_capacity =  round(self.web_plate.shear_capacity_web_plate / 1000, 2)
            # t1 = (KEY_DISP_ALLOW_SHEAR,display_prov(round(self.fact_shear_load / 1000, 2), "V_u"),
            #       allow_shear_capacity(round(self.web_plate.shear_capacity_web_plate / 1000/0.6, 2), round(red_shear_capacity,2)),
            #       get_pass_fail(round(self.fact_shear_load / 1000, 2),
            #                     round(self.web_plate.shear_capacity_web_plate / 1000, 2),relation="lesser"))
            # self.report_check.append(t1)

        Disp_2d_image = []
        Disp_3D_image = "/ResourceFiles/images/3d.png"

        #config = configparser.ConfigParser()
        #config.read_file(open(r'Osdag.config'))
        #desktop_path = config.get("desktop_path", "path1")
        #print("desk:", desktop_path)
        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = os.path.abspath(".") # TEMP
        rel_path = rel_path.replace("\\", "/")

        fname_no_ext = popup_summary['filename']


        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                               rel_path, Disp_2d_image, Disp_3D_image, module=self.module)

# def save_latex(self, uiObj, Design_Check, reportsummary, filename, rel_path, Disp_3d_image):
