# Security Guardrails (PII Redaction for Phone/Email & Prompt Injection defense)
import re

def security_guardrail(user_input: str) -> tuple[bool, str]:
    """
    1. Chặn Prompt Injection: Kiểm tra các từ khóa thao túng hệ thống.
    2. PII Redaction: Ẩn danh số điện thoại và email.
    """
    
    # 1. Danh sách từ khóa cấm (Prompt Injection)
    forbidden_patterns = [
        "ignore previous instructions", "bỏ qua quy định", 
        "system prompt", "quên quy tắc", "hack", "admin"
    ]
    
    for pattern in forbidden_patterns:
        if pattern in user_input.lower():
            return False, "🚨 Security Alert: Prompt Injection detected!"
    
    # 2. Xóa thông tin cá nhân nhạy cảm (PII Redaction)
    # Ẩn số điện thoại (10-11 số)
    sanitized_input = re.sub(r'\b\d{10,11}\b', '[REDACTED_PHONE]', user_input)
    
    # Ẩn Email
    sanitized_input = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED_EMAIL]', sanitized_input)
    
    return True, sanitized_input