from flask import request, redirect, url_for
from urllib.parse import urlparse

def redirect_back(fallback_endpoint, **fallback_kwargs):
    """
    Redirige al referrer (mantiene filtros en la URL).
    Si no hay referrer o es de otro dominio, usa el fallback.
    """
    referrer = request.referrer
    
    if referrer:
        ref_domain = urlparse(referrer).netloc
        own_domain = urlparse(request.host_url).netloc
        if ref_domain == own_domain:
            return redirect(referrer)
    
    return redirect(url_for(fallback_endpoint, **fallback_kwargs))