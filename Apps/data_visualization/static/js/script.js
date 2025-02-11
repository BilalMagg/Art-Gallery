document.addEventListener('DOMContentLoaded', function() {
  const uploadForm = document.getElementById('uploadForm');
  const fileInput = document.getElementById('fileInput');
  const configSection = document.getElementById('configSection');
  const vizType = document.getElementById('vizType');
  const visualization = document.getElementById('visualization');
  const plotOutput = document.getElementById('plotOutput');
  
  // Additional form elements
  const timeControls = document.getElementById('timeControls');
  const countryColumn = document.getElementById('countryColumn');
  const valueColumn = document.getElementById('valueColumn');
  const timeColumn = document.getElementById('timeColumn');
  const timeValue = document.getElementById('timeValue');
  
  let currentFilename = '';
  let currentTimeValues = [];

  fileInput.addEventListener('change', async function(e) {
      const file = e.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('file', file);

      try {
          const response = await fetch('/upload', {
              method: 'POST',
              body: formData
          });

          const data = await response.json();

          if (data.error) {
              alert(data.error);
              return;
          }

          currentFilename = data.filename;

          // Populate all column selectors
          populateColumnSelect(valueColumn, data.columns);
          
          // Populate country column selector with detected columns
          populateColumnSelect(countryColumn, data.country_columns);
          
          // Handle time-related columns
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

  // Update time values when time column is selected
  timeColumn.addEventListener('change', async function() {
      if (!currentFilename || !this.value) return;

      try {
          const response = await fetch('/get_time_values', {
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
              currentTimeValues = data.time_values;
              populateTimeValues(timeValue, currentTimeValues);
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
          const response = await fetch('/visualize', {
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

  function populateColumnSelect(select, columns) {
      select.innerHTML = '<option value="">Select Column</option>';
      columns.forEach(column => {
          const option = document.createElement('option');
          option.value = column;
          option.textContent = column;
          select.appendChild(option);
      });
  }

  function populateTimeValues(select, values) {
      select.innerHTML = '<option value="">Select Time Value</option>';
      values.forEach(value => {
          const option = document.createElement('option');
          option.value = value;
          option.textContent = value;
          select.appendChild(option);
      });
  }
});