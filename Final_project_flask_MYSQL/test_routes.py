#!/usr/bin/env python3
"""
Script to test all routes and fix any remaining issues
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_routes():
    """Test all routes are available"""
    app = create_app()
    
    print("🔍 Verificando rutas disponibles...")
    
    with app.app_context():
        # Get all routes
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'rule': rule.rule,
                'methods': list(rule.methods)
            })
        
        # Print routes by blueprint
        blueprints = {}
        for route in routes:
            blueprint = route['endpoint'].split('.')[0] if '.' in route['endpoint'] else 'main'
            if blueprint not in blueprints:
                blueprints[blueprint] = []
            blueprints[blueprint].append(route)
        
        for blueprint, bp_routes in blueprints.items():
            print(f"\n📁 {blueprint.upper()} Blueprint:")
            for route in bp_routes:
                print(f"   ✅ {route['endpoint']} -> {route['rule']} {route['methods']}")
        
        # Check specific routes that base.html uses
        required_routes = [
            'home.index',
            'auth.logout',
            'grafo.index',
            'grafo.visualizar',
            'user.index'
        ]
        
        print(f"\n🎯 Verificando rutas requeridas por base.html:")
        for route in required_routes:
            found = any(r['endpoint'] == route for r in routes)
            status = "✅" if found else "❌"
            print(f"   {status} {route}")
        
        print(f"\n📊 Total de rutas: {len(routes)}")

if __name__ == "__main__":
    test_routes()
