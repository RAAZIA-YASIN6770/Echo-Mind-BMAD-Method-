import json
import uuid
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from .models import User, UserProfile, ParentSettings
from backend.services.seed_service import get_seed_service
from backend.services.tree_health_service import get_tree_health_service
from backend.services.auth_service import get_auth_service
from backend.services.parent_service import get_parent_service
from backend.services.monitoring_service import get_monitor
from backend.services.response_scrubber import get_response_scrubber
from backend.socratic_engine import get_socratic_engine
from backend.middleware.pii_scrubber import scrub_pii
from backend.safety_filter import SafetyFilter

# Initialize Safety Engine
safety_filter = SafetyFilter()

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'child')
        age = data.get('age')
        
        if not all([email, password, age]):
            return JsonResponse({"success": False, "error": "Missing required fields"}, status=400)
        
        # COPPA Check
        auth_service = get_auth_service()
        if int(age) < 13 and role == 'child':
            parent_email = data.get('parent_email')
            if not parent_email:
                return JsonResponse({
                    "success": False, 
                    "error": "Parental consent (email) is required for children under 13"
                }, status=403)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "error": "User already exists"}, status=409)
        
        user = User.objects.create_user(
            email=email,
            password=password,
            role=role,
            age=age,
            parent_pin=data.get('parent_pin')
        )
        
        return JsonResponse({
            "success": True,
            "message": "User registered successfully",
            "user_id": str(user.user_id)
        }, status=201)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(email=email, password=password)
        if not user:
            return JsonResponse({"success": False, "error": "Invalid email or password"}, status=401)
        
        auth_service = get_auth_service()
        token_data = {
            "sub": str(user.user_id),
            "email": user.email,
            "role": user.role
        }
        
        access_token = auth_service.create_access_token(token_data)
        refresh_token = auth_service.create_refresh_token(token_data)
        
        return JsonResponse({
            "success": True,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "user_id": str(user.user_id),
                "email": user.email,
                "role": user.role
            }
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def onboarding(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        age = int(data.get('age', 10))
        grade_level = int(data.get('grade_level', 5))
        
        # Normally would link to a logged in user
        user_id = str(uuid.uuid4())
        
        seed_service = get_seed_service()
        seed_data = seed_service.assign_random_seed(user_id)
        
        tree_service = get_tree_health_service()
        tree_data = tree_service.calculate_tree_health([])
        
        return JsonResponse({
            "success": True,
            "user": {
                "user_id": user_id,
                "name": name,
                "age": age,
                "grade_level": grade_level,
                "created_at": datetime.utcnow().isoformat()
            },
            "seed": seed_data,
            "tree": tree_data,
            "welcome_message": f"Welcome {name}! You received a {seed_data['seed_emoji']} {seed_data['seed_name']}!"
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def chat_message(request):
    start_time = datetime.utcnow()
    try:
        data = json.loads(request.body)
        user_input = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        session_id = data.get('session_id', 'default')
        grade_level = data.get('grade_level', 5)
        
        # Safety Lock 2: Filter & Scrub
        safety_result = safety_filter.analyze_input(user_input, user_id, session_id)
        if not safety_result['is_safe']:
            return JsonResponse({
                "success": True,
                "response": safety_result['recommended_response'],
                "metadata": {"safety_lock": 2, "violation": safety_result['violations'][0], "passed": False}
            })
            
        scrub_result = scrub_pii(user_input)
        clean_input = scrub_result['scrubbed_text']
        
        # Socratic Engine
        engine = get_socratic_engine()
        engine_result = engine.process_message(
            user_id=user_id,
            session_id=session_id,
            message=clean_input,
            grade_level=grade_level,
            pii_detected=scrub_result['pii_detected']
        )
        
        ai_response = engine_result['response']['message']
        
        # Safety Lock 3: Response Scrubber
        scrubber = get_response_scrubber()
        validation = scrubber.validate(ai_response)
        final_response = ai_response
        if not validation['is_valid']:
            if validation['score'] < 50:
                final_response = "That's a great question! What do you think might be the first step? 🤔"

        latency = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        # Track metric
        monitor = get_monitor()
        monitor.track_request(latency, True)
        
        return JsonResponse({
            "success": True,
            "response": final_response,
            "category": engine_result.get('category', 'general'),
            "metadata": {
                "latency_ms": int(latency),
                "pii_detected": scrub_result['pii_detected'],
                "lock_2_passed": True,
                "lock_3_passed": validation['is_valid']
            },
            "events": engine_result.get('events', {})
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@require_http_methods(["GET"])
def parent_dashboard(request):
    # Simulated token check for demo
    user_id = request.GET.get('user_id', 'parent_1')
    service = get_parent_service()
    summaries = service.get_child_summaries(user_id)
    return JsonResponse({"success": True, "children": summaries})

@require_http_methods(["GET"])
def system_metrics(request):
    monitor = get_monitor()
    return JsonResponse({"success": True, "metrics": monitor.get_system_metrics()})
