from numpy import source
from rest_framework import serializers
from .models import CustomeUser, Material, outlayType, outlay


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomeUser
        fields = (
            "id","first_name","last_name","username","user_type","password"
        )

class CustomMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUser
        fields = (
            "__all__"
        )



class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = '__all__'

class outlayTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = outlayType
        fields = '__all__'

class outlaySerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material_id.material_name', read_only=True)
    outlay_name = serializers.CharField(source="outlay_type.outlay_name",read_only=True)
    user_name = serializers.CharField(source="user_id.first_name",read_only=True)
    class Meta:
        model = outlay
        fields = ["id","material_id","material_name","outlay_type","outlay_name","user_id","user_name","price","date","description"]


