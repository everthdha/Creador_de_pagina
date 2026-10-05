# Importamos el módulo 'models' de Django que contiene las herramientas para interactuar con la base de datos
from django.db import models
# Importamos 'AbstractUser' que es el modelo de usuario predeterminado de Django para extenderlo
from django.contrib.auth.models import AbstractUser

# Definimos nuestra clase 'UsuarioSaaS' que hereda de 'AbstractUser' (obteniendo campos como username, password, email)
class UsuarioSaaS(AbstractUser):
    # Creamos una tupla llamada 'PLANES' que contiene las opciones para el campo de plan_actual (valor de BD, Etiqueta legible)
    PLANES = (
        # Opción 1: valor en base de datos 'gratis', etiqueta 'Freemium (Editor Visual)'
        ('gratis', 'Freemium (Editor Visual)'),
        # Opción 2: valor en base de datos 'subdominio', etiqueta 'Subdominio ($150 MXN)'
        ('subdominio', 'Subdominio ($150 MXN)'),
        # Opción 3: valor en base de datos 'dominio_propio', etiqueta 'Dominio Propio ($200 MXN)'
        ('dominio_propio', 'Dominio Propio ($200 MXN)'),
    )
    # Creamos un campo de caracteres para el plan actual, con longitud máxima 20, opciones desde PLANES, y default 'gratis'
    plan_actual = models.CharField(max_length=20, choices=PLANES, default='gratis')
    # Creamos un campo para almacenar el subdominio asignado, longitud 100, permitiendo que esté en blanco y sea nulo
    subdominio_asignado = models.CharField(max_length=100, blank=True, null=True)
    # Creamos un campo para guardar el ID de cliente en Stripe, longitud 100, permitiendo que esté vacío o sea nulo
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    # Creamos un campo booleano para indicar si la suscripción está activa o no, por defecto es Falso (inactiva)
    suscripcion_activa = models.BooleanField(default=False)

    # Definimos el método __str__ para representar este objeto como una cadena de texto en la consola y admin
    def __str__(self):
        # Retorna el nombre de usuario (username) y la descripción amigable del plan actual (ej: "Juan - Freemium...")
        return f"{self.username} - {self.get_plan_actual_display()}"
