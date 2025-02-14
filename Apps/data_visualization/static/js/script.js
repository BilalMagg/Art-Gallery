document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const uploadForm = document.getElementById('uploadForm');
    const dataSource = document.getElementById('dataSource');
    const uploadSection = document.getElementById('uploadSection');
    const presetControls = document.getElementById('presetControls');
    const configSection = document.getElementById('configSection');
    const customControls = document.getElementById('customControls');
    const presetVizControls = document.getElementById('presetVizControls');
    const visualization = document.getElementById('visualization');
    const plotOutput = document.getElementById('plotOutput');
    
    // Select elements
    const fileInput = document.getElementById('fileInput');
    const yearSelect = document.getElementById('yearSelect');
    const vizType = document.getElementById('vizType');
    const metricSelect = document.getElementById('metricSelect');
    
    // Visualization options
    const presetVizOptions = [
        { value: 'globe', label: '3D Globe View', group: 'Geographical' },
        { value: 'bar', label: 'Top 10 Countries', group: 'Comparisons' },
        { value: 'scatter', label: 'Internet vs. Cellular Usage', group: 'Comparisons' },
        { value: 'line', label: 'Usage Trends Over Time', group: 'Time Series' }
    ];

    const customVizOptions = [
        { value: 'bar', label: 'Bar Chart', group: 'Basic' },
        { value: 'line', label: 'Line Chart', group: 'Basic' },
        { value: 'scatter', label: 'Scatter Plot', group: 'Basic' }
    ];

    // Data source change handler
    dataSource.addEventListener('change', async function() {
        resetForm();
        console.log("source")
        if (this.value === 'upload') {
            uploadSection.classList.remove('hidden');
            presetControls.classList.add('hidden');
            configSection.classList.add('hidden');
            
        } else if (this.value === 'preset') {
            uploadSection.classList.add('hidden');
            presetControls.classList.remove('hidden');
            configSection.classList.remove('hidden');
            presetVizControls.classList.remove('hidden');
            customControls.classList.add('hidden');
            
            // Populate year select
            const response = await fetch('/visualization/get_preset_years');
            const data = await response.json();
            populateSelect(yearSelect, data.years.map(year => ({
                value: year.toString(),
                label: year.toString()
            })));
            
            // Populate visualization types for preset data
            populateVizTypeSelect(presetVizOptions);
        }
    });

    // File upload handler
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

            configSection.classList.remove('hidden');
            customControls.classList.remove('hidden');
            presetVizControls.classList.add('hidden');
            
            // Populate visualization types for custom data
            populateVizTypeSelect(customVizOptions);
            
            // Populate column selectors
            populateSelect(document.getElementById('xAxis'), data.columns.map(col => ({
                value: col,
                label: col
            })));
            populateSelect(document.getElementById('yAxis'), data.numeric_columns.map(col => ({
                value: col,
                label: col
            })));
            populateSelect(document.getElementById('colorBy'), 
                [{ value: '', label: 'None' }].concat(
                    data.categorical_columns.map(col => ({
                        value: col,
                        label: col
                    }))
                )
            );

        } catch (error) {
            console.error('Error:', error);
            alert('Error uploading file');
        }
    });

    // Form submission handler
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const vizData = {
            viz_type: vizType.value,
            data_source: dataSource.value
        };

        if (dataSource.value === 'preset') {
            vizData.year = yearSelect.value;
            vizData.metric = metricSelect.value;
        } else {
            vizData.filename = fileInput.files[0].name;
            vizData.x_column = document.getElementById('xAxis').value;
            vizData.y_column = document.getElementById('yAxis').value;
            const colorBy = document.getElementById('colorBy').value;
            if (colorBy) vizData.color_column = colorBy;
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

    // Helper functions
    function resetForm() {
        uploadForm.reset();
        visualization.classList.add('hidden');
    }

    function populateSelect(select, options) {
        select.innerHTML = '<option value="">Select option</option>';
        const groups = {};
        
        options.forEach(option => {
            if (option.group) {
                if (!groups[option.group]) {
                    groups[option.group] = document.createElement('optgroup');
                    groups[option.group].label = option.group;
                }
                const optElement = document.createElement('option');
                optElement.value = option.value;
                optElement.textContent = option.label;
                groups[option.group].appendChild(optElement);
            } else {
                const optElement = document.createElement('option');
                optElement.value = option.value;
                optElement.textContent = option.label;
                select.appendChild(optElement);
            }
        });
        
        Object.values(groups).forEach(group => select.appendChild(group));
    }

    function populateVizTypeSelect(options) {
        vizType.innerHTML = '<option value="">Select visualization type</option>';
        const groups = {};
        
        options.forEach(option => {
            if (!groups[option.group]) {
                groups[option.group] = document.createElement('optgroup');
                groups[option.group].label = option.group;
            }
            const optElement = document.createElement('option');
            optElement.value = option.value;
            optElement.textContent = option.label;
            groups[option.group].appendChild(optElement);
        });
        
        Object.values(groups).forEach(group => vizType.appendChild(group));
    }
});