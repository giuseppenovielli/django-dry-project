from rest_framework import serializers

from .mixins import  NestedCreateFullCleanMixin, NestedUpdateFullCleanMixin


class WritableNestedFullCleanSerializer(NestedCreateFullCleanMixin, NestedUpdateFullCleanMixin,
                                    serializers.ModelSerializer):
    pass