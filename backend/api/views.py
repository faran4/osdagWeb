from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sqlite3
from .serializers import BoltDiameterSerializer, MaterialSerializer, BeamSerializer, DesignInputSerializer
from django.conf import settings
from .beam_cover_plate import BeamCoverPlate

class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"})
    
class BoltDiameterAPIView(APIView):
    def get(self, request):
        # Define the path to the database
        db_path = settings.BASE_DIR / 'database/Intg_osdag.db'

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
        db_path = settings.BASE_DIR / 'database/Intg_osdag.db'

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
        db_path = settings.BASE_DIR / 'database/Intg_osdag.db'

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

            try:
                # Initialize BeamCoverPlate with input data
                beam_cover_plate = BeamCoverPlate(validated_data)

                # Process Data (Perform Calculations)
                beam_cover_plate.process_data()

                # Define file paths for generated outputs
                model_filename = "beam_cover_plate_3d.step"
                report_filename = "beam_cover_plate_report.pdf"
                model_path = os.path.join(settings.MEDIA_ROOT, model_filename)
                report_path = os.path.join(settings.MEDIA_ROOT, report_filename)

                # Generate the 3D model
                beam_cover_plate.generate_3D_model(model_path)

                # Generate the design report
                beam_cover_plate.generate_design_report(report_path)

                # Construct URLs for accessing generated files
                model_url = request.build_absolute_uri(settings.MEDIA_URL + model_filename)
                report_url = request.build_absolute_uri(settings.MEDIA_URL + report_filename)

                return Response(
                    {
                        "message": "Calculation successful",
                        "3d_model_url": model_url,
                        "report_url": report_url,
                    },
                    status=status.HTTP_200_OK,
                )

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)