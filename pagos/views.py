# Importamos 'JsonResponse' de Django, que nos permite enviar respuestas en formato JSON (muy usado en APIs y webhooks)
from django.http import JsonResponse
# Importamos el decorador 'csrf_exempt' para desactivar temporalmente la protección CSRF en vistas específicas (necesario para Stripe)
from django.views.decorators.csrf import csrf_exempt

# Aplicamos el decorador '@csrf_exempt' a la vista de abajo para que acepte peticiones POST de Stripe sin el token de seguridad CSRF
@csrf_exempt
# Definimos la función 'webhook_pagos' que recibe el objeto 'request' con toda la información de la petición HTTP
def webhook_pagos(request):
    # Verificamos si el método de la petición es POST (Stripe envía la información usando POST)
    if request.method == 'POST':
        # Guardamos en la variable 'payload' el cuerpo (body) de la petición que contiene los datos que envió Stripe
        payload = request.body
        
        # COMENTARIO: Aquí debes añadir la lógica de Stripe para verificar la firma de seguridad (webhook_secret)
        # TODO: Validar firmas criptográficas de Stripe (Seguridad)
        
        # COMENTARIO: Aquí debes buscar al usuario y cambiar su suscripción a activa en la base de datos
        # TODO: Actualizar UsuarioSaaS.suscripcion_activa = True
        
        # Retornamos un JSON exitoso indicando a Stripe que recibimos el mensaje correctamente
        return JsonResponse({'status': 'Webhook recibido de forma segura'})
    
    # Si la petición no fue POST (por ejemplo GET), retornamos un error 405 (Método no permitido) con un JSON
    return JsonResponse({'error': 'Método no permitido'}, status=405)
