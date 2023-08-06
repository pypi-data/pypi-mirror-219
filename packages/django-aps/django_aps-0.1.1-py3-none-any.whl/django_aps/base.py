from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView


class SerializerError(Exception):
    pass


class BaseGenericAPIView(GenericAPIView):
    all_serializers = {}

    result_serializers_class = None

    def get_serializer_class(self):
        """ Return the class to use for the serializer."""
        if self.serializer_class is None:
            self.serializer_class = self.all_serializers.get(self.request.method.lower())
            assert self.serializer_class is not None, (
                    "'%s' should either include a `serializer_class` attribute, "
                    "or include a 'all_serializers' attribute."
                    % self.__class__.__name__
            )

        return self.serializer_class

    @staticmethod
    def check_validate(serializer):
        """ Check the serializer is valid."""
        if not serializer.is_valid():
            raise SerializerError(serializer.errors)
