#!/usr/bin/env python3
"""
Serena Dashboard - Web interface for monitoring and managing Serena agents
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

try:
    from serena.util.logging import MemoryLogHandler
    from serena import serena_version
except ImportError:
    # Fallback if serena is not installed
    class MemoryLogHandler:
        def __init__(self):
            self.logs = []
        
        def get_logs(self):
            return self.logs
    
    def serena_version():
        return "0.1.4"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__, 
           template_folder='dashboard/templates',
           static_folder='dashboard/static')
CORS(app)

# Global memory log handler
memory_handler = MemoryLogHandler()
logging.getLogger().addHandler(memory_handler)

# Sample data for demonstration
SAMPLE_AGENTS = [
    {
        "id": "agent-1",
        "name": "Main Agent",
        "status": "active",
        "project": "/path/to/project",
        "context": "default",
        "modes": ["interactive", "editing"],
        "created_at": "2025-01-16T10:00:00Z",
        "last_activity": "2025-01-16T14:30:00Z"
    },
    {
        "id": "agent-2",
        "name": "Background Agent",
        "status": "idle",
        "project": "/path/to/another/project",
        "context": "minimal",
        "modes": ["monitoring"],
        "created_at": "2025-01-16T09:00:00Z",
        "last_activity": "2025-01-16T12:15:00Z"
    }
]

SAMPLE_PROJECTS = [
    {
        "id": "proj-1",
        "name": "Serena Core",
        "path": "/path/to/serena",
        "language": "Python",
        "status": "active",
        "agents_count": 2,
        "last_modified": "2025-01-16T14:30:00Z"
    },
    {
        "id": "proj-2",
        "name": "Web Dashboard",
        "path": "/path/to/dashboard",
        "language": "JavaScript",
        "status": "idle",
        "agents_count": 0,
        "last_modified": "2025-01-16T12:00:00Z"
    }
]


@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')


@app.route('/dashboard/')
def dashboard():
    """Dashboard page."""
    return render_template('dashboard.html')


@app.route('/api/status')
def api_status():
    """Get system status."""
    return jsonify({
        "status": "running",
        "version": serena_version(),
        "timestamp": datetime.now().isoformat(),
        "agents_count": len(SAMPLE_AGENTS),
        "projects_count": len(SAMPLE_PROJECTS)
    })


@app.route('/api/agents')
def api_agents():
    """Get list of agents."""
    return jsonify({
        "agents": SAMPLE_AGENTS,
        "total": len(SAMPLE_AGENTS)
    })


@app.route('/api/projects')
def api_projects():
    """Get list of projects."""
    return jsonify({
        "projects": SAMPLE_PROJECTS,
        "total": len(SAMPLE_PROJECTS)
    })


@app.route('/api/logs')
def api_logs():
    """Get recent logs."""
    try:
        logs = memory_handler.get_logs()
        
        # Add some sample logs if none exist
        if not logs:
            sample_logs = [
                {
                    "timestamp": datetime.now().isoformat(),
                    "level": "INFO",
                    "logger": "serena.dashboard",
                    "message": "Dashboard started successfully"
                },
                {
                    "timestamp": datetime.now().isoformat(),
                    "level": "INFO",
                    "logger": "serena.agent",
                    "message": "Agent initialized with default configuration"
                },
                {
                    "timestamp": datetime.now().isoformat(),
                    "level": "DEBUG",
                    "logger": "serena.mcp",
                    "message": "MCP server ready to accept connections"
                }
            ]
            logs = sample_logs
        
        return jsonify({
            "logs": logs[-100:],  # Return last 100 logs
            "total": len(logs)
        })
    except Exception as e:
        logger.error(f"Error fetching logs: {e}")
        return jsonify({
            "error": "Failed to fetch logs",
            "message": str(e)
        }), 500


@app.route('/api/metrics')
def api_metrics():
    """Get system metrics."""
    return jsonify({
        "cpu_usage": 25.5,
        "memory_usage": 45.2,
        "disk_usage": 60.1,
        "network_io": {
            "bytes_sent": 1024000,
            "bytes_recv": 2048000
        },
        "uptime": "2h 30m",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files."""
    return send_from_directory('dashboard/static', filename)


