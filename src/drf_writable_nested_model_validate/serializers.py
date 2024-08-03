from rest_framework import serializers

from .mixins import  NestedCreateModelValidateMixin, NestedUpdateModelValidateMixin


class WritableNestedValidateModelSerializer(NestedCreateModelValidateMixin, NestedUpdateModelValidateMixin,
                                    serializers.ModelSerializer):
    pass