from rest_framework import serializers
from .models import FindSH

class FindSHListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindSH
        fields = ['id', 'title', 'content', 'created_at', 'promise_date', 'place', 'age_group',
                  'gender', 'num', 'free_condition', 'fee'] # , nickname

class FindSHDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindSH
        fields = '__all__'

class FindSHSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindSH
        fields = ['place', 'promise_date', 'age_group', 'gender', 'num']
        
class FindSHCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FindSH
        fields = ['id', 'title', 'content', 'place', 'promise_date', 'gender', 'num', 'fee', 'free_condition']

    def validate_free_condition(self, value):
        conditions = value.split('#')
        conditions = [condition.strip() for condition in conditions if condition.strip()]
        
        for condition in conditions:
            if not (condition.startswith('#') and 5 <= len(condition) <= 10):
                raise serializers.ValidationError("Each condition must start with '#' and be 5 to 10 letters long.")
        
        validated_value = ' '.join(conditions)
        return validated_value