#!/usr/bin/env python3
"""
403 Bypass Practice Lab
A comprehensive bug bounty practice lab demonstrating various 403 bypass techniques
"""

from flask import Flask, request, jsonify, render_template_string, make_response
import re
from urllib.parse import unquote

app = Flask(__name__)

# Secret flags for each challenge
FLAGS = {
    'verb_bypass': 'FLAG{HTTP_VERB_BYPASS_SUCCESS}',
    'header_bypass': 'FLAG{HEADER_BYPASS_SUCCESS}',
    'path_bypass1': 'FLAG{PATH_ENCODING_BYPASS}',
    'path_bypass2': 'FLAG{PATH_CASE_BYPASS}',
    'path_bypass3': 'FLAG{PATH_SLASH_BYPASS}',
    'parameter_bypass': 'FLAG{PARAMETER_POLLUTION}',
    'host_bypass': 'FLAG{HOST_HEADER_BYPASS}',
    'method_override': 'FLAG{METHOD_OVERRIDE_BYPASS}',
}

# HTML template for the main page
MAIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>403 Bypass Practice Lab - zack0x01</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.1);
            position: relative;
            overflow: hidden;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        }
        
        .social-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 25px 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            text-align: center;
        }
        
        .social-header h2 {
            color: #ffffff;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 15px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        .social-header .tagline {
            color: rgba(255,255,255,0.95);
            font-size: 16px;
            margin-bottom: 20px;
            font-weight: 500;
        }
        
        .social-links {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .social-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
            color: #ffffff;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s ease;
            border: 2px solid rgba(255,255,255,0.3);
        }
        
        .social-link:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            border-color: rgba(255,255,255,0.5);
        }
        
        .social-link .icon {
            font-size: 18px;
        }
        
        h1 {
            color: #1a1a2e;
            text-align: center;
            font-size: 42px;
            font-weight: 800;
            margin: 30px 0 20px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .intro-text {
            text-align: center;
            font-size: 18px;
            color: #555;
            margin-bottom: 40px;
            line-height: 1.8;
            font-weight: 400;
        }
        
        .challenge {
            background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
            border-left: 5px solid #667eea;
            padding: 25px;
            margin: 25px 0;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .challenge::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 5px;
            height: 100%;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        .challenge:hover {
            transform: translateX(5px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
        }
        
        .challenge h2 {
            color: #1a1a2e;
            margin-top: 0;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 15px;
        }
        
        .challenge p {
            line-height: 1.8;
            color: #555;
            font-size: 16px;
            margin-bottom: 15px;
        }
        
        .endpoint {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #68d391;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', 'Monaco', monospace;
            margin: 15px 0;
            word-break: break-all;
            font-size: 14px;
            border: 1px solid rgba(104, 211, 145, 0.2);
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
        }
        
        .hint {
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border-left: 4px solid #f39c12;
            padding: 18px;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(243, 156, 18, 0.1);
            display: none;
        }
        
        .hint.show {
            display: block;
        }
        
        .hint strong {
            color: #d68910;
            font-weight: 700;
        }
        
        .show-hint-btn {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            margin: 10px 0;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(243, 156, 18, 0.3);
        }
        
        .show-hint-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(243, 156, 18, 0.4);
        }
        
        .show-hint-btn:active {
            transform: translateY(0);
        }
        
        .success {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border-left: 4px solid #28a745;
            padding: 18px;
            margin: 15px 0;
            border-radius: 8px;
            color: #155724;
            box-shadow: 0 2px 8px rgba(40, 167, 69, 0.1);
        }
        
        code {
            background: linear-gradient(135deg, #f4f4f4 0%, #e9ecef 100%);
            padding: 4px 8px;
            border-radius: 5px;
            font-family: 'Courier New', 'Monaco', monospace;
            font-size: 14px;
            color: #e83e8c;
            font-weight: 600;
            border: 1px solid #dee2e6;
        }
        
        .flag {
            background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
            border-left: 4px solid #0c5460;
            padding: 18px;
            margin: 15px 0;
            border-radius: 8px;
            font-weight: 700;
            color: #0c5460;
            box-shadow: 0 2px 8px rgba(12, 84, 96, 0.1);
        }
        
        .resources-box {
            margin-top: 50px;
            padding: 25px;
            background: linear-gradient(135deg, #e7f3ff 0%, #d1ecf1 100%);
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        
        .resources-box h3 {
            color: #0c5460;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 15px;
        }
        
        .resources-box a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
        }
        
        .resources-box a:hover {
            color: #764ba2;
            text-decoration: underline;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 25px;
            }
            
            h1 {
                font-size: 32px;
            }
            
            .social-links {
                flex-direction: column;
                align-items: center;
            }
            
            .social-link {
                width: 100%;
                max-width: 250px;
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="social-header">
            <h2>🔓 Lureab Bug Bounty</h2>
            <div class="tagline">by zack0x01</div>
            <div class="social-links">
                <a href="https://lureo.shop" target="_blank" class="social-link">
                    <span class="icon">🛒</span>
                    <span>Learn Bug Bounty from zack0x01</span>
                </a>
                <a href="https://youtube.com/@zack0x01" target="_blank" class="social-link">
                    <span class="icon">📺</span>
                    <span>YouTube</span>
                </a>
                <a href="https://twitter.com/zack0x01" target="_blank" class="social-link">
                    <span class="icon">🐦</span>
                    <span>Twitter</span>
                </a>
            </div>
        </div>
        
        <h1>403 Bypass Practice Lab</h1>
        <p class="intro-text">
            Welcome to the 403 Bypass Practice Lab! This lab demonstrates various techniques 
            used in bug bounty hunting to bypass 403 Forbidden errors.
        </p>

        <div class="challenge">
            <h2>Challenge 1: HTTP Verb/Method Bypass</h2>
            <p>The endpoint <code>/admin/secret</code> returns 403 with GET requests, but try different HTTP methods!</p>
            <div class="endpoint">GET /admin/secret → 403 Forbidden</div>
            <button class="show-hint-btn" onclick="toggleHint(this)">💡 Show Hint</button>
            <div class="hint" id="hint-1">
                <strong>💡 Hint:</strong> Try using HEAD, POST, PUT, DELETE, or even made-up HTTP methods!
            </div>
        </div>

        <div class="challenge">
            <h2>Challenge 2: HTTP Header Bypass</h2>
            <p>The endpoint <code>/internal/data</code> is protected, but it might trust certain headers.</p>
            <div class="endpoint">GET /internal/data → 403 Forbidden</div>
            <button class="show-hint-btn" onclick="toggleHint(this)">💡 Show Hint</button>
            <div class="hint" id="hint-2">
                <strong>💡 Hint:</strong> Try adding headers like X-Forwarded-For, X-Original-URL, or X-Rewrite-URL with localhost or 127.0.0.1
            </div>
        </div>

        <div class="challenge">
            <h2>Challenge 3: Path Encoding Bypass</h2>
            <p>The path <code>/protected/files</code> is blocked, but URL encoding might help!</p>
            <div class="endpoint">GET /protected/files → 403 Forbidden</div>
            <button class="show-hint-btn" onclick="toggleHint(this)">💡 Show Hint</button>
            <div class="hint" id="hint-3">
                <strong>💡 Hint:</strong> Try URL encoding parts of the path, like <code>%2e</code> for dots, or double encoding!
            </div>
        </div>

        <div class="challenge">
            <h2>Challenge 4: Path Case Bypass</h2>
            <p>The path <code>/sensitive/info</code> is case-sensitive in the protection logic.</p>
            <div class="endpoint">GET /sensitive/info → 403 Forbidden</div>
            <button class="show-hint-btn" onclick="toggleHint(this)">💡 Show Hint</button>
            <div class="hint" id="hint-4">
                <strong>💡 Hint:</strong> Try changing the case of some letters in the path!
            </div>
        </div>

        <div class="challenge">
            <h2>Challenge 5: Path Slash Bypass</h2>
            <p>The path <code>/restricted/area</code> is blocked, but adding slashes might bypass it.</p>
            <div class="endpoint">GET /restricted/area → 403 Forbidden</div>
            <button class="show-hint-btn" onclick="toggleHint(this)">💡 Show Hint</button>
            <div class="hint" id="hint-5">
                <strong>💡 Hint:</strong> Try adding extra slashes, dots, or semicolons to the path!
            </div>
        </div>

        <div class="challenge">
            <h2>Challenge 6: Parameter Pollution</h2>
            <p>The endpoint <code>/api/user</code> checks parameters, but duplicate parameters might confuse it.</p>
            <div class="endpoint">GET /api/user?id=123 → 403 Forbidden</div>
            <button class="show-hint-btn" onclick="toggleHint(this)">💡 Show Hint</button>
            <div class="hint" id="hint-6">
                <strong>💡 Hint:</strong> Try sending duplicate parameters or changing parameter values!
            </div>
        </div>

        <div class="challenge">
            <h2>Challenge 7: Host Header Bypass</h2>
            <p>The endpoint <code>/local/admin</code> only allows localhost access.</p>
            <div class="endpoint">GET /local/admin → 403 Forbidden</div>
            <button class="show-hint-btn" onclick="toggleHint(this)">💡 Show Hint</button>
            <div class="hint" id="hint-7">
                <strong>💡 Hint:</strong> Try changing the Host header to localhost or 127.0.0.1!
            </div>
        </div>

        <div class="challenge">
            <h2>Challenge 8: Method Override Bypass</h2>
            <p>The endpoint <code>/api/update</code> blocks PUT requests, but there's a way to override the method.</p>
            <div class="endpoint">PUT /api/update → 403 Forbidden</div>
            <button class="show-hint-btn" onclick="toggleHint(this)">💡 Show Hint</button>
            <div class="hint" id="hint-8">
                <strong>💡 Hint:</strong> Try using X-HTTP-Method-Override header with a POST request!
            </div>
        </div>

        <div class="resources-box">
            <h3>📚 Learning Resources</h3>
            <p>Check out the <a href="https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-web/403-and-401-bypasses.html" target="_blank">HackTricks 403 Bypass Guide</a> for more techniques!</p>
        </div>
    </div>
    
    <script>
        function toggleHint(button) {
            const hint = button.nextElementSibling;
            if (hint.classList.contains('show')) {
                hint.classList.remove('show');
                button.textContent = '💡 Show Hint';
            } else {
                hint.classList.add('show');
                button.textContent = '🙈 Hide Hint';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page with challenge descriptions"""
    return render_template_string(MAIN_PAGE)

@app.route('/admin/secret', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'TRACE'])
def verb_bypass():
    """
    Challenge 1: HTTP Verb Bypass
    GET returns 403, but other methods might work
    """
    if request.method == 'GET':
        return jsonify({
            'error': '403 Forbidden',
            'message': 'GET method is not allowed on this endpoint',
            'hint': 'Try using a different HTTP method!'
        }), 403
    
    # Any other HTTP method bypasses the protection
    return jsonify({
        'success': True,
        'message': 'Congratulations! You bypassed the 403 using HTTP verb manipulation!',
        'flag': FLAGS['verb_bypass'],
        'technique': f'Used {request.method} method instead of GET'
    }), 200

@app.route('/internal/data')
def header_bypass():
    """
    Challenge 2: HTTP Header Bypass
    Checks for X-Forwarded-For, X-Original-URL, or X-Rewrite-URL headers
    """
    # Check for bypass headers
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    original_url = request.headers.get('X-Original-URL', '')
    rewrite_url = request.headers.get('X-Rewrite-URL', '')
    remote_ip = request.headers.get('X-Remote-IP', '')
    client_ip = request.headers.get('Client-IP', '')
    
    # Check if any header contains localhost or 127.0.0.1
    bypass_headers = [forwarded_for, original_url, rewrite_url, remote_ip, client_ip]
    if any('127.0.0.1' in h or 'localhost' in h.lower() for h in bypass_headers):
        return jsonify({
            'success': True,
            'message': 'Congratulations! You bypassed the 403 using HTTP headers!',
            'flag': FLAGS['header_bypass'],
            'technique': 'Used X-Forwarded-For or similar header with localhost/127.0.0.1'
        }), 200
    
    return jsonify({
        'error': '403 Forbidden',
        'message': 'This endpoint is restricted to internal access only',
        'hint': 'Try adding headers that indicate you are accessing from localhost'
    }), 403

@app.route('/protected/files')
@app.route('/protected/<path:subpath>')
def path_encoding_bypass(subpath=None):
    """
    Challenge 3: Path Encoding Bypass
    The protection checks for exact path match, but URL encoding can bypass it
    """
    # Get the raw URI from WSGI environment (before Flask decodes it)
    raw_uri = request.environ.get('REQUEST_URI', '')
    if not raw_uri:
        # Try PATH_INFO which might preserve encoding
        raw_uri = request.environ.get('PATH_INFO', request.path)
        # If still not found, construct from request
        if raw_uri == request.path:
            # Check if we have the encoded version in the URL
            full_url = str(request.url)
            if request.host in full_url:
                raw_uri = full_url.split(request.host, 1)[1].split('?')[0]
            else:
                raw_uri = request.path
    
    # Check the raw path for encoded characters (before Flask decodes)
    raw_path = raw_uri.split('?')[0]  # Remove query string
    
    # Check if path contains encoded characters that bypass the check
    raw_path_lower = raw_path.lower()
    if '%2e' in raw_path_lower or '%252e' in raw_path_lower or '%2f' in raw_path_lower or '%252f' in raw_path_lower:
        return jsonify({
            'success': True,
            'message': 'Congratulations! You bypassed the 403 using path encoding!',
            'flag': FLAGS['path_bypass1'],
            'technique': 'Used URL encoding to bypass path protection'
        }), 200
    
    # Check if subpath was provided (means it matched the catch-all route)
    if subpath is not None:
        # If subpath exists and contains 'files', it's likely an encoding bypass
        if 'files' in subpath.lower() or 'files' in unquote(subpath).lower():
            return jsonify({
                'success': True,
                'message': 'Congratulations! You bypassed the 403 using path encoding!',
                'flag': FLAGS['path_bypass1'],
                'technique': 'Used URL encoding to bypass path protection'
            }), 200
    
    return jsonify({
        'error': '403 Forbidden',
        'message': 'Access to protected files is restricted',
        'hint': 'Try URL encoding parts of the path (like %2e for dots)'
    }), 403

@app.route('/sensitive/info', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
def path_case_bypass_exact():
    """
    Challenge 4: Path Case Bypass - Exact lowercase route
    """
    # Get the raw path from WSGI environment
    raw_uri = request.environ.get('REQUEST_URI', '')
    if not raw_uri:
        raw_uri = request.environ.get('PATH_INFO', request.path)
    
    raw_path = raw_uri.split('?')[0]
    
    # If accessed with exact lowercase, return 403
    if raw_path == '/sensitive/info':
        return jsonify({
            'error': '403 Forbidden',
            'message': 'Sensitive information is protected',
            'hint': 'The protection might be case-sensitive, but the server might not be!'
        }), 403
    
    # Should not reach here if route matched
    return jsonify({'error': '404 Not Found'}), 404

@app.route('/<path:path1>/<path:path2>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
def path_case_bypass(path1=None, path2=None):
    """
    Challenge 4: Path Case Bypass - Catch-all for case variations
    """
    # Check if this is a case variation of sensitive/info
    if path1 and path2:
        path1_lower = path1.lower()
        path2_lower = path2.lower()
        
        if path1_lower == 'sensitive' and path2_lower == 'info':
            # If it's not the exact lowercase, it's a bypass
            if path1 != 'sensitive' or path2 != 'info':
                return jsonify({
                    'success': True,
                    'message': 'Congratulations! You bypassed the 403 using case manipulation!',
                    'flag': FLAGS['path_bypass2'],
                    'technique': 'Changed case of path characters to bypass protection'
                }), 200
    
    # For other paths, return 404
    return jsonify({'error': '404 Not Found'}), 404

@app.route('/restricted/area')
def path_slash_bypass():
    """
    Challenge 5: Path Slash Bypass
    Adding extra slashes, dots, or semicolons can bypass path protection
    """
    path = request.path
    
    # Check for bypass patterns
    if '//' in path or '/./' in path or '/;' in path or path.endswith('/') or path.endswith('/.'):
        return jsonify({
            'success': True,
            'message': 'Congratulations! You bypassed the 403 using path manipulation!',
            'flag': FLAGS['path_bypass3'],
            'technique': 'Used extra slashes, dots, or semicolons to bypass path protection'
        }), 200
    
    return jsonify({
        'error': '403 Forbidden',
        'message': 'Restricted area access denied',
        'hint': 'Try adding extra slashes, dots, or semicolons to the path!'
    }), 403

@app.route('/api/user')
def parameter_bypass():
    """
    Challenge 6: Parameter Pollution
    Duplicate parameters or parameter manipulation can bypass checks
    """
    # Check for duplicate parameters (parameter pollution)
    ids = request.args.getlist('id')
    
    if len(ids) > 1:
        # Parameter pollution detected
        return jsonify({
            'success': True,
            'message': 'Congratulations! You bypassed the 403 using parameter pollution!',
            'flag': FLAGS['parameter_bypass'],
            'technique': 'Used duplicate parameters to confuse the protection logic'
        }), 200
    
    # Check if id parameter is modified
    user_id = request.args.get('id')
    if user_id and user_id != '123':
        # Try with admin parameter
        if request.args.get('isAdmin') == 'true':
            return jsonify({
                'success': True,
                'message': 'Congratulations! You bypassed the 403 using parameter manipulation!',
                'flag': FLAGS['parameter_bypass'],
                'technique': 'Modified parameters to bypass protection'
            }), 200
    
    return jsonify({
        'error': '403 Forbidden',
        'message': 'User access denied',
        'hint': 'Try sending duplicate parameters or modifying parameter values!'
    }), 403

@app.route('/local/admin')
def host_bypass():
    """
    Challenge 7: Host Header Bypass
    Only allows access when Host header is localhost
    """
    host = request.headers.get('Host', '')
    
    if 'localhost' in host.lower() or '127.0.0.1' in host or host == '':
        return jsonify({
            'success': True,
            'message': 'Congratulations! You bypassed the 403 using Host header manipulation!',
            'flag': FLAGS['host_bypass'],
            'technique': 'Changed Host header to localhost or removed it'
        }), 200
    
    return jsonify({
        'error': '403 Forbidden',
        'message': 'This endpoint is only accessible from localhost',
        'hint': 'Try changing the Host header to localhost or 127.0.0.1!'
    }), 403

@app.route('/api/update', methods=['GET', 'POST', 'PUT', 'DELETE'])
def method_override_bypass():
    """
    Challenge 8: Method Override Bypass
    PUT is blocked, but X-HTTP-Method-Override can be used
    """
    # Check for method override header
    method_override = request.headers.get('X-HTTP-Method-Override', '')
    
    if request.method == 'POST' and method_override.upper() == 'PUT':
        return jsonify({
            'success': True,
            'message': 'Congratulations! You bypassed the 403 using method override!',
            'flag': FLAGS['method_override'],
            'technique': 'Used X-HTTP-Method-Override header to bypass method restriction'
        }), 200
    
    if request.method == 'PUT':
        return jsonify({
            'error': '403 Forbidden',
            'message': 'PUT method is not allowed',
            'hint': 'Try using POST with X-HTTP-Method-Override header!'
        }), 403
    
    return jsonify({
        'error': '403 Forbidden',
        'message': 'This endpoint requires PUT method',
        'hint': 'PUT is blocked, but try using X-HTTP-Method-Override header with POST!'
    }), 403

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║        403 Bypass Practice Lab - Starting Server        ║
    ╚══════════════════════════════════════════════════════════╝
    
    🌐 Server running at: http://localhost:5000
    📚 Main page: http://localhost:5000/
    
    Challenges:
    1. HTTP Verb Bypass: /admin/secret
    2. Header Bypass: /internal/data
    3. Path Encoding: /protected/files
    4. Path Case: /sensitive/info
    5. Path Slash: /restricted/area
    6. Parameter Pollution: /api/user
    7. Host Header: /local/admin
    8. Method Override: /api/update
    
    Press Ctrl+C to stop the server
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)

