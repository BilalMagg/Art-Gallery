document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const configSection = document.getElementById('configSection');
    const vizType = document.getElementById('vizType');
    const vizControls = document.getElementById('vizControls');
    const visualization = document.getElementById('visualization');
    const plotOutput = document.getElementById('plotOutput');
    
    // Control sections
    const globeControls = document.getElementById('globeControls');
    const scatter3dControls = document.getElementById('scatter3dControls');
    const basic2DControls = document.getElementById('basic2DControls');
    const singleVarControls = document.getElementById('singleVarControls');
    
    let currentFilename = '';
    let columnData = {
        all: [],
        numeric: [],
        categorical: [],
        date: [],
        location: []
    };

    // Hide all control sections initially
    hideAllControls();

    fileInput.addEventListener('change', async function(e) {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/visualization/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            if (data.error) {
                alert(data.error);
                return;
            }

            currentFilename = data.filename;
            columnData = {
                all: data.columns,
                numeric: data.numeric_columns,
                categorical: data.categorical_columns,
                date: data.date_columns,
                location: data.location_columns
            };

            configSection.classList.remove('hidden');
            vizType.value = ''; // Reset visualization type
            hideAllControls();

        } catch (error) {
            console.error('Error:', error);
            alert('Error uploading file');
        }
    });

    vizType.addEventListener('change', function() {
        // First hide all controls
        hideAllControls();
        
        // Then show only the relevant controls for the selected visualization type
        switch(this.value) {
            case 'globe':
                showOnlyControl(globeControls);
                populateSelect('#locationColumn', columnData.location);
                populateSelect('#valueColumn', columnData.numeric);
                break;
                
            case 'scatter3d':
                showOnlyControl(scatter3dControls);
                populateSelect('#xColumn', columnData.numeric);
                populateSelect('#yColumn', columnData.numeric);
                populateSelect('#zColumn', columnData.numeric);
                break;
                
            case 'bar':
            case 'line':
                showOnlyControl(basic2DControls);
                populateSelect('#xAxis', columnData.all);
                populateSelect('#yAxis', columnData.numeric);
                populateSelect('#colorBy', [''].concat(columnData.categorical));
                break;
                
            case 'box':
                showOnlyControl(basic2DControls);
                populateSelect('#xAxis', columnData.categorical);
                populateSelect('#yAxis', columnData.numeric);
                break;
                
            case 'histogram':
                showOnlyControl(singleVarControls);
                populateSelect('#dataColumn', columnData.numeric);
                break;
                
            case 'heatmap':
                showOnlyControl(basic2DControls);
                populateSelect('#xAxis', columnData.categorical);
                populateSelect('#yAxis', columnData.categorical);
                populateSelect('#colorBy', columnData.numeric);
                break;
        }
    });

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const vizData = {
            filename: currentFilename,
            viz_type: vizType.value
        };

        // Add visualization-specific parameters
        switch(vizType.value) {
            case 'globe':
                vizData.location_column = document.getElementById('locationColumn').value;
                vizData.value_column = document.getElementById('valueColumn').value;
                break;
                
            case 'scatter3d':
                vizData.x_column = document.getElementById('xColumn').value;
                vizData.y_column = document.getElementById('yColumn').value;
                vizData.z_column = document.getElementById('zColumn').value;
                break;
                
            case 'bar':
            case 'line':
                vizData.x_column = document.getElementById('xAxis').value;
                vizData.y_column = document.getElementById('yAxis').value;
                const colorBy = document.getElementById('colorBy').value;
                if (colorBy) vizData.color_column = colorBy;
                break;
                
            case 'box':
                vizData.category_column = document.getElementById('xAxis').value;
                vizData.value_column = document.getElementById('yAxis').value;
                break;
                
            case 'histogram':
                vizData.value_column = document.getElementById('dataColumn').value;
                break;
                
            case 'heatmap':
                vizData.x_column = document.getElementById('xAxis').value;
                vizData.y_column = document.getElementById('yAxis').value;
                vizData.value_column = document.getElementById('colorBy').value;
                break;
        }

        try {
            const response = await fetch('/visualization/visualize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(vizData)
            });

            const data = await response.json();
            if (data.error) {
                alert(data.error);
                return;
            }

            visualization.classList.remove('hidden');
            const plotData = JSON.parse(data.plot);
            Plotly.newPlot('plotOutput', plotData.data, plotData.layout, {
                responsive: true,
                displayModeBar: true,
                displaylogo: false
            });

        } catch (error) {
            console.error('Error:', error);
            alert('Error generating visualization');
        }
    });

    function hideAllControls() {
        vizControls.classList.add('hidden');
        [globeControls, scatter3dControls, basic2DControls, singleVarControls].forEach(control => {
            if (control) control.classList.add('hidden');
        });
    }

    function showOnlyControl(controlToShow) {
        // First hide all controls
        hideAllControls();
        // Then show the vizControls container and the specified control
        vizControls.classList.remove('hidden');
        if (controlToShow) controlToShow.classList.remove('hidden');
    }

    function populateSelect(selector, options) {
        const select = document.querySelector(selector);
        if (!select) return; // Guard clause for when element doesn't exist
        
        select.innerHTML = '<option value="">Select option</option>';
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            select.appendChild(optionElement);
        });
    }
});