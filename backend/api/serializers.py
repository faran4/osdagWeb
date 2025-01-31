from rest_framework import serializers

class BoltDiameterSerializer(serializers.Serializer):
    # Define a field to hold the list of bolt diameters
    bolt_diameters = serializers.ListField(child=serializers.CharField())

class MaterialSerializer(serializers.Serializer):
    Grade = serializers.CharField(max_length=255)
    Yield_Stress_lt_20 = serializers.IntegerField(source="Yield Stress (< 20)")
    Yield_Stress_20_40 = serializers.IntegerField(source="Yield Stress (20 -40)")
    Yield_Stress_gt_40 = serializers.IntegerField(source="Yield Stress (> 40)")
    Ultimate_Tensile_Stress = serializers.IntegerField(source="Ultimate Tensile Stress")
    Elongation = serializers.IntegerField(source="Elongation ")

class BeamSerializer(serializers.Serializer):
    Designation = serializers.CharField(max_length=50)
    Mass = serializers.FloatField()
    Area = serializers.FloatField()
    D = serializers.FloatField()
    B = serializers.FloatField()
    tw = serializers.FloatField()
    T = serializers.FloatField()
    FlangeSlope = serializers.IntegerField()
    R1 = serializers.FloatField()
    R2 = serializers.FloatField()
    Iz = serializers.FloatField()
    Iy = serializers.FloatField()
    rz = serializers.FloatField()
    ry = serializers.FloatField()
    Zz = serializers.FloatField()
    Zy = serializers.FloatField()
    Zpz = serializers.FloatField()
    Zpy = serializers.FloatField()
    It = serializers.FloatField()
    Iw = serializers.FloatField()
    Source = serializers.CharField(max_length=100)
    Type = serializers.CharField(max_length=100, required=False)

from rest_framework import serializers

class DesignInputSerializer(serializers.Serializer):
    # Float fields (Numeric values can be null)
    bendingMoment = serializers.FloatField(required=False, allow_null=True)
    shearForce = serializers.FloatField(required=False, allow_null=True)
    axialForce = serializers.FloatField(required=False, allow_null=True)
    
    # Arrays / Lists
    selectedDiameters = serializers.ListField(child=serializers.CharField(), required=False)  # List of strings (e.g., ["16", "20"])
    propertyClassSelected = serializers.ListField(child=serializers.FloatField(), required=False)  # List of numbers (e.g., [3.6, 4.6, 4.8])
    flangeThicknessSelected = serializers.ListField(child=serializers.FloatField(), required=False)  # List of numbers (e.g., [16])
    webThicknessSelected = serializers.ListField(child=serializers.FloatField(), required=False)  # List of numbers (e.g., [10, 12])
    
    # String fields
    boltType = serializers.CharField(required=False, allow_blank=True)
    outerPlateValue = serializers.CharField(required=False, allow_blank=True)
    selectedBeam = serializers.CharField(required=False, allow_blank=True)
    type = serializers.CharField(required=False, allow_blank=True)
    holeType = serializers.CharField(required=False, allow_blank=True)
    edgeMethod = serializers.CharField(required=False, allow_blank=True)
    corrosiveInfluence = serializers.CharField(required=False, allow_blank=True)
    designMethod = serializers.CharField(required=False, allow_blank=True)
    typeBeam = serializers.CharField(required=False, allow_blank=True)

    # Handling mixed-type fields (Strings in quotes are converted to Float)
    slipFactor = serializers.FloatField(required=False, allow_null=True)  # Converts "0.3" to 0.3
    gapBetweenBeamAndSupport = serializers.FloatField(required=False, allow_null=True)  # Converts "10" to 10

    # Beam Properties (Complex JSON structure)
    beamProperties = serializers.JSONField(required=False)  

    # Material Strengths
    ultimateStrengthMaterial = serializers.FloatField(required=False, allow_null=True)
    ultimateStrength = serializers.FloatField(required=False, allow_null=True)
    yieldStrength20mmMaterial = serializers.FloatField(required=False, allow_null=True)
    yieldStrength20mm = serializers.FloatField(required=False, allow_null=True)
    yieldStrength40mm = serializers.FloatField(required=False, allow_null=True)
    yieldStrengthGreater40mm = serializers.FloatField(required=False, allow_null=True)

    # Mechanical Properties
    modulusOfElasticity = serializers.FloatField(required=False, allow_null=True)
    modulusOfRigidity = serializers.FloatField(required=False, allow_null=True)
    poissonsRatio = serializers.FloatField(required=False, allow_null=True)
    thermalExpansionCoefficient = serializers.FloatField(required=False, allow_null=True)

