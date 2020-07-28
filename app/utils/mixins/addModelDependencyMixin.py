# Django REST Framework imports
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import get_object_or_404


class addModelDependencyMixin(GenericViewSet):
    """Add dependency mixin

    Manages adding a model object to views
    that require it. And verify that the model exists
    """

    def __init__(self, model_dependency):
        self.model_dependency = model_dependency

    def dispatch(self, request, *args, **kwargs):
        """Return the normal dispatch but adds the model model."""
        self.add_model_dependency_to_self(self.kwargs['id'])
        return super(addModelDependencyMixin, self).dispatch(request, *args, **kwargs)

    def add_model_dependency_to_self(self, id):
        """Handle the model"""
        self.model = get_object_or_404(
            model_dependency,
            id=id
        )
