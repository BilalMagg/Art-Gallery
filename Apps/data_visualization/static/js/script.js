document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const configSection = document.getElementById('configSection');
    const vizType = document.getElementById('vizType');
    const visualization = document.getElementById('visualization');
    const plotOutput = document.getElementById('plotOutput');
    
    const timeControls = document.getElementById('timeControls');
    const countryColumn = document.getElementById('countryColumn');
    const valueColumn = document.getElementById('valueColumn');
    const timeColumn = document.getElementById('timeColumn');
    const timeValue = document.getElementById('timeValue');
    
    let currentFilename = '';

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

            populateColumnSelect(valueColumn, data.columns);
            populateColumnSelect(countryColumn, data.country_columns);
            
            if (data.time_columns.length > 0) {
                populateColumnSelect(timeColumn, data.time_columns);
                timeControls.classList.remove('hidden');
            } else {
                timeControls.classList.add('hidden');
            }

            configSection.classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            alert('Error uploading file');
        }
    });

    timeColumn.addEventListener('change', async function() {
        if (!currentFilename || !this.value) return;

        try {
            const response = await fetch('/visualization/get_time_values', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: currentFilename,
                    time_column: this.value
                })
            });

            const data = await response.json();
            if (data.success) {
                populateColumnSelect(timeValue, data.time_values);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    vizType.addEventListener('change', function() {
        const isGlobe = this.value === 'globe';
        document.getElementById('globeControls').style.display = isGlobe ? 'block' : 'none';
        timeControls.style.display = isGlobe ? 'block' : 'none';
    });

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const vizData = {
            filename: currentFilename,
            viz_type: vizType.value,
            country_column: countryColumn.value,
            value_column: valueColumn.value,
            time_column: timeColumn.value,
            time_value: timeValue.value
        };

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
            Plotly.newPlot('plotOutput', plotData.data, plotData.layout);

        } catch (error) {
            console.error('Error:', error);
            alert('Error generating visualization');
        }
    });

    function populateColumnSelect(select, options) {
        select.innerHTML = '<option value="">Select Column</option>';
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            select.appendChild(optionElement);
        });
    }
});