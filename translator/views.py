from django.shortcuts import render
from deep_translator import GoogleTranslator
from .models import TranslationHistory

def translate_app(request):
    # Tarixni bazadan olish
    history = TranslationHistory.objects.all().order_by('-created_at')[:5]
    
    original = ""
    translated = ""
    lang = "en"

    if request.method == "POST":
        original = request.POST.get('text', '')
        lang = request.POST.get('lang', 'en')
        
        if original:
            try:
                translated = GoogleTranslator(source='auto', target=lang).translate(original)
                # Bazaga saqlash
                TranslationHistory.objects.create(
                    original_text=original,
                    translated_text=translated,
                    language=lang
                )
                # Tarixni yangilash
                history = TranslationHistory.objects.all().order_by('-created_at')[:5]
            except Exception as e:
                translated = f"Xatolik: {str(e)}"
                
    return render(request, 'index.html', {
        'translated': translated,
        'original': original,
        'lang': lang,
        'history': history
    })