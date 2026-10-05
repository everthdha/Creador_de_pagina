from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
from decouple import config

# =========================================================================
# CONFIGURACIÓN API GEMINI
# =========================================================================
genai.configure(api_key=config('GEMINI_API_KEY'))

def landing_page(request):
    return render(request, 'base/landing.html')

def dashboard(request):
    return render(request, 'base/dashboard.html')

def preparar_sitio(request):
    if request.method == 'POST':
        nicho = request.POST.get('nicho', '')
        experiencia = request.POST.get('experiencia', '')
        colores = request.POST.get('colores', '')
        prompt_extra = request.POST.get('prompt_extra', '')
        
        # Guardar en sesión
        request.session['site_prefs'] = {
            'nicho': nicho,
            'experiencia': experiencia,
            'colores': colores,
            'prompt_extra': prompt_extra
        }
        return redirect('editor')
    return redirect('dashboard')

def workspace_editor(request):
    # Obtener preferencias y borrarlas de la sesión (para que no vuelva a auto-generar al recargar)
    prefs = request.session.pop('site_prefs', None)
    prefs_json = json.dumps(prefs) if prefs else 'null'
    
    return render(request, 'editor/workspace.html', {'site_prefs_json': prefs_json})

@csrf_exempt
def api_agente_ia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            nicho = data.get('nicho', '')
            experiencia = data.get('experiencia', '')
            colores = data.get('colores', '')
            
            # Ensamblar prompt completo
            prompt_final = prompt
            if nicho or colores or experiencia:
                prompt_final = f"Nicho del sitio: {nicho}. Paleta de colores requerida: {colores}. Instrucciones extra: {prompt}"
            
            instruccion_sistema = "Eres un experto diseñador web. Genera código HTML puro con clases de Tailwind CSS basado en la petición del usuario. Respeta estrictamente la paleta de colores indicada. Devuelve ÚNICAMENTE el código HTML, sin bloques markdown (```html), sin explicaciones, sin texto adicional."
            
            if experiencia:
                instruccion_sistema += f"\nCRÍTICO: El formato de experiencia exigido es '{experiencia}'."
                if "Cinematográfica" in experiencia:
                    instruccion_sistema += " Debes añadir <script src='https://unpkg.com/aos@next/dist/aos.js'></script> y <link rel='stylesheet' href='https://unpkg.com/aos@next/dist/aos.css' /> al HTML e inicializarlo con <script>AOS.init();</script> al final. Usa atributos data-aos='fade-up' para que todo aparezca fluidamente al hacer scroll."
                elif "Bento Grid" in experiencia:
                    instruccion_sistema += " Debes diseñar una estructura de cuadrícula asimétrica ultra moderna (Bento Grid) usando Tailwind CSS (grid, grid-cols-2, md:grid-cols-4, gap-4, y col-span/row-span para las tarjetas)."
                elif "App" in experiencia or "Link-in-Bio" in experiencia:
                    instruccion_sistema += " El formato debe ser centrado y vertical, optimizado para móvil como un Link-in-Bio, limitando el ancho máximo de la estructura (max-w-md mx-auto)."
            
            model = genai.GenerativeModel(
                model_name='gemini-3.8-flash',
                system_instruction=instruccion_sistema
            )
            
            response = model.generate_content(prompt_final)
            
            respuesta_html = response.text.strip()
            
            # Limpieza de markdown
            if respuesta_html.startswith('```html'):
                respuesta_html = respuesta_html[7:]
            if respuesta_html.startswith('```'):
                respuesta_html = respuesta_html[3:]
            if respuesta_html.endswith('```'):
                respuesta_html = respuesta_html[:-3]
            respuesta_html = respuesta_html.strip()
            
            return JsonResponse({
                'mensaje': '¡Sitio generado por IA!',
                'codigo_html': respuesta_html,
                'status': 'success'
            })
        except Exception as e:
            fallback_html = """
<section class="min-h-screen bg-[#09090b] text-white flex items-center justify-center p-8">
  <div class="max-w-6xl w-full">
    <div class="text-center mb-16">
      <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-indigo-500">
        Diseño de Respaldo
      </h1>
      <p class="text-xl text-gray-400 max-w-2xl mx-auto">
        La API de IA está descansando, pero tu creatividad no se detiene. Este es un Bento Grid autogenerado.
      </p>
      <div class="mt-8 flex gap-4 justify-center">
        <button class="px-8 py-3 rounded-full bg-white text-black font-semibold hover:bg-gray-200 transition-colors">Comenzar</button>
        <button class="px-8 py-3 rounded-full bg-gray-800 text-white font-semibold border border-gray-700 hover:border-gray-500 transition-colors">Saber más</button>
      </div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 auto-rows-[200px]">
      <div class="md:col-span-2 md:row-span-2 rounded-3xl bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-700 p-8 flex flex-col justify-end relative overflow-hidden group">
        <div class="absolute inset-0 bg-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        <h3 class="text-2xl font-bold mb-2">Editor Visual</h3>
        <p class="text-gray-400">Arrastra, suelta y construye sin límites.</p>
      </div>
      
      <div class="md:col-span-1 md:row-span-1 rounded-3xl bg-gray-900 border border-gray-800 p-6 flex items-center justify-center">
        <span class="text-4xl">🎨</span>
      </div>
      
      <div class="md:col-span-1 md:row-span-2 rounded-3xl bg-indigo-950 border border-indigo-900 p-8 flex flex-col">
        <h3 class="text-xl font-bold text-indigo-200 mb-4">Métricas</h3>
        <div class="flex-1 rounded-xl bg-indigo-900/50 flex items-end p-4">
            <div class="w-full flex items-end justify-between gap-2 h-24">
                <div class="w-full bg-indigo-500 rounded-t-md h-[40%]"></div>
                <div class="w-full bg-indigo-400 rounded-t-md h-[70%]"></div>
                <div class="w-full bg-indigo-300 rounded-t-md h-[50%]"></div>
                <div class="w-full bg-white rounded-t-md h-[90%]"></div>
            </div>
        </div>
      </div>
      
      <div class="md:col-span-1 md:row-span-1 rounded-3xl bg-gray-900 border border-gray-800 p-6 flex flex-col justify-center">
        <h3 class="text-lg font-medium text-gray-300">Usuarios</h3>
        <p class="text-3xl font-bold text-white mt-1">+2,500</p>
      </div>
    </div>
  </div>
</section>
"""
            return JsonResponse({
                'mensaje': '⚠️ Límite de IA alcanzado. Mostrando diseño de respaldo (Modo Desarrollo).',
                'codigo_html': fallback_html,
                'status': 'success'
            })
    return JsonResponse({'error': 'Método no permitido'}, status=405)