if __name__ == '__main__':
    # Ensure dashboard directories exist
    dashboard_dir = Path('dashboard')
    templates_dir = dashboard_dir / 'templates'
    static_dir = dashboard_dir / 'static'
    
    templates_dir.mkdir(parents=True, exist_ok=True)
    static_dir.mkdir(parents=True, exist_ok=True)
    
    # Create basic templates if they don't exist
    index_template = templates_dir / 'index.html'
    if not index_template.exists():
        with open(index_template, 'w') as f:
            f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Serena Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background: #0056b3; }
        .status { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .status.active { background: #d4edda; color: #155724; }
        .status.idle { background: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Serena Dashboard</h1>
            <p>AI-powered coding agent toolkit</p>
        </div>
        
        <div class="card">
            <h2>Quick Actions</h2>
            <a href="/dashboard/" class="btn">Open Dashboard</a>
            <a href="/api/status" class="btn">API Status</a>
        </div>
        
        <div class="card">
            <h2>System Status</h2>
            <div id="status-info">Loading...</div>
        </div>
    </div>
    
    <script>
        // Load system status
        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                document.getElementById('status-info').innerHTML = `
                    <p><strong>Status:</strong> <span class="status active">${data.status}</span></p>
                    <p><strong>Version:</strong> ${data.version}</p>
                    <p><strong>Agents:</strong> ${data.agents_count}</p>
                    <p><strong>Projects:</strong> ${data.projects_count}</p>
                    <p><strong>Last Updated:</strong> ${new Date(data.timestamp).toLocaleString()}</p>
                `;
            })
            .catch(error => {
                document.getElementById('status-info').innerHTML = '<p style="color: red;">Error loading status</p>';
            });
    </script>
</body>
</html>
            ''')
    
    dashboard_template = templates_dir / 'dashboard.html'
    if not dashboard_template.exists():
        with open(dashboard_template, 'w') as f:
            f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Serena Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8f9fa; }
        .header { background: white; border-bottom: 1px solid #dee2e6; padding: 1rem 2rem; }
        .header h1 { color: #495057; font-size: 1.5rem; }
        .main { padding: 2rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
        .card { background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h2 { color: #495057; margin-bottom: 1rem; font-size: 1.25rem; }
        .status { padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
        .status.active { background: #d4edda; color: #155724; }
        .status.idle { background: #fff3cd; color: #856404; }
        .logs { max-height: 400px; overflow-y: auto; font-family: monospace; font-size: 0.875rem; }
        .log-entry { padding: 0.5rem; border-bottom: 1px solid #f1f3f4; }
        .log-entry:last-child { border-bottom: none; }
        .log-level { font-weight: bold; margin-right: 0.5rem; }
        .log-level.INFO { color: #007bff; }
        .log-level.ERROR { color: #dc3545; }
        .log-level.DEBUG { color: #6c757d; }
        .refresh-btn { background: #007bff; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; }
        .refresh-btn:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Serena Dashboard</h1>
    </div>
    
    <div class="main">
        <div class="grid">
            <div class="card">
                <h2>System Status</h2>
                <div id="system-status">Loading...</div>
            </div>
            
            <div class="card">
                <h2>Active Agents</h2>
                <div id="agents-list">Loading...</div>
            </div>
            
            <div class="card">
                <h2>Projects</h2>
                <div id="projects-list">Loading...</div>
            </div>
            
            <div class="card">
                <h2>Recent Logs <button class="refresh-btn" onclick="loadLogs()">Refresh</button></h2>
                <div id="logs-container" class="logs">Loading...</div>
            </div>
        </div>
    </div>
    
    <script src="/static/dashboard.js"></script>
</body>
</html>
            ''')
    
    # Create dashboard.js
    js_file = static_dir / 'dashboard.js'
    if not js_file.exists():
        with open(js_file, 'w') as f:
            f.write('''
// Dashboard JavaScript
console.log('Dashboard JavaScript loaded');

// Load system status
function loadSystemStatus() {
    console.log('Loading system status...');
    fetch('/api/status')
        .then(response => {
            console.log('Status response:', response);
            return response.json();
        })
        .then(data => {
            console.log('Status data:', data);
            document.getElementById('system-status').innerHTML = `
                <p><strong>Status:</strong> <span class="status active">${data.status}</span></p>
                <p><strong>Version:</strong> ${data.version}</p>
                <p><strong>Agents:</strong> ${data.agents_count}</p>
                <p><strong>Projects:</strong> ${data.projects_count}</p>
                <p><strong>Last Updated:</strong> ${new Date(data.timestamp).toLocaleString()}</p>
            `;
        })
        .catch(error => {
            console.error('Error loading system status:', error);
            document.getElementById('system-status').innerHTML = '<p style="color: red;">Error loading status</p>';
        });
}

// Load agents
function loadAgents() {
    console.log('Loading agents...');
    fetch('/api/agents')
        .then(response => response.json())
        .then(data => {
            console.log('Agents data:', data);
            const agentsList = data.agents.map(agent => `
                <div style="margin-bottom: 1rem; padding: 0.75rem; border: 1px solid #dee2e6; border-radius: 4px;">
                    <strong>${agent.name}</strong>
                    <span class="status ${agent.status}">${agent.status}</span>
                    <br><small>Project: ${agent.project}</small>
                    <br><small>Modes: ${agent.modes.join(', ')}</small>
                </div>
            `).join('');
            document.getElementById('agents-list').innerHTML = agentsList || '<p>No agents found</p>';
        })
        .catch(error => {
            console.error('Error loading agents:', error);
            document.getElementById('agents-list').innerHTML = '<p style="color: red;">Error loading agents</p>';
        });
}

// Load projects
function loadProjects() {
    console.log('Loading projects...');
    fetch('/api/projects')
        .then(response => response.json())
        .then(data => {
            console.log('Projects data:', data);
            const projectsList = data.projects.map(project => `
                <div style="margin-bottom: 1rem; padding: 0.75rem; border: 1px solid #dee2e6; border-radius: 4px;">
                    <strong>${project.name}</strong>
                    <span class="status ${project.status}">${project.status}</span>
                    <br><small>Language: ${project.language}</small>
                    <br><small>Agents: ${project.agents_count}</small>
                </div>
            `).join('');
            document.getElementById('projects-list').innerHTML = projectsList || '<p>No projects found</p>';
        })
        .catch(error => {
            console.error('Error loading projects:', error);
            document.getElementById('projects-list').innerHTML = '<p style="color: red;">Error loading projects</p>';
        });
}

// Load logs
function loadLogs() {
    console.log('Loading logs...');
    fetch('/api/logs')
        .then(response => {
            console.log('Logs response:', response);
            return response.json();
        })
        .then(data => {
            console.log('Logs data:', data);
            if (data.error) {
                document.getElementById('logs-container').innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
                return;
            }
            
            const logEntries = data.logs.map(log => `
                <div class="log-entry">
                    <span class="log-level ${log.level}">${log.level}</span>
                    <span style="color: #6c757d;">${new Date(log.timestamp).toLocaleTimeString()}</span>
                    <span style="color: #495057;">${log.logger}</span>
                    <br>
                    <span>${log.message}</span>
                </div>
            `).join('');
            
            document.getElementById('logs-container').innerHTML = logEntries || '<p>No logs available</p>';
        })
        .catch(error => {
            console.error('Error loading logs:', error);
            document.getElementById('logs-container').innerHTML = '<p style="color: red;">Error loading logs</p>';
        });
}

// Initialize dashboard
function initDashboard() {
    console.log('Initializing dashboard...');
    loadSystemStatus();
    loadAgents();
    loadProjects();
    loadLogs();
    
    // Set up periodic refresh
    setInterval(() => {
        loadSystemStatus();
        loadAgents();
        loadProjects();
    }, 30000); // Refresh every 30 seconds
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initDashboard);

// Handle errors
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
});
            ''')
    
    print(f"Starting Serena Dashboard on http://localhost:24287")
    print(f"Dashboard interface: http://localhost:24287/dashboard/")
    
    try:
        app.run(host='0.0.0.0', port=24287, debug=True)
    except Exception as e:
        logger.error(f"Failed to start dashboard: {e}")
        sys.exit(1)