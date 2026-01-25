from django.shortcuts import render
from deep_translator import GoogleTranslator
from .models import TranslationHistory

def translate_app(request):
    # 1. Foydalanuvchi uchun maxsus sessiya ID sini olish yoki yaratish
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    # 2. Faqat shu sessiyaga tegishli oxirgi 5 ta tarjimani olish
    # Buning uchun modelga 'session_key' maydonini qo'shishimiz kerak (pastga qarang)
    history = TranslationHistory.objects.filter(session_id=session_id).order_by('-created_at')[:5]
    
    original = ""
    translated = ""
    lang = "en"

    if request.method == "POST":
        original = request.POST.get('text', '')
        lang = request.POST.get('lang', 'en')
        
        if original:
            try:
                translated = GoogleTranslator(source='auto', target=lang).translate(original)
                
                # 3. Tarjimani sessiya ID si bilan birga saqlash
                TranslationHistory.objects.create(
                    original_text=original,
                    translated_text=translated,
                    language=lang,
                    session_id=session_id  # Kim tarjima qilganini eslab qoladi
                )
                
                history = TranslationHistory.objects.filter(session_id=session_id).order_by('-created_at')[:5]
            except Exception as e:
                translated = f"Xatolik: {str(e)}"
                
    return render(request, 'index.html', {
        'translated': translated,
        'original': original,
        'lang': lang,
        'history': history
    })