from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter

from .models import Sensor, Unidad, Proyecto, Lectura, Variable, MayorOIgualRegla, Regla, MenorOIgualRegla, Mensajero, ConsolaMensajero

#########
## ADMINISTRACION DE POLIMORFISMO - REGLAS
#########

class ReglaChildAdmin(PolymorphicChildModelAdmin):
	pass

@admin.register(Regla)
class ReglaParentAdmin(PolymorphicParentModelAdmin):
    # The parent model admin 
    base_model = Regla  # Optional, explicitly set here.
    child_models = (MayorOIgualRegla,MenorOIgualRegla)

@admin.register(MayorOIgualRegla)
class MayorOIgualReglaAdmin(ReglaChildAdmin):
    base_model = MayorOIgualRegla  # Explicitly set here!

@admin.register(MenorOIgualRegla)
class MenorOIgualReglaAdmin(ReglaChildAdmin):
    base_model = MenorOIgualRegla  # Explicitly set here!

###########
## ADMINISTRACION DE POLIMORFISMO - MENSAJEROS
#########
from .models import SmsMensajero, EmailMensajero

class MensajeroChildAdmin(PolymorphicChildModelAdmin):
    pass

@admin.register(Mensajero)
class MensajeroParentAdmin(PolymorphicParentModelAdmin):
    # The parent model admin 
    base_model = Mensajero  # Optional, explicitly set here.
    child_models = (ConsolaMensajero,SmsMensajero, EmailMensajero)

@admin.register(ConsolaMensajero)
class ConsolaMensajeroAdmin(MensajeroChildAdmin):
    base_model = ConsolaMensajero

@admin.register(SmsMensajero)
class SmsMensajeroAdmin(MensajeroChildAdmin):
    base_model = SmsMensajero

@admin.register(EmailMensajero)
class SmsMensajeroAdmin(MensajeroChildAdmin):
    base_model = EmailMensajero    

##### OTROS

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass

@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    pass

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    pass

@admin.register(Lectura)
class LecturaAdmin(admin.ModelAdmin):
    pass

@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    pass

from .models import Alerta
@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    pass

"""
@admin.register(MayorOIgualRegla)
class MayorOIgualReglaAdmin(admin.ModelAdmin):
    pass
"""

# Register your models here.
