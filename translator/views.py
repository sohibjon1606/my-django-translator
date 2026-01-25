from django.shortcuts import render
from deep_translator import GoogleTranslator

def translate_app(request):
    translated_text = ""
    original_text = ""
    target_lang = "en"

    if request.method == "POST":
        original_text = request.POST.get('text')
        target_lang = request.POST.get('lang')
        
        if original_text:
            try:
                # deep-translator orqali tarjima qilish
                translated_text = GoogleTranslator(source='auto', target=target_lang).translate(original_text)
            except Exception as e:
                translated_text = f"Xatolik: {e}"

    return render(request, 'index.html', {
        'translated': translated_text,
        'original': original_text,
        'lang': target_lang
    })