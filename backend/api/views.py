from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import sqlite3
from .serializers import BoltDiameterSerializer, MaterialSerializer, BeamSerializer, DesignInputSerializer
from django.conf import settings
from .osdag.beam_cover_plate import BeamCoverPlate #Import Osdag's beam cover plate module
from .osdag.reportGenerator_latex import CreateLatex #Import report generator

class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"})
    
class BoltDiameterAPIView(APIView):
    def get(self, request):
        # Define the path to the database
        db_path = settings.BASE_DIR / 'database/Intg_osdag.sqlite'

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try: 
            # Execute a query to get the bolt diameters
            cursor.execute("SELECT Bolt_diameter FROM Bolt;")
            rows = cursor.fetchall()

            #Extract the bolt diameters from a list
            bolt_diameters = [row[0] for row in rows]
            
            #serialize the data
            serializer = BoltDiameterSerializer({"bolt_diameters": bolt_diameters})

            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            conn.close()

class MaterialAPIView(APIView):
    def get(self, request):
        # Define the path to the database
        db_path = settings.BASE_DIR / 'database/Intg_osdag.sqlite'

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try: 
            # Execute a query to get the materials
            cursor.execute("SELECT * FROM Material;")
            rows = cursor.fetchall()
            
            #extract column names
            column_names = [desc[0] for desc in cursor.description]

            # Map data to dictionaries
            materials = [dict(zip(column_names, row)) for row in rows]

            #serialize the data
            serializer = MaterialSerializer(materials, many=True)

            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            conn.close()

class BeamAPIView(APIView):
    def get(self, request):
        # Define the path to the database (update the path as needed)
        db_path = settings.BASE_DIR / 'database/Intg_osdag.sqlite'

        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Execute the query to fetch all beams from the Beams table
            cursor.execute("SELECT * FROM Beams;")
            rows = cursor.fetchall()

            # Extract column names from the query result
            column_names = [desc[0] for desc in cursor.description]

            # Map the fetched rows to dictionaries with column names as keys
            beams = [dict(zip(column_names, row)) for row in rows]

            # Serialize the data using the BeamSerializer
            serializer = BeamSerializer(beams, many=True)

            return Response(serializer.data)

        except Exception as e:
            # Handle any exception that occurs during the query execution
            return Response({"error": str(e)}, status=500)

        finally:
            # Always close the database connection
            conn.close()


class SubmitDesignDataAPIView(APIView):
    """
    API View to handle the submission of form data from React,
    perform design calculations, and return STL and PDF reports.
    """

    def post(self, request):
        serializer = DesignInputSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            # ✅ Assign input values with correct keys matching input_values()
            design_data = {
                "Module": "Moment Connection",
                "Connectivity": "Beam-Beam",
                "Load.Shear": validated_data.get("shear_force", 0),
                "Load.Axial": validated_data.get("axial_force", 0),
                "Load.Moment": validated_data.get("bending_moment", 0),
                "Bolt Type": validated_data.get("bolt_type", "HSFG"),
                "Corrosive Influence": validated_data.get("corrosive_influence", "No"),
                "Design Method": validated_data.get("design_method", "Limit State Design"),
                "Edge Method": validated_data.get("edge_method", "Sheared or hand flame cut"),
                "Flange.Thickness": validated_data.get("flange_thickness_selected", []),
                "Gap": validated_data.get("gap_between_beam_and_support", 10),
                "Modulus of Elasticity": validated_data.get("modulus_of_elasticity", 200),
                "Modulus of Rigidity": validated_data.get("modulus_of_rigidity", 76.9),
                "Poisson's Ratio": validated_data.get("poissons_ratio", 0.3),
                "Member.Designation": validated_data.get("selected_beam", ""),
                "Bolt.Diameters": validated_data.get("selected_diameters", []),
                "Slip Factor": validated_data.get("slip_factor", 0.3),
                "Thermal Expansion Coefficient": validated_data.get("thermal_expansion_coefficient", 12),
                "Type of Beam": validated_data.get("type_beam", "Rolled"),
                "Ultimate Strength": validated_data.get("ultimate_strength", 410),
                "Web.Thickness": validated_data.get("web_thickness_selected", []),
                "Yield Strength 20mm": validated_data.get("yield_strength_20mm", 250),
                "Yield Strength 40mm": validated_data.get("yield_strength_40mm", 240),
                "Yield Strength >40mm": validated_data.get("yield_strength_greater_40mm", 230),
                "Beam.Properties": validated_data.get("beam_properties", {})
            }

            # Initialize and set input values
            beam_cover = BeamCoverPlate()
            beam_cover.set_input_values(design_data)

            # Perform design calculations
            beam_cover.member_capacity()

            # Check if the design is valid
            if not beam_cover.member_capacity_status:
                return Response({"status": "error", "message": "Design is unsafe"}, status=400)

            # Generate STL Model (Placeholder)
            stl_path = os.path.join(settings.MEDIA_ROOT, "beam_cover_plate.stl")
            self.generate_stl(beam_cover, stl_path)

            # Generate PDF Report
            report_path = self.generate_design_report(beam_cover)

            return Response({
                "status": "success",
                "stl_file": stl_path,
                "report_file": report_path
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_stl(self, beam_cover, stl_path):
        """
        Placeholder function to generate STL file for the 3D model.
        """
        with open(stl_path, "w") as f:
            f.write("Generated STL file for Beam Cover Plate")

    def generate_design_report(self, beam_cover):
        """
        Generates the design report PDF using PyLaTeX.
        """
        report_dir = os.path.join(settings.MEDIA_ROOT)
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, "design_report.pdf")

        doc = CreateLatex()
        doc.save_latex(beam_cover, {}, {}, report_path, "", "", "", "Beam Cover Plate Bolted")

        return report_path