#------------------------------------------------------- Imports ------------------------------------------------------#     
# Core Flask imports for web application functionality
from flask import Flask, render_template, request, jsonify, send_file
# System and file handling imports
import sys
from pathlib import Path
import os
import io
import tempfile

#------------------------------------------------------- Paths ------------------------------------------------------#   
# Configure system paths to access backend code
# This setup enables importing modules from the backend directory structure
root_dir = Path(__file__).resolve().parents[1]      # Get project root directory
backend_dir = root_dir / 'backend' / 'app'          # Path to backend code
sys.path.append(str(backend_dir))                   # Add backend to Python path

# Import backend functionality for grid generation
from controllers.grid.grid_generator import load_workbook, clear_grid, fill_in_schedule, GRID_FILE_NAME, GRID_FILL_COLOR
from controllers.grid.helper_classes.availability_parser import parse_availability

#------------------------------------------------------- Flask App ------------------------------------------------------#    
# Initialize Flask application instance
app = Flask(__name__)

# In-memory storage for temporary grid data
# Keys are employee IDs, values are file buffers containing Excel data
temp_grids = {}

#------------------------------------------------------- Index Route ------------------------------------------------------#  
@app.route('/')
def index():
    """
    Serves the main HTML page
    Returns:
        Rendered index.html template with the main application interface
    """
    return render_template('index.html')

#------------------------------------------------------- Generate Grid ------------------------------------------------------#     
@app.route('/generate', methods=['POST'])
def generate_grid():
    """
    Handles POST requests to generate grid schedules
    
    Expected JSON input:
    {
        "external_id": "employee_id_here"
    }
    
    Returns:
        JSON response with success/error status and relevant messages
    """
    try:
        # Extract and validate request data
        data = request.get_json()
        external_id = data.get('external_id')
        
        if not external_id:
            return jsonify({'error': 'Employee ID is required'}), 400
            
        try:
            # Initialize Excel workbook and prepare grid
            wb = load_workbook(GRID_FILE_NAME)
            ws = wb.active
            clear_grid(ws)
            
            # Attempt to retrieve and validate employee availability
            avail = parse_availability(external_id)
            
            if not avail:
                return jsonify({
                    'error': 'No schedule available for this ID'
                }), 404
            
            # Generate schedule and store in memory buffer
            fill_in_schedule(ws, external_id, GRID_FILL_COLOR)
            buffer = io.BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            
            # Cache generated schedule for later download
            temp_grids[external_id] = buffer
            
            return jsonify({
                'success': True,
                'message': f'Schedule generated for ID: {external_id}',
                'external_id': external_id
            })
            
        except Exception as e:
            return jsonify({'error': f'Grid generation failed: {str(e)}'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#------------------------------------------------------- Download File ------------------------------------------------------#  
@app.route('/download/<external_id>')
def download_file(external_id):
    """
    Handles file downloads for generated schedules
    
    Args:
        external_id: ID of the schedule to download
        
    Returns:
        Excel file download response or error message
    """
    try:
        # Verify schedule exists in temporary storage
        if external_id not in temp_grids:
            return jsonify({'error': 'Grid not found'}), 404
            
        buffer = temp_grids[external_id]
        buffer.seek(0)
        
        # Get custom filename or use default format
        filename = request.args.get('filename', f'schedule_{external_id}.xlsx')
        
        # Send file as downloadable attachment
        return send_file(
            buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#------------------------------------------------------- Run App ------------------------------------------------------#  
if __name__ == '__main__':
    app.run(debug=True)  # Enable development features when running directly

#   User Input → JavaScript → Flask Backend → Grid Generator → Flask → JavaScript → User Display