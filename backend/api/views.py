from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sqlite3
from .serializers import BoltDiameterSerializer, MaterialSerializer, BeamSerializer, DesignInputSerializer
from django.conf import settings

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
    assign the data to variables, and return a response.
    """

    def post(self, request):
        serializer = DesignInputSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Assigning data to variables
            bending_moment = validated_data.get("bendingMoment")
            shear_force = validated_data.get("shearForce")
            axial_force = validated_data.get("axialForce")
            bolt_type = validated_data.get("boltType")
            selected_beam = validated_data.get("selectedBeam")
            beam_properties = validated_data.get("beamProperties")  # JSON object
            flange_thickness_selected = validated_data.get("flangeThicknessSelected")
            web_thickness_selected = validated_data.get("webThicknessSelected")
            selected_diameters = validated_data.get("selectedDiameters")

            # Mechanical properties
            modulus_of_elasticity = validated_data.get("modulusOfElasticity")
            modulus_of_rigidity = validated_data.get("modulusOfRigidity")
            poissons_ratio = validated_data.get("poissonsRatio")
            thermal_expansion_coefficient = validated_data.get("thermalExpansionCoefficient")

            # Strength parameters
            ultimate_strength = validated_data.get("ultimateStrength")
            yield_strength_20mm = validated_data.get("yieldStrength20mm")
            yield_strength_40mm = validated_data.get("yieldStrength40mm")
            yield_strength_greater_40mm = validated_data.get("yieldStrengthGreater40mm")

            # Additional design parameters
            slip_factor = validated_data.get("slipFactor")
            edge_method = validated_data.get("edgeMethod")
            gap_between_beam_and_support = validated_data.get("gapBetweenBeamAndSupport")
            corrosive_influence = validated_data.get("corrosiveInfluence")
            design_method = validated_data.get("designMethod")
            type_beam = validated_data.get("typeBeam")

            # Example calculation (replace with actual calculations)
            example_calculation = (bending_moment or 0) + (shear_force or 0) - (axial_force or 0)

            # Return response with the received data and example calculations
            return Response(
                {
                    "message": "Form data received successfully",
                    "bending_moment": bending_moment,
                    "shear_force": shear_force,
                    "axial_force": axial_force,
                    "bolt_type": bolt_type,
                    "selected_beam": selected_beam,
                    "beam_properties": beam_properties,
                    "flange_thickness_selected": flange_thickness_selected,
                    "web_thickness_selected": web_thickness_selected,
                    "selected_diameters": selected_diameters,
                    "modulus_of_elasticity": modulus_of_elasticity,
                    "modulus_of_rigidity": modulus_of_rigidity,
                    "poissons_ratio": poissons_ratio,
                    "thermal_expansion_coefficient": thermal_expansion_coefficient,
                    "ultimate_strength": ultimate_strength,
                    "yield_strength_20mm": yield_strength_20mm,
                    "yield_strength_40mm": yield_strength_40mm,
                    "yield_strength_greater_40mm": yield_strength_greater_40mm,
                    "slip_factor": slip_factor,
                    "edge_method": edge_method,
                    "gap_between_beam_and_support": gap_between_beam_and_support,
                    "corrosive_influence": corrosive_influence,
                    "design_method": design_method,
                    "type_beam": type_beam,
                    "example_calculation": example_calculation,
                },
                status=status.HTTP_200_OK,
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)