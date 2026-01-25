from django.shortcuts import render
from deep_translator import Translator
from .models import TranslationHistory  # Biz yaratgan modelni chaqiramiz

def index(request):
    # Dastlab bazadagi oxirgi 5 ta tarjimani olamiz (yangi qo'shilganlari tepada turadi)
    history = TranslationHistory.objects.all().order_by('-created_at')[:5]
    
    if request.method == "POST":
        text = request.POST.get('text', '')
        lang = request.POST.get('lang', 'en')
        
        if text:
            try:
                # Tarjima qilish jarayoni
                translator = Translator()
                translated_obj = translator.translate(text, dest=lang)
                translated_text = translated_obj.text
                
                # 1. Tarjimani ma'lumotlar bazasiga saqlaymiz
                TranslationHistory.objects.create(
                    original_text=text,
                    translated_text=translated_text,
                    language=lang
                )
                
                # 2. Tarixni yangilaymiz (yangi saqlangan element bilan birga)
                history = TranslationHistory.objects.all().order_by('-created_at')[:5]
                
                return render(request, 'index.html', {
                    'translated': translated_text,
                    'original': text,
                    'lang': lang,
                    'history': history  # Sahifaga tarixni yuboramiz
                })
            except Exception as e:
                return render(request, 'index.html', {
                    'translated': f"Xatolik yuz berdi: {str(e)}",
                    'history': history
                })
    
    # POST bo'lmaganda yoki matn bo'sh bo'lganda shunchaki tarixni ko'rsatamiz
    return render(request, 'index.html', {'history': history})