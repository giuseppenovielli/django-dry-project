
class DeleteModelQuerySet:

    def delete(self):
        """
        https://docs.djangoproject.com/en/3.2/topics/db/models/#overriding-predefined-model-methods
        """
        for obj in self.all():
            obj.delete() 


class UpdateModelQuerySet():
    
    def update(self, **kwargs):
        """
        https://docs.djangoproject.com/en/3.2/topics/db/models/#overriding-predefined-model-methods
        WORKAROUND -> Call save() method
        """
        for obj in self.all():
            for field in obj._meta.fields:
                if field.name not in kwargs:
                    continue
                setattr(obj, field.name, kwargs[field.name])
            obj.save()