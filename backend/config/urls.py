import os
from pathlib import Path
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework.schemas import get_schema_view

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST = BASE_DIR.parent / 'frontend' / 'dist'

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'platform': '9-Sonli umumiy o‘rta ta‘lim maktabi boshqaruv tizimi (9-Maktab)',
        'version': '2.0.0-PRO-MAX',
        'environment': 'development' if settings.DEBUG else 'production',
        'timestamp': timezone.now().isoformat(),
        'endpoints': {
            'admin': '/admin/',
            'api_docs': '/api/docs/',
            'health': '/health/',
            'auth': '/api/auth/',
            'accounts': '/api/accounts/',
            'school': '/api/school/',
            'academics': '/api/academics/',
            'attendance': '/api/attendance/',
            'assignments': '/api/assignments/',
            'assessments': '/api/assessments/',
            'analytics': '/api/analytics/',
        }
    })

def swagger_ui(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>9-Maktab API Documentation | Swagger UI</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" crossorigin="anonymous"></script>
        <script>
            window.onload = () => {
                window.ui = SwaggerUIBundle({
                    url: '/api/schema/',
                    dom_id: '#swagger-ui',
                });
            };
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)

def root_index_view(request):
    """
    Serve the production React frontend build from frontend/dist/index.html if available,
    otherwise serve the smart institutional welcome portal.
    """
    dist_index = FRONTEND_DIST / 'index.html'
    if dist_index.exists():
        with open(dist_index, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html; charset=utf-8')

    # Institutional Gateway Page if frontend is not built
    html = f"""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>9-Maktab — Boshqaruv va Ta'lim Portali</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 40px 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 32px; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
            h1 {{ color: #38bdf8; margin-top: 0; font-size: 28px; }}
            p {{ line-height: 1.6; color: #94a3b8; }}
            .badge {{ display: inline-block; background: #0284c7; color: white; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; margin-bottom: 16px; }}
            .links {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-top: 24px; }}
            .link-card {{ background: #0f172a; padding: 14px 18px; border-radius: 8px; border: 1px solid #334155; text-decoration: none; color: #e2e8f0; transition: border-color 0.2s; }}
            .link-card:hover {{ border-color: #38bdf8; color: #38bdf8; }}
            .link-card strong {{ display: block; margin-bottom: 4px; font-size: 15px; }}
            .link-card span {{ font-size: 12px; color: #64748b; }}
            .dev-note {{ margin-top: 24px; padding: 12px; background: #0284c720; border-left: 4px solid #38bdf8; font-size: 13px; color: #bae6fd; }}
        </style>
    </head>
    <body>
        <div class="container">
            <span class="badge">9-MAKTAB ULTRA-PRO MAX</span>
            <h1>9-Sonli umumiy o‘rta ta‘lim maktabi platformasi</h1>
            <p>Toshkent shahar 9-sonli umumiy o'rta ta'lim maktabining zamonaviy raqamli ta'lim, boshqaruv va tahlil platformasi backend tizimi faol ishlamoqda.</p>
            
            <div class="links">
                <a class="link-card" href="/api/docs/">
                    <strong>API Hujjatlari (Swagger)</strong>
                    <span>Barcha REST API yo'llarini sinash</span>
                </a>
                <a class="link-card" href="/health/">
                    <strong>Tizim holati (Healthcheck)</strong>
                    <span>Platforma monitoringi va ma'lumotlar</span>
                </a>
                <a class="link-card" href="/admin/">
                    <strong>Django Boshqaruv Paneli</strong>
                    <span>Ma'murlar uchun ma'lumotlar bazasi</span>
                </a>
                <a class="link-card" href="/api/school/info/">
                    <strong>Maktab Ma'lumotlari API</strong>
                    <span>Muassasa rasmiy rekvizitlari</span>
                </a>
                <a class="link-card" href="/api/analytics/overview/">
                    <strong>Tahliliy Statistika API</strong>
                    <span>Maktab ko'rsatkichlari va tahlillar</span>
                </a>
            </div>

            <div class="dev-note">
                💡 <strong>Frontend ishlab chiqish:</strong> React/Vite frontendini ishga tushirish uchun <code>cd frontend && npm run dev</code> buyrug'idan foydalaning (<code>http://localhost:5173</code>).
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

schema_view = get_schema_view(
    title="9-Maktab Smart School Management API",
    description="Toshkent shahar 9-sonli umumiy o'rta ta'lim maktabi boshqaruv va tahlil platformasi REST API",
    version="2.0.0",
    public=True,
)

urlpatterns = [
    # Root & Health & Docs
    path('', root_index_view, name='root'),
    path('health/', health_check, name='health_check_root'),
    path('api/health/', health_check, name='health_check_api'),
    path('api/schema/', schema_view, name='openapi_schema'),
    path('api/docs/', swagger_ui, name='swagger_ui'),
    path('admin/', admin.site.urls),

    # Preserved legacy and new endpoints
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/school/', include('apps.portal.urls')),
    path('api/portal/', include('apps.portal.urls')),

    # Core academic & management modules
    path('api/academics/', include('apps.academics.urls')),
    path('api/timetables/', include('apps.timetables.urls')),
    path('api/attendance/', include('apps.attendance.urls')),
    path('api/assignments/', include('apps.assignments.urls')),
    path('api/assessments/', include('apps.assessments.urls')),
    path('api/resources/', include('apps.resources.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/audit/', include('apps.audit.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Also serve frontend assets from dist if available
    if FRONTEND_DIST.exists():
        urlpatterns += static('/assets/', document_root=FRONTEND_DIST / 'assets')
