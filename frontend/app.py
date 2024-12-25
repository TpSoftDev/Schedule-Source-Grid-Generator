#------------------------------------------------------------------------ Imports ------------------------------------------------------------------------#    
from flask import Flask, render_template, request, jsonify, send_file
import sys
from pathlib import Path
import os
import io
import tempfile

#------------------------------------------------------------------------ Paths ------------------------------------------------------------------------#    
# Set up path to access backend code
# This allows us to import modules from the backend directory
root_dir = Path(__file__).resolve().parents[1]
backend_dir = root_dir / 'backend' / 'app'
sys.path.append(str(backend_dir))

# Import the existing grid generator functions from your backend
from controllers.grid.grid_generator import load_workbook, clear_grid, fill_in_schedule, GRID_FILE_NAME, GRID_FILL_COLOR
from controllers.grid.helper_classes.availability_parser import parse_availability

#------------------------------------------------------------------------ Flask App ------------------------------------------------------------------------#    
# Initialize Flask application
app = Flask(__name__)

# Add this after your imports
# Dictionary to store temporary grid data
temp_grids = {}

#------------------------------------------------------------------------ Index Route ------------------------------------------------------------------------#    
# Route for the main page
@app.route('/')
def index():
    """Serves the main HTML page"""
    return render_template('index.html')

#------------------------------------------------------------------------ Generate Grid ------------------------------------------------------------------------#    
# Route that handles grid generation requests
@app.route('/generate', methods=['POST'])
def generate_grid():
    """
    Handles POST requests to generate grid schedules
    
    Expected JSON input:
    {
        "external_id": "employee_id_here"
    }
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()
        external_id = data.get('external_id')
        
        # Validate that we received an ID
        if not external_id:
            return jsonify({'error': 'Employee ID is required'}), 400
            
        try:
            # Load the Excel template
            wb = load_workbook(GRID_FILE_NAME)
            ws = wb.active
            clear_grid(ws)
            
            # Try to fill in the schedule
            # Reference to grid_generator.py (lines 210-241)
            avail = parse_availability(external_id)
            
            if not avail:
                return jsonify({
                    'error': 'No schedule available for this ID'
                }), 404
            
            # Generate new schedule using the employee ID
            fill_in_schedule(ws, external_id, GRID_FILL_COLOR)
            
            # Save to bytes buffer instead of file
            buffer = io.BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            
            # Store in memory
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

#------------------------------------------------------------------------ Download File ------------------------------------------------------------------------#    
# Route that handles file downloads
@app.route('/download/<external_id>')
def download_file(external_id):
    """
    Handles file downloads
    Args:
        external_id: ID of the schedule to download
    Returns:
        File download response or error
    """
    try:
        if external_id not in temp_grids:
            return jsonify({'error': 'Grid not found'}), 404
            
        buffer = temp_grids[external_id]
        buffer.seek(0)
        
        # Get custom filename from query parameters or use default
        filename = request.args.get('filename', f'schedule_{external_id}.xlsx')
        
        return send_file(
            buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#------------------------------------------------------------------------ Run App ------------------------------------------------------------------------#    
# Run the application if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)  # debug=True enables development features

#   User Input → JavaScript → Flask Backend → Grid Generator → Flask → JavaScript → User Display