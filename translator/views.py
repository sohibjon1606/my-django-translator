from django.shortcuts import render, redirect
from deep_translator import GoogleTranslator
from .models import TranslationHistory

def translate_app(request):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    # Faqat shu foydalanuvchining tarixi
    history = TranslationHistory.objects.filter(session_id=session_id).order_by('-created_at')
    
    original, translated, lang = "", "", "en"

    if request.method == "POST":
        original = request.POST.get('text', '')
        lang = request.POST.get('lang', 'en')
        
        if original:
            try:
                translated = GoogleTranslator(source='auto', target=lang).translate(original)
                TranslationHistory.objects.create(
                    original_text=original,
                    translated_text=translated,
                    language=lang,
                    session_id=session_id
                )
            except Exception as e:
                translated = f"Xatolik: {str(e)}"
                
    return render(request, 'index.html', {
        'translated': translated,
        'original': original,
        'lang': lang,
        'history': history
    })

def clear_history(request):
    session_id = request.session.session_key
    if session_id:
        TranslationHistory.objects.filter(session_id=session_id).delete()
    return redirect('home')